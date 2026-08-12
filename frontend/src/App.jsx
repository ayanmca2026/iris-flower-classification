import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import PredictionForm from './components/PredictionForm';
import PredictionResult from './components/PredictionResult';
import ModelMetrics from './components/ModelMetrics';
import DatasetInfo from './components/DatasetInfo';
import HowItWorks from './components/HowItWorks';
import Footer from './components/Footer';

import { predictSpecies, getModelInfo, getDatasetInfo, checkHealth } from './services/api';

export default function App() {
  const [isOnline, setIsOnline] = useState(true);
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [modelInfo, setModelInfo] = useState(null);
  const [datasetInfo, setDatasetInfo] = useState(null);

  useEffect(() => {
    async function loadInitialData() {
      const healthy = await checkHealth();
      setIsOnline(healthy);

      const mInfo = await getModelInfo();
      if (mInfo) setModelInfo(mInfo);

      const dInfo = await getDatasetInfo();
      if (dInfo) setDatasetInfo(dInfo);
    }
    loadInitialData();
  }, []);

  const handlePredict = async (formData) => {
    setLoading(true);
    setError('');
    try {
      const data = await predictSpecies(formData);
      setPredictionResult(data);
      setIsOnline(true);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to connect to prediction API. Make sure FastAPI backend is running.');
      setIsOnline(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Navbar isOnline={isOnline} />
      
      <main>
        <Hero />

        {/* Prediction Playground Section */}
        <section id="predict" style={{ padding: '4rem 0' }}>
          <div className="container">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem', alignItems: 'start' }}>
              <PredictionForm onPredict={handlePredict} loading={loading} error={error} />
              <PredictionResult result={predictionResult} />
            </div>
          </div>
        </section>

        <ModelMetrics modelInfo={modelInfo} />
        <DatasetInfo datasetInfo={datasetInfo} />
        <HowItWorks />
      </main>

      <Footer />
    </div>
  );
}
