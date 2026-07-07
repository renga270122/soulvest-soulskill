import streamlit as st


def apply_platform_styles():
    st.markdown(
        """
        <style>
        .platform-shell {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(30, 41, 59, 0.96) 45%, rgba(59, 130, 246, 0.9) 100%);
            border-radius: 24px;
            padding: 1.25rem;
            color: #f8fafc;
            box-shadow: 0 20px 45px rgba(15, 23, 42, 0.22);
        }
        .platform-hero {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.95) 0%, rgba(14, 116, 144, 0.95) 100%);
            border-radius: 24px;
            padding: 1.5rem;
            color: white;
            box-shadow: 0 16px 35px rgba(37, 99, 235, 0.25);
        }
        .platform-card {
            background: rgba(248, 250, 252, 0.96);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
            margin-bottom: 1rem;
        }
        .platform-card h3, .platform-card h4 {
            color: #0f172a;
            margin-bottom: 0.35rem;
        }
        .platform-card p, .platform-card li {
            color: #475569;
            line-height: 1.5;
        }
        .metric-card {
            background: linear-gradient(135deg, #eff6ff 0%, #eef2ff 100%);
            border-left: 4px solid #2563eb;
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 0.85rem;
        }
        .metric-card .label {
            font-size: 0.8rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 700;
        }
        .metric-card .value {
            font-size: 1.4rem;
            color: #0f172a;
            font-weight: 800;
            margin-top: 0.25rem;
        }
        .score-card {
            background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
            border-radius: 20px;
            padding: 1.2rem;
            color: white;
            text-align: center;
        }
        .score-card .score {
            font-size: 2.4rem;
            font-weight: 900;
            margin: 0.3rem 0;
        }
        .icon-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: rgba(37, 99, 235, 0.12);
            margin-bottom: 0.5rem;
            font-size: 1.2rem;
        }
        .timeline-item {
            border-left: 2px solid #bfdbfe;
            padding-left: 1rem;
            margin-bottom: 0.9rem;
            position: relative;
        }
        .timeline-item::before {
            content: '';
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #2563eb;
            position: absolute;
            left: -6px;
            top: 0.35rem;
        }
        .timeline-item strong {
            color: #0f172a;
        }
        .nav-pill-row .stButton>button {
            background: rgba(255,255,255,0.12);
            color: white;
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 999px;
            padding: 0.5rem 0.8rem;
            min-height: 40px;
        }
        .nav-pill-row .stButton>button:hover {
            background: rgba(255,255,255,0.22);
            border-color: rgba(255,255,255,0.3);
        }
        .module-card {
            background: white;
            border-radius: 18px;
            padding: 1rem;
            height: 100%;
            border: 1px solid rgba(148, 163, 184, 0.2);
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
        }
        .module-card .title {
            font-size: 1.05rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.3rem;
        }
        .module-card .desc {
            color: #475569;
            font-size: 0.92rem;
            line-height: 1.45;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_platform_nav(current_mode: str):
    nav_items = [
        ("Overview", "home"),
        ("Career Journey", "journey"),
        ("Career Toolkit", "toolkit"),
        ("Career Coach", "coach"),
        ("Interview Coach", "interview"),
        ("EQ Growth", "eq"),
        ("Assessment", "assessment"),
        ("Monetization", "monetization"),
    ]

    st.markdown('<div class="nav-pill-row">', unsafe_allow_html=True)
    cols = st.columns(len(nav_items))
    for col, (label, mode) in zip(cols, nav_items):
        active = current_mode == mode
        button_label = f"● {label}" if active else label
        with col:
            if st.button(button_label, key=f"nav_{mode}", use_container_width=True):
                st.session_state.mode = mode
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_metric_card(label: str, value: str, detail: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div style="color:#64748b; font-size:0.9rem; margin-top:0.2rem;">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_readiness_score(score: int):
    st.markdown(
        f"""
        <div class="score-card">
            <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:0.08em; opacity:0.8;">Career Readiness Score</div>
            <div class="score">{score}%</div>
            <div style="font-size:0.95rem; opacity:0.86;">Placeholder signal • coaching guidance coming soon</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_module_card(title: str, description: str, icon: str, key_suffix: str):
    st.markdown(
        f"""
        <div class="module-card">
            <div class="icon-pill">{icon}</div>
            <div class="title">{title}</div>
            <div class="desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return st.button("Open", key=f"module_{key_suffix}", use_container_width=True)


def render_placeholder_panel(title: str, description: str, icon: str, bullets: list, action_label: str, action_mode: str, key_suffix: str):
    st.markdown(
        f"""
        <div class="platform-card">
            <div class="icon-pill">{icon}</div>
            <h3>{title}</h3>
            <p>{description}</p>
            <ul>
                {''.join([f'<li>{item}</li>' for item in bullets])}
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return st.button(action_label, key=f"placeholder_{key_suffix}", use_container_width=True)


def render_journey_timeline():
    steps = [
        ("Assess", "Map your current strengths, gaps, and momentum."),
        ("Build", "Use the toolkit to sharpen your resume and story."),
        ("Prepare", "Practice interviews and refine interpersonal growth."),
        ("Advance", "Track momentum and unlock the next opportunity."),
    ]

    st.markdown('<div class="platform-card">', unsafe_allow_html=True)
    st.markdown('### Career Journey')
    for title, text in steps:
        st.markdown(
            f"""
            <div class="timeline-item">
                <strong>{title}</strong><br/>
                {text}
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def render_foundation_summary():
    st.markdown("""
    <div class="platform-card">
        <h3>Foundation overview</h3>
        <p>The platform now combines career growth guidance with your existing resume workflow, giving users a clearer path from first visit to next opportunity.</p>
    </div>
    """, unsafe_allow_html=True)


def render_coaching_panel():
    if "career_goal" not in st.session_state:
        st.session_state.career_goal = ""
    if "current_role" not in st.session_state:
        st.session_state.current_role = ""
    if "coaching_focus" not in st.session_state:
        st.session_state.coaching_focus = "growth"

    st.markdown('<div class="platform-card">', unsafe_allow_html=True)
    st.markdown("### AI Career Coach")
    st.caption("A lightweight coaching experience that helps users clarify next steps without changing the backend.")

    st.session_state.career_goal = st.text_input(
        "What role do you want next?",
        value=st.session_state.career_goal,
        key="career_goal_input",
    )
    st.session_state.current_role = st.text_input(
        "What is your current role?",
        value=st.session_state.current_role,
        key="current_role_input",
    )
    st.session_state.coaching_focus = st.selectbox(
        "What matters most right now?",
        ["growth", "promotion", "transition", "confidence"],
        index=["growth", "promotion", "transition", "confidence"].index(st.session_state.coaching_focus),
        key="coaching_focus_input",
    )

    focus_map = {
        "growth": ["Build a stronger narrative", "Add evidence of leadership", "Refine your resume message"],
        "promotion": ["Highlight impact and ownership", "Prepare a promotion story", "Align with leadership expectations"],
        "transition": ["Shape a transferable story", "Map adjacent skills", "Create a targeted positioning plan"],
        "confidence": ["Practice concise storytelling", "Strengthen your delivery", "Reframe feedback into growth"],
    }

    recommendations = focus_map.get(st.session_state.coaching_focus, focus_map["growth"])
    st.markdown("**Recommended coaching focus**")
    for item in recommendations:
        st.write(f"- {item}")
    st.markdown('</div>', unsafe_allow_html=True)


def render_eq_panel():
    st.markdown('<div class="platform-card">', unsafe_allow_html=True)
    st.markdown("### EQ Growth")
    st.caption("Practice emotional intelligence habits that strengthen collaboration and presence.")
    pillars = [
        ("Self-awareness", "Reflect on your recent wins and triggers."),
        ("Communication", "Use clear, calm language in team settings."),
        ("Relationship growth", "Build trust with thoughtful follow-ups."),
    ]
    for title, description in pillars:
        st.markdown(f"- **{title}:** {description}")
    st.markdown('</div>', unsafe_allow_html=True)


def render_assessment_panel():
    st.markdown('<div class="platform-card">', unsafe_allow_html=True)
    st.markdown("### Career Assessment")
    st.caption("A simple readiness snapshot that can evolve into a richer assessment experience later.")
    if "assessment_scores" not in st.session_state:
        st.session_state.assessment_scores = {
            "clarity": 70,
            "proof": 65,
            "visibility": 60,
            "confidence": 75,
        }

    scores = {}
    for key, label in [("clarity", "Role clarity"), ("proof", "Evidence of impact"), ("visibility", "Visibility in the market"), ("confidence", "Interview confidence")]:
        scores[key] = st.slider(label, 0, 100, int(st.session_state.assessment_scores[key]), key=f"assessment_{key}")
    st.session_state.assessment_scores = scores

    average = int(sum(scores.values()) / len(scores))
    st.metric("Readiness snapshot", f"{average}%")
    st.markdown('</div>', unsafe_allow_html=True)


def render_monetization_panel():
    st.markdown('<div class="platform-card">', unsafe_allow_html=True)
    st.markdown("### Monetization Preview")
    st.caption("Free and Pro paths are now separated cleanly so future subscription flows can slot in without disrupting the app.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Free**\n- Core resume builder\n- Basic toolkit\n- Community guidance")
    with col2:
        st.markdown("**Pro**\n- Advanced coaching\n- Priority insights\n- Premium growth plans")
    st.markdown('</div>', unsafe_allow_html=True)
