# api_service.py
# API service layer for DeckMaster

import json
from typing import Dict, Optional, List
from config import SUBSCRIPTION_PLANS
from design_styles import list_available_designs

class APIService:
    """Service layer for handling API operations"""
    
    def __init__(self, base_url: str = "http://localhost:5000/api"):
        self.base_url = base_url
    
    def get_available_plans(self) -> Dict:
        """Get all available subscription plans"""
        return {'success': True, 'plans': SUBSCRIPTION_PLANS}
    
    def get_available_designs(self) -> Dict:
        """Get all available design styles"""
        try:
            return {
                'success': True,
                'designs': list_available_designs(),
                'total_count': len(list_available_designs())
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Global API service instance
api_service = APIService()