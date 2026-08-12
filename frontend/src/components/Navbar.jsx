import React from 'react';

export default function Navbar({ isOnline }) {
  return (
    <nav className="navbar">
      <div className="container navbar-inner">
        <a href="#home" className="brand-logo">
          <div className="brand-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2a10 10 0 1 0 10 10H12V2z"></path>
              <path d="M12 12L2.1 12.1"></path>
              <path d="M12 12l4.3-4.3"></path>
            </svg>
          </div>
          <span>Iris<span className="gradient-text">AI</span></span>
        </a>

        <ul className="nav-links">
          <li><a href="#home" className="nav-link">Home</a></li>
          <li><a href="#predict" className="nav-link">Predict</a></li>
          <li><a href="#metrics" className="nav-link">Model Specs</a></li>
          <li><a href="#dataset" className="nav-link">Dataset</a></li>
          <li><a href="#how-it-works" className="nav-link">How It Works</a></li>
        </ul>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', fontWeight: '600', color: isOnline ? '#10b981' : '#f43f5e' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: isOnline ? '#10b981' : '#f43f5e', boxShadow: isOnline ? '0 0 10px #10b981' : 'none' }}></span>
          {isOnline ? 'API Connected' : 'Offline Mode'}
        </div>
      </div>
    </nav>
  );
}
