"""
Unit tests for mcp_server.py
==============================
Uses only Python's standard `unittest` module and `unittest.mock`
to mock httpx HTTP calls. No external libraries required.

Run with:
    python -m unittest test_mcp_server.py -v
"""

import unittest
from unittest.mock import MagicMock, patch

import httpx
from mcp.types import TextContent

from mcp_server import (
    BASE_URL,
    _error_result,
    _handle_http_error,
    get_job_status,
    get_results,
    run_suite,
)


# ---------------------------------------------------------------------------
# Shared helper to build simulated httpx.Response objects
# ---------------------------------------------------------------------------

def build_mock_response(status_code: int, body=None, text: str = ""):
    """
    Builds a simulated httpx.Response using MagicMock.

    We use MagicMock instead of a real httpx.Response because constructing
    a real one requires complex transport internals. With MagicMock(spec=...)
    we get an object that behaves like a Response — same attributes and
    methods — without that complexity. The spec= argument also ensures that
    only attributes that actually exist on httpx.Response are allowed,
    which prevents tests from passing for the wrong reasons.

    If 'body' is a dict, .json() is configured to return it.
    If only 'text' is provided, .text is set directly.
    """
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = status_code
    mock_response.text = text
    mock_response.json.return_value = body if body is not None else {}
    return mock_response


# ===========================================================================
# Tests for _error_result
# ===========================================================================

class TestErrorResult(unittest.TestCase):
    """
    We test the most basic building block first: the function that constructs
    error messages. If this fails, everything else will fail in cascade,
    so it's the best starting point for diagnosing problems.
    """

    def test_returns_a_list(self):
        result = _error_result("something went wrong")
        self.assertIsInstance(result, list)

    def test_list_contains_exactly_one_element(self):
        result = _error_result("something went wrong")
        self.assertEqual(len(result), 1)

    def test_element_is_text_content(self):
        result = _error_result("something went wrong")
        self.assertIsInstance(result[0], TextContent)

    def test_message_has_error_prefix(self):
        """
        The 'ERROR:' prefix lets whoever receives the result immediately
        identify that something went wrong, without parsing the full message.
        """
        result = _error_result("connection failure")
        self.assertTrue(result[0].text.startswith("ERROR:"))

    def test_original_message_appears_in_text(self):
        result = _error_result("problem details here")
        self.assertIn("problem details here", result[0].text)


# ===========================================================================
# Tests for _handle_http_error
# ===========================================================================

class TestHandleHttpError(unittest.TestCase):
    """
    We verify that each HTTP error code is translated into a descriptive
    message that tells the user exactly what went wrong, including the
    context (which tool triggered the error) and the server's detail text.
    """

    def test_400_includes_bad_request_in_message(self):
        response = build_mock_response(400, text="missing required field")
        result = _handle_http_error(response, "test_context")
        self.assertIn("400 Bad Request", result[0].text)

    def test_400_includes_the_tool_context(self):
        """
        The context string (tool name) helps debugging: you know which
        function triggered the error without reading a full stack trace.
        """
        response = build_mock_response(400)
        result = _handle_http_error(response, "run_suite")
        self.assertIn("run_suite", result[0].text)

    def test_400_includes_the_response_detail(self):
        response = build_mock_response(
            400, text="'suite_name' field is invalid"
        )
        result = _handle_http_error(response, "ctx")
        self.assertIn("'suite_name' field is invalid", result[0].text)

    def test_404_includes_not_found_in_message(self):
        response = build_mock_response(404, text="resource does not exist")
        result = _handle_http_error(response, "ctx")
        self.assertIn("404 Not Found", result[0].text)

    def test_425_includes_too_early_in_message(self):
        response = build_mock_response(425, text="server not ready")
        result = _handle_http_error(response, "ctx")
        self.assertIn("425 Too Early", result[0].text)

    def test_unmapped_status_code_returns_generic_error_with_code(self):
        """
        A 500 or any other unexpected code must not crash the function —
        it should return a generic error message that includes the code,
        so the user knows what happened even if we didn't predict it.
        """
        response = build_mock_response(500, text="internal server error")
        result = _handle_http_error(response, "ctx")
        self.assertIn("500", result[0].text)


# ===========================================================================
# Tests for run_suite
# ===========================================================================

class TestRunSuite(unittest.TestCase):
    """
    Each test uses @patch to intercept httpx.post before it reaches the
    network. The 'mock_post' argument each method receives is the
    MagicMock object that replaces httpx.post for the duration of that
    single test.

    An important note on the patch target: we patch 'mcp_server.httpx.post'
    rather than 'httpx.post' directly. What matters is where the function
    is *used*, not where it is *defined*.
    """

    @patch("mcp_server.httpx.post")
    def test_success_returns_job_id_as_string(self, mock_post):
        """
        Happy path: the server responds 200 with a job_id UUID.
        The function must return exactly that string, unwrapped.
        """
        job_id = "550e8400-e29b-41d4-a716-446655440000"
        mock_post.return_value = build_mock_response(
            200, body={"job_id": job_id}
        )

        result = run_suite("smoke", "/tests/api")

        self.assertEqual(result, job_id)

    @patch("mcp_server.httpx.post")
    def test_calls_the_correct_endpoint(self, mock_post):
        """
        API contract test: the POST URL must be exactly
        BASE_URL + '/operations'. If the route changes in the future,
        this test will catch it immediately.
        """
        mock_post.return_value = build_mock_response(
            200, body={"job_id": "abc"}
        )

        run_suite("smoke", "/tests/api")

        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], f"{BASE_URL}/operations")

    @patch("mcp_server.httpx.post")
    def test_sends_suite_name_and_tests_route_in_payload(self, mock_post):
        """
        The JSON payload must contain exactly the two fields the API expects.
        If we ever rename a parameter, this test will detect the mismatch.
        """
        mock_post.return_value = build_mock_response(
            200, body={"job_id": "abc"}
        )

        run_suite("regression", "/tests/regr")

        _, kwargs = mock_post.call_args
        payload = kwargs.get("json", {})
        self.assertEqual(payload["suite_name"], "regression")
        self.assertEqual(payload["tests_route"], "/tests/regr")

    @patch("mcp_server.httpx.post")
    def test_response_without_job_id_returns_error(self, mock_post):
        """
        If the server responds 200 but with no job_id in the body, something
        is broken in the API. We must catch that and return an error instead
        of letting a KeyError propagate to the MCP client.
        """
        mock_post.return_value = build_mock_response(
            200, body={"other_field": "x"}
        )

        result = run_suite("smoke", "/tests/api")

        self.assertIsInstance(result, list)
        self.assertIn("job_id", result[0].text)

    @patch("mcp_server.httpx.post")
    def test_http_400_returns_error_text_content(self, mock_post):
        mock_post.return_value = build_mock_response(
            400, text="invalid parameter"
        )

        result = run_suite("", "/tests/api")

        self.assertIsInstance(result, list)
        self.assertIn("400 Bad Request", result[0].text)

    @patch("mcp_server.httpx.post")
    def test_http_404_returns_error_text_content(self, mock_post):
        mock_post.return_value = build_mock_response(404, text="not found")

        result = run_suite("smoke", "/tests/api")

        self.assertIsInstance(result, list)
        self.assertIn("404 Not Found", result[0].text)

    @patch("mcp_server.httpx.post")
    def test_http_425_returns_error_text_content(self, mock_post):
        mock_post.return_value = build_mock_response(425, text="too early")

        result = run_suite("smoke", "/tests/api")

        self.assertIsInstance(result, list)
        self.assertIn("425 Too Early", result[0].text)

    @patch("mcp_server.httpx.post", side_effect=httpx.ConnectError("refused"))
    def test_connection_error_returns_descriptive_message(self, mock_post):
        """
        When httpx.post raises ConnectError (FastAPI is not running),
        the function must catch it and return a clear message to the user.

        We use side_effect instead of return_value here because we want the
        mock to *raise* an exception rather than return a response object.
        This simulates the server being completely unreachable.
        """
        result = run_suite("smoke", "/tests/api")

        self.assertIsInstance(result, list)
        self.assertIn("Could not connect", result[0].text)


# ===========================================================================
# Tests for get_job_status
# ===========================================================================

class TestGetJobStatus(unittest.TestCase):

    JOB_ID = "job-uuid-001"

    @patch("mcp_server.httpx.get")
    def test_success_returns_dict_with_three_fields(self, mock_get):
        """
        We verify that the returned dict has exactly job_id, status, and
        progress, with the correct values coming from the server response.
        """
        mock_get.return_value = build_mock_response(200, body={
            "job_id": self.JOB_ID,
            "status": "running",
            "progress": 45.5,
        })

        result = get_job_status(self.JOB_ID)

        self.assertEqual(result["job_id"], self.JOB_ID)
        self.assertEqual(result["status"], "running")
        self.assertEqual(result["progress"], 45.5)

    @patch("mcp_server.httpx.get")
    def test_calls_the_correct_endpoint(self, mock_get):
        mock_get.return_value = build_mock_response(200, body={
            "job_id": self.JOB_ID, "status": "done", "progress": 100.0,
        })

        get_job_status(self.JOB_ID)

        args, _ = mock_get.call_args
        self.assertEqual(args[0], f"{BASE_URL}/status/{self.JOB_ID}")

    @patch("mcp_server.httpx.get")
    def test_uses_parameter_job_id_as_fallback(self, mock_get):
        """
        If the server omits job_id from its response (rare but possible),
        we fall back to the job_id the caller passed as an argument.
        This prevents returning None in a key field.
        """
        mock_get.return_value = build_mock_response(200, body={
            "status": "completed",
            "progress": 100.0,
            # job_id intentionally absent
        })

        result = get_job_status(self.JOB_ID)

        self.assertEqual(result["job_id"], self.JOB_ID)

    @patch("mcp_server.httpx.get")
    def test_http_404_returns_error(self, mock_get):
        mock_get.return_value = build_mock_response(404, text="job not found")

        result = get_job_status(self.JOB_ID)

        self.assertIsInstance(result, list)
        self.assertIn("404 Not Found", result[0].text)

    @patch("mcp_server.httpx.get")
    def test_http_425_returns_error(self, mock_get):
        mock_get.return_value = build_mock_response(425, text="too early")

        result = get_job_status(self.JOB_ID)

        self.assertIsInstance(result, list)
        self.assertIn("425 Too Early", result[0].text)

    @patch("mcp_server.httpx.get", side_effect=httpx.ConnectError("refused"))
    def test_connection_error_returns_descriptive_message(self, mock_get):
        result = get_job_status(self.JOB_ID)

        self.assertIsInstance(result, list)
        self.assertIn("Could not connect", result[0].text)


# ===========================================================================
# Tests for get_results
# ===========================================================================

class TestGetResults(unittest.TestCase):

    JOB_ID = "job-uuid-002"

    @patch("mcp_server.httpx.get")
    def test_success_returns_complete_dict(self, mock_get):
        """
        We verify the full structure: job_id, a list of results each with
        test_id and verdict, and an aggregated summary dict.
        """
        mock_get.return_value = build_mock_response(200, body={
            "job_id": self.JOB_ID,
            "results": [
                {"test_id": "test_login", "verdict": "passed"},
                {"test_id": "test_logout", "verdict": "failed"},
            ],
            "summary": {"total": 2, "passed": 1, "failed": 1},
        })

        result = get_results(self.JOB_ID)

        self.assertEqual(result["job_id"], self.JOB_ID)
        self.assertEqual(len(result["results"]), 2)
        self.assertEqual(result["results"][0]["verdict"], "passed")
        self.assertEqual(result["summary"]["failed"], 1)

    @patch("mcp_server.httpx.get")
    def test_calls_correct_endpoint_with_query_param(self, mock_get):
        """
        get_results uses query params (?job_id=...) instead of path params.
        We verify the base URL is correct and that the param is passed via
        the 'params' kwarg rather than being manually concatenated to the URL.
        """
        mock_get.return_value = build_mock_response(200, body={
            "job_id": self.JOB_ID, "results": [], "summary": {},
        })

        get_results(self.JOB_ID)

        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], f"{BASE_URL}/jobs")
        self.assertEqual(kwargs.get("params"), {"job_id": self.JOB_ID})

    @patch("mcp_server.httpx.get")
    def test_results_defaults_to_empty_list_when_absent(self, mock_get):
        """
        If the server omits 'results', we return [] instead of None so that
        the caller can safely iterate over the list without a TypeError.
        """
        mock_get.return_value = build_mock_response(200, body={
            "job_id": self.JOB_ID,
            "summary": {},
            # 'results' intentionally absent
        })

        result = get_results(self.JOB_ID)

        self.assertEqual(result["results"], [])

    @patch("mcp_server.httpx.get")
    def test_summary_defaults_to_empty_dict_when_absent(self, mock_get):
        mock_get.return_value = build_mock_response(200, body={
            "job_id": self.JOB_ID,
            "results": [],
            # 'summary' intentionally absent
        })

        result = get_results(self.JOB_ID)

        self.assertEqual(result["summary"], {})

    @patch("mcp_server.httpx.get")
    def test_http_404_returns_error(self, mock_get):
        mock_get.return_value = build_mock_response(
            404, text="job not found"
        )

        result = get_results(self.JOB_ID)

        self.assertIsInstance(result, list)
        self.assertIn("404 Not Found", result[0].text)

    @patch("mcp_server.httpx.get")
    def test_http_400_invalid_parameter_returns_error(self, mock_get):
        mock_get.return_value = build_mock_response(
            400, text="malformed job_id"
        )

        result = get_results("not-a-uuid")

        self.assertIsInstance(result, list)
        self.assertIn("400 Bad Request", result[0].text)

    @patch("mcp_server.httpx.get", side_effect=httpx.ConnectError("refused"))
    def test_connection_error_returns_descriptive_message(self, mock_get):
        result = get_results(self.JOB_ID)

        self.assertIsInstance(result, list)
        self.assertIn("Could not connect", result[0].text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
