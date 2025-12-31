"""
Sharing Service for Calculator Application
Handles social media sharing and result card generation
"""

from typing import Dict, Any
import urllib.parse
import base64
from io import BytesIO

class SharingService:
    """Service for sharing calculator results"""
    
    def __init__(self):
        """Initialize sharing service"""
        self.base_url = "https://your-calculator-app.com"  # Update with actual URL
    
    def generate_share_text(self, calculator_type: str, result: Dict, 
                           inputs: Dict) -> str:
        """Generate shareable text for results"""
        share_texts = {
            'bmi': f"My BMI is {result.get('bmi', 0)} ({result.get('category', 'Unknown')}). Calculate yours!",
            'gpa': f"My GPA is {result.get('gpa', 0):.2f}! Track your academic progress too!",
            'loan': f"Calculated my loan EMI: ${result.get('emi', 0):,.2f}/month. Plan your finances!",
            'calorie': f"My daily calorie needs: {result.get('maintain', 0)} calories. Find yours!",
            'attendance': f"My attendance: {result.get('current_percentage', 0):.1f}%. Track yours!",
            'age': f"I'm {result.get('years', 0)} years, {result.get('months', 0)} months old!",
            'percentage': f"Scored {result.get('percentage', 0):.1f}%! Calculate your percentage!",
            'grade': f"Got {result.get('grade', 'N/A')} grade with {result.get('percentage', 0):.1f}%!",
            'compound_interest': f"Investment projection: ${result.get('amount', 0):,.2f}! Plan your future!",
            'bmr': f"My BMR is {result.get('bmr', 0)} calories/day. Calculate yours!",
            'pregnancy': f"Due date: {result.get('due_date', 'N/A')}. Track your pregnancy journey!",
            'math': f"Calculated: {inputs.get('expression', '')} = {result.get('result', 'N/A')}"
        }
        
        return share_texts.get(calculator_type, "Check out this calculator!")
    
    def generate_whatsapp_link(self, calculator_type: str, result: Dict, 
                              inputs: Dict) -> str:
        """Generate WhatsApp share link"""
        text = self.generate_share_text(calculator_type, result, inputs)
        text += f"\n\n🔗 Try it: {self.base_url}/{calculator_type.replace('_', '-')}"
        
        encoded_text = urllib.parse.quote(text)
        return f"https://wa.me/?text={encoded_text}"
    
    def generate_twitter_link(self, calculator_type: str, result: Dict, 
                             inputs: Dict) -> str:
        """Generate Twitter/X share link"""
        text = self.generate_share_text(calculator_type, result, inputs)
        hashtags = "Calculator,Health,Fitness,Education"
        
        encoded_text = urllib.parse.quote(text)
        return f"https://twitter.com/intent/tweet?text={encoded_text}&hashtags={hashtags}"
    
    def generate_facebook_link(self, calculator_type: str) -> str:
        """Generate Facebook share link"""
        url = f"{self.base_url}/{calculator_type.replace('_', '-')}"
        encoded_url = urllib.parse.quote(url)
        return f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
    
    def generate_linkedin_link(self, calculator_type: str) -> str:
        """Generate LinkedIn share link"""
        url = f"{self.base_url}/{calculator_type.replace('_', '-')}"
        encoded_url = urllib.parse.quote(url)
        return f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}"
    
    def generate_telegram_link(self, calculator_type: str, result: Dict, 
                              inputs: Dict) -> str:
        """Generate Telegram share link"""
        text = self.generate_share_text(calculator_type, result, inputs)
        url = f"{self.base_url}/{calculator_type.replace('_', '-')}"
        
        encoded_text = urllib.parse.quote(text)
        encoded_url = urllib.parse.quote(url)
        return f"https://t.me/share/url?url={encoded_url}&text={encoded_text}"
    
    def generate_email_link(self, calculator_type: str, result: Dict, 
                           inputs: Dict) -> str:
        """Generate email share link"""
        subject = f"Check out my {calculator_type.replace('_', ' ').title()} results!"
        body = self.generate_share_text(calculator_type, result, inputs)
        body += f"\n\nCalculate yours at: {self.base_url}/{calculator_type.replace('_', '-')}"
        
        encoded_subject = urllib.parse.quote(subject)
        encoded_body = urllib.parse.quote(body)
        return f"mailto:?subject={encoded_subject}&body={encoded_body}"
    
    def generate_share_card_data(self, calculator_type: str, result: Dict, 
                                inputs: Dict) -> Dict:
        """Generate data for creating a shareable image card"""
        cards = {
            'bmi': {
                'title': 'My BMI Result',
                'main_value': f"{result.get('bmi', 0)}",
                'subtitle': result.get('category', 'Unknown'),
                'details': [
                    f"Height: {inputs.get('height', 0)} cm",
                    f"Weight: {inputs.get('weight', 0)} kg"
                ],
                'color_scheme': self._get_bmi_color(result.get('category', 'Normal')),
                'icon': '⚖️'
            },
            'gpa': {
                'title': 'My GPA',
                'main_value': f"{result.get('gpa', 0):.2f}",
                'subtitle': 'Academic Performance',
                'details': [
                    f"Courses: {len(inputs.get('courses', []))}",
                    f"Performance: {self._get_gpa_label(result.get('gpa', 0))}"
                ],
                'color_scheme': '#9b59b6',
                'icon': '🎓'
            },
            'loan': {
                'title': 'Loan EMI Calculation',
                'main_value': f"${result.get('emi', 0):,.2f}",
                'subtitle': 'Monthly Payment',
                'details': [
                    f"Principal: ${inputs.get('amount', 0):,.2f}",
                    f"Duration: {inputs.get('duration', 0)} years",
                    f"Rate: {inputs.get('rate', 0)}%"
                ],
                'color_scheme': '#3498db',
                'icon': '💰'
            },
            'calorie': {
                'title': 'Daily Calorie Needs',
                'main_value': f"{result.get('maintain', 0)}",
                'subtitle': 'Maintenance Calories',
                'details': [
                    f"BMR: {result.get('bmr', 0)} cal",
                    f"Activity: {inputs.get('activity', 'moderate').title()}"
                ],
                'color_scheme': '#2ecc71',
                'icon': '🔥'
            },
            'attendance': {
                'title': 'My Attendance',
                'main_value': f"{result.get('current_percentage', 0):.1f}%",
                'subtitle': 'Current Status',
                'details': [
                    f"Attended: {inputs.get('attended', 0)}",
                    f"Total: {inputs.get('total', 0)}",
                    f"Status: {result.get('status', 'N/A')}"
                ],
                'color_scheme': '#e74c3c',
                'icon': '📊'
            },
            'percentage': {
                'title': 'My Score',
                'main_value': f"{result.get('percentage', 0):.1f}%",
                'subtitle': 'Academic Performance',
                'details': [
                    f"Subjects: {len(inputs.get('marks', []))}",
                    f"Grade: {result.get('grade', 'N/A')}"
                ],
                'color_scheme': '#f39c12',
                'icon': '📝'
            },
            'compound_interest': {
                'title': 'Investment Growth',
                'main_value': f"${result.get('amount', 0):,.2f}",
                'subtitle': 'Future Value',
                'details': [
                    f"Principal: ${inputs.get('principal', 0):,.2f}",
                    f"Interest: ${result.get('interest', 0):,.2f}",
                    f"Duration: {inputs.get('time', 0)} years"
                ],
                'color_scheme': '#1abc9c',
                'icon': '📈'
            }
        }
        
        default_card = {
            'title': calculator_type.replace('_', ' ').title(),
            'main_value': 'Result',
            'subtitle': 'Calculator Result',
            'details': [],
            'color_scheme': '#34495e',
            'icon': '🧮'
        }
        
        return cards.get(calculator_type, default_card)
    
    def _get_bmi_color(self, category: str) -> str:
        """Get color based on BMI category"""
        colors = {
            'Underweight': '#3498db',
            'Normal': '#2ecc71',
            'Overweight': '#f39c12',
            'Obese': '#e74c3c'
        }
        return colors.get(category, '#95a5a6')
    
    def _get_gpa_label(self, gpa: float) -> str:
        """Get performance label based on GPA"""
        if gpa >= 3.7:
            return 'Outstanding'
        elif gpa >= 3.3:
            return 'Excellent'
        elif gpa >= 3.0:
            return 'Good'
        elif gpa >= 2.5:
            return 'Satisfactory'
        else:
            return 'Needs Improvement'
    
    def generate_all_share_links(self, calculator_type: str, result: Dict, 
                                 inputs: Dict) -> Dict:
        """Generate all social media share links"""
        return {
            'whatsapp': self.generate_whatsapp_link(calculator_type, result, inputs),
            'twitter': self.generate_twitter_link(calculator_type, result, inputs),
            'facebook': self.generate_facebook_link(calculator_type),
            'linkedin': self.generate_linkedin_link(calculator_type),
            'telegram': self.generate_telegram_link(calculator_type, result, inputs),
            'email': self.generate_email_link(calculator_type, result, inputs)
        }
    
    def generate_copy_text(self, calculator_type: str, result: Dict, 
                          inputs: Dict) -> str:
        """Generate formatted text for copying"""
        text = self.generate_share_text(calculator_type, result, inputs)
        text += f"\n\n📱 Calculate yours at: {self.base_url}/{calculator_type.replace('_', '-')}"
        text += "\n\n#Calculator #Health #Fitness #Education"
        return text
