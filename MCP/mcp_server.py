"""
TBTAF MCP Server
================
MCP server for interacting with the TBTAF API.
Implemented with FastMCP and stdio transport.
"""

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent


BASE_URL = "http://localhost:8000/api/v1"

mcp = FastMCP("TBTAF")


def _error_result(message: str):
    """Returns an error result compatible with MCPToolResult."""
    return [TextContent(type="text", text=f"ERROR: {message}")]


def _handle_http_error(response: httpx.Response, context: str):
    """
    Interprets HTTP errors and returns a descriptive error result.
    Covers status codes 400, 404, and 425.
    """
    code = response.status_code
    if code == 400:
        return _error_result(
            f"[400 Bad Request] {context}: The request contains invalid or "
            f"malformed parameters. Detail: {response.text}"
        )
    if code == 404:
        return _error_result(
            f"[404 Not Found] {context}:The requested resource does not exist."
            f"Detail: {response.text}"
        )
    if code == 425:
        return _error_result(
            f"[425 Too Early] {context}: The server is not ready to process "
            f"the request at this time. Please retry later. "
            f"Detail: {response.text}"
        )
    return _error_result(
        f"[{code}] {context}: Unexpected server error. "
        f"Detail: {response.text}"
    )


@mcp.tool()
def run_suite(suite_name: str, tests_route: str):
    """
    Launches the execution of a test suite on the TBTAF server.

    Invoke this tool when the user wants to start an automated test suite.
    Returns the `job_id` (UUID) assigned to the job, which can later be used
    with `get_job_status` and `get_results`.

    Parameters:
        suite_name  -- Identifier name of the test suite to execute
                       (e.g. "regression", "smoke", "full").
        tests_route -- Relative or absolute path to the directory or file
                       containing the tests (e.g. "/tests/api").

    Returns:
        str -- The UUID `job_id` of the created job, or a descriptive error.
    """
    payload = {"suite_name": suite_name, "tests_route": tests_route}
    try:
        response = httpx.post(f"{BASE_URL}/operations", json=payload)
    except httpx.ConnectError:
        return _error_result(
            "Could not connect to the FastAPI server at "
            f"{BASE_URL}. Please verify that the service is running."
        )

    if response.status_code != 200:
        return _handle_http_error(response, "run_suite")

    data = response.json()
    job_id = data.get("job_id")
    if not job_id:
        return _error_result(
            "The server response does not contain a valid 'job_id'. "
            f"Response received: {data}"
        )

    return job_id


@mcp.tool()
def get_job_status(job_id: str):
    """
    Queries the current status of a running test job.

    Invoke this tool to check the progress of a job previously started with
    `run_suite`. Useful for polling until the job finishes
    (status == "completed" or "failed").

    Parameters:
        job_id -- UUID of the job returned by `run_suite`.

    Returns:
        dict -- Dictionary with the following fields:
                  - job_id   (str):   Unique identifier of the job.
                  - status   (str):   Current state ("pending", "running",
                                      "completed", "failed", etc.).
                  - progress (float): Completion percentage (0.0 – 100.0).
    """
    try:
        response = httpx.get(f"{BASE_URL}/status/{job_id}")
    except httpx.ConnectError:
        return _error_result(
            "Could not connect to the FastAPI server at "
            f"{BASE_URL}. Please verify that the service is running."
        )

    if response.status_code != 200:
        return _handle_http_error(response, "get_job_status")

    data = response.json()
    return {
        "job_id": data.get("job_id", job_id),
        "status": data.get("status"),
        "progress": data.get("progress"),
    }


@mcp.tool()
def get_results(job_id: str):
    """
    Retrieves the detailed results of a completed test job.

    Invoke this tool once `get_job_status` indicates that the job has finished.
    Returns the individual verdict for each test along with a global execution
    summary.

    Parameters:
        job_id -- UUID of the job returned by `run_suite`.

    Returns:
        dict -- Dictionary with the following fields:
                  - job_id   (str):  Unique identifier of the job.
                  - results  (list): List of objects containing:
                                       · test_id (str)  — test name/id.
                                       · verdict (str)  — "passed", "failed",
                                                          "skipped", etc.
                  - summary  (dict): Aggregated summary.
    """
    try:
        response = httpx.get(f"{BASE_URL}/jobs", params={"job_id": job_id})
    except httpx.ConnectError:
        return _error_result(
            "Could not connect to the FastAPI server at "
            f"{BASE_URL}. Please verify that the service is running."
        )

    if response.status_code != 200:
        return _handle_http_error(response, "get_results")

    data = response.json()
    return {
        "job_id": data.get("job_id", job_id),
        "results": data.get("results", []),
        "summary": data.get("summary", {}),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
