## How to Run

1.  **Clone the repository (or create the files manually):**
    ```bash
    cd risk-compliance-agent
    ```

2.  **Backend Setup & Run:**
    ```bash
    # Create and activate virtual environment
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate

    # Install Python dependencies
    pip install fastapi uvicorn "langchain_google_vertexai" "langchainhub" "langchain" "langgraph" "python-dotenv"

    # Set up Google Cloud authentication (if not already done)
    gcloud auth application-default login

    # Create a .env file in the `stlc-ai` root with your GCP project details:
    # GOOGLE_CLOUD_PROJECT=your-gcp-project-id
    # GOOGLE_CLOUD_LOCATION=us-central1

    # Run the FastAPI backend
    python backend/main.py
    ```
    The backend will start on `http://localhost:8000`.

3.  **Frontend Setup & Run:**
    ```bash
    cd frontend

    # Install Node.js dependencies
    npm install

    # Start the React development server
    npm start
    ```
    The React app will open in your browser, usually at `http://localhost:3000`.

4.  **Interact:**
    *   Open `http://localhost:3000` in your browser.
    *   Enter some requirements (e.g., "Implement user login with username and password. User should be redirected to dashboard upon successful login.").
    *   Optionally, add user stories, code diffs (to trigger change impact analysis), or previous test results (for release readiness).
    *   Click "Start STLC Process".
    *   Observe the output from each agent rendered on the page and the console output from the backend.
    *   **To trigger Self-Healing demo:** In the "Software Requirements" input, also include `simulated_self_healing_needed`. This flag in the prompt will cause the `simulate_test_execution` node to report a specific failure, leading to the `self_healing_scripts` node being activated.
    *   **To trigger Bug Report demo:** In the "Software Requirements" input, also include `simulated_bug_present`. This will cause `simulate_test_execution` to report general failures that will then be processed into structured bug reports.

## Further Enhancements

*   **Asynchronous Processing:** For long-running STLC flows, implement asynchronous processing in FastAPI (e.g., using Celery with Redis/RabbitMQ) and WebSockets for real-time updates to the frontend.
*   **Persistent State:** Store `STLCGraphState` in a database (e.g., PostgreSQL, MongoDB) to allow tracking multiple runs, pausing/resuming workflows, and retrieving historical data.
*   **Actual Tool Integrations:** Replace placeholder tools with real-world integrations (Jira API, Git APIs, Selenium/Playwright execution, CI/CD pipelines, static analysis tools).
*   **User Authentication & Authorization:** Implement security for the backend API.
*   **Advanced LangGraph Flows:** Incorporate more complex decision nodes, human-in-the-loop steps (e.g., requiring approval for release readiness), and parallel execution.
*   **Error Handling & Retries:** Add more robust error handling and retry mechanisms for agent failures or external tool issues.
*   **Logging & Monitoring:** Implement comprehensive logging and monitoring for tracking STLC runs, agent performance, and issues.
*   **Structured Outputs for Agents:** Define Pydantic models for each agent's output to ensure consistency and easier parsing by subsequent agents.
*   **Vector Databases:** Use vector databases for storing requirements, test cases, and execution logs to allow for semantic search and more intelligent retrieval for agents (e.g., finding relevant test cases for a code change).
*   **Agent Persona & Memory:** Give agents specific "memory" (e.g., conversation history or access to a knowledge base over long runs).