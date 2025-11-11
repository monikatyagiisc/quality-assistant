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
  const [copiedTC, setCopiedTC] = useState(false);
  const [copiedMap, setCopiedMap] = useState({});
  const [copiedAll, setCopiedAll] = useState(false);

  const backendUrl = 'http://localhost:8000';
 
  const MAX_REQ_LEN = 1000;
  const handleRequirementsChange = (e) => {
    const val = e.target.value || '';
    // Enforce max length defensively even with maxLength attribute
    setRequirements(val.length > MAX_REQ_LEN ? val.slice(0, MAX_REQ_LEN) : val);
  };

  const handleFeatureClick = () => {
    const reqTextarea = document.getElementById('requirements');
    if (reqTextarea) {
      reqTextarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
      reqTextarea.focus();
    }
  };
 
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

  const renderCopyTextarea = (label, value) => (
    value ? (
      <>
        <h3 className="section-title">{label}:</h3>
        <textarea rows="10" readOnly value={value} style={{ width: '100%' }}></textarea>
        <div className="copy-actions">
          <button
            onClick={async () => {
              await navigator.clipboard.writeText(value || '');
              setCopiedMap((prev) => ({ ...prev, [label]: true }));
              setTimeout(() => setCopiedMap((prev) => ({ ...prev, [label]: false })), 1000);
            }}
            className={`copy-btn ${copiedMap[label] ? 'copied' : ''}`}
          >
            {copiedMap[label] ? 'Copied!' : 'Copy'}
          </button>
        </div>
      </>
    ) : null
  );
 
  return (
<div className="App">
<header className="App-header">
<h1>AI-Powered STLC Orchestrator</h1>
</header>
<main className="App-main">

<div className="welcome-banner">
<div className="welcome-header">
<div className="bot-icon">🤖</div>
<div className="welcome-title">
<h3>Welcome to Quality Assistant Agent!</h3>
<p className="subtitle">Your AI-Powered STLC Companion</p>
</div>
</div>
<p className="welcome-description">
            Accelerate your testing lifecycle with intelligent test generation, data creation, automation, 
            and comprehensive analysis—all powered by advanced AI.
</p>
<div className="feature-grid">
<div className="feature-box" onClick={handleFeatureClick}>
<span className="feature-icon">🧪</span>
<span className="feature-text">Test Cases</span>
</div>
<div className="feature-box" onClick={handleFeatureClick}>
<span className="feature-icon">📊</span>
<span className="feature-text">Test Data</span>
</div>
<div className="feature-box" onClick={handleFeatureClick}>
<span className="feature-icon">⚙️</span>
<span className="feature-text">Automation</span>
</div>
<div className="feature-box" onClick={handleFeatureClick}>
<span className="feature-icon">🔍</span>
<span className="feature-text">Impact Analysis</span>
</div>
<div className="feature-box" onClick={handleFeatureClick}>
<span className="feature-icon">🐛</span>
<span className="feature-text">Bug Reports</span>
</div>
<div className="feature-box" onClick={handleFeatureClick}>
<span className="feature-icon">▶️</span>
<span className="feature-text">Test Execution</span>
</div>
</div>
</div>

<div className="input-section">
<h2>Input Software Details</h2>
<div className="input-group">
<label htmlFor="requirements">Software Requirements:</label>
<textarea id="requirements" rows="5" value={requirements} onChange={handleRequirementsChange} maxLength={MAX_REQ_LEN}></textarea>
<div style={{ textAlign: 'right', fontSize: '12px', color: '#555' }}>{requirements.length} / {MAX_REQ_LEN}</div>
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
<div className="disclaimer-text">Do not enter P11 or sensitive data.</div>
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
<div className="section-header">
  <h2>STLC Results</h2>
  <button
    className={`copy-btn ${copiedAll ? 'copied' : ''}`}
    onClick={() => {
      const texts = [];
      const add = (label, value, isJson=false) => {
        if (value == null || value === '') return;
        const content = isJson ? JSON.stringify(value, null, 2) : value;
        texts.push(`${label}:\n${content}`);
      };
      add('Test Cases', stlcResult.test_case_generation?.test_cases);
      add('Test Data', stlcResult.test_data_generation?.test_data);
      add('Automated Scripts', stlcResult.test_script_automation?.automated_scripts);
      add('Change Impact Analysis', stlcResult.change_impact_analysis?.change_impact_analysis, true);
      add('Bug Reports', stlcResult.bug_report_generation?.structured_bug_reports);
      add('Simulated Execution Results', stlcResult.simulate_test_execution?.simulated_execution_results);
      add('Test Summary Report', stlcResult.test_summary_reporting?.test_summary_report);
      add('Release Readiness', stlcResult.release_readiness_advisory?.release_readiness_advice);
      const all = texts.join("\n\n\n");
      if (all) {
        navigator.clipboard.writeText(all).then(() => {
          setCopiedAll(true);
          setTimeout(() => setCopiedAll(false), 1000);
        });
      }
    }}
  >
    {copiedAll ? 'Copied!' : 'Copy All'}
  </button>
</div>
 
            {renderCopyTextarea("Test Cases", stlcResult.test_case_generation?.test_cases)}         


            {renderCopyTextarea("Test Data", stlcResult.test_data_generation?.test_data)}

            {renderCopyTextarea("Automated Scripts", stlcResult.test_script_automation?.automated_scripts)}

            {renderCopyTextarea("Change Impact Analysis", JSON.stringify(stlcResult.change_impact_analysis?.change_impact_analysis, null, 2))}
            {renderCopyTextarea("Bug Reports", stlcResult.bug_report_generation?.structured_bug_reports)}

            {renderCopyTextarea("Simulated Execution Results", stlcResult.simulate_test_execution?.simulated_execution_results)}

            {renderCopyTextarea("Test Summary Report", stlcResult.test_summary_reporting?.test_summary_report)}

            {renderCopyTextarea("Release Readiness", stlcResult.release_readiness_advisory?.release_readiness_advice)}
</div>

        )}
</main>
</div>

  );

}
 
export default App;
 