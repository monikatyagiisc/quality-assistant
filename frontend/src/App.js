import React, { useState } from 'react';

import './App.css';
 
function App() {

  const [requirements, setRequirements] = useState('');

  const [userStories, setUserStories] = useState('');

  const [codeDiffs, setCodeDiffs] = useState('');

  const [previousTestResults, setPreviousTestResults] = useState('');

  const [loading, setLoading] = useState(false);

  const [stlcResult, setStlcResult] = useState(null);

  const [error, setError] = useState(null);
 
  const backendUrl = 'http://localhost:8000';
 
  const handleStartStlc = async () => {

    setLoading(true);

    setStlcResult(null);

    setError(null);
 
    const payload = {

      requirements,

      user_stories: userStories || null,

      code_diffs: codeDiffs || null,

      previous_test_results: previousTestResults || null,

    };
 
    try {

      const response = await fetch(`${backendUrl}/chat`, {

        method: 'POST',

        headers: { 'Content-Type': 'application/json' },

        body: JSON.stringify(payload),

      });
 
      if (!response.ok) {

        const errorData = await response.json();

        throw new Error(errorData.detail || 'STLC process failed');

      }
 
      const data = await response.json();

      setStlcResult(data?.response || {});

    } catch (err) {

      setError(err.message);

    } finally {

      setLoading(false);

    }

  };
 
  const renderTextarea = (label, value) => (

    value ? (
<>
<h3>{label}:</h3>
<textarea rows="10" readOnly value={value} style={{ width: '100%' }}></textarea>
</>

    ) : null

  );
 
  return (
<div className="App">
<header className="App-header">
<h1>AI-Powered STLC Orchestrator</h1>
</header>
<main className="App-main">
<div className="input-section">
<h2>Input Software Details</h2>
<div className="input-group">
<label htmlFor="requirements">Software Requirements:</label>
<textarea id="requirements" rows="5" value={requirements} onChange={(e) => setRequirements(e.target.value)}></textarea>
</div>
<div className="input-group">
<label htmlFor="userStories">User Stories (Optional):</label>
<textarea id="userStories" rows="3" value={userStories} onChange={(e) => setUserStories(e.target.value)}></textarea>
</div>
<div className="input-group">
<label htmlFor="codeDiffs">Code Diffs (Optional):</label>
<textarea id="codeDiffs" rows="4" value={codeDiffs} onChange={(e) => setCodeDiffs(e.target.value)}></textarea>
</div>
<div className="input-group">
<label htmlFor="previousTestResults">Previous Test Results (Optional):</label>
<textarea id="previousTestResults" rows="3" value={previousTestResults} onChange={(e) => setPreviousTestResults(e.target.value)}></textarea>
</div>
<button onClick={handleStartStlc} disabled={loading || !requirements}>

            {loading ? 'Running STLC...' : 'Start STLC Process'}
</button>
</div>
 
        {error && (
<div className="error-message">
<h3>Error:</h3>
<pre>{error}</pre>
</div>

        )}
 
        {stlcResult && (
<div className="output-section">
<h2>STLC Results</h2>
 
            {renderTextarea("Test Cases", stlcResult.test_case_generation?.test_cases)}

            {renderTextarea("Test Data", stlcResult.test_data_generation?.test_data)}

            {renderTextarea("Automated Scripts", stlcResult.test_script_automation?.automated_scripts)}

            {renderTextarea("Change Impact Analysis", JSON.stringify(stlcResult.change_impact_analysis?.change_impact_analysis, null, 2))}
            {renderTextarea("Bug Reports", stlcResult.bug_report_generation?.structured_bug_reports)}

            {renderTextarea("Simulated Execution Results", stlcResult.simulate_test_execution?.simulated_execution_results)}

            {renderTextarea("Test Summary Report", stlcResult.test_summary_reporting?.test_summary_report)}

            {renderTextarea("Release Readiness", stlcResult.release_readiness_advisory?.release_readiness_advice)}
</div>

        )}
</main>
</div>

  );

}
 
export default App;
 