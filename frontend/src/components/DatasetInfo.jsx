import React from 'react';

export default function DatasetInfo({ datasetInfo }) {
  const totalSamples = datasetInfo?.total_samples || 150;
  const totalFeatures = datasetInfo?.total_features || 4;
  const speciesCounts = datasetInfo?.class_distribution || { 'Iris-setosa': 50, 'Iris-versicolor': 50, 'Iris-virginica': 50 };

  const featuresList = [
    {
      title: 'Sepal Length (cm)',
      desc: 'Length of the outer floral envelope (sepal). Helps differentiate Iris Setosa from larger species.',
      avg: datasetInfo?.statistics?.sepal_length?.mean?.toFixed(2) || '5.84'
    },
    {
      title: 'Sepal Width (cm)',
      desc: 'Width of the outer floral envelope. Setosa flowers possess characteristically wider sepals.',
      avg: datasetInfo?.statistics?.sepal_width?.mean?.toFixed(2) || '3.06'
    },
    {
      title: 'Petal Length (cm)',
      desc: 'Length of the inner floral petals. One of the strongest predictive features separating all 3 species.',
      avg: datasetInfo?.statistics?.petal_length?.mean?.toFixed(2) || '3.75'
    },
    {
      title: 'Petal Width (cm)',
      desc: 'Width of the inner floral petals. Exhibits strong positive linear correlation with Petal Length.',
      avg: datasetInfo?.statistics?.petal_width?.mean?.toFixed(2) || '1.20'
    }
  ];

  return (
    <section id="dataset" style={{ padding: '5rem 0', background: 'rgba(15, 23, 42, 0.4)' }}>
      <div className="container">
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <div className="hero-badge">Exploratory Data Analysis</div>
          <h2 style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>Dataset Overview & Features</h2>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '650px', margin: '0 auto' }}>
            The Iris dataset is a classic multivariate data science benchmark collected by Edgar Anderson and introduced by Ronald Fisher.
          </p>
        </div>

        {/* Overview Stat Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
          <div className="glass-card" style={{ padding: '1.5rem', textAlign: 'center' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: '600' }}>Total Dataset Samples</div>
            <div style={{ fontSize: '2.5rem', fontWeight: '800', fontFamily: 'var(--font-heading)', color: 'var(--accent-primary)' }}>{totalSamples}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Cleaned records</div>
          </div>

          <div className="glass-card" style={{ padding: '1.5rem', textAlign: 'center' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: '600' }}>Input Features</div>
            <div style={{ fontSize: '2.5rem', fontWeight: '800', fontFamily: 'var(--font-heading)', color: 'var(--accent-cyan)' }}>{totalFeatures}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Numerical dimensions (cm)</div>
          </div>

          <div className="glass-card" style={{ padding: '1.5rem', textAlign: 'center' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: '600' }}>Target Classes</div>
            <div style={{ fontSize: '2.5rem', fontWeight: '800', fontFamily: 'var(--font-heading)', color: 'var(--accent-emerald)' }}>3</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Setosa, Versicolor, Virginica</div>
          </div>
        </div>

        {/* Feature Cards Grid */}
        <h3 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Iris Botanical Measurements</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.5rem' }}>
          {featuresList.map((feat, idx) => (
            <div key={idx} className="glass-card" style={{ padding: '1.75rem' }}>
              <div style={{ fontSize: '1.15rem', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
                {feat.title}
              </div>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: '1.5' }}>
                {feat.desc}
              </p>
              <div style={{ fontSize: '0.85rem', color: 'var(--accent-cyan)', fontWeight: '600', borderTop: '1px solid var(--border-card)', paddingTop: '0.75rem' }}>
                Dataset Mean: {feat.avg} cm
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
