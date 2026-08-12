import React from 'react';

export default function Footer() {
  return (
    <footer style={{ background: '#070a12', borderTop: '1px solid var(--border-card)', padding: '3rem 0 2rem 0', marginTop: '4rem' }}>
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1.5rem', marginBottom: '2rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '1.4rem', fontWeight: '800', fontFamily: 'var(--font-heading)', marginBottom: '0.5rem' }}>
              <div className="brand-icon" style={{ width: '32px', height: '32px' }}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5">
                  <path d="M12 2a10 10 0 1 0 10 10H12V2z"></path>
                </svg>
              </div>
              Iris<span className="gradient-text">AI</span>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', maxWidth: '400px' }}>
              End-to-End Iris Flower Species Classification project powered by Scikit-Learn, FastAPI, and React.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <span className="preset-chip">Python 3.11+</span>
            <span className="preset-chip">Scikit-Learn</span>
            <span className="preset-chip">FastAPI</span>
            <span className="preset-chip">React 18</span>
            <span className="preset-chip">Vite</span>
            <span className="preset-chip">Pydantic v2</span>
          </div>
        </div>

        <div style={{ borderTop: '1px solid var(--border-card)', paddingTop: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          <div>© {new Date().getFullYear()} IrisAI Project. All Rights Reserved.</div>
          <div>Built for Data Science & Full-Stack Deployment</div>
        </div>
      </div>
    </footer>
  );
}
