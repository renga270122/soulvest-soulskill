"""
Payment Handler for SoulSkill Resume Builder
Razorpay Integration with Subscription Management
"""
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import json
import uuid

try:
    import razorpay
    RAZORPAY_AVAILABLE = True
except Exception:
    razorpay = None
    RAZORPAY_AVAILABLE = False

# Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_YOUR_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'YOUR_KEY_SECRET')

# Pricing Plans (in paise - 1 INR = 100 paise)
PRICING_PLANS = {
    'free': {
        'name': 'Free',
        'price_monthly': 0,
        'price_yearly': 0,
        'features': [
            '✅ 3 Basic Templates',
            '✅ 1 Resume Download/Month',
            '✅ Basic ATS Scoring',
            '✅ Standard Export (PDF)',
            '❌ Premium Templates',
            '❌ AI Suggestions',
            '❌ Unlimited Downloads',
            '❌ Priority Support'
        ],
        'limits': {
            'templates': 3,
            'downloads_per_month': 1,
            'resumes': 2,
            'ai_suggestions': 0,
            'advanced_ats': False,
            'premium_templates': False,
            'version_control': False
        }
    },
    'premium_monthly': {
        'name': 'Premium Monthly',
        'price_monthly': 19900,  # ₹199
        'price_yearly': 0,
        'currency': 'INR',
        'features': [
            '✅ 20+ Premium Templates',
            '✅ Unlimited Downloads',
            '✅ AI-Powered Suggestions',
            '✅ Advanced ATS Optimization',
            '✅ Multiple Export Formats',
            '✅ Resume Version Control',
            '✅ Priority Email Support',
            '✅ 7-Day Free Trial'
        ],
        'limits': {
            'templates': 'unlimited',
            'downloads_per_month': 'unlimited',
            'resumes': 'unlimited',
            'ai_suggestions': 'unlimited',
            'advanced_ats': True,
            'premium_templates': True,
            'version_control': True
        },
        'trial_days': 7
    },
    'premium_yearly': {
        'name': 'Premium Yearly',
        'price_monthly': 0,
        'price_yearly': 99900,  # ₹999
        'currency': 'INR',
        'save_percentage': 58,  # Save 58% compared to monthly
        'features': [
            '✅ All Premium Monthly Features',
            '✅ Save ₹1,389/year (58% off)',
            '✅ Priority Support',
            '✅ Early Access to New Features',
            '✅ Resume Analytics Dashboard',
            '✅ Career Resources Library',
            '✅ Job Application Tracker',
            '✅ Interview Preparation Tools'
        ],
        'limits': {
            'templates': 'unlimited',
            'downloads_per_month': 'unlimited',
            'resumes': 'unlimited',
            'ai_suggestions': 'unlimited',
            'advanced_ats': True,
            'premium_templates': True,
            'version_control': True,
            'analytics': True,
            'job_tracker': True
        },
        'trial_days': 7
    }
}


class PaymentHandler:
    """Handle Razorpay payment processing and subscription management"""
    
    def __init__(self):
        """Initialize Razorpay client"""
        self.client = None
        if RAZORPAY_AVAILABLE:
            self.client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    
    def create_order(self, amount: int, currency: str = 'INR', 
                     receipt: str = None, notes: Dict = None) -> Dict:
        """
        Create a Razorpay order
        
        Args:
            amount: Amount in paise (₹1 = 100 paise)
            currency: Currency code (default: INR)
            receipt: Receipt ID for reference
            notes: Additional notes/metadata
            
        Returns:
            Order details including order_id
        """
        if not self.client:
            return {
                'success': False,
                'error': 'Razorpay SDK unavailable in this environment'
            }

        try:
            order_data = {
                'amount': amount,
                'currency': currency,
                'receipt': receipt or f'receipt_{datetime.now().timestamp()}',
                'notes': notes or {}
            }
            order = self.client.order.create(data=order_data)
            return {
                'success': True,
                'order_id': order['id'],
                'amount': order['amount'],
                'currency': order['currency']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_payment(self, razorpay_order_id: str, razorpay_payment_id: str, 
                       razorpay_signature: str) -> bool:
        """
        Verify payment signature from Razorpay
        
        Args:
            razorpay_order_id: Order ID from Razorpay
            razorpay_payment_id: Payment ID from Razorpay
            razorpay_signature: Payment signature for verification
            
        Returns:
            True if verification successful
        """
        if not self.client:
            return False

        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            self.client.utility.verify_payment_signature(params_dict)
            return True
        except Exception:
            return False
    
    def create_subscription(self, plan_id: str, user_email: str, 
                           total_count: int = 12) -> Dict:
        """
        Create a subscription plan
        
        Args:
            plan_id: 'premium_monthly' or 'premium_yearly'
            user_email: User's email
            total_count: Number of billing cycles
            
        Returns:
            Subscription details
        """
        plan = PRICING_PLANS.get(plan_id)
        if not plan:
            return {'success': False, 'error': 'Invalid plan'}

        if not self.client:
            return {'success': False, 'error': 'Razorpay SDK unavailable in this environment'}
        
        try:
            # For monthly subscription
            if plan_id == 'premium_monthly':
                subscription_data = {
                    'plan_id': plan_id,
                    'customer_notify': 1,
                    'total_count': total_count,
                    'notes': {
                        'user_email': user_email,
                        'plan_name': plan['name']
                    }
                }
            # For yearly subscription (one-time payment, manual renewal)
            else:
                # Create one-time order for yearly plan
                return self.create_order(
                    amount=plan['price_yearly'],
                    notes={
                        'user_email': user_email,
                        'plan_name': plan['name'],
                        'plan_duration': 'yearly'
                    }
                )
            
            subscription = self.client.subscription.create(data=subscription_data)
            return {
                'success': True,
                'subscription_id': subscription['id'],
                'status': subscription['status']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


class SubscriptionManager:
    """Manage user subscriptions and feature access"""
    
    def __init__(self, db_manager):
        """Initialize with database manager"""
        self.db = db_manager
    
    def get_user_subscription(self, user_email: str) -> Dict:
        """
        Get user's current subscription details
        
        Returns:
            Subscription info including plan, status, trial info, limits
        """
        # Get from database (you'll need to add subscription fields)
        user_data = self._get_user_data(user_email)
        
        if not user_data:
            return {
                'plan': 'free',
                'status': 'active',
                'is_trial': False,
                'has_used_trial': False,
                'trial_ends_at': None,
                'subscription_ends_at': None,
                'features': PRICING_PLANS['free']['limits']
            }
        
        return {
            'plan': user_data.get('subscription_plan', 'free'),
            'status': user_data.get('subscription_status', 'active'),
            'is_trial': user_data.get('is_trial', False),
            'has_used_trial': user_data.get('has_used_trial', False),
            'trial_ends_at': user_data.get('trial_ends_at'),
            'subscription_ends_at': user_data.get('subscription_ends_at'),
            'features': PRICING_PLANS[user_data.get('subscription_plan', 'free')]['limits']
        }
    
    def start_trial(self, user_email: str, plan_id: str = 'premium_monthly') -> bool:
        """
        Start a 7-day free trial for user
        
        Args:
            user_email: User's email
            plan_id: Premium plan to trial
            
        Returns:
            True if trial started successfully
        """
        user_sub = self.get_user_subscription(user_email)
        
        # Check if user already had a trial
        if user_sub.get('has_used_trial', False):
            return False
        
        trial_end = datetime.now() + timedelta(days=7)
        
        self._update_user_subscription(user_email, {
            'subscription_plan': plan_id,
            'subscription_status': 'trial',
            'is_trial': True,
            'trial_ends_at': trial_end.isoformat(),
            'has_used_trial': True
        })
        
        return True
    
    def activate_subscription(self, user_email: str, plan_id: str, 
                            payment_id: str, duration_months: int = 1) -> bool:
        """
        Activate paid subscription after successful payment
        
        Args:
            user_email: User's email
            plan_id: Selected plan
            payment_id: Razorpay payment ID
            duration_months: Subscription duration (1 or 12)
            
        Returns:
            True if activation successful
        """
        subscription_end = datetime.now() + timedelta(days=30 * duration_months)
        
        self._update_user_subscription(user_email, {
            'subscription_plan': plan_id,
            'subscription_status': 'active',
            'is_trial': False,
            'trial_ends_at': None,
            'subscription_ends_at': subscription_end.isoformat(),
            'payment_id': payment_id,
            'last_payment_date': datetime.now().isoformat()
        })
        
        return True
    
    def check_feature_access(self, user_email: str, feature: str) -> Tuple[bool, str]:
        """
        Check if user has access to a specific feature
        
        Args:
            user_email: User's email
            feature: Feature name (e.g., 'premium_templates', 'ai_suggestions')
            
        Returns:
            Tuple of (has_access: bool, message: str)
        """
        subscription = self.get_user_subscription(user_email)

        if subscription['status'] not in ('active', 'trial'):
            return False, "Your subscription is not active. Please renew or choose a plan."
        
        # Check if subscription is active or in trial
        if subscription['status'] == 'trial':
            trial_end = datetime.fromisoformat(subscription['trial_ends_at'])
            if datetime.now() > trial_end:
                # Trial expired
                self._update_user_subscription(user_email, {
                    'subscription_status': 'expired',
                    'is_trial': False
                })
                return False, "Your trial has expired. Please upgrade to continue."
        
        if subscription['status'] == 'active':
            subscription_end = subscription.get('subscription_ends_at')
            if subscription_end:
                end_date = datetime.fromisoformat(subscription_end)
                if datetime.now() > end_date:
                    # Subscription expired
                    self._update_user_subscription(user_email, {
                        'subscription_status': 'expired'
                    })
                    return False, "Your subscription has expired. Please renew."
        
        # Check feature access
        features = subscription['features']
        has_access = features.get(feature, False)
        
        if has_access:
            return True, "Access granted"
        else:
            if subscription['plan'] == 'free':
                return False, "This feature is only available in Premium plans. Upgrade now!"
            else:
                return False, "Feature not available in your current plan."
    
    def increment_usage(self, user_email: str, usage_type: str) -> Tuple[bool, int]:
        """
        Track and increment usage (e.g., downloads)
        
        Args:
            user_email: User's email
            usage_type: Type of usage (e.g., 'downloads', 'ai_suggestions')
            
        Returns:
            Tuple of (within_limit: bool, remaining: int)
        """
        subscription = self.get_user_subscription(user_email)
        features = subscription['features']
        
        limit = features.get(f'{usage_type}_per_month')
        if limit == 'unlimited':
            return True, -1  # -1 means unlimited
        if limit is None:
            return False, 0
        
        # Get current usage from database
        current_usage = self._get_usage_count(user_email, usage_type)
        
        if current_usage >= limit:
            return False, 0
        
        # Increment usage
        self._increment_usage_count(user_email, usage_type)
        remaining = limit - current_usage - 1
        
        return True, remaining
    
    def _get_user_data(self, user_email: str) -> Optional[Dict]:
        """Get user data from database"""
        db_type = getattr(self.db, 'db_type', 'json')

        if db_type == 'postgres':
            try:
                cursor = self.db.connection.cursor()
                cursor.execute(
                    """SELECT email, subscription_plan, subscription_status, is_trial, has_used_trial,
                              trial_ends_at, subscription_ends_at, payment_id, last_payment_date,
                              downloads_this_month
                       FROM users WHERE email = %s""",
                    (user_email,)
                )
                row = cursor.fetchone()
                cursor.close()
                if not row:
                    return None
                return {
                    'email': row[0],
                    'subscription_plan': row[1],
                    'subscription_status': row[2],
                    'is_trial': row[3],
                    'has_used_trial': row[4],
                    'trial_ends_at': row[5].isoformat() if row[5] else None,
                    'subscription_ends_at': row[6].isoformat() if row[6] else None,
                    'payment_id': row[7],
                    'last_payment_date': row[8].isoformat() if row[8] else None,
                    'downloads_this_month': row[9] or 0,
                }
            except Exception:
                return None

        if db_type == 'mongodb':
            try:
                return self.db.users.find_one({'email': user_email})
            except Exception:
                return None

        try:
            with open(self.db.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for user in data.get('users', []):
                if user.get('email') == user_email:
                    return user
        except Exception:
            return None
        return None
    
    def _update_user_subscription(self, user_email: str, data: Dict):
        """Update user subscription data in database"""
        db_type = getattr(self.db, 'db_type', 'json')

        if db_type == 'postgres':
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
            existing = cursor.fetchone()
            if not existing:
                cursor.execute(
                    "INSERT INTO users (email, name) VALUES (%s, %s)",
                    (user_email, user_email.split('@')[0])
                )
            set_parts = []
            values = []
            for key, value in data.items():
                set_parts.append(f"{key} = %s")
                if key in ('trial_ends_at', 'subscription_ends_at', 'last_payment_date') and value:
                    values.append(datetime.fromisoformat(value))
                else:
                    values.append(value)
            values.append(user_email)
            cursor.execute(
                f"UPDATE users SET {', '.join(set_parts)} WHERE email = %s",
                tuple(values),
            )
            self.db.connection.commit()
            cursor.close()
            return

        if db_type == 'mongodb':
            self.db.users.update_one(
                {'email': user_email},
                {'$set': {'email': user_email, **data}},
                upsert=True,
            )
            return

        with open(self.db.json_file, 'r', encoding='utf-8') as f:
            db_data = json.load(f)

        users = db_data.setdefault('users', [])
        target_user = None
        for user in users:
            if user.get('email') == user_email:
                target_user = user
                break

        if target_user is None:
            target_user = {
                'id': str(uuid.uuid4()),
                'email': user_email,
                'name': user_email.split('@')[0],
                'created_at': datetime.now().isoformat(),
            }
            users.append(target_user)

        target_user.update(data)
        target_user['updated_at'] = datetime.now().isoformat()

        with open(self.db.json_file, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, indent=2)
    
    def _get_usage_count(self, user_email: str, usage_type: str) -> int:
        """Get current usage count for the month"""
        user_data = self._get_user_data(user_email) or {}
        key = f"{usage_type}_this_month"
        return int(user_data.get(key, 0) or 0)
    
    def _increment_usage_count(self, user_email: str, usage_type: str):
        """Increment usage count"""
        current = self._get_usage_count(user_email, usage_type)
        key = f"{usage_type}_this_month"
        self._update_user_subscription(user_email, {key: current + 1})


def get_plan_price_display(plan_id: str) -> str:
    """Get formatted price display for a plan"""
    plan = PRICING_PLANS.get(plan_id)
    if not plan:
        return "Free"
    
    if plan_id == 'free':
        return "₹0"
    elif plan_id == 'premium_monthly':
        return "₹199/month"
    elif plan_id == 'premium_yearly':
        return "₹999/year"
    return ""


def get_plan_features(plan_id: str) -> list:
    """Get list of features for a plan"""
    plan = PRICING_PLANS.get(plan_id, PRICING_PLANS['free'])
    return plan['features']
