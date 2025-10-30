import os
import operator
from typing import TypedDict, Annotated, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from backend.agents.test_case_generator import TestCaseGenerationAgent
from backend.agents.test_data_generator import TestDataGenerationAgent
from backend.agents.test_script_automation import TestScriptAutomationAgent
from backend.agents.self_healing_test_script import SelfHealingTestScriptAgent
from backend.agents.test_summary_report import TestSummaryReportAgent
from backend.agents.change_impact_analysis import ChangeImpactAnalysisAgent
from backend.agents.release_readiness_advisor import ReleaseReadinessAdvisorAgent
from backend.agents.bug_report_generator import BugReportGenerationAgent
from backend.agents.base import (
    file_writer_tool, code_execution_tool, ui_state_fetcher_tool, issue_log_fetcher_tool, change_impact_analyzer_tool
)

# Define a graph state
class STLCGraphState(TypedDict):
    """
    Represents the state of our STLC automation process.
    Each key represents an output from an agent or an input to the graph.
    """
    requirements: str
    user_stories: str
    code_diffs: Annotated[Optional[str], operator.add] # Append multiple diffs if needed
    previous_test_results: Annotated[Optional[str], operator.add]

    # Agent outputs
    test_cases: str
    test_data: str
    automated_scripts: str
    self_healed_scripts: str # If self-healing occurred
    simulated_execution_results: str # Placeholder for actual execution
    bug_reports_raw_logs: str # Input for bug report gen
    structured_bug_reports: str
    test_summary_report: str
    change_impact_analysis: Dict[str, Any] # e.g., {"impact_level": "high", "recommendations": ["..."]}
    release_readiness_advice: str

    # Control flow
    current_status: str
    messages: Annotated[List[str], operator.add]
    errors: Annotated[List[str], operator.add]
    re_run_test_case_gen: bool # Flag for conditional re-runs


class Orchestrator:
    def __init__(self):
        self.test_case_gen_agent = TestCaseGenerationAgent()
        self.test_data_gen_agent = TestDataGenerationAgent()
        self.test_script_auto_agent = TestScriptAutomationAgent()
        self.test_self_healing_agent = SelfHealingTestScriptAgent()
        self.test_summary_agent = TestSummaryReportAgent()
        self.change_impact_agent = ChangeImpactAnalysisAgent()
        self.release_readiness_agent = ReleaseReadinessAdvisorAgent()
        self.bug_report_gen_agent = BugReportGenerationAgent()

        self.workflow = self._build_workflow()

    def _build_workflow(self):
        workflow = StateGraph(STLCGraphState)

        # 1. Nodes for each agent
        workflow.add_node("test_case_generation", self._test_case_generation)
        workflow.add_node("test_data_generation", self._test_data_generation)
        workflow.add_node("test_script_automation", self._test_script_automation)
        workflow.add_node("change_impact_analysis", self._change_impact_analysis)
        workflow.add_node("simulate_test_execution", self._simulate_test_execution) # Placeholder for actual test runner
        workflow.add_node("self_healing_scripts", self._self_healing_scripts)
        workflow.add_node("bug_report_generation", self._bug_report_generation)
        workflow.add_node("test_summary_reporting", self._test_summary_reporting)
        workflow.add_node("release_readiness_advisory", self._release_readiness_advisory)

        # 2. Define the graph flow
        workflow.set_entry_point("test_case_generation")

        # After Test Case Generation, always go to Test Data Generation
        workflow.add_edge("test_case_generation", "test_data_generation")
        workflow.add_edge("test_data_generation", "test_script_automation")

        # After Test Script Automation, decide based on `code_diffs`
        workflow.add_conditional_edges(
            "test_script_automation",
            self._decide_next_after_script_automation,
            {
                "change_impact_analysis": "change_impact_analysis",
                "simulate_test_execution": "simulate_test_execution",
            },
        )

        # After Change Impact Analysis, decide whether to re-generate test cases or proceed
        workflow.add_conditional_edges(
            "change_impact_analysis",
            self._decide_after_impact_analysis,
            {
                "re_run_test_case_gen": "test_case_generation", # Loop back to generation
                "simulate_test_execution": "simulate_test_execution",
            },
        )

        # After Test Execution, decide if self-healing is needed
        workflow.add_conditional_edges(
            "simulate_test_execution",
            self._decide_after_execution,
            {
                "self_healing_scripts": "self_healing_scripts", # If failures/changes detected
                "bug_report_generation": "bug_report_generation", # If no healing needed, but logs exist
            },
        )

        # After self-healing, go to bug report generation (assuming new logs)
        workflow.add_edge("self_healing_scripts", "bug_report_generation")

        # After bug report generation, go to test summary
        workflow.add_edge("bug_report_generation", "test_summary_reporting")

        # After test summary, go to release readiness
        workflow.add_edge("test_summary_reporting", "release_readiness_advisory")

        # Release readiness is the end point for this flow
        workflow.add_edge("release_readiness_advisory", END)

        return workflow.compile()

    # --- Node Functions (each corresponds to an agent's task) ---

    def _test_case_generation(self, state: STLCGraphState) -> Dict:
        print("\n--- Running Test Case Generation ---")
        requirements = state.get("requirements", "")
        user_stories = state.get("user_stories", "")
        test_cases = self.test_case_gen_agent.generate_test_cases(requirements, user_stories)
        file_writer_tool.run({
                "file_path": "artifacts/test_cases.md",
                "content": test_cases
            })
        return {
            "test_cases": test_cases,
            "current_status": "Test cases generated.",
            "messages": [f"Generated {len(test_cases.splitlines())} lines of test cases."],
            "re_run_test_case_gen": False
        }

    def _test_data_generation(self, state: STLCGraphState) -> Dict:
        print("\n--- Running Test Data Generation ---")
        test_cases = state.get("test_cases", "No test cases provided")
        # In a real scenario, constraints would be more detailed
        constraints = "string max 255, numbers 0-1000, valid emails required"
        test_data = self.test_data_gen_agent.generate_test_data(test_cases, constraints)
        file_writer_tool.run({
            "file_path": "artifacts/test_cases.md",
            "content": test_data
        })
        return {
            "test_data": test_data,
            "current_status": "Test data generated.",
            "messages": [f"Generated {len(test_data.splitlines())} lines of test data."],
        }

    def _test_script_automation(self, state: STLCGraphState) -> Dict:
        print("\n--- Running Test Script Automation ---")
        test_cases = state.get("test_cases", "No test cases provided")
        # Can choose framework dynamically.
        automated_scripts = self.test_script_auto_agent.automate_script(test_cases, "Python Playwright")
        file_writer_tool.run({
            "file_path": "artifacts/test_cases.md",
            "content": automated_scripts
        })
        return {
            "automated_scripts": automated_scripts,
            "current_status": "Test scripts automated.",
            "messages": [f"Automated {len(automated_scripts.splitlines())} lines of scripts."],
        }

    def _change_impact_analysis(self, state: STLCGraphState) -> Dict:
        print("\n--- Running Change Impact Analysis ---")
        code_diffs = state.get("code_diffs", "")
        if not code_diffs:
            return {
                "change_impact_analysis": {"impact_level": "none", "recommendations": []},
                "current_status": "No code diffs for impact analysis.",
                "messages": ["Skipping change impact analysis as no diffs were provided."]
            }
        
        # Use the tool directly within the node function for simplicity or let LLM decide
        impact_analysis_result_str = change_impact_analyzer_tool.run({"code_diff":code_diffs})

        # Parse the string into a structured format for the state
        impact_analysis_result = {
            "impact_level": "medium", # Default/fallback
            "affected_areas": [],
            "recommendations": []
        }
        if "high impact" in impact_analysis_result_str.lower():
            impact_analysis_result["impact_level"] = "high"
            impact_analysis_result["recommendations"].append("Extensive re-testing of affected functionalities is required.")
        elif "low impact" in impact_analysis_result_str.lower():
            impact_analysis_result["impact_level"] = "low"
            impact_analysis_result["recommendations"].append("Focus on visual regression or specific UI interaction tests.")
        
        if "new feature" in impact_analysis_result_str.lower():
            impact_analysis_result["recommendations"].append("New test cases and test data are needed for the new functionality.")
            impact_analysis_result["impact_level"] = "high" # Elevate if new features
            
        impact_analysis_result["recommendations"].append(f"LLM analysis: {impact_analysis_result_str}")

        return {
            "change_impact_analysis": impact_analysis_result,
            "current_status": "Change impact analysis completed.",
            "messages": [f"Impact: {impact_analysis_result.get('impact_level', 'Unknown')}. Recommendations: {', '.join(impact_analysis_result.get('recommendations', []))}"],
        }

    def _simulate_test_execution(self, state: STLCGraphState) -> Dict:
        print("\n--- Simulating Test Execution ---")
        scripts = state.get("automated_scripts", "No scripts to execute.")
        # This is a critical placeholder. Actual execution would run the scripts.
        simulated_result = code_execution_tool.run({
            "code": scripts,
            "language": "python"
        })

        # For demonstration, let's inject a "failure" that requires self-healing
        if "simulated_self_healing_needed" in state.get("requirements", "").lower():
             execution_log_content = "FAILURE: Login button not found (was 'btn-login', expected 'main-login-btn'). Test 2 failed: API endpoint /users not found."
             issue_log_content = "User login failed.\nAPI call failed."
        elif "simulated_bug_present" in state.get("requirements", "").lower():
            execution_log_content = "FAILURE: Test 'search' failed. Test 'checkout' failed."
            issue_log_content = "Search bar issue.\nCheckout button issue."
        else:
             execution_log_content = "All simulated tests passed successfully. No critical issues detected."
             issue_log_content = "No major issues logged from this simulated run."

        file_writer_tool.run({
            "file_path": "artifacts/simulated_execution_log.txt",
            "content": execution_log_content
        })
        return {
            "simulated_execution_results": execution_log_content,
            "bug_reports_raw_logs": issue_log_content, # Pass for bug generation
            "current_status": "Test execution simulated.",
            "messages": ["Simulated test execution. Check internal logs for details."],
        }

    def _self_healing_scripts(self, state: STLCGraphState) -> Dict:
        print("\n--- Running Self-Healing Test Script Agent ---")
        original_script = state.get("automated_scripts", "")
        failure_log = state.get("simulated_execution_results", "")
        ui_api_state = ui_state_fetcher_tool.run() # Fetch mock UI/API state

        healed_script = self.test_self_healing_agent.heal_script(
            original_script=original_script,
            failure_log=failure_log,
            ui_api_state_diff=ui_api_state # Assumes tool provides diff or agent processes it
        )
        file_writer_tool.run(file_path="artifacts/self_healed_scripts.py", content=healed_script)
        return {
            "self_healed_scripts": healed_script,
            "current_status": "Test scripts self-healed.",
            "messages": ["Test scripts updated by self-healing agent."],
        }

    def _bug_report_generation(self, state: STLCGraphState) -> Dict:
        print("\n--- Running Bug Report Generation ---")
        raw_logs = state.get("bug_reports_raw_logs", "") # From execution results
        if not raw_logs or "no major issues logged" in raw_logs.lower():
            return {
                "structured_bug_reports": "No significant issues to report from logs.",
                "current_status": "Bug report generation skipped (no issues).",
                "messages": ["No issues detected for bug report generation."]
            }

        # Fetch simulated raw logs (or use logs from earlier state)
        full_raw_logs = issue_log_fetcher_tool.run() + "\n" + raw_logs # Combine with any pre-existing
        structured_reports = self.bug_report_gen_agent.generate_bug_reports(full_raw_logs)
        file_writer_tool.run({
            "file_path": "artifacts/bug_reports.md",
            "content": structured_reports
        })

        return {
            "structured_bug_reports": structured_reports,
            "current_status": "Bug reports generated.",
            "messages": [f"Generated bug reports."],
        }

    def _test_summary_reporting(self, state: STLCGraphState) -> Dict:
        print("\n--- Running Test Summary Reporting ---")
        execution_data = state.get("simulated_execution_results", "")
        bug_reports = state.get("structured_bug_reports", "")
        # Placeholder for coverage data
        test_coverage = "Simulated test coverage: 85% code, 70% requirements."
        summary_report = self.test_summary_agent.generate_report(execution_data, bug_reports, test_coverage)
        file_writer_tool.run({
            "file_path": "artifacts/test_summary_report.md",
            "content": summary_report
        })

        return {
            "test_summary_report": summary_report,
            "current_status": "Test summary report generated.",
            "messages": ["Test summary report created."],
        }

    def _release_readiness_advisory(self, state: STLCGraphState) -> Dict:
        print("\n--- Running Release Readiness Advisory ---")
        test_summary = state.get("test_summary_report", "")
        bug_summary = state.get("structured_bug_reports", "")
        # Placeholder quality metrics
        quality_metrics = "Code quality score: 8/10. Critical bugs: 0. High bugs: 1. Passed tests: 95%."
        readiness_advice = self.release_readiness_agent.assess_readiness(
            test_summary, bug_summary, quality_metrics
        )
        return {
            "release_readiness_advice": readiness_advice,
            "current_status": "Release readiness assessed.",
            "messages": ["Release readiness assessment complete."],
        }

    # --- Conditional Edge Deciders ---

    def _decide_next_after_script_automation(self, state: STLCGraphState) -> str:
        """
        Decides whether to perform Change Impact Analysis or go straight to execution.
        """
        if state.get("code_diffs"):
            print("Decision: Code diffs present, proceeding to Change Impact Analysis.")
            return "change_impact_analysis"
        else:
            print("Decision: No code diffs, proceeding directly to Simulate Test Execution.")
            return "simulate_test_execution"

    def _decide_after_impact_analysis(self, state: STLCGraphState) -> str:
        """
        Decides whether to re-run test case generation based on change impact analysis.
        """
        impact = state.get("change_impact_analysis", {}).get("impact_level", "low")
        recommendations = state.get("change_impact_analysis", {}).get("recommendations", [])

        if "new test cases" in " ".join(recommendations).lower() or impact == "high":
            print(f"Decision: High impact ({impact}) or new features detected. Re-running test case generation.")
            return "re_run_test_case_gen" # This will loop back
        else:
            print("Decision: Impact is low/medium, proceeding to Simulate Test Execution.")
            return "simulate_test_execution"

    def _decide_after_execution(self, state: STLCGraphState) -> str:
        """
        Decides whether to trigger self-healing or proceed to bug report generation.
        """
        execution_results = state.get("simulated_execution_results", "").lower()
        # Simple heuristic: If "failure" and "button" or "api endpoint" is mentioned, assume self-healing needed
        if ("failure" in execution_results or "error" in execution_results) and \
           ("button" in execution_results or "api endpoint" in execution_results or "locator" in execution_results):
            print("Decision: Execution failures related to UI/API changes detected. Proceeding to Self-Healing.")
            return "self_healing_scripts"
        elif "failure" in execution_results or "error" in execution_results:
            print("Decision: General execution failures detected. Proceeding to Bug Report Generation.")
            return "bug_report_generation"
        else:
            print("Decision: No major failures or healing needed. Proceeding to Bug Report Generation.")
            return "bug_report_generation"

    def run_stlc(self, initial_state: Dict) -> Dict:
        """Runs the STLC workflow."""
        # Ensure 'artifacts' directory exists
        os.makedirs("artifacts", exist_ok=True)

        full_state = {
            "requirements": initial_state.get("requirements", ""),
            "user_stories": initial_state.get("user_stories", ""),
            "code_diffs": initial_state.get("code_diffs", ""),
            "previous_test_results": initial_state.get("previous_test_results", ""),
            "test_cases": "",
            "test_data": "",
            "automated_scripts": "",
            "self_healed_scripts": "",
            "simulated_execution_results": "",
            "bug_reports_raw_logs": "",
            "structured_bug_reports": "",
            "test_summary_report": "",
            "change_impact_analysis": {},
            "release_readiness_advice": "",
            "current_status": "Initialized",
            "messages": ["STLC workflow started."],
            "errors": [],
            "re_run_test_case_gen": False
        }
        
        # Stream the graph run for real-time updates (optional, for CLI)
        # For HTTP API, we might run it fully and return final state or use background tasks/websockets
        final_state = {}
        for s in self.workflow.stream(full_state):
            print(f"Current step: {list(s.keys())[0]}")
            final_state.update(s)
            
        print("\n--- STLC Workflow Completed ---")
        return final_state