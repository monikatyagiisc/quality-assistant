from backend.agents.base import AIAgent, file_writer_tool
from langchain_core.tools import StructuredTool
from typing import List

from backend.agents.base import AIAgent, file_writer_tool
from langchain_core.tools import StructuredTool
from typing import List
 
 
class TestDataGenerationAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Test Data Generation Agent",
            description="Produces valid, edge-case, and negative datasets tailored to application constraints.",
            system_prompt=(
                "You are an expert Test Data Generation Agent. Given a set of test cases and data "
                "constraints (e.g., string length, numeric range, data types, specific formats like email/URL), "
                "generate diverse test data including valid, invalid, boundary, and edge cases. "
                "Output as a well-formatted JSON string with keys as field names and values as lists of example inputs."
            ),
            tools=[file_writer_tool]
        )
 
    def generate_test_data(self, test_cases_summary: str, constraints: str) -> str:
        """
        Generates diverse test data based on test case summaries and constraints.
        Returns data in JSON-like string format.
        """
        input_text = (
            "Based on the test case summary and data constraints below, generate test data covering:\n"
            "- Valid values\n"
            "- Invalid values\n"
            "- Boundary values\n"
            "- Edge cases\n\n"
            "Output format: JSON with fields and arrays of values.\n\n"
            f"Test Case Summary:\n{test_cases_summary}\n\n"
            f"Constraints:\n{constraints}"
        )
 
        response = self.get_runnable().invoke({"input": input_text})
 
        generated_content = response.content if hasattr(response, "content") else str(response)
 
        # Optional: write to file (uncomment if needed)
        # file_writer_tool.run({
        #     "file_path": "artifacts/generated_test_data.json",
        #     "content": generated_content
        # })
 
        return generated_content