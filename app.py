from pathlib import Path
import html
import re

import streamlit as st

from auth import create_users_table, create_user, verify_user
from orchestrator import Orchestrator


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="DevTeam AI — Build Something.",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# DATABASE SETUP
# ==================================================

create_users_table()


# ==================================================
# SESSION STATE
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "development_result" not in st.session_state:
    st.session_state.development_result = None

if "last_project_idea" not in st.session_state:
    st.session_state.last_project_idea = ""


# ==================================================
# VISUAL SYSTEM — self-contained; no external fonts, images, or dependencies.
# Native Streamlit widgets stay native. CSS only changes their presentation.
# data-testid selectors may need revisiting after a major Streamlit update.
# ==================================================

st.markdown(
    """
<style>
:root {
    color-scheme: light;
    --bg: #f8f5ef; --paper: #fffdfa; --ink: #171715; --muted: #67655f;
    --line: #e5e0d7; --pink: #f9d9df; --lavender: #ded4ff;
    --peach: #f8d0b6; --lime: #e8eea6;
}
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg) !important; color: var(--ink) !important;
    font-family: Arial, Helvetica, sans-serif;
}
.block-container {max-width: 1240px !important; padding: 2rem 3rem 3rem !important;}
[data-testid="stHeader"] {background: transparent !important;}
[data-testid="stDecoration"] {display: none;}
#MainMenu, footer {visibility: hidden;}
h1,h2,h3,h4,p,label {color: var(--ink);}
h1,h2,h3 {letter-spacing: -.055em;}
p {line-height: 1.65;}
.brand-bar {display: flex; align-items: center; justify-content: space-between;
    gap: 20px; padding: 8px 0 25px; margin-bottom: 10px;}
.brand-logo {font-size: 24px; font-weight: 800; letter-spacing: -1.2px;
    display: flex; gap: 10px; align-items: center;}
.brand-flower {font-size: 40px; line-height: 1; display: inline-block;}
.brand-label {font-size: 10px; letter-spacing: .16em; color: var(--muted);}
.brand-note {border: 1px solid var(--line); border-radius: 30px; padding: 10px 15px;
    font-size: 11px; color: var(--muted);}
.hero {position: relative; isolation: isolate; min-height: 370px; padding: 54px 0 30px;}
.hero-copy {position: relative; z-index: 2; width: 59%;}
.eyebrow,.section-label {font-family: monospace; font-size: 11px; font-weight: 500;
    letter-spacing: .19em; text-transform: uppercase; color: var(--muted); margin: 0 0 18px;}
.hero-title {font-size: clamp(54px, 7.4vw, 100px); line-height: .94;
    letter-spacing: -.075em; font-weight: 850; margin: 0 0 25px; color: var(--ink);}
.hero-title .underlined {position: relative; display: inline-block;}
.hero-title .underlined:after {content: ''; position: absolute; left: 2%; bottom: -8px;
    width: 96%; height: 4px; background: var(--ink); border-radius: 60%; transform: rotate(-2deg);}
.hero-description {font-size: 16px; color: var(--muted); max-width: 440px;
    line-height: 1.7; margin: 24px 0 10px;}
.hero-art {position: absolute; right: 0; top: 4px; width: 43%; height: 370px;
    z-index: 0; pointer-events: none;}
.blob {position: absolute; animation: drift 9s ease-in-out infinite alternate;}
.blob.pink {width: 68%; height: 82%; top: 0; right: 10%; background: var(--pink);
    border-radius: 55% 35% 62% 28% / 38% 42% 58% 65%; transform: rotate(22deg);}
.blob.lavender {width: 62%; height: 47%; right: -2%; bottom: 2%; background: var(--lavender);
    border-radius: 32% 63% 35% 60%; transform: rotate(30deg); animation-delay: -3s;}
.blob.lime {width: 50%; height: 46%; left: 0; bottom: 14%; background: var(--lime);
    border-radius: 60% 42% 55% 35%; transform: rotate(-24deg); animation-delay: -6s;}
.idea-paper {position: absolute; top: 27%; left: 20%; width: 66%; padding: 25px 22px;
    background: rgba(255,253,250,.88); border: 1px solid #ffffff; border-radius: 24px;
    box-shadow: 0 16px 40px #63554e0c; transform: rotate(-8deg);}
.paper-kicker {font: 10px monospace; letter-spacing: .15em; color: var(--muted);}
.paper-title {font-size: 32px; font-weight: 800; letter-spacing: -.05em; margin: 14px 0;}
.paper-line {display: block; height: 5px; border-radius: 10px; background: #ded8cf; width: 80%; margin: 9px 0;}
.paper-line.short {width: 53%; background: var(--lavender);}
.hand-note {font: italic 13px monospace; letter-spacing: .12em; line-height: 1.8;
    transform: rotate(-7deg); margin: 25px 0;}
.art-star {position: absolute; right: 1%; top: 12%; font-size: 55px; transform: rotate(12deg);}
.art-loop {position: absolute; left: 5%; top: 14%; font-size: 70px; transform: rotate(25deg);}
.section-label {margin-top: 25px; margin-bottom: 12px;}
.section-heading {font-size: clamp(28px,4vw,46px); font-weight: 800;
    letter-spacing: -.055em; line-height: 1.05; margin: 0 0 18px;}
.muted-copy {color: var(--muted); font-size: 14px; line-height: 1.75;}
.editorial-card {background: var(--paper); border: 1px solid #fff;
    border-radius: 25px; padding: 26px; margin: 12px 0 20px; box-shadow: 0 8px 30px #342b2105;}
.card-index {font: 10px monospace; letter-spacing: .15em; color: var(--muted); margin-bottom: 16px;}
.card-title {font-size: 25px; font-weight: 750; letter-spacing: -.04em; margin-bottom: 10px; overflow-wrap: anywhere;}
.status-grid {display: grid; grid-template-columns: repeat(4,minmax(0,1fr)); gap: 14px; margin: 18px 0 36px;}
.status-card {background: var(--paper); border: 1px solid #fff; border-radius: 22px;
    padding: 23px 20px; min-height: 110px; transition: transform .2s;}
.status-card:nth-child(1) {background: #efeadf;}
.status-card:nth-child(2) {background: #edf0cd;}
.status-card:nth-child(3) {background: #ece5fb;}
.status-card:nth-child(4) {background: #fae7db;}
.status-card:hover {transform: translateY(-3px);}
.status-label {font: 10px monospace; letter-spacing: .1em; color: var(--muted); margin-bottom: 16px;}
.status-value {font-size: 18px; font-weight: 750; letter-spacing: -.03em;}
.status-value.good {color: #34613a;} .status-value.warn {color: #785318;} .status-value.bad {color: #9b3434;}
[data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"] > div[style*="border"],
[data-testid="stVerticalBlockBorderWrapper"][style*="border"] {
    border-color: var(--line) !important; border-radius: 26px !important;
    background: var(--paper); padding: 24px !important;
}
[data-testid="stWidgetLabel"] p {font-size: 12px; color: var(--muted) !important;}
[data-testid="stTextInputRootElement"], [data-testid="stTextAreaRootElement"],
.stTextInput [data-baseweb="input"], .stTextArea [data-baseweb="textarea"] {
    background: #fff !important; border-color: var(--line) !important; border-radius: 16px !important;
}
.stTextArea textarea, .stTextInput input {background: #fff !important; color: var(--ink) !important;
    border-radius: 16px !important; font-size: 15px !important; caret-color: #171715;}
.stTextArea textarea {padding: 20px !important; line-height: 1.8;}
.stTextInput input {padding: 12px 16px !important;}
.stTextArea textarea::placeholder,.stTextInput input::placeholder {color: #817d77 !important; opacity: 1;}
.stTextArea:focus-within,.stTextInput:focus-within {border-radius: 16px; outline: 2px solid #aa96d5; outline-offset: 3px;}
.stButton button,.stDownloadButton button,.stFormSubmitButton button {
    border-radius: 999px !important; padding: .7rem 1.4rem !important; min-height: 48px;
    border: 1px solid var(--line) !important; background: var(--paper) !important;
    color: var(--ink) !important; transition: transform .2s, box-shadow .2s, background .2s;
}
.stButton button p,.stDownloadButton button p,.stFormSubmitButton button p {color: inherit !important; font-size: 13px; font-weight: 600;}
.stButton button[kind="primary"],.stDownloadButton button[kind="primary"],.stFormSubmitButton button[kind="primary"] {
    color: #fff !important; background: #171715 !important; border-color: #171715 !important;
}
.stButton button:hover,.stDownloadButton button:hover,.stFormSubmitButton button:hover {
    transform: translateY(-2px); box-shadow: 0 6px 16px #342b2110; background: #eee7fb !important; color: #171715 !important;
}
button:focus-visible {outline: 3px solid #a58bd7 !important; outline-offset: 3px;}
.stTabs [data-baseweb="tab-list"] {gap: 20px; border-bottom: 1px solid var(--line);}
.stTabs [data-baseweb="tab"] {background: transparent !important; color: var(--muted) !important;}
.stTabs [aria-selected="true"] {color: var(--ink) !important;}
.stTabs [data-baseweb="tab-highlight"] {background: #171715;}
[data-testid="stExpander"] {background: var(--paper); border: 1px solid var(--line) !important; border-radius: 20px !important;}
[data-testid="stAlert"] {border-radius: 18px;}
[data-testid="stCaptionContainer"] p {color: var(--muted) !important; font-size: 12px;}
.chip-row {display: flex; flex-wrap: wrap; gap: 7px; margin: 4px 0 14px;}
.idea-chip {background: #efede8; border-radius: 30px; padding: 7px 12px; font-size: 10px; color: #54524d;}
.studio-note {font-size: 12px; color: var(--muted); margin-top: 25px; line-height: 1.8;}
.working-card {background: #eee8fb; border-radius: 24px; padding: 24px; margin: 20px 0;}
.working-title {font-size: 25px; font-weight: 750; letter-spacing: -.04em;}
.agent-orbits {display: flex; gap: 9px; margin: 17px 0;}
.agent-orbits span {width: 28px; height: 28px; border: 1px solid #a897ce; border-radius: 50%;
    animation: breathe 1.8s ease-in-out infinite alternate; background: #fff9;}
.agent-orbits span:nth-child(2n) {animation-delay: -.6s; background: var(--lime);}
.agent-orbits span:nth-child(3n) {animation-delay: -1.2s; background: var(--pink);}
.custom-footer {margin-top: 65px; padding-top: 22px; border-top: 1px solid var(--line);
    display: flex; justify-content: space-between; gap: 20px; font: 10px monospace;
    letter-spacing: .1em; color: var(--muted);}
.red-dot {color: #9784bf;}
@keyframes drift {to {translate: 0 -10px;}}
@keyframes breathe {to {opacity: .4; transform: translateY(-4px);}}
@media (prefers-reduced-motion: reduce) {
    .blob,.agent-orbits span {animation: none;} *,*::before,*::after {transition: none !important;}
}
@media (max-width: 850px) {
    .block-container {padding: 1.6rem 1.4rem 3rem !important;}
    .hero {min-height: 330px;} .hero-title {font-size: 68px;}
    .hero-art {width: 43%; height: 300px; top: 25px;} .idea-paper {padding: 18px;}
    .paper-title {font-size: 23px;} .status-grid {grid-template-columns: repeat(2,minmax(0,1fr));}
}
@media (max-width: 600px) {
    .brand-label {font-size: 9px;} .brand-note {display: none;}
    .hero {padding-top: 28px; min-height: 0; padding-bottom: 18px;}
    .hero-copy {width: 100%;} .hero-title {font-size: clamp(49px,13vw,70px);}
    .hero-art {position: relative; width: 90%; height: 220px; margin: 12px auto 0; top: 0;}
    .idea-paper {top: 15%; left: 25%; width: 60%; padding: 16px;}
    .paper-title {font-size: 24px; margin: 8px 0;}
    .hero-description {font-size: 14px;} .custom-footer {flex-direction: column;}
    .status-card {padding: 18px 14px;} .status-value {font-size: 16px;}
}
</style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SMALL UI HELPERS
# ==================================================

def render_brand():

    st.markdown(
        """
        <div class="brand-bar">
            <div class="brand-logo">
                <span class="brand-flower" aria-hidden="true">✿</span> DevTeam AI
            </div>
            <div class="brand-label">
                YOUR IDEA. A TEAM EFFORT.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_hero(auth=False):
    """Self-contained abstract artwork; no assumed image assets or network calls."""
    title = ('From Idea<br>to <span class="underlined">Project.</span>' if auth else
             'A little idea.<br>A <span class="underlined">big beginning.</span>')
    description = (
        "Your personal AI development team. Describe your idea and turn it into "
        "a structured project, with source files and documentation."
        if auth else
        "You bring the idea. Your AI team brings it together. "
        "Let’s make something worth building."
    )
    st.markdown(
        f"""
        <section class="hero">
          <div class="hero-copy">
            <div class="eyebrow">YOUR AI DEVELOPMENT STUDIO</div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-description">{description}</p>
          </div>
          <div class="hero-art" aria-hidden="true">
            <div class="blob pink"></div><div class="blob lime"></div>
            <div class="blob lavender"></div>
            <div class="idea-paper">
              <div class="paper-kicker">A LITTLE POSSIBILITY</div>
              <div class="paper-title">What if<br>we built it?</div>
              <span class="paper-line"></span><span class="paper-line short"></span>
              <div class="hand-note">One idea. Six AI agents. ↗</div>
            </div>
            <span class="art-star">✳</span><span class="art-loop">↝</span>
          </div>
        </section>
        """, unsafe_allow_html=True
    )


def render_working_state():
    """Indeterminate activity only: team.run provides no per-agent callbacks."""
    st.markdown(
        """
        <div class="working-card" role="status" aria-live="polite">
          <div class="eyebrow">02 / GENERATING</div>
          <div class="working-title">Your AI team is at work.</div>
          <div class="agent-orbits" aria-hidden="true">
            <span></span><span></span><span></span><span></span><span></span><span></span>
          </div>
          <div class="muted-copy">Turning your brief into a project. This may take a few minutes.</div>
        </div>
        """, unsafe_allow_html=True
    )


def render_footer():

    st.markdown(
        """
        <div class="custom-footer">
            <span>DEVTEAM.AI <span class="red-dot">●</span> 2026</span>
            <span>IMAGINE / GENERATE / BUILD</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_status_card(label, value, tone="normal"):

    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))

    allowed_tones = {"normal", "good", "warn", "bad"}

    if tone not in allowed_tones:
        tone = "normal"

    return f"""
    <div class="status-card">
        <div class="status-label">{safe_label}</div>
        <div class="status-value {tone}">{safe_value}</div>
    </div>
    """


def get_project_title(idea):

    # Derive a short title from the user's original idea.
    title = idea.strip().splitlines()[0]

    title = re.sub(
        r"^(please\\s+)?(build|create|make|develop|design)\\s+",
        "",
        title,
        flags=re.IGNORECASE
    )

    title = title.strip(" .:-")

    if not title:
        return "Your Generated Project"

    if len(title) > 65:
        title = title[:62].rstrip() + "..."

    return title


def get_file_count(result):

    files = result.get("saved_files", [])

    return len(files) if isinstance(files, list) else 0


# ==================================================
# LOGIN / SIGN UP PAGE
# ==================================================

def show_auth_page():

    render_brand()

    render_hero(auth=True)

    left, right = st.columns(
        [1.1, 0.9],
        gap="large"
    )

    with left:

        st.markdown(
            """
            <div class="editorial-card">
                <div class="card-index">001 / THE PLATFORM</div>
                <div class="card-title">Build without the busywork.</div>
                <div class="muted-copy">
                    Describe what you want to create.
                    DevTeam AI handles requirements,
                    architecture, development, review,
                    and project documentation.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:

        login_tab, signup_tab = st.tabs(
            ["SIGN IN", "CREATE ACCOUNT"]
        )

        with login_tab:

            with st.form("login_form"):

                username = st.text_input(
                    "Username",
                    key="login_username"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    key="login_password"
                )

                login_button = st.form_submit_button(
                    "SIGN IN →",
                    type="primary",
                    use_container_width=True
                )

            if login_button:

                if verify_user(username, password):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.session_state.development_result = None
                    st.session_state.last_project_idea = ""

                    st.rerun()

                else:
                    st.error(
                        "Invalid username or password."
                    )

        with signup_tab:

            with st.form("signup_form"):

                new_username = st.text_input(
                    "Choose a username",
                    key="signup_username"
                )

                new_password = st.text_input(
                    "Choose a password",
                    type="password",
                    key="signup_password"
                )

                confirm_password = st.text_input(
                    "Confirm password",
                    type="password",
                    key="confirm_password"
                )

                signup_button = st.form_submit_button(
                    "CREATE ACCOUNT →",
                    type="primary",
                    use_container_width=True
                )

            if signup_button:

                if not new_username.strip():
                    st.warning(
                        "Please enter a username."
                    )

                elif len(new_password) < 6:
                    st.warning(
                        "Password must contain at least 6 characters."
                    )

                elif new_password != confirm_password:
                    st.warning(
                        "Passwords do not match."
                    )

                else:

                    success, message = create_user(
                        new_username,
                        new_password
                    )

                    if success:
                        st.success(
                            "Account created! You can now sign in."
                        )
                    else:
                        st.error(message)

    render_footer()


# ==================================================
# PROJECT OVERVIEW
# ==================================================

def show_project_overview(result):

    project_title = get_project_title(
        st.session_state.last_project_idea
    )

    st.markdown(
        '<div class="section-label">/ 002 — YOUR PROJECT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">Your project, brought together.</div>',
        unsafe_allow_html=True
    )

    safe_title = html.escape(project_title)

    file_count = get_file_count(result)

    st.markdown(
        f"""
        <div class="editorial-card">
            <div class="card-index">PROJECT / GENERATED OUTPUT</div>
            <div class="card-title">{safe_title}</div>
            <div class="muted-copy">
                Your project has been processed by DevTeam AI.
                Review the result and download your files below.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    repair_status = result.get(
        "repair_status",
        "UNKNOWN"
    )

    documentation_status = result.get(
        "documentation_status",
        "SKIPPED"
    )

    if repair_status == "PASS":
        syntax_value = "PASSED"
        syntax_tone = "good"
    else:
        syntax_value = "NEEDS ATTENTION"
        syntax_tone = "bad"

    if documentation_status == "SUCCESS":
        report_value = "READY"
        report_tone = "good"
    elif documentation_status == "ERROR":
        report_value = "FAILED"
        report_tone = "bad"
    else:
        report_value = "NOT AVAILABLE"
        report_tone = "warn"

    st.markdown(
        f"""
        <div class="status-grid">
            {render_status_card(
                "PROJECT FILES",
                f"{file_count} FILES"
            )}

            {render_status_card(
                "SYNTAX CHECK",
                syntax_value,
                syntax_tone
            )}

            {render_status_card(
                "PROJECT REPORT",
                report_value,
                report_tone
            )}

            {render_status_card(
                "TEST EXECUTION",
                "NOT RUN",
                "warn"
            )}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- REVIEW SUMMARY ----------------

    st.markdown(
        '<div class="section-label">/ 003 — AI ASSESSMENT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">A second pair of eyes.</div>',
        unsafe_allow_html=True
    )

    review = result.get("review")

    if review:
          with st.container(border=True):
            st.markdown(str(review))
    else:
        st.info(
            "No project review is available."
        )

    # ---------------- DOWNLOADS ----------------

    st.markdown(
        '<div class="section-label">/ 004 — DELIVERABLES</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">Made to be yours.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="muted-copy">
            Download the complete project package or
            get the academic project report separately.
        </p>
        """,
        unsafe_allow_html=True
    )

    zip_path = result.get("zip_path")
    pdf_path = result.get("pdf_path")

    zip_file = Path(zip_path) if zip_path else None
    pdf_file = Path(pdf_path) if pdf_path else None

    left, right = st.columns(2, gap="medium")

    with left:

        if zip_file and zip_file.is_file():

            with zip_file.open("rb") as file:
                st.download_button(
                    label="↓ Download Project ZIP",
                    data=file.read(),
                    file_name=zip_file.name,
                    mime="application/zip",
                    type="primary",
                    use_container_width=True,
                    key="download_project_zip"
                )

        else:

            st.warning(
                "Project ZIP is unavailable."
            )



    with right:

        if pdf_file and pdf_file.is_file():

            with pdf_file.open("rb") as file:
                st.download_button(
                    label="↓ Download PDF Report",
                    data=file.read(),
                    file_name="Project_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_project_pdf"
                )

        else:

            st.info(
                "PDF report is unavailable."
            )



    st.caption(
        "The ZIP contains the generated source files "
        "and the PDF report when available."
    )

    # ---------------- ADVANCED DETAILS ----------------

    with st.expander(
        "Behind the build · Technical details",
        expanded=False
    ):

        st.caption(
            "Detailed agent outputs for debugging and evaluation."
        )

        if result.get("zip_error"):
            st.markdown("#### ZIP export details")
            st.caption(str(result["zip_error"]))
        if result.get("documentation_error"):
            st.markdown("#### Report export details")
            st.caption(str(result["documentation_error"]))

        st.markdown("#### Requirements")
        st.markdown(
            str(result.get("requirements", ""))
        )

        st.markdown("#### Architecture")
        st.markdown(
            str(result.get("architecture", ""))
        )

        st.markdown("#### Generated Code")
        st.code(
            str(result.get("generated_code", "")),
            language="markdown"
        )

        st.markdown("#### Saved Files")

        for filename in result.get(
            "saved_files",
            []
        ):
            st.write(f"• {filename}")

        st.markdown("#### Syntax Check Results")

        for test in result.get(
            "test_results",
            []
        ):

            status = test.get("status", "UNKNOWN")
            filename = test.get("file", "File")
            message = test.get("message", "")

            st.write(
                f"**{filename}** — {status}: {message}"
            )

        st.markdown("#### Test Availability")

        availability = result.get(
            "test_availability",
            {}
        )

        st.write(
            availability.get(
                "message",
                "No test information available."
            )
        )

        st.caption(
            "Pytest files may be detected, but tests "
            "are not executed automatically."
        )


# ==================================================
# MAIN DASHBOARD
# ==================================================

def show_main_page():

    render_brand()

    # ---------------- TOP BAR ----------------

    top_left, top_right = st.columns(
        [4, 1],
        vertical_alignment="center"
    )

    with top_left:

        username = html.escape(
            st.session_state.username
        )

        st.markdown(
            f"""
            <div class="brand-label">
                WORKSPACE / {username}
            </div>
            """,
            unsafe_allow_html=True
        )

    with top_right:

        if st.button(
            "LOG OUT",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.development_result = None
            st.session_state.last_project_idea = ""

            st.rerun()

    render_hero()

    # ---------------- IDEA INPUT ----------------

    idea_left, idea_right = st.columns([0.8, 1.2], gap="large")
    with idea_left:
        st.markdown(
            """
            <div class="section-label">01 / CREATE</div>
            <h2 class="section-heading">What do you<br>want to build?</h2>
            <div class="hand-note">Describe your idea<br>in your own words. ↗</div>
            <p class="muted-copy">Tell us who it’s for, what it should do,<br>
            and the features that matter most.</p>
            <div class="studio-note">✳ &nbsp; Six agents. One shared brief.<br>
            Source code · AI review · Project report</div>
            """, unsafe_allow_html=True
        )

    with idea_right:
        with st.container(border=True):
            requirement = st.text_area(
                "DESCRIBE YOUR PROJECT",
                placeholder=(
                    "Example: Build a Student Management System "
                    "where I can add, update, delete, "
                    "and search students..."
                ),
                height=180
            )

            st.caption(
                "Be specific about the features you want."
            )

            if st.button(
                "Generate My Project ↗",
                type="primary",
                use_container_width=True
            ):

                if not requirement.strip():

                    st.warning(
                        "Please describe your project first."
                    )

                else:

                    st.session_state.development_result = None
                    st.session_state.last_project_idea = requirement

                    working = st.empty()
                    with working.container():
                        render_working_state()

                    try:

                        with st.spinner(
                            "Your AI development team is building "
                            "your project. This may take a few minutes..."
                        ):

                            team = Orchestrator(
                                provider="gemini"
                            )

                            result = team.run(
                                requirement
                            )

                        st.session_state.development_result = result

                        st.success(
                            "Your project is ready to review!"
                        )

                    except Exception as error:

                        st.error(
                            f"Project generation failed: {error}"
                        )

                    finally:
                        working.empty()

    # ---------------- RESULTS ----------------

    result = st.session_state.development_result

    if result is not None:

        st.divider()

        show_project_overview(result)

    render_footer()


# ==================================================
# APP ROUTING
# ==================================================

if st.session_state.logged_in:
    show_main_page()
else:
    show_auth_page()
