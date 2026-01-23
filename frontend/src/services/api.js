import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Analyze a screenplay script
   * @param {string} scriptText - The fountain format script text
   * @returns {Promise} - Analysis results with job_id
   */
  async analyzeScript(scriptText) {
    const response = await this.client.post('/analyze', {
      script_text: scriptText,
    });
    return response.data;
  }

  /**
   * Get job status and results
   * @param {string} jobId - The job ID returned from analyze
   * @returns {Promise} - Job status and results
   */
  async getJobStatus(jobId) {
    const response = await this.client.get(`/jobs/${jobId}`);
    return response.data;
  }

  /**
   * Health check
   * @returns {Promise}
   */
  async healthCheck() {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export default new ApiService();
