import React from 'react';

export default function PredictionResult({ result }) {
  if (!result) {
    return (
      <div className="glass-card" style={{ padding: '2.5rem', textAlign: 'center', minHeight: '380px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'rgba(99, 102, 241, 0.1)', border: '1px dashed var(--border-glow)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.25rem' }}>
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 8v4l3 3"></path>
          </svg>
        </div>
        <h3 style={{ fontSize: '1.25rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>No Prediction Yet</h3>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', maxWidth: '320px' }}>
          Enter flower sepal & petal measurements on the left form and click "Predict Species" to run machine learning inference.
        </p>
      </div>
    );
  }

  const { prediction, confidence, probabilities } = result;

  const getBadgeClass = (species) => {
    const s = species.toLowerCase();
    if (s.includes('setosa')) return 'badge-setosa';
    if (s.includes('versicolor')) return 'badge-versicolor';
    if (s.includes('virginica')) return 'badge-virginica';
    return 'badge-setosa';
  };

  const getSpeciesColor = (species) => {
    const s = species.toLowerCase();
    if (s.includes('setosa')) return '#3b82f6';
    if (s.includes('versicolor')) return '#10b981';
    if (s.includes('virginica')) return '#8b5cf6';
    return '#6366f1';
  };

  const formattedConfidence = (confidence * 100).toFixed(2);

  return (
    <div className="result-card">
      <div style={{ textTransform: 'uppercase', fontSize: '0.8rem', fontWeight: '700', color: 'var(--accent-cyan)', letterSpacing: '0.05em' }}>
        ML Model Output
      </div>
      
      <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Predicted Species</div>
      <div className={`species-badge ${getBadgeClass(prediction)}`}>
        {prediction}
      </div>

      <div style={{ margin: '1rem 0' }}>
        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', uppercase: 'true' }}>Confidence Score</div>
        <div style={{ fontSize: '2.2rem', fontWeight: '800', fontFamily: 'var(--font-heading)', color: getSpeciesColor(prediction) }}>
          {formattedConfidence}%
        </div>
      </div>

      {/* Dynamic Probability Bar Breakdown */}
      <div style={{ marginTop: '2rem', textAlign: 'left' }}>
        <div style={{ fontSize: '0.9rem', fontWeight: '700', marginBottom: '1rem', color: 'var(--text-primary)', borderBottom: '1px solid var(--border-card)', paddingBottom: '0.5rem' }}>
          Probability Breakdown
        </div>

        {probabilities && Object.entries(probabilities).map(([cls, prob]) => {
          const pct = (prob * 100).toFixed(1);
          const color = getSpeciesColor(cls);
          return (
            <div key={cls} className="progress-bar-container" style={{ marginBottom: '1rem' }}>
              <div className="progress-bar-label">
                <span>{cls}</span>
                <span style={{ color: color, fontWeight: '700' }}>{pct}%</span>
              </div>
              <div className="progress-track">
                <div
                  className="progress-fill"
                  style={{
                    width: `${pct}%`,
                    background: color,
                    boxShadow: `0 0 10px ${color}88`
                  }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
