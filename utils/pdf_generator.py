from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Only add styles if they don't already exist
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ))
        
        if 'SectionHeader' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionHeader',
                parent=self.styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#34495e'),
                spaceAfter=12,
                spaceBefore=12,
                fontName='Helvetica-Bold'
            ))
        
        if 'CustomBodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomBodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                alignment=TA_JUSTIFY,
                spaceAfter=12
            ))
    
    def _add_header(self, elements, title, subtitle=None):
        """Add header to PDF"""
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        if subtitle:
            elements.append(Paragraph(subtitle, self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
    
    def _add_results_table(self, elements, data):
        """Add results table"""
        table = Table(data, colWidths=[3*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
    
    def _add_section(self, elements, title, content):
        """Add a section with title and content"""
        elements.append(Paragraph(title, self.styles['SectionHeader']))
        if isinstance(content, list):
            for item in content:
                elements.append(Paragraph(f"• {item}", self.styles['CustomBodyText']))
        else:
            elements.append(Paragraph(content, self.styles['CustomBodyText']))
        elements.append(Spacer(1, 0.2*inch))
    
    def _add_footer(self, elements):
        """Add footer"""
        elements.append(Spacer(1, 0.5*inch))
        footer_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        elements.append(Paragraph(footer_text, self.styles['Normal']))
        disclaimer = "Disclaimer: This report is for informational purposes only. Please consult with qualified professionals for personalized advice."
        elements.append(Paragraph(disclaimer, self.styles['Italic']))
    
    def generate_pdf(self, calculator_type, result_data, user_inputs):
        """Generate PDF based on calculator type"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        elements = []
        
        # Route to specific calculator PDF generator
        generator_map = {
            'bmi': self._generate_bmi_pdf,
            'bmr': self._generate_bmr_pdf,
            'loan': self._generate_loan_pdf,
            'calorie': self._generate_calorie_pdf,
            'age': self._generate_age_pdf,
            'gpa': self._generate_gpa_pdf,
            'grade': self._generate_grade_pdf,
            'pregnancy': self._generate_pregnancy_pdf,
            'percentage': self._generate_percentage_pdf,
            'attendance': self._generate_attendance_pdf,
            'compound_interest': self._generate_compound_interest_pdf,
            'math': self._generate_math_pdf
        }
        
        generator = generator_map.get(calculator_type)
        if generator:
            generator(elements, result_data, user_inputs)
        
        self._add_footer(elements)
        doc.build(elements)
        
        buffer.seek(0)
        return buffer

    
    def _generate_bmi_pdf(self, elements, result, inputs):
        """Generate BMI Calculator PDF"""
        self._add_header(elements, "BMI (Body Mass Index) Report", 
                        "Complete Analysis and Health Recommendations")
        
        # Results
        results_data = [
            ['Metric', 'Value'],
            ['Height', f"{inputs['height']} cm"],
            ['Weight', f"{inputs['weight']} kg"],
            ['BMI', f"{result['bmi']}"],
            ['Category', result['category']]
        ]
        self._add_results_table(elements, results_data)
        
        # Understanding BMI
        self._add_section(elements, "Understanding Your BMI", 
            "Body Mass Index (BMI) is a measure of body fat based on height and weight. "
            "It provides a reliable indicator of body fatness for most people and is used to "
            "screen for weight categories that may lead to health problems.")
        
        # BMI Categories
        categories_info = [
            "Underweight: BMI less than 18.5 - May indicate malnutrition or health issues",
            "Normal weight: BMI 18.5-24.9 - Healthy weight range for most adults",
            "Overweight: BMI 25-29.9 - Increased risk of health problems",
            "Obese: BMI 30 or greater - High risk of serious health conditions"
        ]
        self._add_section(elements, "BMI Categories Explained", categories_info)
        
        # Personalized Recommendations
        recommendations = self._get_bmi_recommendations(result['category'])
        self._add_section(elements, "Personalized Recommendations", recommendations)
        
        # Health Tips
        health_tips = [
            "Maintain a balanced diet rich in fruits, vegetables, whole grains, and lean proteins",
            "Engage in at least 150 minutes of moderate aerobic activity per week",
            "Stay hydrated by drinking 8-10 glasses of water daily",
            "Get 7-9 hours of quality sleep each night",
            "Manage stress through meditation, yoga, or other relaxation techniques",
            "Regular health check-ups to monitor your progress"
        ]
        self._add_section(elements, "General Health Tips", health_tips)
        
        # Important Notes
        self._add_section(elements, "Important Considerations",
            "BMI is a screening tool and does not diagnose body fatness or health. "
            "Athletes and individuals with high muscle mass may have a high BMI but low body fat. "
            "Always consult with healthcare professionals for personalized health advice.")
    
    def _get_bmi_recommendations(self, category):
        """Get specific recommendations based on BMI category"""
        recommendations = {
            'Underweight': [
                "Increase caloric intake with nutrient-dense foods",
                "Include healthy fats like nuts, avocados, and olive oil",
                "Eat frequent, smaller meals throughout the day",
                "Consider strength training to build muscle mass",
                "Consult a nutritionist for a personalized meal plan",
                "Rule out underlying health conditions with your doctor"
            ],
            'Normal': [
                "Maintain your current healthy lifestyle",
                "Continue balanced nutrition and regular exercise",
                "Monitor your weight periodically",
                "Focus on overall wellness and fitness",
                "Stay active with activities you enjoy",
                "Keep up with preventive health screenings"
            ],
            'Overweight': [
                "Create a modest calorie deficit (300-500 calories/day)",
                "Increase physical activity gradually",
                "Focus on portion control and mindful eating",
                "Reduce processed foods and added sugars",
                "Set realistic weight loss goals (1-2 lbs per week)",
                "Consider working with a dietitian or fitness coach"
            ],
            'Obese': [
                "Consult with healthcare providers for a comprehensive plan",
                "Consider medical supervision for weight loss",
                "Start with low-impact exercises like walking or swimming",
                "Address emotional eating and stress management",
                "Explore behavioral therapy or support groups",
                "Focus on sustainable lifestyle changes, not quick fixes"
            ]
        }
        return recommendations.get(category, [])

    
    def _generate_loan_pdf(self, elements, result, inputs):
        """Generate Loan Calculator PDF"""
        self._add_header(elements, "Loan EMI Analysis Report",
                        "Comprehensive Loan Repayment Plan")
        
        # Results
        results_data = [
            ['Loan Details', 'Amount'],
            ['Principal Amount', f"${result['principal']:,.2f}"],
            ['Interest Rate', f"{inputs['rate']}% per annum"],
            ['Loan Duration', f"{inputs['duration']} years"],
            ['Monthly EMI', f"${result['emi']:,.2f}"],
            ['Total Interest', f"${result['total_interest']:,.2f}"],
            ['Total Payment', f"${result['total_payment']:,.2f}"]
        ]
        self._add_results_table(elements, results_data)
        
        # Understanding EMI
        self._add_section(elements, "Understanding Your Loan",
            "EMI (Equated Monthly Installment) is the fixed amount you pay every month to repay your loan. "
            "It includes both principal and interest components. Initially, a larger portion goes toward interest, "
            "but over time, more goes toward the principal.")
        
        # Repayment Strategy
        strategies = [
            "Make extra payments when possible to reduce principal faster",
            "Consider bi-weekly payments instead of monthly to save on interest",
            "Round up your EMI to the nearest hundred for faster repayment",
            "Avoid missing payments to maintain good credit score",
            "Review refinancing options if interest rates drop",
            "Set up automatic payments to never miss a due date"
        ]
        self._add_section(elements, "Smart Repayment Strategies", strategies)
        
        # Financial Tips
        tips = [
            "Maintain an emergency fund of 3-6 months expenses",
            "Budget carefully to ensure EMI doesn't exceed 40% of income",
            "Avoid taking multiple loans simultaneously",
            "Read all loan terms and conditions carefully",
            "Keep track of your credit score regularly",
            "Consider loan insurance for financial security"
        ]
        self._add_section(elements, "Financial Management Tips", tips)
        
        # Tax Benefits
        self._add_section(elements, "Potential Tax Benefits",
            "Depending on your loan type and location, you may be eligible for tax deductions. "
            "Home loans often offer deductions on principal and interest payments. "
            "Consult with a tax professional to understand your specific benefits.")

    
    def _generate_calorie_pdf(self, elements, result, inputs):
        """Generate Calorie Calculator PDF"""
        self._add_header(elements, "Daily Calorie Needs Report",
                        "Personalized Nutrition Guide")
        
        # Results
        results_data = [
            ['Metric', 'Value'],
            ['Gender', inputs['gender'].capitalize()],
            ['Age', f"{inputs['age']} years"],
            ['Weight', f"{inputs['weight']} kg"],
            ['Height', f"{inputs['height']} cm"],
            ['Activity Level', inputs['activity'].replace('_', ' ').title()],
            ['BMR (Basal Metabolic Rate)', f"{result['bmr']} calories/day"],
            ['Maintenance Calories', f"{result['maintain']} calories/day"],
            ['Weight Loss Goal', f"{result['lose']} calories/day"],
            ['Weight Gain Goal', f"{result['gain']} calories/day"]
        ]
        self._add_results_table(elements, results_data)
        
        # Understanding Calories
        self._add_section(elements, "Understanding Your Calorie Needs",
            "Your Basal Metabolic Rate (BMR) is the number of calories your body needs at rest. "
            "Your Total Daily Energy Expenditure (TDEE) includes your activity level. "
            "To lose weight, create a deficit of 500 calories/day for approximately 1 lb/week loss. "
            "To gain weight, add 500 calories/day for approximately 1 lb/week gain.")
        
        # Nutrition Recommendations
        nutrition = [
            "Protein: 0.8-1g per kg body weight (more for active individuals)",
            "Carbohydrates: 45-65% of total calories for energy",
            "Healthy Fats: 20-35% of total calories for hormone production",
            "Fiber: 25-30g daily for digestive health",
            "Water: At least 8 glasses (2 liters) per day",
            "Vitamins & Minerals: Eat a variety of colorful fruits and vegetables"
        ]
        self._add_section(elements, "Macronutrient Guidelines", nutrition)
        
        # Meal Planning Tips
        meal_tips = [
            "Eat 5-6 smaller meals throughout the day to boost metabolism",
            "Never skip breakfast - it jumpstarts your metabolism",
            "Include protein in every meal to maintain muscle mass",
            "Choose whole grains over refined carbohydrates",
            "Prepare meals in advance to avoid unhealthy choices",
            "Practice portion control using smaller plates",
            "Limit processed foods, added sugars, and saturated fats"
        ]
        self._add_section(elements, "Meal Planning Strategies", meal_tips)
        
        # Exercise Recommendations
        exercise = [
            "Combine cardio and strength training for best results",
            "Aim for 150 minutes of moderate activity per week",
            "Include 2-3 days of resistance training",
            "Stay consistent - exercise at the same time daily",
            "Track your progress with a fitness journal or app",
            "Listen to your body and allow adequate recovery time"
        ]
        self._add_section(elements, "Exercise Guidelines", exercise)

    
    def _generate_bmr_pdf(self, elements, result, inputs):
        """Generate BMR Calculator PDF"""
        self._add_header(elements, "Basal Metabolic Rate (BMR) Report",
                        "Understanding Your Metabolism")
        
        results_data = [
            ['Personal Information', 'Value'],
            ['Gender', inputs['gender'].capitalize()],
            ['Age', f"{inputs['age']} years"],
            ['Height', f"{inputs['height']} cm"],
            ['Weight', f"{inputs['weight']} kg"],
            ['BMR', f"{result['bmr']} calories/day"]
        ]
        self._add_results_table(elements, results_data)
        
        self._add_section(elements, "What is BMR?",
            "Basal Metabolic Rate (BMR) represents the minimum number of calories your body needs "
            "to maintain basic physiological functions at rest, including breathing, circulation, "
            "cell production, and nutrient processing. This accounts for 60-75% of daily calorie expenditure.")
        
        metabolism_tips = [
            "Build muscle mass through strength training to increase BMR",
            "Eat protein-rich foods to boost thermic effect of food",
            "Stay hydrated - even mild dehydration can slow metabolism",
            "Get adequate sleep (7-9 hours) for optimal metabolic function",
            "Avoid extreme calorie restriction which can lower BMR",
            "Eat regular meals to keep metabolism active",
            "Include metabolism-boosting foods: green tea, chili peppers, coffee"
        ]
        self._add_section(elements, "Boosting Your Metabolism", metabolism_tips)
        
        factors = [
            "Age: Metabolism slows by 2-3% per decade after age 30",
            "Gender: Men typically have higher BMR due to more muscle mass",
            "Body Composition: More muscle = higher BMR",
            "Genetics: Some people naturally have faster metabolism",
            "Hormones: Thyroid function significantly affects BMR",
            "Climate: Cold environments can increase BMR"
        ]
        self._add_section(elements, "Factors Affecting BMR", factors)
    
    def _generate_age_pdf(self, elements, result, inputs):
        """Generate Age Calculator PDF"""
        self._add_header(elements, "Age Analysis Report",
                        "Comprehensive Age Breakdown")
        
        results_data = [
            ['Time Unit', 'Value'],
            ['Date of Birth', inputs['dob']],
            ['Current Age', f"{result.get('years', 0)} years"],
            ['Total Months', f"{result.get('months', 0)} months"],
            ['Total Weeks', f"{result.get('weeks', 0)} weeks"],
            ['Total Days', f"{result.get('days', 0)} days"],
            ['Total Hours', f"{result.get('hours', 0):,} hours"],
            ['Next Birthday', result.get('next_birthday', 'N/A')]
        ]
        self._add_results_table(elements, results_data)
        
        self._add_section(elements, "Age-Appropriate Health Guidelines",
            "Different life stages require different health approaches. Understanding your age helps "
            "you make informed decisions about nutrition, exercise, and preventive care.")
        
        # Age-specific recommendations would be added based on actual age
        general_tips = [
            "Schedule regular health check-ups appropriate for your age",
            "Maintain age-appropriate exercise routines",
            "Adjust nutrition based on changing metabolic needs",
            "Stay mentally active with learning and social engagement",
            "Prioritize preventive care and screenings",
            "Maintain strong social connections for emotional well-being"
        ]
        self._add_section(elements, "Health Recommendations", general_tips)

    
    def _generate_gpa_pdf(self, elements, result, inputs):
        """Generate GPA Calculator PDF"""
        self._add_header(elements, "GPA Analysis Report",
                        "Academic Performance Summary")
        
        results_data = [['Course', 'Credits', 'Grade']]
        for course in inputs['courses']:
            results_data.append([course['name'], str(course['credits']), course['grade']])
        results_data.append(['', '', ''])
        results_data.append(['Total GPA', '', f"{result['gpa']:.2f}"])
        
        self._add_results_table(elements, results_data)
        
        self._add_section(elements, "Understanding Your GPA",
            "Grade Point Average (GPA) is a standardized way of measuring academic achievement. "
            "It's calculated by dividing total grade points by total credit hours. "
            "A strong GPA opens doors to scholarships, graduate programs, and career opportunities.")
        
        improvement_tips = [
            "Attend all classes and participate actively",
            "Create a consistent study schedule and stick to it",
            "Form study groups with motivated classmates",
            "Seek help from professors during office hours",
            "Use campus tutoring and academic support services",
            "Break large assignments into manageable tasks",
            "Review material regularly, not just before exams",
            "Take care of physical and mental health",
            "Minimize distractions during study time",
            "Set specific, achievable academic goals"
        ]
        self._add_section(elements, "Academic Improvement Strategies", improvement_tips)
        
        gpa_ranges = [
            "4.0: Perfect - Exceptional achievement",
            "3.5-3.9: Excellent - Strong academic performance",
            "3.0-3.4: Good - Above average achievement",
            "2.5-2.9: Average - Satisfactory performance",
            "2.0-2.4: Below Average - Needs improvement",
            "Below 2.0: Poor - Academic probation risk"
        ]
        self._add_section(elements, "GPA Scale Interpretation", gpa_ranges)
    
    def _generate_grade_pdf(self, elements, result, inputs):
        """Generate Grade Calculator PDF"""
        self._add_header(elements, "Grade Analysis Report",
                        "Performance Evaluation")
        
        results_data = [
            ['Assessment Details', 'Value'],
            ['Marks Scored', f"{inputs['scored']}"],
            ['Total Marks', f"{inputs['total']}"],
            ['Percentage', f"{result['percentage']:.2f}%"],
            ['Grade', result['grade']],
            ['Status', result.get('status', 'N/A')]
        ]
        self._add_results_table(elements, results_data)
        
        study_tips = [
            "Review mistakes to understand concepts better",
            "Create summary notes for quick revision",
            "Practice with past papers and sample questions",
            "Teach concepts to others to reinforce learning",
            "Use active recall and spaced repetition techniques",
            "Take regular breaks during study sessions (Pomodoro technique)",
            "Stay organized with a planner or digital calendar",
            "Get adequate sleep before exams"
        ]
        self._add_section(elements, "Study Tips for Better Grades", study_tips)

    
    def _generate_pregnancy_pdf(self, elements, result, inputs):
        """Generate Pregnancy Calculator PDF"""
        self._add_header(elements, "Pregnancy Due Date Report",
                        "Your Pregnancy Journey Guide")
        
        results_data = [
            ['Pregnancy Information', 'Date'],
            ['Last Menstrual Period', inputs['last_period']],
            ['Estimated Due Date', result.get('due_date', 'N/A')],
            ['Current Week', f"Week {result.get('weeks', 0)}"],
            ['Trimester', result.get('trimester', 'N/A')],
            ['Days Until Due Date', f"{result.get('days_remaining', 0)} days"]
        ]
        self._add_results_table(elements, results_data)
        
        self._add_section(elements, "Understanding Your Pregnancy Timeline",
            "Pregnancy typically lasts 40 weeks (280 days) from the first day of your last menstrual period. "
            "It's divided into three trimesters, each with unique developmental milestones and changes.")
        
        trimester_guide = [
            "First Trimester (Weeks 1-12): Major organ development, morning sickness common",
            "Second Trimester (Weeks 13-26): Energy returns, baby movements felt, anatomy scan",
            "Third Trimester (Weeks 27-40): Rapid growth, preparation for birth, frequent check-ups"
        ]
        self._add_section(elements, "Trimester Guide", trimester_guide)
        
        prenatal_care = [
            "Attend all scheduled prenatal appointments",
            "Take prenatal vitamins with folic acid daily",
            "Eat a balanced diet rich in nutrients",
            "Stay hydrated with plenty of water",
            "Get moderate exercise (walking, prenatal yoga)",
            "Avoid alcohol, smoking, and harmful substances",
            "Get adequate rest and manage stress",
            "Track baby movements in third trimester",
            "Prepare for childbirth with classes",
            "Create a birth plan and discuss with healthcare provider"
        ]
        self._add_section(elements, "Prenatal Care Recommendations", prenatal_care)
        
        nutrition_tips = [
            "Increase calorie intake by 300-500 calories/day",
            "Eat protein-rich foods for baby's growth",
            "Include calcium for bone development",
            "Consume iron-rich foods to prevent anemia",
            "Eat omega-3 fatty acids for brain development",
            "Avoid raw fish, unpasteurized dairy, and deli meats",
            "Limit caffeine to 200mg per day"
        ]
        self._add_section(elements, "Nutrition During Pregnancy", nutrition_tips)
        
        warning_signs = [
            "Severe abdominal pain or cramping",
            "Heavy bleeding or fluid leakage",
            "Severe headaches or vision changes",
            "Decreased fetal movement",
            "Signs of preterm labor before 37 weeks",
            "Severe swelling of hands and face",
            "Persistent vomiting"
        ]
        self._add_section(elements, "Warning Signs - Contact Your Doctor If You Experience:", warning_signs)
    
    def _generate_percentage_pdf(self, elements, result, inputs):
        """Generate Percentage Calculator PDF"""
        self._add_header(elements, "Academic Percentage Report",
                        "Marks Analysis")
        
        results_data = [['Subject', 'Marks Obtained', 'Total Marks']]
        total_scored = 0
        total_max = 0
        for mark in inputs['marks']:
            results_data.append([mark['subject'], str(mark['scored']), str(mark['total'])])
            total_scored += mark['scored']
            total_max += mark['total']
        
        results_data.append(['', '', ''])
        results_data.append(['Total', str(total_scored), str(total_max)])
        results_data.append(['Percentage', f"{result['percentage']:.2f}%", ''])
        
        self._add_results_table(elements, results_data)
        
        performance_tips = [
            "Identify weak subjects and allocate more study time",
            "Maintain consistent effort across all subjects",
            "Set realistic improvement goals for each subject",
            "Use subject-specific study techniques",
            "Seek additional help for challenging topics",
            "Practice time management during exams",
            "Review and learn from past mistakes"
        ]
        self._add_section(elements, "Performance Improvement Tips", performance_tips)

    
    def _generate_attendance_pdf(self, elements, result, inputs):
        """Generate Attendance Calculator PDF"""
        self._add_header(elements, "Attendance Analysis Report",
                        "Track Your Academic Attendance")
        
        results_data = [
            ['Attendance Details', 'Value'],
            ['Classes Attended', f"{inputs['attended']}"],
            ['Total Classes', f"{inputs['total']}"],
            ['Current Attendance', f"{result['current_percentage']:.2f}%"],
            ['Target Attendance', f"{inputs.get('target', 75)}%"],
            ['Status', result.get('status', 'N/A')],
            ['Classes Needed', f"{result.get('classes_needed', 0)} more classes"],
            ['Can Skip', f"{result.get('can_skip', 0)} classes"]
        ]
        self._add_results_table(elements, results_data)
        
        self._add_section(elements, "Why Attendance Matters",
            "Regular attendance is crucial for academic success. Studies show a direct correlation "
            "between attendance and academic performance. Attending classes helps you understand concepts, "
            "participate in discussions, and stay connected with course material.")
        
        attendance_tips = [
            "Set multiple alarms to wake up on time",
            "Prepare materials the night before",
            "Sit in front rows to stay engaged",
            "Build relationships with classmates for accountability",
            "Communicate with professors if you must miss class",
            "Review notes from missed classes immediately",
            "Track attendance regularly to avoid surprises",
            "Understand your institution's attendance policy"
        ]
        self._add_section(elements, "Tips for Better Attendance", attendance_tips)
        
        consequences = [
            "Low attendance may result in grade penalties",
            "Risk of being barred from exams",
            "Missing important announcements and deadlines",
            "Difficulty understanding cumulative course material",
            "Negative impact on professor recommendations",
            "Potential academic probation"
        ]
        self._add_section(elements, "Consequences of Poor Attendance", consequences)
    
    def _generate_compound_interest_pdf(self, elements, result, inputs):
        """Generate Compound Interest Calculator PDF"""
        self._add_header(elements, "Compound Interest Analysis Report",
                        "Investment Growth Projection")
        
        results_data = [
            ['Investment Details', 'Amount'],
            ['Principal Amount', f"${inputs['principal']:,.2f}"],
            ['Annual Interest Rate', f"{inputs['rate']}%"],
            ['Time Period', f"{inputs['time']} years"],
            ['Compounding Frequency', f"{inputs['frequency']} times/year"],
            ['Final Amount', f"${result['amount']:,.2f}"],
            ['Total Interest Earned', f"${result['interest']:,.2f}"],
            ['Total Return', f"{result.get('return_percentage', 0):.2f}%"]
        ]
        self._add_results_table(elements, results_data)
        
        self._add_section(elements, "The Power of Compound Interest",
            "Compound interest is often called the 'eighth wonder of the world.' It's the interest "
            "calculated on both the initial principal and the accumulated interest from previous periods. "
            "This creates exponential growth over time, making it a powerful tool for wealth building.")
        
        investment_strategies = [
            "Start investing early to maximize compound growth",
            "Invest regularly through systematic investment plans",
            "Reinvest dividends and interest for compounding effect",
            "Diversify investments to manage risk",
            "Stay invested for the long term - avoid panic selling",
            "Increase contributions as income grows",
            "Take advantage of tax-advantaged accounts",
            "Review and rebalance portfolio annually",
            "Keep investment costs and fees low",
            "Automate investments to maintain discipline"
        ]
        self._add_section(elements, "Smart Investment Strategies", investment_strategies)
        
        financial_wisdom = [
            "Time in the market beats timing the market",
            "Compound interest works best over long periods",
            "Small, consistent investments can grow substantially",
            "Higher compounding frequency increases returns",
            "Inflation should be considered in real returns",
            "Emergency fund should be separate from investments",
            "Understand your risk tolerance before investing"
        ]
        self._add_section(elements, "Financial Wisdom", financial_wisdom)
        
        self._add_section(elements, "Investment Considerations",
            "Past performance doesn't guarantee future results. Consider your financial goals, "
            "risk tolerance, and time horizon. Consult with financial advisors for personalized advice. "
            "Diversification and regular monitoring are key to successful investing.")
    
    def _generate_math_pdf(self, elements, result, inputs):
        """Generate Math Calculator PDF"""
        self._add_header(elements, "Mathematical Calculation Report",
                        "Expression Evaluation")
        
        results_data = [
            ['Calculation', 'Result'],
            ['Expression', inputs['expression']],
            ['Answer', str(result.get('result', 'Error'))],
            ['Status', result.get('status', 'N/A')]
        ]
        self._add_results_table(elements, results_data)
        
        self._add_section(elements, "Mathematical Operations",
            "This calculator supports basic arithmetic operations, parentheses for order of operations, "
            "and follows standard mathematical conventions (PEMDAS/BODMAS).")
        
        math_tips = [
            "Always use parentheses to clarify order of operations",
            "Double-check your input for typos",
            "Break complex calculations into smaller steps",
            "Verify results with estimation",
            "Understand the mathematical concepts behind calculations",
            "Use calculator as a tool, not a replacement for understanding"
        ]
        self._add_section(elements, "Calculation Tips", math_tips)
        
        operations = [
            "Addition (+): Combining numbers",
            "Subtraction (-): Finding the difference",
            "Multiplication (* or ×): Repeated addition",
            "Division (/ or ÷): Splitting into equal parts",
            "Exponentiation (** or ^): Raising to a power",
            "Parentheses ( ): Control order of operations"
        ]
        self._add_section(elements, "Supported Operations", operations)
