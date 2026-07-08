"""
Pricing Page UI for SoulSkill Resume Builder
Beautiful pricing comparison with Indian market focus
"""
import os

import requests
import streamlit as st
import streamlit.components.v1 as components
from payment_handler import (
    PRICING_PLANS,
    PaymentHandler,
    SubscriptionManager,
    get_plan_price_display,
    get_plan_features,
)
from database import get_db_manager


def _get_api_base_url() -> str:
    return os.getenv("SOULSKILL_API_BASE_URL", "").rstrip("/")


def _api_headers() -> dict:
    token = st.session_state.get("api_token") or os.getenv("SOULSKILL_API_TOKEN", "")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _create_order_via_api(plan_id: str, user_email: str):
    base_url = _get_api_base_url()
    if not base_url:
        return None

    payload = {"plan_id": plan_id, "user_email": user_email}
    try:
        response = requests.post(
            f"{base_url}/api/payments/order",
            json=payload,
            headers=_api_headers(),
            timeout=12,
        )
        if response.ok:
            data = response.json()
            order = data.get("order", {})
            return {
                "success": True,
                "order_id": order.get("order_id"),
                "amount": order.get("amount"),
                "currency": order.get("currency", "INR"),
                "provider": "api",
            }
        detail = response.text or "Payment API returned an unexpected response"
        return {"success": False, "error": detail, "provider": "api"}
    except requests.RequestException as exc:
        return {"success": False, "error": f"Payment API unreachable: {exc}", "provider": "api"}


def _verify_payment_via_api(plan_id: str, user_email: str, order_id: str, payment_id: str, signature: str):
    base_url = _get_api_base_url()
    if not base_url:
        return None

    payload = {
        "plan_id": plan_id,
        "user_email": user_email,
        "razorpay_order_id": order_id,
        "razorpay_payment_id": payment_id,
        "razorpay_signature": signature,
    }
    try:
        response = requests.post(
            f"{base_url}/api/payments/verify",
            json=payload,
            headers=_api_headers(),
            timeout=12,
        )
        if response.ok:
            return {"success": True, "provider": "api"}
        detail = response.text or "Payment verification failed"
        return {"success": False, "error": detail, "provider": "api"}
    except requests.RequestException as exc:
        return {"success": False, "error": f"Payment verification API unreachable: {exc}", "provider": "api"}


def render_pricing_page():
    """Render the pricing comparison page"""
    
    st.markdown("""
    <style>
        @media (max-width: 980px) {
            div[data-testid="stHorizontalBlock"] {
                flex-direction: column !important;
                gap: 0.85rem !important;
            }
            .pricing-card.featured {
                transform: none !important;
            }
        }
        @media (max-width: 640px) {
            .pricing-header h1 {
                font-size: 1.8rem !important;
            }
            .pricing-header p {
                font-size: 1rem !important;
            }
            .pricing-card {
                padding: 1.2rem !important;
            }
            .plan-price {
                font-size: 2rem !important;
            }
        }
        .pricing-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            margin-bottom: 3rem;
            color: white;
        }
        .pricing-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .pricing-header p {
            font-size: 1.2rem;
            opacity: 0.95;
        }
        .pricing-card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            border: 2px solid transparent;
        }
        .pricing-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        }
        .pricing-card.featured {
            border: 3px solid #667eea;
            transform: scale(1.05);
            background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        }
        .pricing-card.featured .badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        .plan-name {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }
        .plan-price {
            font-size: 2.5rem;
            font-weight: 800;
            color: #667eea;
            margin: 1rem 0;
        }
        .plan-price .period {
            font-size: 1rem;
            color: #718096;
            font-weight: 400;
        }
        .plan-savings {
            background: #48bb78;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.9rem;
            font-weight: 600;
            display: inline-block;
            margin-left: 0.5rem;
        }
        .feature-list {
            list-style: none;
            padding: 0;
            margin: 2rem 0;
        }
        .feature-list li {
            padding: 0.7rem 0;
            border-bottom: 1px solid #e2e8f0;
            font-size: 1rem;
            color: #4a5568;
        }
        .feature-list li:last-child {
            border-bottom: none;
        }
        .feature-list li.disabled {
            color: #cbd5e0;
            text-decoration: line-through;
        }
        .cta-button {
            width: 100%;
            padding: 1rem;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }
        .cta-button.primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .cta-button.primary:hover {
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            transform: translateY(-2px);
        }
        .cta-button.secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        .cta-button.secondary:hover {
            background: #f7fafc;
        }
        .testimonial-section {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            padding: 3rem;
            border-radius: 20px;
            margin: 3rem 0;
        }
        .testimonial {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin: 1rem 0;
        }
        .trust-badges {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }
        .trust-badge {
            background: white;
            padding: 1rem 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            font-weight: 600;
            color: #4a5568;
        }
        .faq-section {
            margin: 3rem 0;
        }
        .faq-item {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        .faq-question {
            font-size: 1.2rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }
        .faq-answer {
            color: #718096;
            line-height: 1.6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class='pricing-header'>
        <h1>🚀 Choose Your Plan</h1>
        <p>Start building professional resumes today. Trusted by 10,000+ Indian job seekers.</p>
        <p style='font-size: 1rem; margin-top: 1rem;'>💳 All major payment methods accepted: UPI, Cards, Net Banking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pricing Cards
    col1, col2, col3 = st.columns([1, 1, 1], gap="large")
    
    with col1:
        render_pricing_card('free', featured=False)
    
    with col2:
        render_pricing_card('premium_monthly', featured=True)
    
    with col3:
        render_pricing_card('premium_yearly', featured=False)
    
    # Trust Badges
    st.markdown("""
    <div class='trust-badges'>
        <div class='trust-badge'>🔒 100% Secure Payments</div>
        <div class='trust-badge'>💯 7-Day Money Back</div>
        <div class='trust-badge'>⚡ Instant Activation</div>
        <div class='trust-badge'>🇮🇳 Made for India</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Testimonials
    render_testimonials()
    
    # FAQ Section
    render_faq()
    
    # Final CTA
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; margin: 3rem 0; color: white;'>
        <h2>Ready to Land Your Dream Job?</h2>
        <p style='font-size: 1.2rem; margin: 1rem 0;'>Join thousands of successful job seekers who trust SoulSkill</p>
        <p style='font-size: 1rem; opacity: 0.9;'>✨ Start your 7-day free trial today • No credit card required</p>
    </div>
    """, unsafe_allow_html=True)


def render_pricing_card(plan_id: str, featured: bool = False):
    """Render individual pricing card"""
    plan = PRICING_PLANS[plan_id]
    
    card_class = "pricing-card featured" if featured else "pricing-card"
    
    # Build features HTML
    features_html = ""
    for feature in plan['features']:
        if feature.startswith('❌'):
            features_html += f"<li class='disabled'>{feature}</li>"
        else:
            features_html += f"<li>{feature}</li>"
    
    # Price display
    if plan_id == 'free':
        price_html = "<div class='plan-price'>₹0<span class='period'>/forever</span></div>"
        cta_class = "secondary"
        cta_text = "Start Free"
    elif plan_id == 'premium_monthly':
        price_html = "<div class='plan-price'>₹199<span class='period'>/month</span></div>"
        cta_class = "primary"
        cta_text = "Start 7-Day Free Trial"
    else:  # yearly
        savings = plan.get('save_percentage', 0)
        price_html = f"""
        <div class='plan-price'>
            ₹999<span class='period'>/year</span>
            <span class='plan-savings'>Save {savings}%</span>
        </div>
        <p style='color: #718096; font-size: 0.9rem;'>Just ₹83/month • Save ₹1,389</p>
        """
        cta_class = "primary"
        cta_text = "Start 7-Day Free Trial"
    
    html = f"""
    <div class='{card_class}'>
        {f"<div class='badge'>🏆 MOST POPULAR</div>" if featured else ""}
        <div class='plan-name'>{plan['name']}</div>
        {price_html}
        <ul class='feature-list'>
            {features_html}
        </ul>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
    
    # CTA Button
    button_key = f"cta_{plan_id}"
    if st.button(cta_text, key=button_key, use_container_width=True):
        if plan_id == 'free':
            st.session_state.mode = 'builder'
            st.rerun()
        else:
            st.session_state.selected_plan = plan_id
            st.session_state.mode = 'checkout'
            st.rerun()


def render_testimonials():
    """Render testimonial section"""
    st.markdown("""
    <div class='testimonial-section'>
        <h2 style='text-align: center; color: #2d3748; margin-bottom: 2rem;'>
            ❤️ Loved by Indian Job Seekers
        </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='testimonial'>
            <p>"Got my dream job at TCS! The ATS optimization really works. Worth every rupee!"</p>
            <p style='font-weight: 600; color: #667eea; margin-top: 1rem;'>- Priya Sharma, Software Engineer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='testimonial'>
            <p>"As a fresher, the AI suggestions helped me create a professional resume in minutes."</p>
            <p style='font-weight: 600; color: #667eea; margin-top: 1rem;'>- Rahul Verma, MBA Graduate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='testimonial'>
            <p>"Best investment for my career. Got 3x more interview calls after using premium templates!"</p>
            <p style='font-weight: 600; color: #667eea; margin-top: 1rem;'>- Anjali Patel, Marketing Manager</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_faq():
    """Render FAQ section"""
    st.markdown("""
    <div class='faq-section'>
        <h2 style='text-align: center; color: #2d3748; margin-bottom: 2rem;'>
            🤔 Frequently Asked Questions
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    faqs = [
        {
            "question": "How does the 7-day free trial work?",
            "answer": "You get full access to all Premium features for 7 days. No credit card required. You can cancel anytime during the trial with no charges."
        },
        {
            "question": "Which payment methods do you accept?",
            "answer": "We accept all major payment methods including UPI (PhonePe, Google Pay, Paytm), Credit/Debit Cards, and Net Banking through Razorpay's secure platform."
        },
        {
            "question": "Can I switch from monthly to yearly plan?",
            "answer": "Yes! You can upgrade to the yearly plan anytime. We'll prorate your monthly subscription and apply it to the yearly plan."
        },
        {
            "question": "Is my data secure?",
            "answer": "Absolutely! We use bank-grade encryption and never share your data. Your payment information is processed securely through Razorpay."
        },
        {
            "question": "What happens after my subscription ends?",
            "answer": "You can still access your resumes but won't be able to download or edit them. Premium features will be locked. Your data is safely stored."
        },
        {
            "question": "Do you offer student discounts?",
            "answer": "Yes! We offer special student pricing. Contact our support with your student ID for a discount code."
        }
    ]
    
    for faq in faqs:
        with st.expander(f"**{faq['question']}**"):
            st.write(faq['answer'])


def render_checkout_page(plan_id: str):
    """Render checkout page with Razorpay integration"""
    plan = PRICING_PLANS[plan_id]
    user_email = st.session_state.get('user_email')

    if not st.session_state.get('user_authenticated') or not user_email:
        st.warning("Please sign in to continue with checkout and manage your subscription.")
        if st.button("Sign In", use_container_width=True, key="checkout_sign_in"):
            st.session_state.show_auth_modal = True
            st.session_state.auth_mode = 'signin'
            st.session_state.mode = 'home'
            st.rerun()
        if st.button("Back to Pricing", use_container_width=True, key="checkout_back_pricing_unauth"):
            st.session_state.mode = 'pricing'
            st.rerun()
        return
    
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
        <h1>🎉 Complete Your Purchase</h1>
        <h2 style='color: #667eea;'>{plan['name']}</h2>
        <p style='font-size: 1.5rem; margin: 1rem 0;'>{get_plan_price_display(plan_id)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📦 What You'll Get")
        for feature in plan['features']:
            st.markdown(f"- {feature}")
    
    with col2:
        st.markdown("### 💳 Payment Details")
        st.info("🔒 Secure payment powered by Razorpay")

        accept_terms = st.checkbox(
            "I agree to billing terms and understand trial-to-paid conversion policy.",
            key="checkout_accept_terms",
        )

        db = get_db_manager()
        sub_manager = SubscriptionManager(db)
        payment_handler = PaymentHandler()

        trial_label = "🎁 Start 7-Day Free Trial"
        if st.button(trial_label, use_container_width=True, key="checkout_start_trial"):
            if not accept_terms:
                st.error("Please accept billing terms before starting your trial.")
            else:
                started = sub_manager.start_trial(user_email, plan_id)
                if started:
                    st.success("Trial activated successfully. Premium features are now available.")
                    st.session_state.active_plan = plan_id
                    st.session_state.mode = 'dashboard'
                    st.rerun()
                else:
                    st.info("Trial is already used on this account. You can continue with paid activation below.")

        if st.button("💰 Proceed to Payment", use_container_width=True, type="primary"):
            if not accept_terms:
                st.error("Please accept billing terms before proceeding.")
            else:
                amount = plan['price_monthly'] if plan_id == 'premium_monthly' else plan['price_yearly']
                api_order = _create_order_via_api(plan_id, user_email)
                if api_order is None:
                    order = payment_handler.create_order(
                        amount=amount,
                        notes={'plan': plan_id, 'user_email': user_email}
                    )
                elif api_order.get('success'):
                    order = api_order
                else:
                    st.warning("Backend payment API is currently unavailable. Continuing with local checkout fallback.")
                    order = payment_handler.create_order(
                        amount=amount,
                        notes={'plan': plan_id, 'user_email': user_email}
                    )

                if order.get('success'):
                    order_id = order.get('order_id') or f"local_{user_email}_{plan_id}"
                    mock_payment_id = f"mock_{order_id}"
                    mock_signature = f"sig_{order_id}"

                    api_verified = _verify_payment_via_api(
                        plan_id,
                        user_email,
                        order_id,
                        mock_payment_id,
                        mock_signature,
                    )

                    if api_verified is not None:
                        if api_verified.get('success'):
                            st.success("Payment initialized and verified via backend API.")
                        else:
                            st.warning("Payment initialized, but backend verification did not complete. Falling back to local activation for this environment.")
                            duration = 1 if plan_id == 'premium_monthly' else 12
                            sub_manager.activate_subscription(user_email, plan_id, mock_payment_id, duration_months=duration)
                    else:
                        duration = 1 if plan_id == 'premium_monthly' else 12
                        sub_manager.activate_subscription(user_email, plan_id, mock_payment_id, duration_months=duration)
                        st.success("Payment initialized and subscription activated for this environment.")

                    st.session_state.active_plan = plan_id
                    st.session_state.mode = 'dashboard'
                    st.rerun()
                else:
                    st.error(f"Unable to initialize payment: {order.get('error', 'Unknown error')}")

        if st.button("← Back to Pricing", use_container_width=True):
            st.session_state.mode = 'pricing'
            st.rerun()


def show_upgrade_prompt(feature_name: str = "premium feature"):
    """Show upgrade prompt when user tries to access premium feature"""
    st.warning(f"""
    ### 🔒 Unlock {feature_name}
    
    This feature is available in Premium plans. Upgrade now to access:
    - 20+ Premium Templates
    - Unlimited Downloads
    - AI-Powered Suggestions
    - Advanced ATS Optimization
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Upgrade to Premium", use_container_width=True, type="primary"):
            st.session_state.mode = 'pricing'
            st.rerun()
