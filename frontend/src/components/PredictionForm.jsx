import React, { useState } from 'react';

export default function PredictionForm({ onPredict, loading, error }) {
  const [formData, setFormData] = useState({
    sepal_length: '5.1',
    sepal_width: '3.5',
    petal_length: '1.4',
    petal_width: '0.2'
  });

  const [validationErr, setValidationErr] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setValidationErr('');
  };

  const applyPreset = (presetValues) => {
    setFormData(presetValues);
    setValidationErr('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setValidationErr('');

    const sl = parseFloat(formData.sepal_length);
    const sw = parseFloat(formData.sepal_width);
    const pl = parseFloat(formData.petal_length);
    const pw = parseFloat(formData.petal_width);

    if (isNaN(sl) || isNaN(sw) || isNaN(pl) || isNaN(pw)) {
      setValidationErr('Please enter valid numeric values for all four measurements.');
      return;
    }

    if (sl <= 0 || sw <= 0 || pl <= 0 || pw <= 0) {
      setValidationErr('All measurements must be strictly positive numbers.');
      return;
    }

    if (sl > 15 || sw > 15 || pl > 15 || pw > 15) {
      setValidationErr('Measurement values exceed reasonable flower dimensions (< 15 cm).');
      return;
    }

    onPredict({ sepal_length: sl, sepal_width: sw, petal_length: pl, petal_width: pw });
  };

  const handleReset = () => {
    setFormData({
      sepal_length: '',
      sepal_width: '',
      petal_length: '',
      petal_width: ''
    });
    setValidationErr('');
  };

  return (
    <div className="glass-card" style={{ padding: '2.5rem' }}>
      <div style={{ marginBottom: '1.5rem', textTransform: 'uppercase', fontSize: '0.8rem', fontWeight: '700', color: 'var(--accent-cyan)', letterSpacing: '0.05em' }}>
        Interactive Classification
      </div>
      <h2 style={{ fontSize: '1.8rem', marginBottom: '1rem' }}>Enter Flower Measurements</h2>

      {/* Preset Quick Fill Buttons */}
      <div className="presets-container">
        <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: '600' }}>Sample Presets:</span>
        <button
          type="button"
          className="preset-chip"
          onClick={() => applyPreset({ sepal_length: '5.1', sepal_width: '3.5', petal_length: '1.4', petal_width: '0.2' })}
        >
          Setosa Sample
        </button>
        <button
          type="button"
          className="preset-chip"
          onClick={() => applyPreset({ sepal_length: '6.0', sepal_width: '2.9', petal_length: '4.5', petal_width: '1.5' })}
        >
          Versicolor Sample
        </button>
        <button
          type="button"
          className="preset-chip"
          onClick={() => applyPreset({ sepal_length: '6.9', sepal_width: '3.1', petal_length: '5.4', petal_width: '2.1' })}
        >
          Virginica Sample
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className="form-group">
            <label className="form-label">
              <span>Sepal Length (cm)</span>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Range: 4.0 – 8.0</span>
            </label>
            <input
              type="number"
              step="0.1"
              name="sepal_length"
              value={formData.sepal_length}
              onChange={handleInputChange}
              placeholder="e.g. 5.1"
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              <span>Sepal Width (cm)</span>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Range: 2.0 – 4.5</span>
            </label>
            <input
              type="number"
              step="0.1"
              name="sepal_width"
              value={formData.sepal_width}
              onChange={handleInputChange}
              placeholder="e.g. 3.5"
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              <span>Petal Length (cm)</span>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Range: 1.0 – 7.0</span>
            </label>
            <input
              type="number"
              step="0.1"
              name="petal_length"
              value={formData.petal_length}
              onChange={handleInputChange}
              placeholder="e.g. 1.4"
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              <span>Petal Width (cm)</span>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Range: 0.1 – 2.5</span>
            </label>
            <input
              type="number"
              step="0.1"
              name="petal_width"
              value={formData.petal_width}
              onChange={handleInputChange}
              placeholder="e.g. 0.2"
              className="form-input"
              required
            />
          </div>
        </div>

        {(validationErr || error) && (
          <div style={{ marginTop: '1.25rem', padding: '0.85rem 1.25rem', borderRadius: 'var(--radius-md)', background: 'rgba(244, 63, 94, 0.15)', border: '1px solid rgba(244, 63, 94, 0.4)', color: '#fda4af', fontSize: '0.9rem', fontWeight: '500' }}>
            ⚠️ {validationErr || error}
          </div>
        )}

        <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
          <button
            type="submit"
            className="btn-primary"
            disabled={loading}
            style={{ flex: 1, justifyContent: 'center', opacity: loading ? 0.7 : 1 }}
          >
            {loading ? 'Predicting...' : 'Predict Species'}
          </button>
          <button
            type="button"
            className="btn-secondary"
            onClick={handleReset}
            disabled={loading}
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  );
}
