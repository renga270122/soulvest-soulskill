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


def render_module_card(title: str, description: str, icon: str, target_mode: str, key_suffix: str):
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
