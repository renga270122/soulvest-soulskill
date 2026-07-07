"""
Pricing Page UI for SoulSkill Resume Builder
Beautiful pricing comparison with Indian market focus
"""
import streamlit as st
import streamlit.components.v1 as components
from payment_handler import PRICING_PLANS, get_plan_price_display, get_plan_features


def render_pricing_page():
    """Render the pricing comparison page"""
    
    st.markdown("""
    <style>
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
        
        # In a real implementation, you'd integrate Razorpay's payment gateway here
        if st.button("💰 Proceed to Payment", use_container_width=True, type="primary"):
            # This would trigger Razorpay payment flow
            st.success("🎉 Redirecting to secure payment gateway...")
            st.balloons()
            
            # Show payment integration code
            st.code("""
# Razorpay Payment Integration
from payment_handler import PaymentHandler

payment = PaymentHandler()
order = payment.create_order(
    amount=plan['price_monthly'] if plan_id == 'premium_monthly' else plan['price_yearly'],
    notes={'plan': plan_id, 'user_email': user_email}
)

# Then redirect to Razorpay checkout
# In production, use Razorpay's JavaScript SDK
            """, language="python")
        
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
