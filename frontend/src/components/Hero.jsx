import React from 'react';

export default function Hero() {
  return (
    <section id="home" className="hero-section">
      <div className="container">
        <div className="hero-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
          Supervised Machine Learning System
        </div>

        <h1 className="hero-title">
          Iris Flower <br />
          <span className="gradient-text">Species Classification</span>
        </h1>

        <p className="hero-subtitle">
          Predict Iris flower species (Setosa, Versicolor, Virginica) instantly using tuned scikit-learn machine learning models trained on physical sepal & petal dimensions.
        </p>

        <div className="hero-cta">
          <a href="#predict" className="btn-primary">
            Start Prediction
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </a>
          <a href="#metrics" className="btn-secondary">
            View Model Metrics
          </a>
        </div>
      </div>
    </section>
  );
}
