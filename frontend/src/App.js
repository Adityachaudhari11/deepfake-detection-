import React, { useState, useEffect } from "react";
import { detectDeepfake } from "./Api";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    window.particlesJS.load("particles-js", "/particles.json", () => {});
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const handleDetect = async () => {
    if (!file) return;
    setLoading(true);
    const detection = await detectDeepfake(file);
    setResult(detection);
    setLoading(false);
  };

  return (
    <div className="main-content">
      <h1>Deepfake Detector</h1>
      <h2>Expose the Fake</h2>
      <p>
        Harness the power of AI to detect manipulated images.
        <br /> Upload, analyze, and detect with confidence.
      </p>

      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button className="cssbuttons-io" onClick={handleDetect}>
        <span>Start Detection</span>
      </button>

      {loading && <p>Analyzing...</p>}

      {result && (
        <div>
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <div>
              <h3>{result.label}</h3>
              <p>{result.message}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
