# user_manager.py
# User management and subscription handling

import threading
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from config import SUBSCRIPTION_PLANS

class UserManager:
    """Manages user data, subscriptions, and usage limits"""
    
    def __init__(self):
        self.users_db = {}
        self.user_lock = threading.Lock()
        self.admin_sessions = {}  # Store admin sessions with timestamps
        self.admin_lock = threading.Lock()
    
    def activate_admin_mode(self, password: str, user_id: str) -> Tuple[bool, str]:
        """Activate admin mode with password verification"""
        from config import ADMIN_PASSWORD, ADMIN_SESSION_TIMEOUT
        
        if password == ADMIN_PASSWORD:
            with self.admin_lock:
                # Create admin session
                session_id = str(uuid.uuid4())
                self.admin_sessions[user_id] = {
                    'session_id': session_id,
                    'activated_at': time.time(),
                    'expires_at': time.time() + ADMIN_SESSION_TIMEOUT
                }
                
                print(f"🔧 ADMIN MODE ACTIVATED for user: {user_id}")
                return True, f"Admin mode activated successfully! Session expires in {ADMIN_SESSION_TIMEOUT//60} minutes."
        else:
            print(f"⚠️ FAILED ADMIN LOGIN ATTEMPT from user: {user_id}")
            return False, "Invalid admin password"
    
    def is_admin_user(self, user_id: str) -> bool:
        """Check if user has active admin session"""
        with self.admin_lock:
            if user_id in self.admin_sessions:
                session = self.admin_sessions[user_id]
                if time.time() < session['expires_at']:
                    return True
                else:
                    # Session expired, remove it
                    del self.admin_sessions[user_id]
                    print(f"🔧 Admin session expired for user: {user_id}")
            return False
    
    def deactivate_admin_mode(self, user_id: str) -> bool:
        """Deactivate admin mode for user"""
        with self.admin_lock:
            if user_id in self.admin_sessions:
                del self.admin_sessions[user_id]
                print(f"🔧 ADMIN MODE DEACTIVATED for user: {user_id}")
                return True
            return False
    
    def get_admin_status(self, user_id: str) -> Dict:
        """Get admin status for user"""
        is_admin = self.is_admin_user(user_id)
        if is_admin:
            session = self.admin_sessions.get(user_id, {})
            expires_at = session.get('expires_at', 0)
            time_remaining = max(0, int(expires_at - time.time()))
            return {
                'is_admin': True,
                'time_remaining': time_remaining,
                'expires_at': expires_at
            }
        else:
            return {'is_admin': False}
    
    def get_user_data(self, user_id: str) -> Dict:
        """Get user data with thread safety and daily reset"""
        with self.user_lock:
            if user_id not in self.users_db:
                self.users_db[user_id] = {
                    'user_id': user_id,
                    'plan': 'free',
                    'daily_usage': 0,
                    'total_usage': 0,
                    'last_reset_date': datetime.now().date().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'last_activity': datetime.now().isoformat()
                }
            
            user = self.users_db[user_id]
            
            # Reset daily usage if it's a new day
            today = datetime.now().date().isoformat()
            if user['last_reset_date'] != today:
                user['daily_usage'] = 0
                user['last_reset_date'] = today
            
            # Update last activity
            user['last_activity'] = datetime.now().isoformat()
            
            return user
    
    def update_user_data(self, user_id: str, updates: Dict) -> Optional[Dict]:
        """Update user data with thread safety"""
        with self.user_lock:
            if user_id in self.users_db:
                self.users_db[user_id].update(updates)
                self.users_db[user_id]['last_activity'] = datetime.now().isoformat()
                return self.users_db[user_id]
            return None
    
    def can_generate_ppt(self, user_id: str) -> Dict:
        """Check if user can generate PPT based on their plan limits"""
        # Check if user is admin first
        if self.is_admin_user(user_id):
            return {
                'can_generate': True,
                'reason': 'Admin mode - unlimited access',
                'remaining_daily': 999999,
                'remaining_total': None
            }
        
        user = self.get_user_data(user_id)
        plan = SUBSCRIPTION_PLANS[user['plan']]
        
        # Check total limit for free plan (lifetime limit)
        if plan['total_limit'] and user['total_usage'] >= plan['total_limit']:
            return {
                'can_generate': False,
                'reason': f'You have reached the lifetime limit of {plan["total_limit"]} presentations for the Free plan. Please upgrade to continue.',
                'limit_type': 'total',
                'usage': user['total_usage'],
                'limit': plan['total_limit']
            }
        
        # Check daily limit
        if user['daily_usage'] >= plan['daily_limit']:
            return {
                'can_generate': False,
                'reason': f'Daily limit of {plan["daily_limit"]} presentations reached. Try again tomorrow or upgrade your plan.',
                'limit_type': 'daily',
                'usage': user['daily_usage'],
                'limit': plan['daily_limit']
            }
        
        return {
            'can_generate': True,
            'remaining_daily': plan['daily_limit'] - user['daily_usage'],
            'remaining_total': plan['total_limit'] - user['total_usage'] if plan['total_limit'] else None
        }
    
    def increment_usage(self, user_id: str) -> Dict:
        """Increment user's PPT generation usage"""
        user = self.get_user_data(user_id)
        updates = {
            'daily_usage': user['daily_usage'] + 1,
            'total_usage': user['total_usage'] + 1
        }
        return self.update_user_data(user_id, updates)
    
    def update_plan(self, user_id: str, new_plan: str) -> Tuple[bool, str, Optional[Dict]]:
        """Update user's subscription plan (with simple admin mode for testing)"""
        if new_plan not in SUBSCRIPTION_PLANS:
            return False, 'Invalid plan selected', None
        
        # Import here to avoid circular import
        from config import ADMIN_MODE
        
        user = self.get_user_data(user_id)
        old_plan = user['plan']
        
        # Check if admin mode is enabled (simple testing mode)
        if ADMIN_MODE:
            # Admin mode enabled - all users can upgrade for free (testing)
            updates = {'plan': new_plan}
            if new_plan != 'free':
                updates['daily_usage'] = 0  # Reset usage when upgrading
            
            updated_user = self.update_user_data(user_id, updates)
            
            plan_info = SUBSCRIPTION_PLANS[new_plan]
            message = f'[ADMIN MODE] Successfully upgraded from {SUBSCRIPTION_PLANS[old_plan]["name"]} to {plan_info["name"]} plan (FREE for testing)'
            
            return True, message, updated_user
        else:
            # Regular users would need payment integration here
            if new_plan == 'free':
                # Downgrade to free is always allowed
                updates = {'plan': new_plan}
                updated_user = self.update_user_data(user_id, updates)
                
                plan_info = SUBSCRIPTION_PLANS[new_plan]
                message = f'Successfully downgraded to {plan_info["name"]} plan'
                
                return True, message, updated_user
            else:
                # Paid plans require payment (not implemented yet)
                return False, 'Payment integration required for paid plans. Contact admin for upgrade.', None
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Get comprehensive user statistics"""
        user = self.get_user_data(user_id)
        plan = SUBSCRIPTION_PLANS[user['plan']]
        can_generate = self.can_generate_ppt(user_id)
        
        # Check if user is admin and override plan limits
        is_admin = self.is_admin_user(user_id)
        if is_admin:
            # Create admin plan with unlimited features
            admin_plan = {
                'name': 'Admin',
                'daily_limit': 999999,  # Unlimited
                'total_limit': None,    # No limit
                'max_slides': 50,       # Admin max slides
                'has_ads': False,
                'visual_elements': True,
                'price': 0,
                'description': 'Admin mode with unlimited access'
            }
            plan = admin_plan
            
            # Override can_generate for admin
            can_generate = {
                'can_generate': True,
                'reason': 'Admin mode - unlimited access',
                'limit_type': None
            }
        
        return {
            'user': user,
            'plan': plan,
            'can_generate': can_generate,
            'is_admin': is_admin,
            'usage_stats': {
                'daily_usage': user['daily_usage'],
                'daily_limit': plan['daily_limit'],
                'daily_remaining': plan['daily_limit'] - user['daily_usage'] if plan['daily_limit'] != 999999 else 999999,
                'total_usage': user['total_usage'],
                'total_limit': plan['total_limit'],
                'total_remaining': plan['total_limit'] - user['total_usage'] if plan['total_limit'] else None
            }
        }
    
    def get_all_users_stats(self) -> Dict:
        """Get statistics for all users"""
        with self.user_lock:
            total_users = len(self.users_db)
            plan_distribution = {}
            total_presentations = 0
            
            for user in self.users_db.values():
                plan = user['plan']
                plan_distribution[plan] = plan_distribution.get(plan, 0) + 1
                total_presentations += user['total_usage']
            
            return {
                'total_users': total_users,
                'plan_distribution': plan_distribution,
                'total_presentations_generated': total_presentations,
                'active_users_today': len([u for u in self.users_db.values() 
                                         if u['last_reset_date'] == datetime.now().date().isoformat() 
                                         and u['daily_usage'] > 0])
            }
    
    def cleanup_inactive_users(self, days_inactive: int = 30):
        """Remove users inactive for specified days (for memory management)"""
        cutoff_date = datetime.now() - timedelta(days=days_inactive)
        
        with self.user_lock:
            inactive_users = []
            for user_id, user_data in self.users_db.items():
                last_activity = datetime.fromisoformat(user_data['last_activity'])
                if last_activity < cutoff_date:
                    inactive_users.append(user_id)
            
            for user_id in inactive_users:
                del self.users_db[user_id]
            
            return len(inactive_users)

# Global user manager instance
user_manager = UserManager()