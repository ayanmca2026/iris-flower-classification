import React from 'react';

export default function HowItWorks() {
  const steps = [
    { num: '01', title: 'Enter Measurements', desc: 'Input 4 physical flower metrics: Sepal Length, Sepal Width, Petal Length, and Petal Width.' },
    { num: '02', title: 'Validate Input', desc: 'Pydantic v2 schemas inspect numeric data types, range boundaries, and prevent NaN/Infinity values.' },
    { num: '03', title: 'Scale Features', desc: 'StandardScaler normalizes the 4 measurements using pre-fitted training set mean and variance.' },
    { num: '04', title: 'Run ML Model', desc: 'The trained K-Nearest Neighbors / Random Forest classifier computes distance vectors and class probabilities.' },
    { num: '05', title: 'Predict Species', desc: 'LabelEncoder maps the highest likelihood class index back to Iris-setosa, Versicolor, or Virginica.' },
    { num: '06', title: 'Display Confidence', desc: 'Renders prediction label, confidence score, and interactive probability breakdown bars.' }
  ];

  return (
    <section id="how-it-works" style={{ padding: '5rem 0' }}>
      <div className="container">
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <div className="hero-badge">Pipeline Architecture</div>
          <h2 style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>How IrisAI Classification Works</h2>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
            From raw user input to production machine learning inference in 6 real-time steps.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          {steps.map((step, idx) => (
            <div key={idx} className="glass-card" style={{ padding: '2rem', position: 'relative' }}>
              <div style={{ fontSize: '2.5rem', fontWeight: '800', fontFamily: 'var(--font-heading)', color: 'rgba(99, 102, 241, 0.3)', marginBottom: '0.5rem' }}>
                {step.num}
              </div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>{step.title}</h3>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
