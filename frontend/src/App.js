import React, { useState } from 'react';
import './App.css';
import imageUrl from 'url:./image.png';

 
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


  const [isRequirementsOpen, setIsRequirementsOpen] = useState(true);

  const [isUserStoriesOpen, setIsUserStoriesOpen] = useState(false);

  const [isCodeDiffsOpen, setIsCodeDiffsOpen] = useState(false);

  const [isPreviousTestResultsOpen, setIsPreviousTestResultsOpen] = useState(false);
 

  const backendUrl = 'http://localhost:8000';

  // Handle file upload for Software Requirements
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Check if it's a text file
      if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          setRequirements(e.target.result);
        };
        reader.onerror = () => {
          setError('Failed to read file. Please try again.');
        };
        reader.readAsText(file);
      } else {
        setError('Please upload a valid text file (.txt)');
      }
    }
  };
 
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
              setTimeout(() => setCopiedMap((prev) => ({ ...prev, [label]: false })), 2000);
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
<div className="header-content">
<img 
            src={imageUrl} 
            alt="Quality Assistant Agent Logo" 
            className="header-logo"
          />
<div className="header-text">
<h1>Quality Assistant Agent</h1>
<h2>Driving Intelligent Test Automation</h2>
</div>
</div>
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
<div className="accordion-item">
<div 
            className="accordion-header" 
            onClick={() => setIsRequirementsOpen(!isRequirementsOpen)}
          >
<span>Requirements</span>
<span className="accordion-icon">{isRequirementsOpen ? '−' : '+'}</span>

</div>
          {isRequirementsOpen && (
<div className="accordion-content">
<div className="input-group">
<label htmlFor="requirements">Enter a requirement, and the Quality Assistant Agent will generate relevant test cases, along with additional analysis outputs.</label>

<textarea 
                  id="requirements" 
                  rows="5" 
                  value={requirements} 
                  onChange={(e) => setRequirements(e.target.value)}
                  placeholder=" Requirements"
                ></textarea>
<div className="file-upload-container">
<input 
                      type="file" 
                      id="fileUpload" 
                      accept=".txt,text/plain" 
                      onChange={handleFileUpload}
                      style={{ marginBottom: '10px' }}
                    />
<label htmlFor="fileUpload" style={{ fontSize: '0.9em', color: '#666' }}>
                      Upload a text file or type above
</label>
</div>
</div>
</div>
          )}
</div>
<div className="accordion-item">
<div 
            className="accordion-header" 
            onClick={() => setIsUserStoriesOpen(!isUserStoriesOpen)}
          >
<span>User Stories (Optional)</span>
<span className="accordion-icon">{isUserStoriesOpen ? '−' : '+'}</span>
</div>
          {isUserStoriesOpen && (
<div className="accordion-content">
<div className="input-group">
<label htmlFor="userStories">User Stories (Optional):</label>
<textarea id="userStories" rows="3" value={userStories} onChange={(e) => setUserStories(e.target.value)}></textarea>
</div>
</div>
          )}
</div>
<div className="accordion-item">
<div 
            className="accordion-header" 
            onClick={() => setIsCodeDiffsOpen(!isCodeDiffsOpen)}
          >
<span>Code Diffs (Optional)</span>
<span className="accordion-icon">{isCodeDiffsOpen ? '−' : '+'}</span>
</div>
          {isCodeDiffsOpen && (
<div className="accordion-content">
<div className="input-group">
<label htmlFor="codeDiffs">Code Diffs (Optional):</label>
<textarea id="codeDiffs" rows="4" value={codeDiffs} onChange={(e) => setCodeDiffs(e.target.value)}></textarea>
</div>
</div>
          )}
</div>
<div className="accordion-item">
<div 
            className="accordion-header" 
            onClick={() => setIsPreviousTestResultsOpen(!isPreviousTestResultsOpen)}
          >
<span>Previous Test Results (Optional)</span>
<span className="accordion-icon">{isPreviousTestResultsOpen ? '−' : '+'}</span>
</div>
          {isPreviousTestResultsOpen && (
<div className="accordion-content">
<div className="input-group">
<label htmlFor="previousTestResults">Previous Test Results (Optional):</label>
<textarea id="previousTestResults" rows="3" value={previousTestResults} onChange={(e) => setPreviousTestResults(e.target.value)}></textarea>
</div>

<div className="disclaimer-text">Do not enter personal or sensitive information. Use only technical or system-related data</div>

</div>
          )}
</div>

<button onClick={handleStartStlc} disabled={loading || !requirements}>

            {loading ? 'Running...' : 'Start Process'}
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
  <h1>Software Testing Lifecycle Results</h1>
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
          setTimeout(() => setCopiedAll(false), 2000);
        });
      }
    }}
  >
    {copiedAll ? 'Copied All!' : 'Copy All Results'}
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
 