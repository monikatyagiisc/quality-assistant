from backend.agents.base import AIAgent, file_writer_tool
from langchain_core.tools import StructuredTool
 
 
class BugReportGenerationAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Bug Report Generation Agent",
            description="Creates structured, consistent, and prioritized bug reports from raw issue logs.",
            system_prompt=(
                "You are an expert Bug Report Generation Agent. Given raw issue logs, "
                "extract relevant information to create structured, consistent, and prioritized "
                "bug reports.\n\nEach report must include the following fields:\n"
                "- **Title**\n- **Description**\n- **Steps to Reproduce**\n"
                "- **Expected vs. Actual Results**\n- **Environment**\n"
                "- **Severity** (Critical, Major, Minor)\n- **Priority** (High, Medium, Low)\n\n"
                "Output as a Markdown-formatted list of bug reports with appropriate headings and bullet points."
            ),
            tools=[file_writer_tool]
        )
 
    def generate_bug_reports(self, raw_issue_logs: str) -> str:
        """
        Generates structured Markdown bug reports from raw issue logs.
        """
        input_text = (
            "Transform the following raw issue logs into structured bug reports in Markdown format. "
            "Each report must include Title, Description, Steps to Reproduce, Expected vs. Actual Results, "
            "Environment, Severity, and Priority.\n\n"
            f"Raw Logs:\n{raw_issue_logs}"
        )
 
        response = self.get_runnable().invoke({"input": input_text})
        generated_bug_reports = response.content if hasattr(response, "content") else str(response)
 
        # Optional: save to file
        # file_writer_tool.run({
        #     "file_path": "artifacts/bug_reports.md",
        #     "content": generated_bug_reports
        # })
 
        return generated_bug_reports