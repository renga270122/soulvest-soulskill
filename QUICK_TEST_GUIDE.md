# Quick Start Guide - Test Freemium Features

## 🚀 Quick Test (5 Minutes)

### 1. Install Razorpay
```bash
pip install razorpay
```

### 2. Start the App
```bash
streamlit run streamlit_app.py
```

### 3. Test Features

#### A. View Pricing Page
1. Open the app
2. Scroll to bottom
3. Click **"💰 Pricing"** button
4. See the 3-tier pricing comparison

#### B. Test Upgrade Flow
1. On pricing page
2. Click **"Start 7-Day Free Trial"** on Premium Monthly
3. See checkout page with plan details
4. (Don't complete payment in test mode yet)

#### C. Test Premium CTA on Homepage
1. Go back to homepage (click logo or "Home" button)
2. Scroll down to see the premium CTA banner
3. Shows ₹199/month and ₹999/year options
4. Click **"💎 View Pricing Plans"** → redirects to pricing

---

## 🧪 Full Test with Payment (10 Minutes)

### Prerequisites
1. Razorpay account created
2. Test API keys obtained
3. Keys added to `.env` file

### Test Flow

#### 1. Setup Test Environment
```bash
# Create .env file
echo "RAZORPAY_KEY_ID=rzp_test_YOUR_KEY_ID" > .env
echo "RAZORPAY_KEY_SECRET=YOUR_KEY_SECRET" >> .env
```

#### 2. Modify for Testing
In `payment_handler.py`, temporarily change:
```python
'price_monthly': 1000,  # ₹10 instead of ₹199
'price_yearly': 5000,   # ₹50 instead of ₹999
```

#### 3. Test Payment
1. Go to Pricing page
2. Click "Start 7-Day Free Trial"
3. Click "Proceed to Payment"
4. Use Razorpay test card:
   - Card: **4111 1111 1111 1111**
   - Expiry: Any future date
   - CVV: Any 3 digits
   - Name: Any name

5. Complete payment
6. Verify:
   - Payment success message
   - Trial activated
   - Premium features unlocked

#### 4. Test Feature Access
After payment:
1. Go to resume builder
2. Access premium templates (should work)
3. Try AI suggestions (should work)
4. Download multiple times (should work)

#### 5. Revert Changes
In `payment_handler.py`, change back:
```python
'price_monthly': 19900,  # ₹199
'price_yearly': 99900,   # ₹999
```

---

## 📱 Test on Mobile

### 1. Run with External Access
```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

### 2. Access from Phone
- Find your local IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
- Open on phone: `http://YOUR_IP:8501`

### 3. Test Mobile UX
- Responsive pricing cards
- Touch-friendly buttons
- Payment gateway mobile view
- Navigation menu

---

## 🔍 What to Check

### Visual Elements
- [ ] Pricing cards display correctly
- [ ] Premium badge shows on templates
- [ ] Upgrade prompts appear for locked features
- [ ] Trial banner shows at top
- [ ] Pricing CTAs on homepage

### Functionality
- [ ] Pricing page loads without errors
- [ ] Can navigate to checkout
- [ ] Free tier limits enforced
- [ ] Premium features locked for free users
- [ ] Trial system works

### Payment Flow (with test keys)
- [ ] Order creation successful
- [ ] Razorpay modal opens
- [ ] Payment completes
- [ ] Subscription activates
- [ ] Database updated

---

## 🐛 Common Issues & Fixes

### Issue: "Module 'razorpay' not found"
```bash
pip install razorpay
```

### Issue: Pricing page doesn't load
**Check:**
1. `pricing_ui.py` exists
2. Import added to `app_enhanced.py`
3. No syntax errors in pricing_ui.py

### Issue: Payment button does nothing
**Check:**
1. Razorpay keys configured
2. `.env` file loaded
3. Check browser console for errors

### Issue: "Invalid API key"
**Fix:**
1. Verify key format: starts with `rzp_test_`
2. No extra spaces in `.env`
3. Restart Streamlit after changing `.env`

---

## ✅ Pre-Launch Checklist

### Technical
- [ ] Razorpay package installed
- [ ] Test mode payment successful
- [ ] Database schema updated
- [ ] All imports working
- [ ] No console errors

### Content
- [ ] Pricing page displays correctly
- [ ] Indian rupee (₹) symbol shows
- [ ] Testimonials updated
- [ ] FAQ answers complete
- [ ] Trust badges present

### UX
- [ ] Pricing accessible from multiple places
- [ ] Upgrade prompts clear and actionable
- [ ] Trial banner shows correctly
- [ ] Mobile responsive
- [ ] Navigation intuitive

### Payment
- [ ] Test card works
- [ ] Payment confirmation shows
- [ ] Trial activates correctly
- [ ] Features unlock immediately
- [ ] Usage tracking works

---

## 🎯 Ready for Production?

### Final Steps Before Launch:

1. **Switch to Live Keys**
   ```bash
   RAZORPAY_KEY_ID=rzp_live_YOUR_LIVE_KEY_ID
   RAZORPAY_KEY_SECRET=YOUR_LIVE_KEY_SECRET
   ```

2. **Test with Real Amount**
   - Use actual pricing (₹199/₹999)
   - Test with your own card
   - Verify receipt email
   - Check Razorpay dashboard

3. **Deploy**
   - Push to GitHub
   - Deploy to Streamlit Cloud/Heroku
   - Add secrets in production
   - Verify production URL works

4. **Monitor**
   - Watch first transactions
   - Check error logs
   - Monitor conversion rate
   - Gather user feedback

---

## 🚀 You're All Set!

Once you've completed the tests above, you're ready to launch! 

**Next:** Start your marketing campaign and watch the conversions roll in! 💰

Good luck! 🎉
