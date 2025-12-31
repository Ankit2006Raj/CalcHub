/**
 * Pro Features JavaScript
 * Handles History, Analytics, Sharing, and Visualization
 */

// ============= HISTORY MANAGEMENT =============

class HistoryManager {
    constructor() {
        this.historyCache = null;
    }

    async saveCalculation(calculatorType, inputs, results) {
        try {
            const response = await fetch('/api/history/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    calculator_type: calculatorType,
                    inputs: inputs,
                    results: results
                })
            });
            const data = await response.json();
            this.historyCache = null; // Invalidate cache
            return data;
        } catch (error) {
            console.error('Error saving history:', error);
            return { success: false, error: error.message };
        }
    }

    async getHistory(calculatorType = null, limit = null) {
        try {
            let url = '/api/history/get';
            const params = new URLSearchParams();
            if (calculatorType) params.append('calculator_type', calculatorType);
            if (limit) params.append('limit', limit);

            if (params.toString()) url += '?' + params.toString();

            const response = await fetch(url);
            const data = await response.json();
            this.historyCache = data.history;
            return data;
        } catch (error) {
            console.error('Error fetching history:', error);
            return { history: [], total: 0 };
        }
    }

    async getMonthlySummary(year = null, month = null) {
        try {
            let url = '/api/history/monthly-summary';
            const params = new URLSearchParams();
            if (year) params.append('year', year);
            if (month) params.append('month', month);

            if (params.toString()) url += '?' + params.toString();

            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            console.error('Error fetching monthly summary:', error);
            return null;
        }
    }

    async deleteEntry(entryId) {
        try {
            const response = await fetch(`/api/history/delete/${entryId}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            this.historyCache = null; // Invalidate cache
            return data;
        } catch (error) {
            console.error('Error deleting entry:', error);
            return { success: false, error: error.message };
        }
    }

    async clearHistory(calculatorType = null) {
        try {
            let url = '/api/history/clear';
            if (calculatorType) url += `?calculator_type=${calculatorType}`;

            const response = await fetch(url, { method: 'DELETE' });
            const data = await response.json();
            this.historyCache = null; // Invalidate cache
            return data;
        } catch (error) {
            console.error('Error clearing history:', error);
            return { success: false, error: error.message };
        }
    }

    displayHistory(containerId, calculatorType) {
        this.getHistory(calculatorType, 10).then(data => {
            const container = document.getElementById(containerId);
            if (!container) return;

            if (data.history.length === 0) {
                container.innerHTML = `
                    <div class="no-history">
                        <i class="fas fa-history"></i>
                        <p>No calculation history yet</p>
                        <small>Your calculations will appear here</small>
                    </div>
                `;
                return;
            }

            let html = '<div class="history-list">';
            data.history.forEach(entry => {
                html += this.createHistoryCard(entry);
            });
            html += '</div>';

            container.innerHTML = html;
            this.attachHistoryEventListeners();
        });
    }

    createHistoryCard(entry) {
        const date = new Date(entry.timestamp);
        const formattedDate = date.toLocaleDateString();
        const formattedTime = date.toLocaleTimeString();

        return `
            <div class="history-card" data-entry-id="${entry.id}">
                <div class="history-header">
                    <span class="history-date">${formattedDate} ${formattedTime}</span>
                    <button class="delete-history-btn" data-entry-id="${entry.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="history-content">
                    ${this.formatHistoryContent(entry)}
                </div>
            </div>
        `;
    }

    formatHistoryContent(entry) {
        const type = entry.calculator_type;
        const results = entry.results;
        const inputs = entry.inputs;

        const formats = {
            'bmi': `BMI: ${results.bmi} (${results.category})`,
            'gpa': `GPA: ${results.gpa?.toFixed(2)}`,
            'loan': `EMI: $${results.emi?.toLocaleString()}`,
            'calorie': `Maintenance: ${results.maintain} cal`,
            'attendance': `Attendance: ${results.current_percentage?.toFixed(1)}%`,
            'percentage': `Score: ${results.percentage?.toFixed(1)}%`
        };

        return formats[type] || 'Calculation Result';
    }

    attachHistoryEventListeners() {
        document.querySelectorAll('.delete-history-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.stopPropagation();
                const entryId = btn.dataset.entryId;
                if (confirm('Delete this entry?')) {
                    const result = await this.deleteEntry(entryId);
                    if (result.success) {
                        btn.closest('.history-card').remove();
                        showNotification('Entry deleted', 'success');
                    }
                }
            });
        });
    }
}

// ============= ANALYTICS & CHARTS =============

class AnalyticsManager {
    constructor() {
        this.charts = {};
    }

    async getTrends(calculatorType) {
        try {
            const response = await fetch(`/api/analytics/trends?calculator_type=${calculatorType}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching trends:', error);
            return null;
        }
    }

    async getChartData(calculatorType) {
        try {
            const response = await fetch(`/api/analytics/chart/${calculatorType}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching chart data:', error);
            return null;
        }
    }

    async getInsights(calculatorType) {
        try {
            const response = await fetch(`/api/analytics/insights?calculator_type=${calculatorType}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching insights:', error);
            return { insights: [], recommendations: [] };
        }
    }

    async displayChart(canvasId, calculatorType) {
        const chartData = await this.getChartData(calculatorType);
        if (!chartData || !chartData.labels) return;

        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        // Destroy existing chart if any
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        const ctx = canvas.getContext('2d');
        this.charts[canvasId] = new Chart(ctx, {
            type: chartData.type || 'line',
            data: {
                labels: chartData.labels,
                datasets: chartData.datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: this.getChartTitle(calculatorType)
                    }
                },
                scales: chartData.yAxis ? {
                    y: chartData.yAxis
                } : {}
            }
        });
    }

    getChartTitle(calculatorType) {
        const titles = {
            'bmi': 'BMI Trend Over Time',
            'gpa': 'GPA Progress',
            'calorie': 'Calorie Needs History',
            'attendance': 'Attendance Improvement',
            'loan': 'Loan Analysis'
        };
        return titles[calculatorType] || 'Progress Chart';
    }

    async displayInsights(containerId, calculatorType) {
        const data = await this.getInsights(calculatorType);
        const container = document.getElementById(containerId);
        if (!container) return;

        let html = '<div class="insights-container">';

        if (data.insights && data.insights.length > 0) {
            html += '<div class="insights-section"><h3>📊 Insights</h3><ul>';
            data.insights.forEach(insight => {
                html += `<li>${insight}</li>`;
            });
            html += '</ul></div>';
        }

        if (data.recommendations && data.recommendations.length > 0) {
            html += '<div class="recommendations-section"><h3>💡 Recommendations</h3><ul>';
            data.recommendations.forEach(rec => {
                html += `<li>${rec}</li>`;
            });
            html += '</ul></div>';
        }

        html += '</div>';
        container.innerHTML = html;
    }

    async displayMonthlySummary(containerId) {
        const historyMgr = new HistoryManager();
        const summary = await historyMgr.getMonthlySummary();
        const container = document.getElementById(containerId);
        if (!container || !summary) return;

        const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

        let html = `
            <div class="monthly-summary">
                <h3>📅 ${monthNames[summary.month - 1]} ${summary.year} Summary</h3>
                <div class="summary-stats">
                    <div class="stat-card">
                        <div class="stat-value">${summary.total_calculations}</div>
                        <div class="stat-label">Total Calculations</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${summary.most_used || 'N/A'}</div>
                        <div class="stat-label">Most Used</div>
                    </div>
                </div>
                <div class="calculator-breakdown">
                    <h4>By Calculator</h4>
                    <ul>
        `;

        for (const [calc, count] of Object.entries(summary.by_calculator)) {
            html += `<li>${calc.replace('_', ' ').toUpperCase()}: ${count}</li>`;
        }

        html += `
                    </ul>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }
}

// ============= SHARING FUNCTIONALITY =============

class SharingManager {
    async getShareLinks(calculatorType, results, inputs) {
        try {
            const response = await fetch('/api/share/links', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    calculator_type: calculatorType,
                    result: results,
                    inputs: inputs
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Error getting share links:', error);
            return {};
        }
    }

    async getShareCardData(calculatorType, results, inputs) {
        try {
            const response = await fetch('/api/share/card-data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    calculator_type: calculatorType,
                    result: results,
                    inputs: inputs
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Error getting card data:', error);
            return null;
        }
    }

    async getCopyText(calculatorType, results, inputs) {
        try {
            const response = await fetch('/api/share/copy-text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    calculator_type: calculatorType,
                    result: results,
                    inputs: inputs
                })
            });
            const data = await response.json();
            return data.text;
        } catch (error) {
            console.error('Error getting copy text:', error);
            return '';
        }
    }

    displayShareButtons(containerId, calculatorType, results, inputs) {
        this.getShareLinks(calculatorType, results, inputs).then(links => {
            const container = document.getElementById(containerId);
            if (!container) return;

            const html = `
                <div class="share-buttons">
                    <h3>📤 Share Your Results</h3>
                    <div class="share-grid">
                        <a href="${links.whatsapp}" target="_blank" class="share-btn whatsapp">
                            <i class="fab fa-whatsapp"></i> WhatsApp
                        </a>
                        <a href="${links.twitter}" target="_blank" class="share-btn twitter">
                            <i class="fab fa-twitter"></i> Twitter
                        </a>
                        <a href="${links.facebook}" target="_blank" class="share-btn facebook">
                            <i class="fab fa-facebook"></i> Facebook
                        </a>
                        <a href="${links.linkedin}" target="_blank" class="share-btn linkedin">
                            <i class="fab fa-linkedin"></i> LinkedIn
                        </a>
                        <a href="${links.telegram}" target="_blank" class="share-btn telegram">
                            <i class="fab fa-telegram"></i> Telegram
                        </a>
                        <a href="${links.email}" class="share-btn email">
                            <i class="fas fa-envelope"></i> Email
                        </a>
                        <button class="share-btn copy" onclick="sharingManager.copyToClipboard('${calculatorType}', ${JSON.stringify(results)}, ${JSON.stringify(inputs)})">
                            <i class="fas fa-copy"></i> Copy
                        </button>
                    </div>
                </div>
            `;

            container.innerHTML = html;
        });
    }

    async copyToClipboard(calculatorType, results, inputs) {
        const text = await this.getCopyText(calculatorType, results, inputs);
        try {
            await navigator.clipboard.writeText(text);
            showNotification('Copied to clipboard!', 'success');
        } catch (error) {
            console.error('Error copying to clipboard:', error);
            showNotification('Failed to copy', 'error');
        }
    }

    async generateShareCard(containerId, calculatorType, results, inputs) {
        const cardData = await this.getShareCardData(calculatorType, results, inputs);
        if (!cardData) return;

        const container = document.getElementById(containerId);
        if (!container) return;

        const html = `
            <div class="share-card" style="background: linear-gradient(135deg, ${cardData.color_scheme}, ${cardData.color_scheme}dd);">
                <div class="card-icon">${cardData.icon}</div>
                <div class="card-title">${cardData.title}</div>
                <div class="card-main-value">${cardData.main_value}</div>
                <div class="card-subtitle">${cardData.subtitle}</div>
                <div class="card-details">
                    ${cardData.details.map(detail => `<div>${detail}</div>`).join('')}
                </div>
                <div class="card-footer">
                    <button onclick="sharingManager.downloadCard('${containerId}')" class="download-card-btn">
                        <i class="fas fa-download"></i> Download Card
                    </button>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    downloadCard(containerId) {
        const card = document.querySelector(`#${containerId} .share-card`);
        if (!card) return;

        // Use html2canvas library to convert card to image
        if (typeof html2canvas !== 'undefined') {
            html2canvas(card).then(canvas => {
                const link = document.createElement('a');
                link.download = 'calculator-result.png';
                link.href = canvas.toDataURL();
                link.click();
            });
        } else {
            showNotification('Download feature requires html2canvas library', 'error');
        }
    }
}

// ============= UTILITY FUNCTIONS =============

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.toggle('collapsed');
    }
}

// ============= INITIALIZE GLOBAL INSTANCES =============

const historyManager = new HistoryManager();
const analyticsManager = new AnalyticsManager();
const sharingManager = new SharingManager();

// ============= EXPORT FOR USE IN OTHER FILES =============

window.historyManager = historyManager;
window.analyticsManager = analyticsManager;
window.sharingManager = sharingManager;
window.showNotification = showNotification;
