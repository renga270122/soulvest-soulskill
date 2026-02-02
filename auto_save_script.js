// Auto-save indicator for mobile devices
(function() {
    let saveTimeout;
    let saveIndicator;
    
    // Create save indicator
    function createSaveIndicator() {
        if (!saveIndicator) {
            saveIndicator = document.createElement('div');
            saveIndicator.className = 'auto-save-indicator';
            saveIndicator.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #10b981;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 25px;
                font-size: 0.85rem;
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
                z-index: 10000;
                display: none;
                animation: fadeIn 0.3s ease;
            `;
            saveIndicator.textContent = '💾 Saved';
            document.body.appendChild(saveIndicator);
        }
    }
    
    // Show save indicator
    function showSaveIndicator() {
        createSaveIndicator();
        saveIndicator.style.display = 'block';
        
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            saveIndicator.style.display = 'none';
        }, 2000);
    }
    
    // Listen for input events on textareas
    document.addEventListener('input', function(e) {
        if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(showSaveIndicator, 500);
        }
    });
})();
