/**
 * Command Palette - Global Search (Ctrl+K)
 * Quick navigation to any calculator
 */

class CommandPalette {
    constructor() {
        this.isOpen = false;
        this.calculators = [
            // Health & Fitness
            { name: 'BMI Calculator', url: '/bmi', icon: '⚖️', keywords: ['body', 'mass', 'index', 'weight', 'health'] },
            { name: 'BMR Calculator', url: '/bmr', icon: '🔥', keywords: ['basal', 'metabolic', 'rate', 'calories', 'metabolism'] },
            { name: 'Calorie Calculator', url: '/calorie', icon: '🍎', keywords: ['calories', 'diet', 'nutrition', 'food', 'tdee'] },
            { name: 'Calorie Burn Calculator', url: '/calorie-burn', icon: '🏃', keywords: ['calorie', 'burn', 'exercise', 'workout', 'activity'] },
            { name: 'Water Intake Calculator', url: '/water-intake', icon: '💧', keywords: ['water', 'hydration', 'intake', 'drink', 'health'] },
            { name: 'Macros Calculator', url: '/macros', icon: '🥗', keywords: ['macros', 'protein', 'carbs', 'fat', 'nutrition', 'diet'] },
            { name: 'Sleep Calculator', url: '/sleep', icon: '😴', keywords: ['sleep', 'rest', 'wake', 'cycle', 'bedtime'] },
            { name: 'Pregnancy Calculator', url: '/pregnancy', icon: '🤰', keywords: ['pregnancy', 'due', 'date', 'baby', 'trimester'] },

            // Finance
            { name: 'Loan Calculator', url: '/loan', icon: '💰', keywords: ['emi', 'loan', 'interest', 'mortgage', 'finance'] },
            { name: 'Mortgage Calculator', url: '/mortgage', icon: '🏠', keywords: ['mortgage', 'home', 'loan', 'property', 'house'] },
            { name: 'Compound Interest', url: '/compound-interest', icon: '📈', keywords: ['compound', 'interest', 'investment', 'savings'] },
            { name: 'Discount Calculator', url: '/discount', icon: '🏷️', keywords: ['discount', 'sale', 'price', 'savings', 'offer'] },
            { name: 'Percentage Calculator', url: '/percentage', icon: '📊', keywords: ['percentage', 'marks', 'score', 'result'] },
            { name: 'Currency Converter', url: '/currency-converter', icon: '💱', keywords: ['currency', 'exchange', 'convert', 'money', 'forex'] },
            { name: 'Credit Card EMI', url: '/credit-card-emi', icon: '💳', keywords: ['credit', 'card', 'emi', 'interest', 'fee'] },
            { name: 'FD Calculator', url: '/fd-calculator', icon: '🏦', keywords: ['fixed', 'deposit', 'fd', 'interest', 'maturity'] },
            { name: 'Electricity Bill', url: '/electricity-bill', icon: '⚡', keywords: ['electricity', 'bill', 'power', 'energy', 'units'] },
            { name: 'GST Calculator', url: '/gst-calculator', icon: '🧾', keywords: ['gst', 'tax', 'rate', 'inclusive', 'exclusive'] },

            // Education
            { name: 'GPA Calculator', url: '/gpa', icon: '📚', keywords: ['gpa', 'grade', 'academic', 'school', 'college'] },
            { name: 'Grade Calculator', url: '/grade', icon: '📝', keywords: ['grade', 'marks', 'percentage', 'score'] },
            { name: 'Attendance Calculator', url: '/attendance', icon: '✅', keywords: ['attendance', 'class', 'present', 'absent'] },

            // Tools
            { name: 'Age Calculator', url: '/age', icon: '🎂', keywords: ['age', 'birthday', 'years', 'date'] },
            { name: 'Math Calculator', url: '/math', icon: '🔢', keywords: ['math', 'calculator', 'scientific', 'calculate'] },
            { name: 'Unit Converter', url: '/unit-converter', icon: '📏', keywords: ['unit', 'convert', 'measurement', 'length', 'weight'] }
        ];
        this.filteredCalculators = [...this.calculators];
        this.selectedIndex = 0;
        this.init();
    }

    init() {
        this.createPalette();
        this.attachEventListeners();
    }

    createPalette() {
        const paletteHTML = `
            <div id="command-palette" class="command-palette">
                <div class="command-palette-backdrop" onclick="commandPalette.close()"></div>
                <div class="command-palette-container">
                    <div class="command-palette-header">
                        <span class="search-icon">🔍</span>
                        <input 
                            type="text" 
                            id="command-search" 
                            placeholder="Search calculators... (Ctrl+K)"
                            autocomplete="off"
                        >
                        <span class="close-icon" onclick="commandPalette.close()">×</span>
                    </div>
                    <div class="command-palette-results" id="command-results">
                        ${this.renderResults()}
                    </div>
                    <div class="command-palette-footer">
                        <span><kbd>↑</kbd><kbd>↓</kbd> Navigate</span>
                        <span><kbd>Enter</kbd> Select</span>
                        <span><kbd>Esc</kbd> Close</span>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', paletteHTML);
    }

    attachEventListeners() {
        // Ctrl+K or Cmd+K to open
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.toggle();
            }

            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Search input
        const searchInput = document.getElementById('command-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.search(e.target.value);
            });

            searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    this.selectNext();
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    this.selectPrevious();
                } else if (e.key === 'Enter') {
                    e.preventDefault();
                    this.selectCurrent();
                }
            });
        }
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        const palette = document.getElementById('command-palette');
        if (palette) {
            palette.classList.add('active');
            this.isOpen = true;
            setTimeout(() => {
                document.getElementById('command-search').focus();
            }, 100);
        }
    }

    close() {
        const palette = document.getElementById('command-palette');
        if (palette) {
            palette.classList.remove('active');
            this.isOpen = false;
            document.getElementById('command-search').value = '';
            this.filteredCalculators = [...this.calculators];
            this.selectedIndex = 0;
            this.updateResults();
        }
    }

    search(query) {
        const lowerQuery = query.toLowerCase().trim();

        if (!lowerQuery) {
            this.filteredCalculators = [...this.calculators];
        } else {
            this.filteredCalculators = this.calculators.filter(calc => {
                const nameMatch = calc.name.toLowerCase().includes(lowerQuery);
                const keywordMatch = calc.keywords.some(keyword =>
                    keyword.toLowerCase().includes(lowerQuery)
                );
                return nameMatch || keywordMatch;
            });
        }

        this.selectedIndex = 0;
        this.updateResults();
    }

    renderResults() {
        if (this.filteredCalculators.length === 0) {
            return '<div class="no-results">No calculators found</div>';
        }

        return this.filteredCalculators.map((calc, index) => `
            <div class="command-result ${index === this.selectedIndex ? 'selected' : ''}" 
                 data-index="${index}"
                 onclick="commandPalette.navigate('${calc.url}')">
                <span class="result-icon">${calc.icon}</span>
                <span class="result-name">${calc.name}</span>
                <span class="result-arrow">→</span>
            </div>
        `).join('');
    }

    updateResults() {
        const resultsContainer = document.getElementById('command-results');
        if (resultsContainer) {
            resultsContainer.innerHTML = this.renderResults();
        }
    }

    selectNext() {
        if (this.selectedIndex < this.filteredCalculators.length - 1) {
            this.selectedIndex++;
            this.updateResults();
            this.scrollToSelected();
        }
    }

    selectPrevious() {
        if (this.selectedIndex > 0) {
            this.selectedIndex--;
            this.updateResults();
            this.scrollToSelected();
        }
    }

    selectCurrent() {
        if (this.filteredCalculators[this.selectedIndex]) {
            this.navigate(this.filteredCalculators[this.selectedIndex].url);
        }
    }

    scrollToSelected() {
        const selected = document.querySelector('.command-result.selected');
        if (selected) {
            selected.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
    }

    navigate(url) {
        this.close();
        window.location.href = url;
    }
}

// Initialize Command Palette
let commandPalette;
document.addEventListener('DOMContentLoaded', () => {
    commandPalette = new CommandPalette();
});
