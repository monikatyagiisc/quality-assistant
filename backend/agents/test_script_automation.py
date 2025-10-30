from backend.agents.base import AIAgent, file_writer_tool, code_execution_tool

from langchain_core.tools import StructuredTool
 
 
class TestScriptAutomationAgent(AIAgent):

    def __init__(self):

        super().__init__(

            name="Test Script Automation Agent",

            description="Transforms test cases into automated scripts (e.g., Playwright, Selenium, Pytest, Postman).",

            system_prompt=(

                "You are an expert Test Script Automation Agent. Given structured test cases, "

                "generate automated test scripts using the specified test automation framework.\n\n"

                "Framework options may include Python Playwright, Java Selenium, JavaScript Cypress, "

                "Postman collection, or Pytest. Follow best practices for the selected framework, "

                "and assume necessary dependencies are already installed.\n\n"

                "Return only valid runnable code blocks with comments as needed."

            ),

            tools=[file_writer_tool, code_execution_tool]  # Optional: allow saving or simulating execution

        )
 
    def automate_script(self, test_cases: str, framework: str = "Python Playwright") -> str:

        """

        Generates automated test scripts based on structured test cases and the specified framework.

        """

        input_text = (

            f"Transform the following structured test cases into automated test scripts using the framework: {framework}.\n\n"

            "Follow best practices and generate runnable code only.\n\n"

            f"Test Cases:\n{test_cases}"

        )
 
        response = self.get_runnable().invoke({"input": input_text})

        generated_script = response.content if hasattr(response, "content") else str(response)
 
        # Optional: write to file

        # file_writer_tool.run({

        #     "file_path": f"artifacts/automated_script_{framework.lower().replace(' ', '_')}.py",

        #     "content": generated_script

        # })
 
        return generated_script
 