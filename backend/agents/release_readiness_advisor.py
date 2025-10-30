from backend.agents.base import AIAgent, file_writer_tool
from langchain_core.tools import StructuredTool
 
 
class ReleaseReadinessAdvisorAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Release Readiness Advisor Agent",
            description="Evaluates test results and quality metrics to assess release readiness.",
            system_prompt=(
                "You are a Release Readiness Advisor Agent. Based on aggregated test results, "
                "bug reports (severity, status), code quality metrics, and predefined release "
                "criteria, assess the overall release readiness of the software.\n\n"
                "Provide a clear, actionable recommendation as one of the following:\n"
                "- 'Ready for Release'\n"
                "- 'Proceed with Caution'\n"
                "- 'Not Ready'\n\n"
                "Justify your recommendation using:\n"
                "- Test results (pass/fail rate, regressions)\n"
                "- Bug status and severity\n"
                "- Code quality metrics (coverage, linting, static analysis)\n"
                "- Any known risks or gaps\n\n"
                "Respond with a concise and well-formatted Markdown summary."
            ),
            tools=[]  # You can add file_writer_tool here if you want to persist the output
        )
 
    def assess_readiness(self, test_summary: str, bug_summary: str, quality_metrics: str) -> str:
        """
        Assesses release readiness based on test summary, bug report summary, and quality metrics.
        Returns a clear recommendation with justification.
        """
        input_text = (
            "Please assess release readiness based on the following inputs:\n\n"
            "### Test Summary:\n"
            f"{test_summary}\n\n"
            "### Bug Summary:\n"
            f"{bug_summary}\n\n"
            "### Code Quality Metrics:\n"
            f"{quality_metrics}\n\n"
            "Provide a final recommendation and rationale in Markdown format."
        )
 
        response = self.get_runnable().invoke({"input": input_text})
        recommendation_report = response.content if hasattr(response, "content") else str(response)
 
        # Optional: Save output to a file
        # file_writer_tool.run({
        #     "file_path": "artifacts/release_readiness_recommendation.md",
        #     "content": recommendation_report
        # })
 
        return recommendation_report