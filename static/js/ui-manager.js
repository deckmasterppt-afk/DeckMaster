// DeckMaster UI Manager - Professional UI State Management

class UIManager {
    constructor() {
        this.statusElement = document.getElementById('statusMessage');
        this.generateButton = document.getElementById('generateBtn');
        this.progressBar = document.getElementById('usageProgress');
        this.slideCountInput = document.getElementById('slideCount');
        
        this.initializeAnimations();
    }

    /**
     * Initialize scroll animations
     */
    initializeAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        // Observe all fade-in elements
        document.querySelectorAll('.fade-in').forEach(el => {
            observer.observe(el);
        });
    }

    /**
     * Show loading state
     */
    showLoading(message = 'Loading...') {
        if (this.statusElement) {
            this.statusElement.innerHTML = `<span class="spinner"></span>${message}`;
            this.statusElement.className = 'status-message status-info';
            this.statusElement.style.display = 'block';
        }
    }

    /**
     * Hide loading state
     */
    hideLoading() {
        if (this.statusElement) {
            this.statusElement.style.display = 'none';
        }
    }

    /**
     * Show success message
     */
    showSuccess(message) {
        this.showStatus(message, 'success');
        setTimeout(() => this.hideLoading(), 5000);
    }

    /**
     * Show error message
     */
    showError(message) {
        this.showStatus(message, 'error');
    }

    /**
     * Show warning message
     */
    showWarning(message) {
        this.showStatus(message, 'warning');
    }

    /**
     * Show info message
     */
    showInfo(message) {
        this.showStatus(message, 'info');
    }

    /**
     * Show status message with type
     */
    showStatus(message, type = 'info') {
        if (this.statusElement) {
            this.statusElement.textContent = message;
            this.statusElement.className = `status-message status-${type}`;
            this.statusElement.style.display = 'block';
        }
    }

    /**
     * Update element text with animation
     */
    updateElementText(elementId, text) {
        const element = document.getElementById(elementId);
        if (element && element.textContent !== text) {
            element.style.transition = 'opacity 0.3s ease';
            element.style.opacity = '0.5';
            setTimeout(() => {
                element.textContent = text;
                element.style.opacity = '1';
            }, 150);
        }
    }

    /**
     * Update progress bar
     */
    updateProgressBar(percentage, color = null) {
        if (this.progressBar) {
            this.progressBar.style.transition = 'width 0.5s ease-in-out';
            this.progressBar.style.width = Math.min(percentage, 100) + '%';
            
            if (color) {
                this.progressBar.style.background = color;
            } else {
                // Auto color based on percentage
                if (percentage >= 90) {
                    this.progressBar.style.background = 'linear-gradient(45deg, #ef4444, #dc2626)'; // Red
                } else if (percentage >= 70) {
                    this.progressBar.style.background = 'linear-gradient(45deg, #f59e0b, #d97706)'; // Orange
                } else {
                    this.progressBar.style.background = 'linear-gradient(45deg, #667eea, #764ba2)'; // Default
                }
            }
        }
    }

    /**
     * Set button loading state
     */
    setButtonLoading(button, loading, originalText = null) {
        if (!button) return;
        
        if (loading) {
            button.disabled = true;
            button.dataset.originalText = button.textContent;
            button.innerHTML = '<span class="spinner"></span>Processing...';
        } else {
            button.disabled = false;
            button.textContent = originalText || button.dataset.originalText || 'Submit';
        }
    }

    /**
     * Validate slide count input
     */
    validateSlideCount(maxSlides, planName) {
        if (this.slideCountInput) {
            const currentValue = parseInt(this.slideCountInput.value);
            
            this.slideCountInput.max = maxSlides;
            
            if (currentValue > maxSlides) {
                this.slideCountInput.value = maxSlides;
                this.showWarning(`Maximum ${maxSlides} slides allowed for ${planName} plan`);
            } else if (currentValue < 1) {
                this.slideCountInput.value = 1;
            }
            
            // Add real-time validation
            this.slideCountInput.addEventListener('input', () => {
                const value = parseInt(this.slideCountInput.value);
                if (value > maxSlides) {
                    this.slideCountInput.value = maxSlides;
                    this.showWarning(`Maximum ${maxSlides} slides allowed for ${planName} plan`);
                } else if (value < 1) {
                    this.slideCountInput.value = 1;
                }
            });
        }
    }

    /**
     * Update visual elements checkboxes
     */
    updateVisualElements(hasVisualElements) {
        const visualCheckboxes = document.querySelectorAll('.visual-options input[type="checkbox"]');
        
        visualCheckboxes.forEach(checkbox => {
            checkbox.disabled = !hasVisualElements;
            if (!hasVisualElements) {
                checkbox.checked = false;
            }
            
            // Add visual feedback
            const label = checkbox.parentElement;
            if (hasVisualElements) {
                label.style.opacity = '1';
                label.style.cursor = 'pointer';
            } else {
                label.style.opacity = '0.5';
                label.style.cursor = 'not-allowed';
            }
        });
    }

    /**
     * Add ripple effect to buttons
     */
    addRippleEffect() {
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('click', function(e) {
                if (this.disabled) return;
                
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    width: ${size}px;
                    height: ${size}px;
                    left: ${x}px;
                    top: ${y}px;
                    background: rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    transform: scale(0);
                    animation: ripple 0.6s linear;
                    pointer-events: none;
                `;
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
        
        // Add ripple animation CSS
        if (!document.getElementById('ripple-styles')) {
            const style = document.createElement('style');
            style.id = 'ripple-styles';
            style.textContent = `
                @keyframes ripple {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    /**
     * Setup smooth scrolling
     */
    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    /**
     * Initialize all UI features
     */
    initialize() {
        this.addRippleEffect();
        this.setupSmoothScrolling();
        console.log('UI Manager initialized');
    }
}

// Export for use in other modules
window.UIManager = UIManager;