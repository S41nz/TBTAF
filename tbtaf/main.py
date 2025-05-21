from __future__ import absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI, HTTPException, BackgroundTasks
from uuid import uuid4
from typing import Dict
import time
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator
from interpreter.TBTAFInterpreter import TBTAFInterpreter
from databridge.TBTAFSqliteDatabridge import TBTAFSqliteDatabridge
from rest.TBTAFAgentDriver import TBTAFAgentDriver
from rest.JobResultResponse import JobResultResponse
from rest.JobStatusResponse import JobStatusResponse
from rest.SuitesResponse import SuitesResponse
from rest.OperationRequest import OperationRequest
import os

app = FastAPI()

# In-memory storage for jobs
jobs_db: Dict[str, TBTAFAgentDriver] = {}

# In-memory storage for suites by job_id
suites_db: Dict[str, object] = {}  

targetDatabridge = TBTAFSqliteDatabridge()
orch = TBTAFOrchestrator(targetDatabridge=targetDatabridge)
interpreter = TBTAFInterpreter()

def execute_suite_async(job_id: str, suite_name: str, tests_route: str):
    time.sleep(1)

    try:
        # Get test suite from TBTAF
        test_suite = orch.createTestSuite(tests_route, testSuiteID=job_id)
        test_bed = orch.createTestBed()

        suites_db[job_id] = test_suite

        project_name = suite_name
        print(f"\nCreating project '{project_name}'...")
        orch.createNewProject(test_suite, test_bed, project_name)
        
        # Update status to in-progress
        jobs_db[job_id].status = "in_progress"
        
        # Execute suite and track progress
        results = []
        total_tests = len(test_suite.getTestCases())
        progress = 0
        for idx, test_case in enumerate(test_suite.getTestCases()):
            # Execute test case
            test_result = test_case.execute()

            test_result_data = test_case.getResult()

            results.append({
                "test_id": test_case.getTestMetadata().getAssetID(),
                "verdict": test_result_data.getVerdict(),
            })
            
            # Update progress
            progress = int((idx + 1) / total_tests * 100)
        
        # Simulate some delay for progress update
        time.sleep(5)
        # Final status update
        jobs_db[job_id].status = "completed"
        jobs_db[job_id].results = results
        jobs_db[job_id].progress = progress


        print([jobs_db])
        
    except Exception as e:
        jobs_db[job_id].status = f"failed: {str(e)}"

@app.post("/api/v1/operations", response_model=dict)
async def create_operation(request: OperationRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid4())
    
    # Initialize job
    jobs_db[job_id] = TBTAFAgentDriver(
        status="queued",
        progress=0,
        suite_name=request.suite_name
    )
    
    # Get tests_route from request
    tests_route = request.tests_route
    if not tests_route:
        tests_route = "./test/discoverer/samples"
        print(f"Using default tests_route: {tests_route}")
    else:
        tests_route = request.tests_route
        candidate_path = os.path.realpath(tests_route)
        allowed_base = os.path.realpath("./test")

        # Check for directory traversal attacks
        # Ensure the candidate path starts with the allowed base path
        # and does not contain ".." or "~" or start with "/"
        if not candidate_path.startswith(allowed_base) or tests_route.find("..") != -1 or tests_route.find("~") != -1 or tests_route.startswith("/"):
            raise HTTPException(status_code=400, detail="Invalid tests route: directory traversal detected.")
        if not os.path.isdir(candidate_path):
            raise HTTPException(status_code=400, detail="Invalid tests route: not a directory.")
        tests_route = candidate_path



    # Start async execution
    background_tasks.add_task(execute_suite_async, job_id, request.suite_name, tests_route=request.tests_route)
    
    return {"job_id": job_id, "status": "accepted"}

@app.get("/api/v1/status/{job_id}", response_model=JobStatusResponse)
async def get_status(job_id: str):
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs_db[job_id]
    return {
        "job_id": job_id,
        "status": job.status,
        "progress": job.progress,
        "results": job.results if job.results else None,
    }

@app.get("/api/v1/jobs", response_model=JobResultResponse)
async def get_job_results(job_id: str):
    print( "recuperando suite")
    print( [suites_db] )
    suite = suites_db[job_id]

    suite_result = suite.getSuiteResult()
    if not isinstance(suite_result, list):
        suite_result = [suite_result]

    # Collect individual test case results
    results = []
    test_cases_list = suite.getTestCases()
    for test_case in test_cases_list:
        test_result_data = test_case.getResult()

        results.append({
            "test_id": test_case.getTestMetadata().getAssetID(),
            "verdict": test_result_data.getVerdict(),
        })

    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs_db[job_id]
    if job.status != "completed":
        raise HTTPException(status_code=425, detail="Job not completed yet")
    

    return {
        "job_id": job_id,
        "results": results,
        "summary": "Passed" if all(r['verdict'] == "Passed" for r in job.results) else "Failed"
    }

@app.post("/api/v1/suites", response_model=SuitesResponse)
async def get_suites(request: SuitesResponse):
    try:
        if request.project_name:
            tags = orch.getTests(request.project_name)
        else:
            raise HTTPException(status_code=500, detail=f"Error retrieving suites: Must provide a project name")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving suites: {str(e)}")
    
    print(f"Retrieved suites: {tags}")
    return {
        "project_name": request.project_name,
        "tags": tags
    }