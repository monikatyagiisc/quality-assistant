from backend.agents.base import AIAgent, file_writer_tool

from langchain_core.tools import StructuredTool
 
 
class TestSummaryReportAgent(AIAgent):

    def __init__(self):

        super().__init__(

            name="Test Summary Report Agent",

            description="Generates concise and structured test summary reports from execution data and bug reports.",

            system_prompt=(

                "You are an expert Test Summary Report Agent. Consolidate test execution results, "

                "bug reports, and test coverage information into a clear, concise, and structured "

                "test summary report.\n\n"

                "The report should include:\n"

                "- Overall test execution statistics (pass/fail rate, total tests)\n"

                "- Highlights of critical bugs or regressions\n"

                "- Summary of test coverage and areas not tested\n"

                "- Observations and risks\n"

                "- Recommendations for improvement or next steps\n\n"

                "Output the report in clean Markdown format with proper headings and bullet points."

            ),

            tools=[file_writer_tool]

        )
 
    def generate_report(self, execution_data: str, bug_reports: str, test_coverage: str) -> str:

        """

        Generates a structured test summary report from execution logs, bug reports, and test coverage input.

        """

        input_text = (

            "Based on the following data, generate a professional and concise test summary report:\n\n"

            "### Test Execution Data:\n"

            f"{execution_data}\n\n"

            "### Bug Reports:\n"

            f"{bug_reports}\n\n"

            "### Test Coverage Info:\n"

            f"{test_coverage}"

        )
 
        response = self.get_runnable().invoke({"input": input_text})

        summary_report = response.content if hasattr(response, "content") else str(response)
 
        # Optional: Save to file

        # file_writer_tool.run({

        #     "file_path": "artifacts/test_summary_report.md",

        #     "content": summary_report

        # })
 
        return summary_report
 