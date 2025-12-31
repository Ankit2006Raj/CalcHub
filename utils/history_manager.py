"""
History Manager for Calculator Application
Handles saving, retrieving, and managing calculation history
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class HistoryManager:
    """Manages calculation history with local storage"""
    
    def __init__(self, storage_dir='data'):
        """Initialize history manager"""
        self.storage_dir = storage_dir
        self.history_file = os.path.join(storage_dir, 'calculation_history.json')
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage directory if it doesn't exist"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)
    
    def save_calculation(self, user_id: str, calculator_type: str, 
                        inputs: Dict, results: Dict) -> Dict:
        """Save a calculation to history"""
        history = self._load_history()
        
        entry = {
            'id': self._generate_id(),
            'user_id': user_id,
            'calculator_type': calculator_type,
            'inputs': inputs,
            'results': results,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S')
        }
        
        history.append(entry)
        self._save_history(history)
        
        return {'success': True, 'entry_id': entry['id']}
    
    def get_user_history(self, user_id: str, calculator_type: str = None, 
                        limit: int = None) -> List[Dict]:
        """Get calculation history for a user"""
        history = self._load_history()
        
        # Filter by user
        user_history = [h for h in history if h['user_id'] == user_id]
        
        # Filter by calculator type if specified
        if calculator_type:
            user_history = [h for h in user_history if h['calculator_type'] == calculator_type]
        
        # Sort by timestamp (newest first)
        user_history.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Limit results if specified
        if limit:
            user_history = user_history[:limit]
        
        return user_history
    
    def get_monthly_summary(self, user_id: str, year: int = None, 
                           month: int = None) -> Dict:
        """Get monthly summary of calculations"""
        if not year:
            year = datetime.now().year
        if not month:
            month = datetime.now().month
        
        history = self.get_user_history(user_id)
        
        # Filter by month
        month_history = []
        for entry in history:
            entry_date = datetime.fromisoformat(entry['timestamp'])
            if entry_date.year == year and entry_date.month == month:
                month_history.append(entry)
        
        # Calculate statistics
        summary = {
            'year': year,
            'month': month,
            'total_calculations': len(month_history),
            'by_calculator': {},
            'most_used': None,
            'calculations': month_history
        }
        
        # Count by calculator type
        for entry in month_history:
            calc_type = entry['calculator_type']
            summary['by_calculator'][calc_type] = summary['by_calculator'].get(calc_type, 0) + 1
        
        # Find most used calculator
        if summary['by_calculator']:
            summary['most_used'] = max(summary['by_calculator'].items(), 
                                      key=lambda x: x[1])[0]
        
        return summary
    
    def get_analytics_data(self, user_id: str, calculator_type: str) -> Dict:
        """Get analytics data for charts and trends"""
        history = self.get_user_history(user_id, calculator_type)
        
        analytics = {
            'calculator_type': calculator_type,
            'total_entries': len(history),
            'date_range': self._get_date_range(history),
            'trends': self._calculate_trends(history, calculator_type),
            'statistics': self._calculate_statistics(history, calculator_type)
        }
        
        return analytics
    
    def _calculate_trends(self, history: List[Dict], calculator_type: str) -> List[Dict]:
        """Calculate trends for visualization"""
        trends = []
        
        if calculator_type == 'bmi':
            for entry in history:
                trends.append({
                    'date': entry['date'],
                    'value': entry['results'].get('bmi', 0),
                    'category': entry['results'].get('category', 'Unknown')
                })
        
        elif calculator_type == 'calorie':
            for entry in history:
                trends.append({
                    'date': entry['date'],
                    'bmr': entry['results'].get('bmr', 0),
                    'maintain': entry['results'].get('maintain', 0),
                    'activity': entry['inputs'].get('activity', 'unknown')
                })
        
        elif calculator_type == 'loan':
            for entry in history:
                trends.append({
                    'date': entry['date'],
                    'emi': entry['results'].get('emi', 0),
                    'total_interest': entry['results'].get('total_interest', 0),
                    'amount': entry['inputs'].get('amount', 0)
                })
        
        elif calculator_type == 'gpa':
            for entry in history:
                trends.append({
                    'date': entry['date'],
                    'gpa': entry['results'].get('gpa', 0),
                    'courses': len(entry['inputs'].get('courses', []))
                })
        
        elif calculator_type == 'attendance':
            for entry in history:
                trends.append({
                    'date': entry['date'],
                    'percentage': entry['results'].get('current_percentage', 0),
                    'attended': entry['inputs'].get('attended', 0),
                    'total': entry['inputs'].get('total', 0)
                })
        
        return trends
    
    def _calculate_statistics(self, history: List[Dict], calculator_type: str) -> Dict:
        """Calculate statistical insights"""
        if not history:
            return {}
        
        stats = {}
        
        if calculator_type == 'bmi':
            bmis = [h['results'].get('bmi', 0) for h in history]
            stats = {
                'average_bmi': round(sum(bmis) / len(bmis), 2),
                'lowest_bmi': min(bmis),
                'highest_bmi': max(bmis),
                'change': round(bmis[0] - bmis[-1], 2) if len(bmis) > 1 else 0
            }
        
        elif calculator_type == 'gpa':
            gpas = [h['results'].get('gpa', 0) for h in history]
            stats = {
                'average_gpa': round(sum(gpas) / len(gpas), 2),
                'lowest_gpa': min(gpas),
                'highest_gpa': max(gpas),
                'improvement': round(gpas[0] - gpas[-1], 2) if len(gpas) > 1 else 0
            }
        
        elif calculator_type == 'attendance':
            percentages = [h['results'].get('current_percentage', 0) for h in history]
            stats = {
                'average_attendance': round(sum(percentages) / len(percentages), 2),
                'lowest_attendance': min(percentages),
                'highest_attendance': max(percentages),
                'improvement': round(percentages[0] - percentages[-1], 2) if len(percentages) > 1 else 0
            }
        
        return stats
    
    def _get_date_range(self, history: List[Dict]) -> Dict:
        """Get date range of history"""
        if not history:
            return {'start': None, 'end': None}
        
        dates = [datetime.fromisoformat(h['timestamp']) for h in history]
        return {
            'start': min(dates).strftime('%Y-%m-%d'),
            'end': max(dates).strftime('%Y-%m-%d')
        }
    
    def delete_entry(self, user_id: str, entry_id: str) -> Dict:
        """Delete a specific history entry"""
        history = self._load_history()
        
        # Find and remove entry
        original_length = len(history)
        history = [h for h in history if not (h['id'] == entry_id and h['user_id'] == user_id)]
        
        if len(history) < original_length:
            self._save_history(history)
            return {'success': True, 'message': 'Entry deleted'}
        
        return {'success': False, 'message': 'Entry not found'}
    
    def clear_history(self, user_id: str, calculator_type: str = None) -> Dict:
        """Clear all history for a user"""
        history = self._load_history()
        
        if calculator_type:
            # Clear only specific calculator type
            history = [h for h in history if not (h['user_id'] == user_id and 
                                                  h['calculator_type'] == calculator_type)]
        else:
            # Clear all history for user
            history = [h for h in history if h['user_id'] != user_id]
        
        self._save_history(history)
        return {'success': True, 'message': 'History cleared'}
    
    def _load_history(self) -> List[Dict]:
        """Load history from file"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _save_history(self, history: List[Dict]):
        """Save history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def _generate_id(self) -> str:
        """Generate unique ID for entry"""
        return f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
