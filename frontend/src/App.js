import React, { useState } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    prompt: "",
    model1: "",
    model2: "",
    model3: "",
  });
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await fetch("http://localhost:8000/evaluate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!result.ok) {
        throw new Error(`HTTP error! status: ${result.status}`);
      }

      const data = await result.json();
      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Model Evaluation Tool</h1>

        <form onSubmit={handleSubmit} className="evaluation-form">
          <div className="input-group">
            <label htmlFor="prompt">Prompt:</label>
            <textarea
              id="prompt"
              name="prompt"
              value={formData.prompt}
              onChange={handleInputChange}
              placeholder="Enter your prompt here..."
              rows="4"
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="model1">Model 1:</label>
            <textarea
              id="model1"
              name="model1"
              value={formData.model1}
              onChange={handleInputChange}
              placeholder="Enter model 1 content..."
              rows="4"
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="model2">Model 2:</label>
            <textarea
              id="model2"
              name="model2"
              value={formData.model2}
              onChange={handleInputChange}
              placeholder="Enter model 2 content..."
              rows="4"
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="model3">Model 3:</label>
            <textarea
              id="model3"
              name="model3"
              value={formData.model3}
              onChange={handleInputChange}
              placeholder="Enter model 3 content..."
              rows="4"
              required
            />
          </div>

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? "Evaluating..." : "Evaluate Models"}
          </button>
        </form>

        {error && (
          <div className="error">
            <h3>Error:</h3>
            <p>{error}</p>
          </div>
        )}

        {response && (
          <div className="response">
            <h3>Evaluation Results:</h3>
            <pre className="json-response">
              {JSON.stringify(response, null, 2)}
            </pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
