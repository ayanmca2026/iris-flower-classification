import React from 'react';

export default function ModelMetrics({ modelInfo }) {
  if (!modelInfo) return null;

  const {
    best_algorithm = 'K-Nearest Neighbors',
    accuracy = 1.0,
    precision = 1.0,
    recall = 1.0,
    f1_score = 1.0,
    cv_mean_accuracy = 0.9583,
    cv_std = 0.0456,
    model_comparison = []
  } = modelInfo;

  return (
    <section id="metrics" style={{ padding: '5rem 0' }}>
      <div className="container">
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <div className="hero-badge">Model Performance & Evaluation</div>
          <h2 style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>
            Model Benchmarks & Metrics
          </h2>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
            Selected Best Model: <strong style={{ color: 'var(--accent-cyan)' }}>{best_algorithm}</strong> (Selected dynamically based on test F1 score & 5-fold cross-validation).
          </p>
        </div>

        {/* Primary Metric Boxes */}
        <div className="metrics-grid">
          <div className="metric-box glass-card">
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: '600' }}>Selected Algorithm</div>
            <div className="metric-val" style={{ fontSize: '1.4rem', color: 'var(--accent-cyan)', marginTop: '0.5rem' }}>
              {best_algorithm}
            </div>
          </div>

          <div className="metric-box glass-card">
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: '600' }}>Test Accuracy</div>
            <div className="metric-val" style={{ color: '#34d399' }}>
              {(accuracy * 100).toFixed(1)}%
            </div>
          </div>

          <div className="metric-box glass-card">
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: '600' }}>Precision (Weighted)</div>
            <div className="metric-val" style={{ color: '#60a5fa' }}>
              {(precision * 100).toFixed(1)}%
            </div>
          </div>

          <div className="metric-box glass-card">
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: '600' }}>Recall (Weighted)</div>
            <div className="metric-val" style={{ color: '#c084fc' }}>
              {(recall * 100).toFixed(1)}%
            </div>
          </div>

          <div className="metric-box glass-card">
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: '600' }}>F1 Score (Weighted)</div>
            <div className="metric-val" style={{ color: '#f43f5e' }}>
              {(f1_score * 100).toFixed(1)}%
            </div>
          </div>

          <div className="metric-box glass-card">
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: '600' }}>5-Fold CV Mean Accuracy</div>
            <div className="metric-val" style={{ color: '#fbbf24' }}>
              {(cv_mean_accuracy * 100).toFixed(1)}%
            </div>
          </div>
        </div>

        {/* Model Comparison Table */}
        {model_comparison && model_comparison.length > 0 && (
          <div className="glass-card" style={{ marginTop: '3rem', padding: '2rem' }}>
            <h3 style={{ fontSize: '1.3rem', marginBottom: '1rem' }}>Model Comparison Matrix</h3>
            <div style={{ overflowX: 'auto' }}>
              <table className="custom-table">
                <thead>
                  <tr>
                    <th>Model Algorithm</th>
                    <th>Test Accuracy</th>
                    <th>Precision</th>
                    <th>Recall</th>
                    <th>F1 Score</th>
                    <th>5-Fold CV Mean</th>
                  </tr>
                </thead>
                <tbody>
                  {model_comparison.map((item, idx) => {
                    const isSelected = item.model === best_algorithm;
                    return (
                      <tr key={idx} style={{ background: isSelected ? 'rgba(99, 102, 241, 0.12)' : 'transparent', fontWeight: isSelected ? '700' : '400' }}>
                        <td style={{ color: isSelected ? 'var(--accent-cyan)' : 'var(--text-primary)' }}>
                          {item.model} {isSelected && '⭐ (Best)'}
                        </td>
                        <td>{(item.accuracy * 100).toFixed(1)}%</td>
                        <td>{(item.precision * 100).toFixed(1)}%</td>
                        <td>{(item.recall * 100).toFixed(1)}%</td>
                        <td>{(item.f1_score * 100).toFixed(1)}%</td>
                        <td>{(item.cv_mean * 100).toFixed(1)}%</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
