# CalcHub – All-in-One Smart Calculator Suite

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A comprehensive web-based calculator platform featuring 20+ specialized calculators with an intuitive, modern interface. Built with Flask and designed for seamless user experience across all devices.

</div>

---

## 📋 Overview

CalcHub is a professional-grade calculator suite that consolidates essential computational tools into a single, elegant web application. Whether you're tracking fitness goals, managing finances, calculating academic performance, or performing everyday conversions, CalcHub provides accurate, instant results with a beautiful gradient-based UI.

## ✨ Key Features

### 🏥 Health & Fitness Calculators
- **BMI Calculator** – Determine Body Mass Index with health category classification
- **BMR Calculator** – Calculate Basal Metabolic Rate for metabolic insights
- **Calorie Calculator** – Estimate daily caloric requirements based on activity level
- **Calorie Burn Calculator** – Track calories burned during various physical activities
- **Water Intake Calculator** – Personalized daily hydration recommendations
- **Macros Calculator** – Calculate optimal macronutrient distribution (protein, carbs, fats)
- **Sleep Calculator** – Optimize sleep schedules based on natural sleep cycles

### 💰 Financial Calculators
- **Loan EMI Calculator** – Compute monthly loan installments with amortization details
- **Mortgage Calculator** – Comprehensive home loan payment breakdown
- **Compound Interest Calculator** – Project investment growth over time
- **Discount Calculator** – Calculate sale prices, savings, and multiple discount scenarios

### 🎓 Academic Calculators
- **GPA Calculator** – Compute Grade Point Average with customizable credit hours
- **Grade Calculator** – Convert marks to letter grades with percentage analysis
- **Percentage Calculator** – Calculate marks percentage and grade distribution
- **Attendance Calculator** – Track and manage class attendance requirements

### 🔧 Utility Calculators
- **Age Calculator** – Calculate precise age with years, months, and days
- **Pregnancy Calculator** – Estimate due dates and pregnancy milestones
- **Math Calculator** – Advanced scientific calculator with expression evaluation
- **Currency Converter** – Real-time conversion between 25+ global currencies
- **Unit Converter** – Convert length, weight, temperature, volume, area, and speed units

## Project Structure

```
CalcHub/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── calculators/                # Calculator logic modules
│   ├── __init__.py
│   ├── bmi_calculator.py
│   ├── bmr_calculator.py
│   ├── loan_calculator.py
│   ├── mortgage_calculator.py
│   ├── age_calculator.py
│   ├── gpa_calculator.py
│   ├── grade_calculator.py
│   ├── calorie_calculator.py
│   ├── calorie_burn_calculator.py
│   ├── water_intake_calculator.py
│   ├── pregnancy_calculator.py
│   ├── percentage_calculator.py
│   ├── discount_calculator.py
│   ├── attendance_calculator.py
│   ├── compound_interest_calculator.py
│   ├── math_calculator.py
│   ├── currency_converter.py
│   ├── unit_converter.py
│   ├── macros_calculator.py
│   └── sleep_calculator.py
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── bmi.html
│   ├── bmr.html
│   ├── loan.html
│   ├── mortgage.html
│   ├── age.html
│   ├── gpa.html
│   ├── grade.html
│   ├── calorie.html
│   ├── calorie_burn.html
│   ├── water_intake.html
│   ├── pregnancy.html
│   ├── percentage.html
│   ├── discount.html
│   ├── attendance.html
│   ├── compound_interest.html
│   ├── math.html
│   ├── currency_converter.html
│   ├── unit_converter.html
│   ├── macros.html
│   └── sleep.html
└── static/                     # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ankit2006Raj/CalcHub.git
   cd CalcHub
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   
   Open your browser and navigate to `http://localhost:5000`

### Quick Start Guide

1. Browse the calculator collection on the homepage
2. Use the search functionality to quickly find specific calculators
3. Click "Open Calculator" on any card to access the tool
4. Enter the required parameters and click calculate
5. View detailed results with explanations and recommendations

## 🛠️ Technology Stack

- **Backend Framework**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Architecture**: RESTful API design
- **UI/UX**: Responsive gradient-based design
- **Data Storage**: JSON-based calculation history

## 📡 API Reference

CalcHub provides RESTful API endpoints for programmatic access to all calculators:

### Health & Fitness Endpoints
- `POST /api/bmi` – BMI calculation
- `POST /api/bmr` – BMR calculation
- `POST /api/calorie` – Daily calorie needs
- `POST /api/calorie-burn` – Calories burned calculation
- `GET /api/calorie-burn/activities` – List available activities
- `POST /api/water-intake` – Water intake recommendation
- `POST /api/macros` – Macronutrient calculation
- `POST /api/sleep` – Sleep schedule optimization
- `GET /api/sleep/tips` – Sleep improvement tips

### Financial Endpoints
- `POST /api/loan` – Loan EMI calculation
- `POST /api/mortgage` – Mortgage payment breakdown
- `POST /api/compound-interest` – Investment growth projection
- `POST /api/discount` – Discount and savings calculation

### Academic Endpoints
- `POST /api/gpa` – GPA calculation
- `POST /api/grade` – Grade conversion
- `POST /api/percentage` – Percentage calculation
- `POST /api/attendance` – Attendance tracking

### Utility Endpoints
- `POST /api/age` – Age calculation
- `POST /api/pregnancy` – Due date estimation
- `POST /api/math` – Mathematical expression evaluation
- `POST /api/currency-converter` – Currency conversion
- `GET /api/currency-converter/currencies` – Available currencies list
- `POST /api/unit-converter` – Unit conversion
- `GET /api/unit-converter/categories` – Conversion categories
- `GET /api/unit-converter/units/<category>` – Units by category

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Ankit Raj**

Full-Stack Developer passionate about creating practical, user-friendly web applications that solve real-world problems.

- 🌐 GitHub: [@Ankit2006Raj](https://github.com/Ankit2006Raj)
- 💼 LinkedIn: [Ankit Raj](https://www.linkedin.com/in/ankit-raj-226a36309)
- 📧 Email: ankit9905163014@gmail.com

---

<div align="center">

**If you find this project helpful, please consider giving it a ⭐️**

Made with ❤️ by Ankit Raj

</div>
"# CalcHub" 
