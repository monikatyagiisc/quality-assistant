from backend.agents.base import AIAgent, file_writer_tool
from langchain_core.tools import StructuredTool
from typing import List

class TestCaseGenerationAgent(AIAgent):
    def __init__(self):
        super().__init__(
            name="Test Case Generation Agent",
            description="Converts software requirements and user stories into structured test cases (e.g., in Gherkin or tabular format).",
            system_prompt=(
                "You are an expert Test Case Generation Agent. Your task is to transform provided "
                "software requirements and user stories into comprehensive, structured test cases. "
                "Each test case should include a unique ID, description, preconditions, steps, expected results, "
                "and priority. Aim for clear, atomic, and testable cases. Output in Markdown table format."
            ),
            tools=[file_writer_tool]
        )

    # def generate_test_cases(self, requirements: str, user_stories: str) -> str:
    #     """
    #     Generates structured test cases based on requirements and user stories.
    #     Calls the underlying LLM with the formulated prompt.
    #     """
    #     input_text = f"Requirements:\n{requirements}\n\nUser Stories:\n{user_stories}"
    #     # Execute the runnable with the input (the prompt's {input} variable)
    #     response = self.get_runnable().invoke({"input": input_text})
        
    #     # Assume LLM generates a string response.
    #     # In a real scenario, you might parse this and validate.
    #     generated_content = response.content # Access content from AIMessage
        
    #     # Example of tool usage *after* generation (or LLM decides WHEN to use it based on prompt)
    #     # LLM based agents will output thoughts and actions. For simplicity, we just take the content.
    #     # If the LLM was set up as an AgentExecutor, it would automatically call tools.
    #     # Here, we simulate saving if a tool was to be used directly by orchestrator
    #     # file_writer_tool.run(file_path="generated_test_cases.md", content=generated_content)
        
    #     return generated_content

    def generate_test_cases(self, requirements: str, user_stories: str) -> str:
        """
        Generates structured test cases based on requirements and user stories.
        Calls the underlying LLM with the formulated prompt.
        """
        # input_text = f"Requirements:\n{requirements}\n\nUser Stories:\n{user_stories}"
        input_text = (
                "Below are software requirements and user stories. "
                "Generate structured test cases in a Markdown table with the following columns: "
                "Test ID, Description, Preconditions, Steps, Expected Result, Priority.\n\n"
                f"Software Requirements:\n{requirements}\n\nUser Stories:\n{user_stories}"
            )
        
        # Invoke the runnable
        response = self.get_runnable().invoke({"input": input_text})
    
        # Extract content from HumanMessage or AIMessage
        if hasattr(response, "content"):
            generated_content = response.content
        elif isinstance(response, dict) and "content" in response:
            generated_content = response["content"]
        else:
            generated_content = str(response)
    
        return generated_content
    