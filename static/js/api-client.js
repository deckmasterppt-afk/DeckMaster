// DeckMaster API Client - Professional API Communication

class APIClient {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
        this.maxRetries = 3;
        this.timeout = 30000; // 30 seconds
    }

    /**
     * Make API request with retry logic and error handling
     */
    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        let lastError;
        
        for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), this.timeout);
                
                const response = await fetch(url, {
                    ...options,
                    signal: controller.signal,
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    }
                });
                
                clearTimeout(timeoutId);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                return await response.json();
                
            } catch (error) {
                lastError = error;
                console.warn(`API request attempt ${attempt} failed:`, error.message);
                
                if (attempt < this.maxRetries && !error.name === 'AbortError') {
                    // Exponential backoff: 1s, 2s, 4s
                    await this.delay(1000 * Math.pow(2, attempt - 1));
                }
            }
        }
        
        throw new Error(`API request failed after ${this.maxRetries} attempts: ${lastError.message}`);
    }

    /**
     * GET request
     */
    async get(endpoint) {
        return this.makeRequest(endpoint, { method: 'GET' });
    }

    /**
     * POST request
     */
    async post(endpoint, data) {
        return this.makeRequest(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * Health check
     */
    async healthCheck() {
        try {
            const data = await this.get('/health');
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Get user information
     */
    async getUserInfo(userId) {
        try {
            const data = await this.get(`/user/${userId}`);
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Update user plan
     */
    async updateUserPlan(userId, plan) {
        try {
            const data = await this.post(`/user/${userId}/plan`, { plan });
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Generate presentation
     */
    async generatePresentation(requestData) {
        try {
            const data = await this.post('/generate', requestData);
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Get job status
     */
    async getJobStatus(jobId) {
        try {
            const data = await this.get(`/job/${jobId}`);
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Get available plans
     */
    async getPlans() {
        try {
            const data = await this.get('/plans');
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Get available designs
     */
    async getDesigns() {
        try {
            const data = await this.get('/designs');
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Activate admin mode with password
     */
    async activateAdmin(userId, password) {
        try {
            const data = await this.post('/admin/activate', { user_id: userId, password });
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Get admin status
     */
    async getAdminStatus(userId) {
        try {
            const data = await this.get(`/admin/status/${userId}`);
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Deactivate admin mode
     */
    async deactivateAdmin(userId) {
        try {
            const data = await this.post('/admin/deactivate', { user_id: userId });
            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Utility: Delay function
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Download file
     */
    downloadFile(url, filename) {
        try {
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            return true;
        } catch (error) {
            console.error('Download failed:', error);
            return false;
        }
    }
}

// Export for use in other modules
window.APIClient = APIClient;