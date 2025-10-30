import os
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from typing import Any, Dict, List, Optional, Callable

# Initialize Vertex AI LLM
# Ensure GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION are set in .env or environment variables
llm = ChatVertexAI(
    model_name="gemini-2.5-flash",
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    temperature=0.3
)

class AIAgent:
    def __init__(self, name: str, description: str, system_prompt: str, tools: Optional[List[StructuredTool]] = None):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.tools = tools if tools is not None else []
        self._runnable = self._create_runnable()

    def _create_runnable(self) -> Runnable:
        """Creates the core LangChain Runnable for the agent."""
        # Simple agent: LLM with a system prompt. Can be extended with tool usage.
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content="{input}")
        ])

        if self.tools:
            # For complex agents with tools, you'd use AgentExecutor or a custom tool-calling chain
            # This is a simplified example. For real tool usage, consider:
            # from langchain.agents import AgentExecutor, create_json_agent
            # from langchain.agents.agent_types import AgentType
            # agent = create_json_agent(llm, self.tools, AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION)
            # return agent
            # For now, we'll just expose a placeholder. LLM can "decide" based on prompt.
            tool_names = ", ".join([tool.name for tool in self.tools])
            self.system_prompt += f"\n\nAvailable tools: {tool_names}. If needed, you can indicate which tool you'd use."
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=self.system_prompt),
                HumanMessage(content="{input}")
            ])


        return prompt | llm

    def get_runnable(self) -> Runnable:
        return self._runnable

    def get_name(self) -> str:
        return self.name

# --- Placeholder Tools ---
# In a real system, these would interact with databases, file systems, external APIs, etc.

def write_to_file_tool(file_path: str, content: str) -> str:
    """Writes content to a specified file path."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Content successfully written to {file_path}"
    except Exception as e:
        return f"Error writing to file {file_path}: {e}"

def simulate_code_execution_tool(code: str, language: str) -> str:
    """Simulates the execution of code and returns dummy results."""
    # In a real environment, this would execute code in a sandbox or via a CI system.
    print(f"Simulating {language} code execution:\n{code[:200]}...")
    return "Simulated execution successful. All tests passed. (This is a placeholder result)"

def get_current_ui_state_tool() -> str:
    """Fetches the current UI element structure (e.g., DOM, API schema)."""
    # Placeholder: In reality, interacts with a live application or test environment.
    return "Simulated UI State: Login button changed from 'btn-login' to 'main-login-btn'. Password field ID unchanged. API endpoint '/users' now '/api/v1/users'."

def fetch_issue_logs_tool() -> str:
    """Fetches raw issue logs from a bug tracking system or test run."""
    # Placeholder: In reality, connects to Jira, Azure DevOps, etc.
    return """
    Issue 1: User cannot login with valid credentials. Error: "Invalid username or password".
    Issue 2: Search functionality broken for special characters.
    Issue 3: Checkout button occasionally unresponsive on mobile.
    Issue 4: Typo in 'Welcome' message after successful login.
    """

# Structured Tools for LangChain
file_writer_tool = StructuredTool.from_function(
    func=write_to_file_tool,
    name="file_writer",
    description="Writes given content to a specified file path. Useful for saving test cases, scripts, or reports."
)

code_execution_tool = StructuredTool.from_function(
    func=simulate_code_execution_tool,
    name="code_execution_simulator",
    description="Simulates the execution of provided code in a given language. Returns a dummy success message for demonstration."
)

ui_state_fetcher_tool = StructuredTool.from_function(
    func=get_current_ui_state_tool,
    name="ui_state_fetcher",
    description="Fetches a simulated current UI element structure or API schema. Useful for detecting changes for self-healing."
)

issue_log_fetcher_tool = StructuredTool.from_function(
    func=fetch_issue_logs_tool,
    name="issue_log_fetcher",
    description="Fetches simulated raw issue logs from a bug tracking system or test run. Useful for bug report generation."
)

# Example placeholder tool for Change Impact Analysis to analyze diffs
def analyze_code_diff_tool(code_diff: str) -> str:
    """
    Analyzes a given code diff to identify affected modules, features,
    and potential impact on existing tests.
    """
    # In a real scenario, this would use AST parsing, code dependency graphs, etc.
    if "database" in code_diff.lower() or "db" in code_diff.lower():
        return "High impact: Database schema or ORM changes detected. This likely affects multiple features and requires re-testing data integrity and CRUD operations extensively."
    elif "ui-button" in code_diff.lower() or "css" in code_diff.lower():
        return "Low impact: UI styling or minor component changes. Primarily affects visual regression tests and specific UI element interactions."
    elif "new_feature" in code_diff.lower():
        return "New feature added. Requires new test cases and test data for the new functionality."
    else:
        return "Medium impact: General code changes. Review affected logical paths for test updates."

change_impact_analyzer_tool = StructuredTool.from_function(
    func=analyze_code_diff_tool,
    name="change_impact_analyzer",
    description="Analyzes code differences (diffs) to determine the impact on existing functionalities and tests."
)