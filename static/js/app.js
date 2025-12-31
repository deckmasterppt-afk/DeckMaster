// DeckMaster Main Application - Professional PPT Generation

class DeckMasterApp {
    constructor() {
        this.apiClient = new APIClient();
        this.uiManager = new UIManager();
        this.planManager = new PlanManager(this.apiClient, this.uiManager);
        
        this.initialize();
    }

    /**
     * Initialize the application
     */
    async initialize() {
        console.log('🚀 DeckMaster Application Starting...');
        
        // Initialize UI components
        this.uiManager.initialize();
        
        // Load user data and plans
        const userId = this.planManager.getUserId();
        await Promise.all([
            this.planManager.loadUserData(userId),
            this.planManager.loadPlans()
        ]);
        
        // Setup form handling
        this.setupFormHandling();
        
        // Health check
        this.performHealthCheck();
        
        console.log('✅ DeckMaster Application Ready');
    }

    /**
     * Setup form handling
     */
    setupFormHandling() {
        const form = document.getElementById('pptForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }
    }

    /**
     * Handle form submission
     */
    async handleFormSubmit(event) {
        event.preventDefault();
        
        // Check admin status first
        const userId = this.planManager.getUserId();
        const isAdmin = this.planManager.isAdminUser(userId);
        console.log('🔧 Form submission - Admin status:', isAdmin);
        
        // Check if user can generate
        const checkResult = this.planManager.canGeneratePPT();
        console.log('🔧 Can generate PPT:', checkResult);
        
        if (!checkResult.canGenerate) {
            console.log('🔧 Generation blocked:', checkResult.reason);
            this.uiManager.showWarning(checkResult.reason);
            return;
        }
        
        const formData = new FormData(event.target);
        const generateBtn = document.getElementById('generateBtn');
        
        // Set button loading state
        this.uiManager.setButtonLoading(generateBtn, true, 'Generate Presentation');
        
        try {
            this.uiManager.showInfo('Generating your presentation using our advanced AI algorithm...');
            
            const result = await this.generatePresentation(formData);
            
            if (result.success) {
                // Reload user data to get updated usage
                const userId = this.planManager.getUserId();
                await this.planManager.loadUserData(userId);
                
                this.uiManager.showSuccess(`✅ Success! Your presentation "${result.filename}" is ready for download!`);
                
                // Trigger download
                if (result.downloadUrl && result.downloadUrl !== '#') {
                    const fullUrl = window.location.origin + result.downloadUrl;
                    this.apiClient.downloadFile(fullUrl, result.filename);
                }
            } else {
                this.uiManager.showError('❌ Generation failed. Please try again.');
            }
        } catch (error) {
            this.uiManager.showError(`❌ Error: ${error.message}`);
            console.error('Generation error:', error);
        } finally {
            // Reset button state
            this.uiManager.setButtonLoading(generateBtn, false, 'Generate Presentation');
        }
    }

    /**
     * Generate presentation
     */
    async generatePresentation(formData) {
        const userId = this.planManager.getUserId();
        
        // Validate form data
        const task = formData.get('task')?.trim();
        if (!task || task.length < 10) {
            throw new Error('Please provide a more detailed presentation topic (at least 10 characters)');
        }
        
        if (task.length > 500) {
            throw new Error('Presentation topic is too long (maximum 500 characters)');
        }
        
        // Prepare request data
        const requestData = {
            user_id: userId,
            task: task,
            url: formData.get('url')?.trim() || '',
            design_style: formData.get('designStyle') || 'minimal_1',
            slide_count: parseInt(formData.get('slideCount')) || 3,
            graphs: formData.get('graphs') === 'on',
            tables: formData.get('tables') === 'on',
            pie_charts: formData.get('pieCharts') === 'on',
            images: formData.get('images') === 'on'
        };
        
        // Validate slide count - skip validation in admin mode
        const userId = this.planManager.getUserId();
        const isAdmin = this.planManager.isAdminUser(userId);
        
        if (!isAdmin) {
            const plan = this.planManager.plans[this.planManager.currentUser.plan] || 
                         this.planManager.getDefaultPlan(this.planManager.currentUser.plan);
            const maxSlides = plan.maxSlides || plan.max_slides || 5;
            if (requestData.slide_count > maxSlides) {
                throw new Error(`Maximum ${maxSlides} slides allowed for ${plan.name} plan`);
            }
        } else {
            console.log('🔧 Admin mode: Skipping slide count validation, allowing up to 50 slides');
            if (requestData.slide_count > 50) {
                requestData.slide_count = 50; // Cap at 50 for admin mode
            }
        }
        
        // Start generation
        this.uiManager.showInfo('🚀 Starting presentation generation...');
        
        const result = await this.apiClient.generatePresentation(requestData);
        
        if (!result.success) {
            throw new Error(result.error || 'Generation failed');
        }
        
        // Poll for completion
        const jobId = result.data.job_id;
        const estimatedTime = result.data.estimated_time || 30;
        
        this.uiManager.showInfo(`⚙️ Generating ${requestData.slide_count} slides with ${requestData.design_style} design...`);
        
        return await this.pollJobStatus(jobId, estimatedTime);
    }

    /**
     * Poll job status with progress updates
     */
    async pollJobStatus(jobId, estimatedTime) {
        const maxAttempts = Math.max(30, Math.ceil(estimatedTime / 2));
        let attempts = 0;
        const startTime = Date.now();
        
        const progressMessages = [
            '📝 Analyzing your content...',
            '🎨 Applying design styles...',
            '📊 Creating visual elements...',
            '✨ Adding finishing touches...',
            '🔧 Optimizing presentation...',
            '📋 Finalizing slides...'
        ];
        
        while (attempts < maxAttempts) {
            try {
                const result = await this.apiClient.getJobStatus(jobId);
                
                if (!result.success) {
                    throw new Error(result.error || 'Job status check failed');
                }
                
                const data = result.data;
                
                if (data.state === 'DONE') {
                    return {
                        success: true,
                        filename: data.filename,
                        downloadUrl: data.download_url
                    };
                } else if (data.state === 'FAILED') {
                    throw new Error(data.error || 'Generation failed on server');
                }
                
                // Update progress message
                const elapsed = Date.now() - startTime;
                const progress = Math.min((elapsed / (estimatedTime * 1000)) * 100, 90);
                const messageIndex = Math.floor((attempts / maxAttempts) * progressMessages.length);
                const message = progressMessages[Math.min(messageIndex, progressMessages.length - 1)];
                
                this.uiManager.showInfo(`${message} (${Math.round(progress)}%)`);
                
                // Wait 2 seconds before next poll
                await this.apiClient.delay(2000);
                attempts++;
                
            } catch (error) {
                console.warn(`Job polling attempt ${attempts + 1} failed:`, error.message);
                
                if (attempts >= 3) {
                    throw new Error(`Unable to check generation status: ${error.message}`);
                }
                
                await this.apiClient.delay(3000);
                attempts++;
            }
        }
        
        throw new Error('Generation timeout - the presentation is taking longer than expected. Please try again.');
    }

    /**
     * Perform health check
     */
    async performHealthCheck() {
        try {
            const result = await this.apiClient.healthCheck();
            if (result.success) {
                console.log('✅ API Health Check Passed');
            } else {
                console.warn('⚠️ API Health Check Failed:', result.error);
            }
        } catch (error) {
            console.error('❌ API Health Check Error:', error);
        }
    }
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.deckMasterApp = new DeckMasterApp();
});