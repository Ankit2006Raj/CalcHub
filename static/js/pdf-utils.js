// PDF Download Utility Functions

/**
 * Generic function to download PDF report
 * @param {string} endpoint - API endpoint for PDF generation
 * @param {object} data - Data to send to the endpoint
 * @param {string} calculatorName - Name of calculator for user feedback
 */
async function downloadPDF(endpoint, data, calculatorName) {
    try {
        // Show loading indicator
        showPDFLoading(true);

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Failed to generate PDF');
        }

        // Get the blob from response
        const blob = await response.blob();

        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;

        // Extract filename from Content-Disposition header or use default
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = `${calculatorName}_Report_${new Date().toISOString().split('T')[0]}.pdf`;

        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }

        a.download = filename;
        document.body.appendChild(a);
        a.click();

        // Cleanup
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showPDFLoading(false);
        showPDFSuccess(calculatorName);

    } catch (error) {
        console.error('PDF Download Error:', error);
        showPDFLoading(false);
        showPDFError(calculatorName);
    }
}

/**
 * Show loading indicator
 */
function showPDFLoading(show) {
    let loader = document.getElementById('pdf-loader');

    if (!loader && show) {
        loader = document.createElement('div');
        loader.id = 'pdf-loader';
        loader.className = 'pdf-notification';
        loader.innerHTML = `
            <div class="pdf-notification-content">
                <div class="spinner"></div>
                <span>Generating PDF Report...</span>
            </div>
        `;
        document.body.appendChild(loader);
    } else if (loader && !show) {
        loader.remove();
    }
}

/**
 * Show success message
 */
function showPDFSuccess(calculatorName) {
    showNotification(`${calculatorName} PDF report downloaded successfully!`, 'success');
}

/**
 * Show error message
 */
function showPDFError(calculatorName) {
    showNotification(`Failed to generate ${calculatorName} PDF report. Please try again.`, 'error');
}

/**
 * Generic notification function
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `pdf-notification pdf-notification-${type}`;
    notification.innerHTML = `
        <div class="pdf-notification-content">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="close-btn">&times;</button>
        </div>
    `;

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

/**
 * Add PDF download button to result container
 */
function addPDFDownloadButton(containerId, endpoint, getData, calculatorName) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Remove existing button if any
    const existingBtn = container.querySelector('.pdf-download-btn');
    if (existingBtn) {
        existingBtn.remove();
    }

    // Create new button
    const button = document.createElement('button');
    button.className = 'pdf-download-btn';
    button.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
        </svg>
        Download PDF Report
    `;

    button.onclick = async () => {
        const data = getData();
        if (data) {
            await downloadPDF(endpoint, data, calculatorName);
        }
    };

    container.appendChild(button);
}

// Add CSS styles dynamically
const style = document.createElement('style');
style.textContent = `
    .pdf-download-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 24px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .pdf-download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .pdf-download-btn:active {
        transform: translateY(0);
    }
    
    .pdf-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    }
    
    .pdf-notification-content {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .pdf-notification-success {
        border-left: 4px solid #10b981;
    }
    
    .pdf-notification-error {
        border-left: 4px solid #ef4444;
    }
    
    .pdf-notification .close-btn {
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        color: #666;
        padding: 0;
        margin-left: 12px;
    }
    
    .spinner {
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
