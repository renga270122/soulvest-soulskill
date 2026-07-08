from datetime import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient

import api
from auth import AuthManager
from career_readiness import calculate_career_readiness_score
from database import get_db_manager
from payment_handler import SubscriptionManager


def main() -> int:
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    test_email = f"e2e_{stamp}@soulskill.ai"
    password = "StrongPass123"
    test_name = "E2E User"

    results = []

    # 1) Sign up + login
    auth = AuthManager()
    created = auth.create_account(test_name, test_email, password)
    logged_in = auth.login_with_email(test_email, password)
    current_user = auth.get_current_user() or {}

    results.append(("create_account", created))
    results.append(("login_with_email", logged_in))
    results.append(("current_user_email", current_user.get("email") == test_email))

    # 2) Trial + feature gates
    db = get_db_manager()
    sub_manager = SubscriptionManager(db)

    before = sub_manager.get_user_subscription(test_email)
    access_before, _ = sub_manager.check_feature_access(test_email, "premium_templates")

    trial_started = sub_manager.start_trial(test_email, "premium_monthly")
    during = sub_manager.get_user_subscription(test_email)
    access_trial_templates, _ = sub_manager.check_feature_access(test_email, "premium_templates")
    access_trial_ai, _ = sub_manager.check_feature_access(test_email, "ai_suggestions")

    results.append(("default_plan_free", before.get("plan") == "free"))
    results.append(("premium_locked_before_trial", not bool(access_before)))
    results.append(("trial_started", trial_started))
    results.append(("trial_mode", during.get("status") == "trial"))
    results.append(("templates_unlocked_on_trial", bool(access_trial_templates)))
    results.append(("mentor_unlocked_on_trial", bool(access_trial_ai)))

    # 3) Simulate payment verify API endpoint (mock signature verification)
    client = TestClient(api.app)
    payload = {
        "plan_id": "premium_yearly",
        "user_email": test_email,
        "razorpay_order_id": "order_test_123",
        "razorpay_payment_id": "pay_test_123",
        "razorpay_signature": "sig_test_123",
    }

    with patch("api.PaymentHandler.verify_payment", return_value=True):
        response = client.post(
            "/api/payments/verify",
            json=payload,
            headers={"Authorization": "Bearer smoke-test-token"},
        )

    after_payment = sub_manager.get_user_subscription(test_email)
    results.append(("api_verify_status_200", response.status_code == 200))
    results.append(("plan_after_payment", after_payment.get("plan") == "premium_yearly"))
    results.append(("active_after_payment", after_payment.get("status") == "active"))

    # 4) Saved resumes flow
    resume_id = db.save_resume(
        test_email,
        {
            "full_name": test_name,
            "email": test_email,
            "job_title_target": "Product Manager",
            "summary": "Testing E2E save and retrieval flow.",
            "tech_skills": "python,sql,analytics",
            "selected_template": "professional_blue",
        },
    )
    saved_resumes = db.get_user_resumes(test_email)

    results.append(("resume_saved", bool(resume_id)))
    results.append(("resume_retrieved", len(saved_resumes) >= 1))

    # 5) Weighted readiness score
    score, breakdown, insights = calculate_career_readiness_score(
        {
            "resume_quality": 72,
            "ats_compatibility": 69,
            "technical_skills": 66,
            "soft_skills": 74,
            "emotional_intelligence": 78,
            "interview_readiness": 64,
            "career_planning": 71,
        }
    )

    results.append(("readiness_score_range", 0 <= score <= 100))
    results.append(("readiness_has_breakdown", isinstance(breakdown, dict) and len(breakdown) == 7))
    results.append(("readiness_has_insights", isinstance(insights, dict) and "focus" in insights))

    # Summary output
    print("\n=== SoulSkill E2E Smoke Test ===")
    all_pass = True
    for name, ok in results:
        state = "PASS" if ok else "FAIL"
        print(f"{state}: {name}")
        all_pass = all_pass and bool(ok)

    print(f"\nReadiness Score Sample: {score}")
    print(f"Subscription After Payment: {after_payment.get('plan')} ({after_payment.get('status')})")
    print(f"Saved Resumes Count: {len(saved_resumes)}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
