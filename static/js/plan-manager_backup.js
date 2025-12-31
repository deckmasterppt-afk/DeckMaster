// DeckMaster Plan Manager - Professional Plan Management

class PlanManager {
    constructor(apiClient, uiManager) {
        this.apiClient = apiClient;
        this.uiManager = uiManager;
        this.currentUser = {
            plan: 'free',
            dailyUsage: 0,
            totalUsage: 0,
            lastResetDate: new Date().toDateString()
        };
        this.plans = {};
        this.adminStatus = { is_admin: false };
        
        this.initializePlanButtons();
        this.initializeAdminPanel();
    }

    /**
     * Initialize admin panel functionality
     */
    initializeAdminPanel() {
        // Secret key combination to open admin panel (Ctrl+Shift+A)
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'A') {
                e.preventDefault();
                console.log('🔧 Admin panel hotkey pressed');
                this.showAdminPanel();
            }
        });

        // Setup admin event listeners when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                console.log('🔧 Setting up admin event listeners');
                this.setupAdminEventListeners();
            });
        } else {
            console.log('🔧 Setting up admin event listeners (DOM already ready)');
            this.setupAdminEventListeners();
        }
    }

    /**
     * Setup admin event listeners
     */
    setupAdminEventListeners() {
        const adminLoginBtn = document.getElementById('adminLoginBtn');
        const adminCancelBtn = document.getElementById('adminCancelBtn');
        const adminDeactivateBtn = document.getElementById('adminDeactivateBtn');
        const adminCloseBtn = document.getElementById('adminCloseBtn');
        const adminOverlay = document.getElementById('adminOverlay');

        console.log('🔧 Admin elements found:', {
            loginBtn: !!adminLoginBtn,
            cancelBtn: !!adminCancelBtn,
            deactivateBtn: !!adminDeactivateBtn,
            closeBtn: !!adminCloseBtn,
            overlay: !!adminOverlay
        });

        if (adminLoginBtn) {
            adminLoginBtn.addEventListener('click', () => {
                console.log('🔧 Admin login button clicked');
                this.handleAdminLogin();
            });
        }
        if (adminCancelBtn) {
            adminCancelBtn.addEventListener('click', () => {
                console.log('🔧 Admin cancel button clicked');
                this.hideAdminPanel();
            });
        }
        if (adminDeactivateBtn) {
            adminDeactivateBtn.addEventListener('click', () => {
                console.log('🔧 Admin deactivate button clicked');
                this.handleAdminDeactivate();
            });
        }
        if (adminCloseBtn) {
            adminCloseBtn.addEventListener('click', () => {
                console.log('🔧 Admin close button clicked');
                this.hideAdminPanel();
            });
        }
        if (adminOverlay) {
            adminOverlay.addEventListener('click', () => {
                console.log('🔧 Admin overlay clicked');
                this.hideAdminPanel();
            });
        }

        // Enter key in password field
        const adminPassword = document.getElementById('adminPassword');
        if (adminPassword) {
            adminPassword.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    console.log('🔧 Enter key pressed in password field');
                    this.handleAdminLogin();
                }
            });
        }

        // Test admin button (for testing)
        const testAdminBtn = document.getElementById('testAdminBtn');
        if (testAdminBtn) {
            testAdminBtn.addEventListener('click', () => {
                console.log('🔧 Test admin button clicked');
                this.showAdminPanel();
            });
        }

        // Debug admin status button
        const debugAdminBtn = document.getElementById('debugAdminBtn');
        if (debugAdminBtn) {
            debugAdminBtn.addEventListener('click', () => {
                const userId = this.getUserId();
                const isAdmin = this.isAdminUser(userId);
                console.log('🔧 DEBUG Admin Status:');
                console.log('  User ID:', userId);
                console.log('  Admin Status Object:', this.adminStatus);
                console.log('  Is Admin:', isAdmin);
                console.log('  Current Plan:', this.currentUser.plan);
                console.log('  Can Generate PPT:', this.canGeneratePPT());
                
                alert(`Admin Status Debug:
User ID: ${userId}
Is Admin: ${isAdmin}
Admin Status: ${JSON.stringify(this.adminStatus, null, 2)}
Current Plan: ${this.currentUser.plan}
Can Generate: ${this.canGeneratePPT().canGenerate}`);
            });
        }
    }

    /**
     * Show admin panel
     */
    showAdminPanel() {
        console.log('🔧 Attempting to show admin panel');
        const panel = document.getElementById('adminPanel');
        const overlay = document.getElementById('adminOverlay');
        
        console.log('🔧 Admin panel elements:', {
            panel: !!panel,
            overlay: !!overlay
        });
        
        if (panel && overlay) {
            overlay.style.display = 'block';
            panel.style.display = 'block';
            console.log('🔧 Admin panel shown');
            
            // Focus password field
            const passwordField = document.getElementById('adminPassword');
            if (passwordField) {
                passwordField.focus();
                console.log('🔧 Password field focused');
            }
        } else {
            console.error('🔧 Admin panel elements not found!');
        }
    }

    /**
     * Hide admin panel
     */
    hideAdminPanel() {
        const panel = document.getElementById('adminPanel');
        const overlay = document.getElementById('adminOverlay');
        if (panel && overlay) {
            panel.style.display = 'none';
            overlay.style.display = 'none';
            
            // Clear password field
            const passwordField = document.getElementById('adminPassword');
            if (passwordField) {
                passwordField.value = '';
            }
        }
    }

    /**
     * Handle admin login
     */
    async handleAdminLogin() {
        const passwordField = document.getElementById('adminPassword');
        const password = passwordField?.value;
        
        console.log('🔧 Admin login attempt with password:', password ? '***' : 'empty');
        
        if (!password) {
            this.uiManager.showError('Please enter admin password');
            return;
        }

        const loginBtn = document.getElementById('adminLoginBtn');
        this.uiManager.setButtonLoading(loginBtn, true, 'Activate Admin Mode');

        try {
            const userId = this.getUserId();
            
            // Check if password matches the expected admin password
            if (password === 'DeckMaster2024!@#SecureAdmin') {
                console.log('🔧 Admin password correct, activating admin mode');
                
                // Try API first, but fallback to local mode if server not available
                try {
                    const result = await this.apiClient.activateAdmin(userId, password);
                    if (result.success) {
                        this.adminStatus = result.data.admin_status;
                        this.showAdminDashboard();
                        this.updatePlanDisplay();
                        this.uiManager.showSuccess('Admin mode activated successfully!');
                        return;
                    }
                } catch (apiError) {
                    console.warn('🔧 API not available, using local admin mode:', apiError.message);
                }
                
                // Fallback to local admin mode (for testing without server)
                this.adminStatus = { 
                    is_admin: true, 
                    time_remaining: 3600,
                    expires_at: Date.now() / 1000 + 3600
                };
                this.showAdminDashboard();
                this.updatePlanDisplay();
                this.uiManager.showSuccess('Admin mode activated (local testing mode)!');
                
            } else {
                console.log('🔧 Admin password incorrect');
                this.uiManager.showError('Invalid admin password');
            }
        } catch (error) {
            console.error('🔧 Admin login error:', error);
            this.uiManager.showError('Admin login failed: ' + error.message);
        } finally {
            this.uiManager.setButtonLoading(loginBtn, false, 'Activate Admin Mode');
        }
    }

    /**
     * Handle admin deactivate
     */
    async handleAdminDeactivate() {
        try {
            const userId = this.getUserId();
            
            // Try API first, but fallback to local deactivation
            try {
                const result = await this.apiClient.deactivateAdmin(userId);
                if (result.success) {
                    this.adminStatus = { is_admin: false };
                    this.hideAdminPanel();
                    this.updatePlanDisplay();
                    this.uiManager.showInfo('Admin mode deactivated');
                    
                    // Clear timer interval
                    if (this.adminTimeInterval) {
                        clearInterval(this.adminTimeInterval);
                        this.adminTimeInterval = null;
                    }
                    return;
                }
            } catch (apiError) {
                console.warn('🔧 API not available, using local deactivation:', apiError.message);
            }
            
            // Fallback to local deactivation
            this.adminStatus = { is_admin: false };
            this.hideAdminPanel();
            this.updatePlanDisplay();
            this.uiManager.showInfo('Admin mode deactivated (local mode)');
            
            // Clear timer interval
            if (this.adminTimeInterval) {
                clearInterval(this.adminTimeInterval);
                this.adminTimeInterval = null;
            }
            
        } catch (error) {
            this.uiManager.showError('Deactivation failed: ' + error.message);
        }
    }

    /**
     * Show admin dashboard
     */
    showAdminDashboard() {
        const loginDiv = document.getElementById('adminLogin');
        const dashboardDiv = document.getElementById('adminDashboard');
        
        if (loginDiv && dashboardDiv) {
            loginDiv.style.display = 'none';
            dashboardDiv.style.display = 'block';
            
            // Update time remaining immediately
            this.updateAdminTimeRemaining();
            
            // Set interval to update time every second
            if (this.adminTimeInterval) {
                clearInterval(this.adminTimeInterval);
            }
            
            this.adminTimeInterval = setInterval(() => {
                this.updateAdminTimeRemaining();
                
                // Check if admin session expired
                if (this.adminStatus.time_remaining <= 0) {
                    this.handleAdminExpired();
                }
            }, 1000); // Update every second
        }
    }

    /**
     * Update admin time remaining display
     */
    updateAdminTimeRemaining() {
        const timeElement = document.getElementById('adminTimeRemaining');
        if (timeElement && this.adminStatus && this.adminStatus.time_remaining !== undefined) {
            // Decrease time remaining by 1 second
            if (this.adminStatus.time_remaining > 0) {
                this.adminStatus.time_remaining--;
            }
            
            const totalSeconds = this.adminStatus.time_remaining;
            const hours = Math.floor(totalSeconds / 3600);
            const minutes = Math.floor((totalSeconds % 3600) / 60);
            const seconds = totalSeconds % 60;
            
            if (hours > 0) {
                timeElement.textContent = `Time remaining: ${hours}h ${minutes}m ${seconds}s`;
            } else if (minutes > 0) {
                timeElement.textContent = `Time remaining: ${minutes}m ${seconds}s`;
            } else {
                timeElement.textContent = `Time remaining: ${seconds}s`;
            }
            
            // Change color when time is running low
            if (totalSeconds < 300) { // Less than 5 minutes
                timeElement.style.color = '#ff6b6b';
            } else if (totalSeconds < 600) { // Less than 10 minutes
                timeElement.style.color = '#ffa726';
            } else {
                timeElement.style.color = '#155724';
            }
        }
    }

    /**
     * Handle admin session expiration
     */
    handleAdminExpired() {
        console.log('🔧 Admin session expired');
        this.adminStatus = { is_admin: false };
        this.hideAdminPanel();
        this.updatePlanDisplay();
        this.uiManager.showWarning('Admin session expired. Please reactivate if needed.');
        
        if (this.adminTimeInterval) {
            clearInterval(this.adminTimeInterval);
            this.adminTimeInterval = null;
        }
    }

    /**
     * Check admin status on load
     */
    async checkAdminStatus() {
        try {
            const userId = this.getUserId();
            const result = await this.apiClient.getAdminStatus(userId);
            
            if (result.success) {
                this.adminStatus = result.data.admin_status;
            }
        } catch (error) {
            console.warn('Admin status check failed:', error);
        }
    }

    /**
     * Load user data from API
     */
    async loadUserData(userId) {
        try {
            this.uiManager.showLoading('Loading your profile...');
            
            // Check admin status first
            await this.checkAdminStatus();
            
            // Check for admin plan override (for testing)
            const adminPlan = localStorage.getItem('deckmaster_admin_plan');
            const isAdmin = this.isAdminUser(userId);
            
            if (isAdmin && adminPlan) {
                console.log('🔧 Admin mode: using stored admin plan:', adminPlan);
                this.currentUser.plan = adminPlan;
            }
            
            try {
                const result = await this.apiClient.getUserInfo(userId);
                
                if (result.success) {
                    // Don't override admin plan if in admin mode
                    if (!isAdmin || !adminPlan) {
                        this.currentUser = result.data.user;
                    } else {
                        // Keep admin plan but update other user data
                        const savedPlan = this.currentUser.plan;
                        this.currentUser = { ...result.data.user, plan: savedPlan };
                    }
                    
                    if (result.data.plan) {
                        this.plans[this.currentUser.plan] = result.data.plan;
                    }
                    this.updatePlanDisplay();
                    this.uiManager.showSuccess('Profile loaded successfully');
                } else {
                    console.warn('Failed to load user data:', result.error);
                    this.updatePlanDisplay(); // Use defaults
                    this.uiManager.showWarning('Using offline mode - some features may be limited');
                }
            } catch (apiError) {
                console.warn('API not available:', apiError.message);
                this.updatePlanDisplay(); // Use defaults
                this.uiManager.showWarning('Connection issue - using offline mode');
            }
        } catch (error) {
            console.error('Error loading user data:', error);
            this.updatePlanDisplay(); // Use defaults
            this.uiManager.showWarning('Connection issue - using offline mode');
        } finally {
            this.uiManager.hideLoading();
        }
    }

    /**
     * Load available plans from API
     */
    async loadPlans() {
        try {
            const cached = localStorage.getItem('deckmaster_plans_cache');
            const cacheTime = localStorage.getItem('deckmaster_plans_cache_time');
            
            // Use cache if less than 1 hour old
            if (cached && cacheTime && (Date.now() - parseInt(cacheTime)) < 3600000) {
                this.plans = JSON.parse(cached);
                return;
            }
            
            const result = await this.apiClient.getPlans();
            
            if (result.success) {
                this.plans = result.data.plans;
                // Cache the plans
                localStorage.setItem('deckmaster_plans_cache', JSON.stringify(this.plans));
                localStorage.setItem('deckmaster_plans_cache_time', Date.now().toString());
            }
        } catch (error) {
            console.warn('Error loading plans, using defaults:', error);
        }
    }

    /**
     * Update plan display in UI
     */
    updatePlanDisplay() {
        const userId = this.getUserId();
        const isAdmin = this.isAdminUser(userId);
        
        // Admin mode: use premium plan features for everything
        let plan;
        if (isAdmin) {
            plan = {
                name: 'ADMIN (All Features Free)',
                dailyLimit: 999,
                daily_limit: 999,
                maxSlides: 50,
                max_slides: 50,
                hasAds: false,
                has_ads: false,
                visualElements: true,
                visual_elements: true,
                price: 0
            };
            console.log('🔧 Admin mode: using unlimited plan features');
        } else {
            plan = this.plans[this.currentUser.plan] || this.getDefaultPlan(this.currentUser.plan);
        }
        
        // Show admin badge if in admin mode
        const adminBadge = document.getElementById('adminBadge');
        const adminMessage = document.getElementById('adminMessage');
        if (adminBadge) {
            adminBadge.style.display = isAdmin ? 'inline' : 'none';
        }
        if (adminMessage) {
            adminMessage.style.display = isAdmin ? 'block' : 'none';
        }
        
        // Update plan information
        this.uiManager.updateElementText('currentPlan', plan.name);
        this.uiManager.updateElementText('dailyUsage', isAdmin ? 0 : this.currentUser.dailyUsage);
        this.uiManager.updateElementText('dailyLimit', plan.dailyLimit || plan.daily_limit);
        this.uiManager.updateElementText('maxSlides', plan.maxSlides || plan.max_slides);
        this.uiManager.updateElementText('adsStatus', (plan.hasAds || plan.has_ads) ? 'Included' : 'No Ads');
        
        // Update slide count validation
        const maxSlides = plan.maxSlides || plan.max_slides;
        this.uiManager.validateSlideCount(maxSlides, plan.name);
        
        // Update visual elements - enable all in admin mode
        const hasVisualElements = isAdmin ? true : (plan.visualElements || plan.visual_elements);
        this.uiManager.updateVisualElements(hasVisualElements);
        
        // Update usage progress - always 0% in admin mode
        let usagePercent = 0;
        if (!isAdmin) {
            const dailyLimit = plan.dailyLimit || plan.daily_limit;
            const totalLimit = plan.totalLimit || plan.total_limit;
            usagePercent = totalLimit ? 
                (this.currentUser.totalUsage / totalLimit) * 100 :
                (this.currentUser.dailyUsage / dailyLimit) * 100;
        }
        
        this.uiManager.updateProgressBar(usagePercent);
        
        // Update plan buttons
        this.updatePlanButtons();
        
        // Show admin message if applicable
        if (isAdmin) {
            console.log('🔧 ADMIN MODE: All features unlocked, unlimited usage, no restrictions');
        }
    }

    /**
     * Update plan selection buttons
     */
    updatePlanButtons() {
        const userId = this.getUserId();
        const isAdmin = this.isAdminUser(userId);
        
        document.querySelectorAll('.plan-select-btn').forEach(btn => {
            const btnPlan = btn.dataset.plan;
            
            // Reset button classes
            btn.classList.remove('btn-secondary', 'btn-primary');
            btn.disabled = false;
            
            if (btnPlan === this.currentUser.plan) {
                // Current plan button
                btn.textContent = '✓ Current Plan';
                btn.disabled = true;
                btn.classList.add('btn-secondary');
                btn.style.opacity = '0.7';
            } else {
                // Other plan buttons
                btn.disabled = false;
                btn.classList.add('btn-primary');
                btn.style.opacity = '1';
                
                if (btnPlan === 'free') {
                    btn.textContent = 'Switch to Free';
                } else {
                    const planPrice = this.plans[btnPlan]?.price || this.getDefaultPlan(btnPlan).price;
                    if (isAdmin) {
                        btn.textContent = `✅ ${btnPlan.toUpperCase()} UNLOCKED`;
                        btn.style.background = 'linear-gradient(45deg, #4CAF50, #45a049)'; // Green for unlocked
                        btn.style.boxShadow = '0 4px 15px rgba(76, 175, 80, 0.4)';
                        btn.disabled = true; // Disabled because already unlocked
                        btn.style.opacity = '0.8';
                        btn.style.cursor = 'not-allowed';
                    } else {
                        btn.textContent = `Upgrade - $${planPrice}/mo`;
                    }
                }
            }
        });
    }

    /**
     * Switch user plan
     */
    async switchPlan(newPlan, userId) {
        const isAdmin = this.isAdminUser(userId);
        
        // In admin mode, don't actually switch plans - just show success
        if (isAdmin) {
            console.log('🔧 Admin mode: All plans are already unlocked, no need to switch');
            const planName = this.getDefaultPlan(newPlan).name;
            this.uiManager.showSuccess(`✅ [ADMIN] ${planName} features already unlocked! All plans are free in admin mode.`);
            return;
        }
        
        // Regular plan switching for non-admin users
        if (newPlan === this.currentUser.plan) {
            console.log('🔧 Already on this plan:', newPlan);
            return;
        }
        
        const button = document.querySelector(`[data-plan="${newPlan}"]`);
        this.uiManager.setButtonLoading(button, true);
        
        try {
            this.uiManager.showInfo(`Switching to ${this.plans[newPlan]?.name || newPlan} plan...`);
            
            const result = await this.apiClient.updateUserPlan(userId, newPlan);
            
            if (result.success) {
                // Update local user data with API response
                this.currentUser = result.data.user;
                if (result.data.plan) {
                    this.plans[newPlan] = result.data.plan;
                }
                
                // Update UI immediately
                this.updatePlanDisplay();
                
                this.uiManager.showSuccess(`✅ Successfully switched to ${this.plans[newPlan].name} plan!`);
                
                // Clear cached plan data
                localStorage.removeItem('deckmaster_plans_cache');
                localStorage.removeItem('deckmaster_plans_cache_time');
                
            } else {
                throw new Error(result.error || 'Failed to update plan');
            }
            
        } catch (error) {
            console.error('Plan update error:', error);
            this.uiManager.showError(`Failed to switch plan: ${error.message}`);
        } finally {
            this.uiManager.setButtonLoading(button, false);
            this.updatePlanButtons();
        }
    }

    /**
     * Check if user can generate PPT
     */
    canGeneratePPT() {
        const userId = this.getUserId();
        const isAdmin = this.isAdminUser(userId);
        
        // Admin mode: unlimited everything
        if (isAdmin) {
            return { 
                canGenerate: true,
                reason: 'Admin mode: unlimited access'
            };
        }
        
        // Regular user limits
        const plan = this.plans[this.currentUser.plan] || this.getDefaultPlan(this.currentUser.plan);
        const dailyLimit = plan.dailyLimit || plan.daily_limit;
        const totalLimit = plan.totalLimit || plan.total_limit;
        
        if (totalLimit && this.currentUser.totalUsage >= totalLimit) {
            return { 
                canGenerate: false, 
                reason: `You have reached the lifetime limit of ${totalLimit} presentations for the Free plan. Please upgrade to continue.` 
            };
        }
        
        if (this.currentUser.dailyUsage >= dailyLimit) {
            return { 
                canGenerate: false, 
                reason: `Daily limit of ${dailyLimit} presentations reached. Try again tomorrow or upgrade your plan.` 
            };
        }
        
        return { canGenerate: true };
    }

    /**
     * Get default plan configuration
     */
    getDefaultPlan(planName) {
        const defaultPlans = {
            free: {
                name: 'Free',
                dailyLimit: 3,
                totalLimit: 3,
                maxSlides: 5,
                hasAds: true,
                visualElements: false,
                price: 0
            },
            elite: {
                name: 'Elite',
                dailyLimit: 5,
                totalLimit: null,
                maxSlides: 15,
                hasAds: false,
                visualElements: true,
                price: 10
            },
            pro: {
                name: 'Pro',
                dailyLimit: 10,
                totalLimit: null,
                maxSlides: 10,
                hasAds: false,
                visualElements: true,
                price: 20
            },
            premium: {
                name: 'Premium',
                dailyLimit: 20,
                totalLimit: null,
                maxSlides: 20,
                hasAds: false,
                visualElements: true,
                price: 25
            }
        };
        
        return defaultPlans[planName] || defaultPlans.free;
    }

    /**
     * Initialize plan selection buttons
     */
    initializePlanButtons() {
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('.plan-select-btn').forEach(btn => {
                btn.addEventListener('click', async () => {
                    const selectedPlan = btn.dataset.plan;
                    const userId = this.getUserId();
                    await this.switchPlan(selectedPlan, userId);
                });
            });
        });
    }

    /**
     * Get user ID from storage (with admin mode detection)
     */
    getUserId() {
        let userId = localStorage.getItem('deckmaster_user_id');
        if (!userId) {
            const timestamp = Date.now();
            const random = Math.random().toString(36).substr(2, 12);
            const entropy = performance.now().toString(36).substr(2, 8);
            userId = `user_${timestamp}_${random}_${entropy}`;
            localStorage.setItem('deckmaster_user_id', userId);
        }
        return userId;
    }

    /**
     * Check if current user is admin
     */
    isAdminUser(userId) {
        return this.adminStatus && this.adminStatus.is_admin === true;
    }
}

// Export for use in other modules
window.PlanManager = PlanManager;