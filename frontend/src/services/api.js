const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function predictSpecies(payload) {
  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Prediction failed with status code ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API predict error:', error);
    throw error;
  }
}

export async function getModelInfo() {
  try {
    const response = await fetch(`${API_BASE_URL}/model-info`);
    if (!response.ok) throw new Error('Failed to fetch model info');
    return await response.json();
  } catch (error) {
    console.error('API getModelInfo error:', error);
    return null;
  }
}

export async function getDatasetInfo() {
  try {
    const response = await fetch(`${API_BASE_URL}/dataset-info`);
    if (!response.ok) throw new Error('Failed to fetch dataset info');
    return await response.json();
  } catch (error) {
    console.error('API getDatasetInfo error:', error);
    return null;
  }
}

export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) return false;
    const data = await response.json();
    return data.status === 'healthy';
  } catch {
    return false;
  }
}
