/**
 * AI Features for Calculator Application
 * Provides AI recommendations, chatbot, and smart explanations
 */

// AI Recommendations
async function getAIRecommendations(calculatorType, data) {
    try {
        const response = await fetch(`/api/ai/${calculatorType}-recommendations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error('Failed to get AI recommendations');

        const recommendations = await response.json();
        displayAIRecommendations(calculatorType, recommendations);
        return recommendations;
    } catch (error) {
        console.error('AI Recommendations Error:', error);
        return null;
    }
}

// Display AI Recommendations
function displayAIRecommendations(calculatorType, recommendations) {
    let container = document.getElementById('ai-recommendations');

    if (!container) {
        container = document.createElement('div');
        container.id = 'ai-recommendations';
        container.className = 'ai-recommendations-container';
        document.querySelector('.result-box').appendChild(container);
    }

    container.innerHTML = generateRecommendationsHTML(calculatorType, recommendations);
    container.style.display = 'block';
}

// Generate Recommendations HTML
function generateRecommendationsHTML(calculatorType, recommendations) {
    if (calculatorType === 'bmi') {
        return generateBMIRecommendations(recommendations);
    } else if (calculatorType === 'loan') {
        return generateLoanRecommendations(recommendations);
    } else if (calculatorType === 'gpa') {
        return generateGPARecommendations(recommendations);
    }
    return '';
}


// BMI Recommendations HTML
function generateBMIRecommendations(recommendations) {
    let html = '<div class="ai-section">';
    html += '<h3>🤖 AI-Powered Recommendations</h3>';

    // Diet Plan
    html += '<div class="ai-card">';
    html += '<h4>📋 Personalized Diet Plan</h4>';
    html += '<div class="diet-plan">';
    recommendations.diet_plan.forEach(meal => {
        html += `<div class="meal-card">
            <div class="meal-header">
                <strong>${meal.meal}</strong>
                <span class="calories">${meal.calories} cal</span>
            </div>
            <ul class="meal-items">
                ${meal.items.map(item => `<li>${item}</li>`).join('')}
            </ul>
        </div>`;
    });
    html += '</div></div>';

    // Workout Plan
    html += '<div class="ai-card">';
    html += '<h4>💪 Personalized Workout Plan</h4>';
    html += '<div class="workout-plan">';
    recommendations.workout_plan.forEach(day => {
        html += `<div class="workout-card">
            <div class="workout-header">
                <strong>${day.day}</strong>
                <span class="duration">${day.duration}</span>
            </div>
            <div class="workout-focus">${day.focus}</div>
            <ul class="workout-exercises">
                ${day.exercises.map(ex => `<li>${ex}</li>`).join('')}
            </ul>
        </div>`;
    });
    html += '</div></div>';

    // Calorie Plan
    html += '<div class="ai-card">';
    html += '<h4>🎯 Calorie Management Plan</h4>';
    html += `<div class="calorie-plan">
        <div class="plan-goal"><strong>Goal:</strong> ${recommendations.calorie_plan.goal}</div>
        <div class="plan-target"><strong>Weekly Target:</strong> ${recommendations.calorie_plan.weekly_target}</div>
        <div class="plan-daily"><strong>Daily Adjustment:</strong> ${recommendations.calorie_plan.daily_deficit}</div>
        <div class="plan-timeline"><strong>Timeline:</strong> ${recommendations.calorie_plan.timeline}</div>
        <div class="plan-tips">
            <strong>Tips:</strong>
            <ul>
                ${recommendations.calorie_plan.tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
    </div>`;
    html += '</div>';

    html += '</div>';
    return html;
}

// Loan Recommendations HTML
function generateLoanRecommendations(recommendations) {
    let html = '<div class="ai-section">';
    html += '<h3>🤖 AI-Powered Loan Analysis</h3>';

    // Best Tenure
    html += '<div class="ai-card">';
    html += '<h4>📊 Optimal Loan Tenure Options</h4>';
    html += '<div class="tenure-options">';
    html += '<table class="tenure-table"><thead><tr>';
    html += '<th>Years</th><th>Monthly EMI</th><th>Total Interest</th><th>Affordability</th>';
    html += '</tr></thead><tbody>';
    recommendations.best_tenure.options.forEach(option => {
        const affordClass = option.affordability.toLowerCase();
        html += `<tr class="afford-${affordClass}">
            <td>${option.years}</td>
            <td>$${option.monthly_emi}</td>
            <td>$${option.total_interest}</td>
            <td><span class="badge badge-${affordClass}">${option.affordability}</span></td>
        </tr>`;
    });
    html += '</tbody></table>';
    html += `<div class="recommendation-note">💡 ${recommendations.best_tenure.recommendation}</div>`;
    html += '</div></div>';

    // Future Rates
    html += '<div class="ai-card">';
    html += '<h4>📈 Interest Rate Predictions</h4>';
    html += `<div class="rate-predictions">
        <div class="current-rate">Current Rate: <strong>${recommendations.future_rates.current_rate}%</strong></div>
        <div class="trend">Trend: <span class="trend-${recommendations.future_rates.trend}">${recommendations.future_rates.trend}</span></div>
        <div class="predictions">
            <div>6 Months: ${recommendations.future_rates.predictions['6_months']}%</div>
            <div>1 Year: ${recommendations.future_rates.predictions['1_year']}%</div>
            <div>2 Years: ${recommendations.future_rates.predictions['2_years']}%</div>
        </div>
        <div class="advice">💡 ${recommendations.future_rates.advice}</div>
    </div>`;
    html += '</div>';

    // Prepayment Strategy
    html += '<div class="ai-card">';
    html += '<h4>💰 Prepayment Strategy</h4>';
    html += `<div class="prepayment-strategy">
        <div class="strategy-name"><strong>${recommendations.prepayment_strategy.strategy}</strong></div>
        <ul class="strategy-recommendations">
            ${recommendations.prepayment_strategy.recommendations.map(rec => `<li>${rec}</li>`).join('')}
        </ul>
        <div class="savings-potential">
            <strong>Savings Potential:</strong>
            <div>10% Extra Payment: ${recommendations.prepayment_strategy.savings_potential['10_percent_extra']}</div>
            <div>20% Extra Payment: ${recommendations.prepayment_strategy.savings_potential['20_percent_extra']}</div>
        </div>
    </div>`;
    html += '</div>';

    html += '</div>';
    return html;
}

// GPA Recommendations HTML
function generateGPARecommendations(recommendations) {
    let html = '<div class="ai-section">';
    html += '<h3>🤖 AI-Powered Academic Analysis</h3>';

    // Focus Subjects
    if (recommendations.focus_subjects && recommendations.focus_subjects.length > 0) {
        html += '<div class="ai-card">';
        html += '<h4>🎯 Subjects to Focus On</h4>';
        html += '<div class="focus-subjects">';
        recommendations.focus_subjects.forEach(subject => {
            html += `<div class="subject-card priority-${subject.priority.toLowerCase()}">
                <div class="subject-name">${subject.course}</div>
                <div class="subject-details">
                    <span>Current Grade: ${subject.current_grade}</span>
                    <span>Credits: ${subject.credits}</span>
                    <span class="priority-badge">${subject.priority} Priority</span>
                </div>
                <div class="subject-impact">Potential Impact: ${subject.potential_impact} points</div>
                <div class="subject-recommendation">${subject.recommendation}</div>
            </div>`;
        });
        html += '</div></div>';
    }

    // Predicted GPA
    html += '<div class="ai-card">';
    html += '<h4>📈 GPA Predictions</h4>';
    html += `<div class="gpa-predictions">
        <div class="prediction-item">
            <span>Current GPA:</span>
            <strong>${recommendations.predicted_gpa.current_gpa}</strong>
        </div>
        <div class="prediction-item">
            <span>If Maintain:</span>
            <strong>${recommendations.predicted_gpa.if_maintain}</strong>
        </div>
        <div class="prediction-item highlight">
            <span>Realistic Target:</span>
            <strong>${recommendations.predicted_gpa.realistic_target}</strong>
        </div>
        <div class="prediction-item">
            <span>With 10% Improvement:</span>
            <strong>${recommendations.predicted_gpa.if_improve_10_percent}</strong>
        </div>
        <div class="prediction-item">
            <span>With 20% Improvement:</span>
            <strong>${recommendations.predicted_gpa.if_improve_20_percent}</strong>
        </div>
        <div class="timeline">Timeline: ${recommendations.predicted_gpa.timeline}</div>
    </div>`;
    html += '</div>';

    // Improvement Plan
    html += '<div class="ai-card">';
    html += '<h4>📚 Improvement Plan</h4>';
    html += `<div class="improvement-plan">
        <div class="plan-status status-${recommendations.improvement_plan.status.toLowerCase().replace(' ', '-')}">
            Status: <strong>${recommendations.improvement_plan.status}</strong>
        </div>
        <div class="plan-goal">Goal: ${recommendations.improvement_plan.goal}</div>
        <div class="plan-strategies">
            <strong>Strategies:</strong>
            <ul>
                ${recommendations.improvement_plan.strategies.map(strategy => `<li>${strategy}</li>`).join('')}
            </ul>
        </div>
    </div>`;
    html += '</div>';

    html += '</div>';
    return html;
}


// AI Chatbot
class AIChatbot {
    constructor(calculatorType) {
        this.calculatorType = calculatorType;
        this.messages = [];
        this.isOpen = false;
        this.createChatbot();
    }

    createChatbot() {
        const chatbotHTML = `
            <div id="ai-chatbot" class="ai-chatbot">
                <div class="chatbot-header">
                    <span>🤖 AI Assistant</span>
                    <button onclick="aiChatbot.toggle()" class="close-btn">×</button>
                </div>
                <div class="chatbot-messages" id="chatbot-messages">
                    <div class="bot-message">
                        Hi! I'm your AI assistant. Ask me anything about ${this.calculatorType} calculations!
                    </div>
                </div>
                <div class="chatbot-input">
                    <input type="text" id="chatbot-input" placeholder="Ask a question..." 
                           onkeypress="if(event.key==='Enter') aiChatbot.sendMessage()">
                    <button onclick="aiChatbot.sendMessage()" class="send-btn">Send</button>
                </div>
            </div>
            <button id="chatbot-toggle" onclick="aiChatbot.toggle()" class="chatbot-toggle">
                💬 Ask AI
            </button>
        `;

        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    toggle() {
        const chatbot = document.getElementById('ai-chatbot');
        const toggle = document.getElementById('chatbot-toggle');
        this.isOpen = !this.isOpen;

        if (this.isOpen) {
            chatbot.classList.add('open');
            toggle.style.display = 'none';
        } else {
            chatbot.classList.remove('open');
            toggle.style.display = 'flex';
        }
    }

    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();

        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        input.value = '';

        // Show typing indicator
        this.showTyping();

        try {
            const response = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    calculator_type: this.calculatorType
                })
            });

            const data = await response.json();
            this.hideTyping();
            this.addMessage(data.response, 'bot');
        } catch (error) {
            this.hideTyping();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    }

    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `${sender}-message`;
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    showTyping() {
        const messagesContainer = document.getElementById('chatbot-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'bot-message typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = '<span></span><span></span><span></span>';
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideTyping() {
        const typing = document.getElementById('typing-indicator');
        if (typing) typing.remove();
    }
}

// Smart Explain Mode
async function showSmartExplanation(calculatorType, result, inputs) {
    try {
        const response = await fetch('/api/ai/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                calculator_type: calculatorType,
                result: result,
                inputs: inputs
            })
        });

        const explanation = await response.json();
        displaySmartExplanation(explanation);
    } catch (error) {
        console.error('Smart Explanation Error:', error);
    }
}

function displaySmartExplanation(explanation) {
    let container = document.getElementById('smart-explanation');

    if (!container) {
        container = document.createElement('div');
        container.id = 'smart-explanation';
        container.className = 'smart-explanation-container';
        document.querySelector('.result-box').appendChild(container);
    }

    let html = '<div class="smart-explain">';
    html += '<h3>🧠 Smart Explanation</h3>';

    if (explanation.formula) {
        html += `<div class="explain-card">
            <h4>📐 Formula</h4>
            <div class="formula">${explanation.formula}</div>
        </div>`;
    }

    if (explanation.components) {
        html += `<div class="explain-card">
            <h4>🔢 Components</h4>
            <ul class="components-list">`;
        for (const [key, value] of Object.entries(explanation.components)) {
            html += `<li><strong>${key}:</strong> ${value}</li>`;
        }
        html += `</ul></div>`;
    }

    if (explanation.your_calculation) {
        html += `<div class="explain-card">
            <h4>📊 Your Calculation</h4>
            <p>${explanation.your_calculation}</p>
        </div>`;
    }

    if (explanation.what_it_means) {
        html += `<div class="explain-card">
            <h4>💡 What It Means</h4>
            <p>${explanation.what_it_means}</p>
        </div>`;
    }

    if (explanation.why_this_value) {
        html += `<div class="explain-card">
            <h4>❓ Why This Value</h4>
            <p>${explanation.why_this_value}</p>
        </div>`;
    }

    if (explanation.health_implications) {
        html += `<div class="explain-card">
            <h4>⚕️ Health Implications</h4>
            <ul class="implications-list">
                ${explanation.health_implications.map(imp => `<li>${imp}</li>`).join('')}
            </ul>
        </div>`;
    }

    html += '</div>';
    container.innerHTML = html;
    container.style.display = 'block';
}

// Initialize chatbot
let aiChatbot = null;

function initAIFeatures(calculatorType) {
    aiChatbot = new AIChatbot(calculatorType);
}

// Add AI button to results
function addAIButton(containerId, calculatorType, getData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const existingBtn = container.querySelector('.ai-analyze-btn');
    if (existingBtn) existingBtn.remove();

    const button = document.createElement('button');
    button.className = 'ai-analyze-btn';
    button.innerHTML = '🤖 Get AI Recommendations';
    button.onclick = async () => {
        const data = getData();
        if (data) {
            button.disabled = true;
            button.innerHTML = '⏳ Analyzing...';
            await getAIRecommendations(calculatorType, data);
            button.innerHTML = '✅ Analysis Complete';
            setTimeout(() => {
                button.disabled = false;
                button.innerHTML = '🤖 Get AI Recommendations';
            }, 2000);
        }
    };

    container.appendChild(button);
}

// Add Smart Explain button
function addSmartExplainButton(containerId, calculatorType, getResult, getInputs) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const existingBtn = container.querySelector('.smart-explain-btn');
    if (existingBtn) existingBtn.remove();

    const button = document.createElement('button');
    button.className = 'smart-explain-btn';
    button.innerHTML = '🧠 Smart Explain';
    button.onclick = async () => {
        const result = getResult();
        const inputs = getInputs();
        if (result && inputs) {
            await showSmartExplanation(calculatorType, result, inputs);
        }
    };

    container.appendChild(button);
}
