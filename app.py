from flask import Flask, render_template, request, jsonify, send_file, session
from calculators.bmi_calculator import calculate_bmi
from calculators.bmr_calculator import calculate_bmr
from calculators.loan_calculator import calculate_loan
from calculators.age_calculator import calculate_age
from calculators.gpa_calculator import calculate_gpa
from calculators.grade_calculator import calculate_grade
from calculators.calorie_calculator import calculate_calories
from calculators.pregnancy_calculator import calculate_due_date
from calculators.percentage_calculator import calculate_percentage
from calculators.attendance_calculator import calculate_attendance

from calculators.compound_interest_calculator import calculate_compound_interest
from calculators.math_calculator import evaluate_expression
from calculators.mortgage_calculator import calculate_mortgage
from calculators.discount_calculator import calculate_discount, calculate_multiple_discounts, calculate_bulk_discount
from calculators.calorie_burn_calculator import calculate_calorie_burn, calculate_multiple_activities, get_all_activities
from calculators.water_intake_calculator import calculate_water_intake
from calculators.currency_converter import convert_currency, get_all_currencies as get_currencies, compare_multiple_currencies
from calculators.unit_converter import convert_unit, get_all_units, get_all_categories
from calculators.macros_calculator import calculate_macros
from calculators.sleep_calculator import calculate_sleep_times, calculate_sleep_debt, get_sleep_tips
from utils.pdf_generator import PDFGenerator
from utils.ai_service import AIService
from utils.history_manager import HistoryManager
from utils.analytics_service import AnalyticsService
from utils.sharing_service import SharingService
from datetime import datetime
import uuid
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
pdf_generator = PDFGenerator()
ai_service = AIService()
history_manager = HistoryManager()
analytics_service = AnalyticsService()
sharing_service = SharingService()

# Helper function to get or create user ID
def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bmi')
def bmi():
    return render_template('bmi.html')

@app.route('/bmr')
def bmr():
    return render_template('bmr.html')

@app.route('/loan')
def loan():
    return render_template('loan.html')

@app.route('/age')
def age():
    return render_template('age.html')

@app.route('/gpa')
def gpa():
    return render_template('gpa.html')

@app.route('/grade')
def grade():
    return render_template('grade.html')

@app.route('/calorie')
def calorie():
    return render_template('calorie.html')

@app.route('/pregnancy')
def pregnancy():
    return render_template('pregnancy.html')

@app.route('/percentage')
def percentage():
    return render_template('percentage.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')



@app.route('/compound-interest')
def compound_interest():
    return render_template('compound_interest.html')

@app.route('/math')
def math():
    return render_template('math.html')

@app.route('/mortgage')
def mortgage():
    return render_template('mortgage.html')

@app.route('/discount')
def discount():
    return render_template('discount.html')

@app.route('/calorie-burn')
def calorie_burn():
    return render_template('calorie_burn.html')

@app.route('/water-intake')
def water_intake():
    return render_template('water_intake.html')

@app.route('/currency-converter')
def currency_converter():
    return render_template('currency_converter.html')

@app.route('/unit-converter')
def unit_converter():
    return render_template('unit_converter.html')

@app.route('/macros')
def macros():
    return render_template('macros.html')

@app.route('/sleep')
def sleep():
    return render_template('sleep.html')

# API Routes
@app.route('/api/bmi', methods=['POST'])
def api_bmi():
    data = request.json
    result = calculate_bmi(float(data['height']), float(data['weight']))
    return jsonify(result)

@app.route('/api/bmr', methods=['POST'])
def api_bmr():
    data = request.json
    result = calculate_bmr(data['gender'], int(data['age']), float(data['height']), float(data['weight']))
    return jsonify(result)

@app.route('/api/loan', methods=['POST'])
def api_loan():
    data = request.json
    result = calculate_loan(float(data['amount']), float(data['rate']), int(data['duration']))
    return jsonify(result)

@app.route('/api/age', methods=['POST'])
def api_age():
    data = request.json
    result = calculate_age(data['dob'])
    return jsonify(result)

@app.route('/api/gpa', methods=['POST'])
def api_gpa():
    data = request.json
    result = calculate_gpa(data['courses'])
    return jsonify(result)

@app.route('/api/grade', methods=['POST'])
def api_grade():
    data = request.json
    result = calculate_grade(float(data['scored']), float(data['total']))
    return jsonify(result)

@app.route('/api/calorie', methods=['POST'])
def api_calorie():
    data = request.json
    result = calculate_calories(data['gender'], int(data['age']), float(data['weight']), 
                                float(data['height']), data['activity'])
    return jsonify(result)

@app.route('/api/pregnancy', methods=['POST'])
def api_pregnancy():
    data = request.json
    result = calculate_due_date(data['last_period'])
    return jsonify(result)

@app.route('/api/percentage', methods=['POST'])
def api_percentage():
    data = request.json
    result = calculate_percentage(data['marks'])
    return jsonify(result)

@app.route('/api/attendance', methods=['POST'])
def api_attendance():
    data = request.json
    result = calculate_attendance(int(data['attended']), int(data['total']), int(data.get('target', 75)))
    return jsonify(result)



@app.route('/api/compound-interest', methods=['POST'])
def api_compound_interest():
    data = request.json
    result = calculate_compound_interest(float(data['principal']), float(data['rate']), 
                                        int(data['time']), int(data['frequency']))
    return jsonify(result)

@app.route('/api/math', methods=['POST'])
def api_math():
    data = request.json
    result = evaluate_expression(data['expression'])
    return jsonify(result)

@app.route('/api/mortgage', methods=['POST'])
def api_mortgage():
    data = request.json
    result = calculate_mortgage(
        float(data['home_price']),
        float(data['down_payment']),
        float(data['interest_rate']),
        int(data['loan_term']),
        float(data.get('property_tax', 0)),
        float(data.get('home_insurance', 0)),
        float(data.get('pmi', 0)),
        float(data.get('hoa_fees', 0))
    )
    return jsonify(result)

@app.route('/api/discount', methods=['POST'])
def api_discount():
    data = request.json
    calc_type = data.get('type', 'simple')
    
    if calc_type == 'multiple':
        result = calculate_multiple_discounts(
            float(data['original_price']),
            data['discounts']
        )
    elif calc_type == 'bulk':
        result = calculate_bulk_discount(
            float(data['unit_price']),
            int(data['quantity']),
            data.get('bulk_tiers')
        )
    else:
        result = calculate_discount(
            float(data['original_price']),
            data.get('discount_percent'),
            data.get('sale_price'),
            data.get('discount_amount')
        )
    return jsonify(result)

@app.route('/api/calorie-burn', methods=['POST'])
def api_calorie_burn():
    data = request.json
    
    if 'activities' in data:
        result = calculate_multiple_activities(
            float(data['weight']),
            data['activities'],
            data.get('weight_unit', 'kg')
        )
    else:
        result = calculate_calorie_burn(
            float(data['weight']),
            data['activity'],
            int(data['duration']),
            data.get('weight_unit', 'kg')
        )
    return jsonify(result)

@app.route('/api/calorie-burn/activities', methods=['GET'])
def api_calorie_burn_activities():
    activities = get_all_activities()
    return jsonify(activities)

@app.route('/api/water-intake', methods=['POST'])
def api_water_intake():
    data = request.json
    result = calculate_water_intake(
        float(data['weight']),
        data['activity_level'],
        data.get('climate', 'moderate'),
        data.get('gender', 'male'),
        int(data.get('age', 30)),
        data.get('weight_unit', 'kg'),
        data.get('pregnant', False),
        data.get('breastfeeding', False)
    )
    return jsonify(result)

@app.route('/api/currency-converter', methods=['POST'])
def api_currency_converter():
    data = request.json
    if 'to_currencies' in data:
        result = compare_multiple_currencies(
            float(data['amount']),
            data['from_currency'],
            data['to_currencies']
        )
    else:
        result = convert_currency(
            float(data['amount']),
            data['from_currency'],
            data['to_currency']
        )
    return jsonify(result)

@app.route('/api/currency-converter/currencies', methods=['GET'])
def api_get_currencies():
    currencies = get_currencies()
    return jsonify(currencies)

@app.route('/api/unit-converter', methods=['POST'])
def api_unit_converter():
    data = request.json
    result = convert_unit(
        float(data['value']),
        data['from_unit'],
        data['to_unit'],
        data['category']
    )
    return jsonify(result)

@app.route('/api/unit-converter/categories', methods=['GET'])
def api_get_categories():
    categories = get_all_categories()
    return jsonify(categories)

@app.route('/api/unit-converter/units/<category>', methods=['GET'])
def api_get_units(category):
    units = get_all_units(category)
    return jsonify(units)

@app.route('/api/macros', methods=['POST'])
def api_macros():
    data = request.json
    result = calculate_macros(
        float(data['weight']),
        float(data['height']),
        int(data['age']),
        data['gender'],
        data['activity_level'],
        data['goal'],
        data.get('weight_unit', 'kg')
    )
    return jsonify(result)

@app.route('/api/sleep', methods=['POST'])
def api_sleep():
    data = request.json
    calc_type = data.get('type', 'sleep_times')
    
    if calc_type == 'sleep_debt':
        result = calculate_sleep_debt(data['hours_slept'])
    else:
        result = calculate_sleep_times(
            data.get('wake_time'),
            data.get('sleep_time')
        )
    return jsonify(result)

@app.route('/api/sleep/tips', methods=['GET'])
def api_sleep_tips():
    tips = get_sleep_tips()
    return jsonify({'tips': tips})

# PDF Download Routes
@app.route('/api/pdf/bmi', methods=['POST'])
def pdf_bmi():
    data = request.json
    result = calculate_bmi(float(data['height']), float(data['weight']))
    pdf_buffer = pdf_generator.generate_pdf('bmi', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf', 
                    as_attachment=True, download_name=f'BMI_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/api/pdf/bmr', methods=['POST'])
def pdf_bmr():
    data = request.json
    result = calculate_bmr(data['gender'], int(data['age']), float(data['height']), float(data['weight']))
    pdf_buffer = pdf_generator.generate_pdf('bmr', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'BMR_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/api/pdf/loan', methods=['POST'])
def pdf_loan():
    data = request.json
    result = calculate_loan(float(data['amount']), float(data['rate']), int(data['duration']))
    pdf_buffer = pdf_generator.generate_pdf('loan', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'Loan_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/api/pdf/calorie', methods=['POST'])
def pdf_calorie():
    data = request.json
    result = calculate_calories(data['gender'], int(data['age']), float(data['weight']), 
                                float(data['height']), data['activity'])
    pdf_buffer = pdf_generator.generate_pdf('calorie', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'Calorie_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/api/pdf/age', methods=['POST'])
def pdf_age():
    data = request.json
    result = calculate_age(data['dob'])
    pdf_buffer = pdf_generator.generate_pdf('age', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'Age_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/api/pdf/gpa', methods=['POST'])
def pdf_gpa():
    data = request.json
    result = calculate_gpa(data['courses'])
    pdf_buffer = pdf_generator.generate_pdf('gpa', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'GPA_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/api/pdf/grade', methods=['POST'])
def pdf_grade():
    data = request.json
    result = calculate_grade(float(data['scored']), float(data['total']))
    pdf_buffer = pdf_generator.generate_pdf('grade', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'Grade_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/api/pdf/pregnancy', methods=['POST'])
def pdf_pregnancy():
    data = request.json
    result = calculate_due_date(data['last_period'])
    pdf_buffer = pdf_generator.generate_pdf('pregnancy', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'Pregnancy_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/api/pdf/percentage', methods=['POST'])
def pdf_percentage():
    data = request.json
    result = calculate_percentage(data['marks'])
    pdf_buffer = pdf_generator.generate_pdf('percentage', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'Percentage_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/api/pdf/attendance', methods=['POST'])
def pdf_attendance():
    data = request.json
    result = calculate_attendance(int(data['attended']), int(data['total']), int(data.get('target', 75)))
    pdf_buffer = pdf_generator.generate_pdf('attendance', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'Attendance_Report_{datetime.now().strftime("%Y%m%d")}.pdf')



@app.route('/api/pdf/compound-interest', methods=['POST'])
def pdf_compound_interest():
    data = request.json
    result = calculate_compound_interest(float(data['principal']), float(data['rate']), 
                                        int(data['time']), int(data['frequency']))
    pdf_buffer = pdf_generator.generate_pdf('compound_interest', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'Investment_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/api/pdf/math', methods=['POST'])
def pdf_math():
    data = request.json
    result = evaluate_expression(data['expression'])
    pdf_buffer = pdf_generator.generate_pdf('math', result, data)
    return send_file(pdf_buffer, mimetype='application/pdf',
                    as_attachment=True, download_name=f'Math_Report_{datetime.now().strftime("%Y%m%d")}.pdf')

# AI-Powered Recommendation Endpoints
@app.route('/api/ai/bmi-recommendations', methods=['POST'])
def ai_bmi_recommendations():
    data = request.json
    result = calculate_bmi(float(data['height']), float(data['weight']))
    recommendations = ai_service.get_bmi_recommendations(
        result['bmi'], result['category'], 
        float(data['height']), float(data['weight'])
    )
    return jsonify(recommendations)

@app.route('/api/ai/loan-recommendations', methods=['POST'])
def ai_loan_recommendations():
    data = request.json
    result = calculate_loan(float(data['amount']), float(data['rate']), int(data['duration']))
    recommendations = ai_service.get_loan_recommendations(
        float(data['amount']), float(data['rate']), 
        int(data['duration']), result['emi']
    )
    return jsonify(recommendations)

@app.route('/api/ai/gpa-recommendations', methods=['POST'])
def ai_gpa_recommendations():
    data = request.json
    result = calculate_gpa(data['courses'])
    recommendations = ai_service.get_gpa_recommendations(result['gpa'], data['courses'])
    return jsonify(recommendations)

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    message = data.get('message', '')
    calculator_type = data.get('calculator_type', 'general')
    context = data.get('context', {})
    response = ai_service.chat_with_ai(message, calculator_type, context)
    return jsonify({'response': response})

@app.route('/api/ai/explain', methods=['POST'])
def ai_explain():
    data = request.json
    calculator_type = data.get('calculator_type')
    result = data.get('result', {})
    inputs = data.get('inputs', {})
    explanation = ai_service.get_smart_explanation(calculator_type, result, inputs)
    return jsonify(explanation)

# ============= HISTORY MANAGEMENT ENDPOINTS =============

@app.route('/api/history/save', methods=['POST'])
def save_history():
    """Save calculation to history"""
    data = request.json
    user_id = get_user_id()
    calculator_type = data.get('calculator_type')
    inputs = data.get('inputs', {})
    results = data.get('results', {})
    
    response = history_manager.save_calculation(user_id, calculator_type, inputs, results)
    return jsonify(response)

@app.route('/api/history/get', methods=['GET'])
def get_history():
    """Get user's calculation history"""
    user_id = get_user_id()
    calculator_type = request.args.get('calculator_type')
    limit = request.args.get('limit', type=int)
    
    history = history_manager.get_user_history(user_id, calculator_type, limit)
    return jsonify({'history': history, 'total': len(history)})

@app.route('/api/history/monthly-summary', methods=['GET'])
def monthly_summary():
    """Get monthly summary of calculations"""
    user_id = get_user_id()
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    summary = history_manager.get_monthly_summary(user_id, year, month)
    return jsonify(summary)

@app.route('/api/history/delete/<entry_id>', methods=['DELETE'])
def delete_history_entry(entry_id):
    """Delete a specific history entry"""
    user_id = get_user_id()
    response = history_manager.delete_entry(user_id, entry_id)
    return jsonify(response)

@app.route('/api/history/clear', methods=['DELETE'])
def clear_history():
    """Clear all history for user"""
    user_id = get_user_id()
    calculator_type = request.args.get('calculator_type')
    response = history_manager.clear_history(user_id, calculator_type)
    return jsonify(response)

# ============= ANALYTICS ENDPOINTS =============

@app.route('/api/analytics/trends', methods=['GET'])
def get_analytics_trends():
    """Get analytics trends for a calculator"""
    user_id = get_user_id()
    calculator_type = request.args.get('calculator_type')
    
    analytics = history_manager.get_analytics_data(user_id, calculator_type)
    return jsonify(analytics)

@app.route('/api/analytics/chart/<calculator_type>', methods=['GET'])
def get_chart_data(calculator_type):
    """Get chart data for visualization"""
    user_id = get_user_id()
    history = history_manager.get_user_history(user_id, calculator_type)
    
    chart_data = None
    if calculator_type == 'bmi':
        chart_data = analytics_service.generate_bmi_chart_data(history)
    elif calculator_type == 'calorie':
        chart_data = analytics_service.generate_calorie_chart_data(history)
    elif calculator_type == 'gpa':
        chart_data = analytics_service.generate_gpa_progress_chart(history)
    elif calculator_type == 'attendance':
        chart_data = analytics_service.generate_attendance_chart(history)
    
    return jsonify(chart_data or {})

@app.route('/api/analytics/loan-visualization', methods=['POST'])
def loan_visualization():
    """Get loan visualization data"""
    data = request.json
    result = calculate_loan(float(data['amount']), float(data['rate']), int(data['duration']))
    
    visualization = analytics_service.generate_loan_visualization(result)
    schedule = analytics_service.generate_loan_amortization_schedule(
        float(data['amount']), float(data['rate']), 
        int(data['duration']), result['emi']
    )
    
    return jsonify({
        'visualization': visualization,
        'amortization_schedule': schedule
    })

@app.route('/api/analytics/insights', methods=['GET'])
def get_insights():
    """Get AI-powered insights"""
    user_id = get_user_id()
    calculator_type = request.args.get('calculator_type')
    
    history = history_manager.get_user_history(user_id, calculator_type)
    current_result = history[0]['results'] if history else {}
    
    insights = analytics_service.generate_insights(calculator_type, history, current_result)
    recommendations = analytics_service.generate_recommendations_based_on_trends(calculator_type, history)
    
    return jsonify({
        'insights': insights,
        'recommendations': recommendations
    })

@app.route('/api/analytics/usage-stats', methods=['GET'])
def usage_stats():
    """Get calculator usage statistics"""
    user_id = get_user_id()
    history = history_manager.get_user_history(user_id)
    
    stats = analytics_service.generate_calculator_usage_stats(history)
    heatmap = analytics_service.generate_monthly_activity_heatmap(history)
    
    return jsonify({
        'usage_stats': stats,
        'activity_heatmap': heatmap
    })

# ============= SHARING ENDPOINTS =============

@app.route('/api/share/links', methods=['POST'])
def get_share_links():
    """Get all social media share links"""
    data = request.json
    calculator_type = data.get('calculator_type')
    result = data.get('result', {})
    inputs = data.get('inputs', {})
    
    links = sharing_service.generate_all_share_links(calculator_type, result, inputs)
    return jsonify(links)

@app.route('/api/share/card-data', methods=['POST'])
def get_share_card_data():
    """Get data for creating shareable image card"""
    data = request.json
    calculator_type = data.get('calculator_type')
    result = data.get('result', {})
    inputs = data.get('inputs', {})
    
    card_data = sharing_service.generate_share_card_data(calculator_type, result, inputs)
    return jsonify(card_data)

@app.route('/api/share/copy-text', methods=['POST'])
def get_copy_text():
    """Get formatted text for copying"""
    data = request.json
    calculator_type = data.get('calculator_type')
    result = data.get('result', {})
    inputs = data.get('inputs', {})
    
    text = sharing_service.generate_copy_text(calculator_type, result, inputs)
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
