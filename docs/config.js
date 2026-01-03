/**
 * UMAJA-Core Configuration
 * Environment-based backend URL detection
 */

(function() {
    'use strict';
    
    // Define backend URLs for different environments
    const BACKEND_URLS = {
        production: 'https://web-production-6ec45.up.railway.app',
        staging: null,  // Set this when staging environment is available
        development: 'http://localhost:5000'
    };
    
    /**
     * Detect current environment based on hostname
     * @returns {string} Environment name (production, staging, or development)
     */
    function detectEnvironment() {
        const hostname = window.location.hostname;
        
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'development';
        } else if (hostname.includes('staging') || hostname.includes('dev')) {
            return 'staging';
        } else {
            return 'production';
        }
    }
    
    /**
     * Get backend URL for current environment
     * @returns {string} Backend URL
     */
    function getBackendURL() {
        const env = detectEnvironment();
        const url = BACKEND_URLS[env];
        
        // Fallback to production if environment URL not configured
        const finalUrl = url || BACKEND_URLS.production;
        
        console.log(`🔧 Environment detected: ${env}`);
        console.log(`🔗 Backend URL: ${finalUrl}`);
        
        return finalUrl;
    }
    
    /**
     * Allow manual override via URL parameter
     * Usage: ?backendUrl=https://custom-url.com
     */
    function getBackendURLWithOverride() {
        const urlParams = new URLSearchParams(window.location.search);
        const override = urlParams.get('backendUrl');
        
        if (override) {
            console.warn(`⚠️  Backend URL overridden via URL parameter: ${override}`);
            return override;
        }
        
        return getBackendURL();
    }
    
    // Export configuration to global scope
    window.UMAJAConfig = {
        backendURL: getBackendURLWithOverride(),
        environment: detectEnvironment(),
        urls: BACKEND_URLS
    };
    
    console.log('✅ UMAJA Configuration loaded');
})();
