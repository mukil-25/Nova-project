
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from backend.analyser import extract_resume_text, rank_resumes

st.set_page_config(
    page_title="NovaHire AI | Smart Recruitment",
    page_icon="✦",
    layout="wide"
)

# ==================================================
# GLOBAL DESIGN - SHARP NEON UI
# ==================================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 15% 5%, #111d48 0%, transparent 32%),
        radial-gradient(ellipse at 85% 75%, #24103d 0%, transparent 35%),
        #040713;
    color: #ffffff;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1280px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #ffffff !important;
}

p, label {
    color: #d0dcf5;
}

.brand {
    font-size: 32px;
    font-weight: 900;
    letter-spacing: -1px;
    color: #60eaff;
    padding: 8px 0 18px;
}

.brand span {
    color: #ffffff;
}

.stButton > button,
.stDownloadButton > button,
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(100deg, #087edb, #5048e5);
    color: white !important;
    border: 1px solid #618aff;
    border-radius: 10px;
    font-weight: 750;
    min-height: 44px;
    transition: 0.2s;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #70eaff;
    box-shadow: 0 0 14px #277bff66;
    transform: translateY(-2px);
}

.stTextInput input,
.stTextArea textarea {
    background: #0a1328 !important;
    color: #ffffff !important;
    border: 1px solid #3d5482 !important;
    border-radius: 9px !important;
}

[data-testid="stFileUploader"] {
    background: #0b1429;
    border: 1px dashed #55a9ff;
    border-radius: 13px;
    padding: 14px;
}

[data-testid="stMetric"] {
    background: #101d39;
    border: 1px solid #354d7b;
    padding: 15px;
    border-radius: 12px;
}

[data-testid="stMetricValue"] {
    color: #78eaff !important;
}

[data-testid="stProgressBar"] > div > div > div {
    background: linear-gradient(90deg, #00d9ff, #7565ff);
}

hr {
    border-color: #293b60;
}

.step-label {
    color: #66eaff;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.feature-card {
    background: #0b1429;
    border: 1px solid #314b7d;
    border-radius: 13px;
    padding: 20px;
    min-height: 150px;
    transition: 0.2s;
}

.feature-card:hover {
    border-color: #64eaff;
    box-shadow: 0 0 16px #277bff33;
    transform: translateY(-3px);
}

[data-testid="stExpander"] {
    background: #0b1429;
    border: 1px solid #30466e;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================

defaults = {
    "page": "Home",
    "resumes": [],
    "job_title": "",
    "job_description": "",
    "results": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================================================
# NAVIGATION
# ==================================================

st.markdown(
    '<div class="brand">✦ NovaHire <span>AI</span></div>',
    unsafe_allow_html=True
)

pages = [
    ("✦ Home", "Home"),
    ("📄 Upload Resumes", "Upload Resumes"),
    ("💼 Job Description", "Job Description"),
    ("📊 Analyze & Compare", "Analyze & Compare")
]

cols = st.columns(4)

for col, (label, page) in zip(cols, pages):
    with col:
        if st.button(label, key="nav_" + page,
                     use_container_width=True):
            st.session_state.page = page
            st.rerun()

st.divider()


# ==================================================
# HOME PAGE - SHARP 3D-STYLE VISUAL
# ==================================================

if st.session_state.page == "Home":

    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        background: transparent;
        color: white;
        font-family: Arial, sans-serif;
    }

    .scene {
        width: 100%;
        height: 600px;
        position: relative;
        overflow: hidden;
        border: 1px solid #315cb4;
        border-radius: 18px;
        background:
            radial-gradient(ellipse at 20% 25%,
                #14285d 0%, transparent 35%),
            radial-gradient(ellipse at 80% 80%,
                #35144e 0%, transparent 35%),
            linear-gradient(145deg, #030611, #080d20 65%, #09051b);
        perspective: 1000px;
    }

    /* Crisp star field */
    .stars {
        position: absolute;
        inset: 0;
        background-image:
            radial-gradient(2px 2px at 10% 15%, #ffffff 98%, transparent),
            radial-gradient(2px 2px at 28% 30%, #76eaff 98%, transparent),
            radial-gradient(2px 2px at 80% 12%, #ffffff 98%, transparent),
            radial-gradient(2px 2px at 90% 52%, #b6a1ff 98%, transparent),
            radial-gradient(2px 2px at 17% 75%, #78d8ff 98%, transparent),
            radial-gradient(2px 2px at 72% 85%, #ffffff 98%, transparent),
            radial-gradient(2px 2px at 53% 18%, #d5c6ff 98%, transparent),
            radial-gradient(1px 1px at 45% 68%, #ffffff 98%, transparent);
        background-size: 230px 190px;
        animation: starsMove 40s linear infinite;
    }

    /* Decorative planet */
    .planet {
        position: absolute;
        top: 8%;
        right: 8%;
        width: 58px;
        height: 58px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 25%,
            #ffffff, #83dfff 9%, #3677dc 40%, #08122d 85%);
        border: 1px solid #91dfff;
        box-shadow: 0 0 18px #277cff66;
    }

    .planet-ring {
        position: absolute;
        top: 18px;
        left: -15px;
        width: 88px;
        height: 24px;
        border: 2px solid #7d9dff;
        border-radius: 50%;
        transform: rotate(-20deg);
    }

    /* Globe and orbit system */
    .system {
        position: absolute;
        left: 50%;
        top: 36%;
        width: 270px;
        height: 250px;
        transform: translate(-50%, -50%);
        transform-style: preserve-3d;
        animation: float 5s ease-in-out infinite;
    }

    .globe {
        position: absolute;
        left: 50px;
        top: 25px;
        width: 170px;
        height: 170px;
        border-radius: 50%;
        overflow: hidden;
        border: 2px solid #8cefff;
        background:
            radial-gradient(circle at 30% 25%,
                #ffffff 0%, #a5f9ff 4%,
                #259de8 17%, #17499d 42%,
                #0b1c52 70%, #020716 100%);
        box-shadow:
            0 0 12px #16caff,
            0 0 28px #246dff66,
            inset -18px -15px 28px #02051a,
            inset 7px 5px 20px #9bf4ff77;
    }

    .globe-grid {
        position: absolute;
        inset: 0;
        border-radius: 50%;
        background:
            repeating-linear-gradient(
                0deg,
                transparent 0 20px,
                #a1f3ff55 21px,
                transparent 22px
            ),
            repeating-linear-gradient(
                90deg,
                transparent 0 24px,
                #a1f3ff44 25px,
                transparent 26px
            );
        animation: gridRotate 16s linear infinite;
    }

    .globe-label {
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
        font-size: 38px;
        font-weight: 900;
        color: white;
        text-shadow: 0 0 12px #48eaff;
    }

    .orbit {
        position: absolute;
        left: -12px;
        top: 57px;
        width: 294px;
        height: 105px;
        border: 2px solid #4bdfff;
        border-radius: 50%;
        transform: rotate(-25deg) rotateX(60deg);
    }

    .orbit.two {
        border-color: #a781ff;
        transform: rotate(40deg) rotateX(60deg);
        animation: orbitSpin 12s linear infinite;
    }

    .orbit.three {
        left: 15px;
        width: 240px;
        border-color: #5b9dff;
        transform: rotate(90deg) rotateX(65deg);
    }

    /* Sharp floating cards */
    .card {
        position: absolute;
        z-index: 5;
        width: 165px;
        padding: 13px;
        background: #071329;
        border: 1px solid #4e75bd;
        border-radius: 10px;
        box-shadow: 0 5px 15px #0008;
        color: #ffffff;
        font-size: 12px;
        animation: cardFloat 4s ease-in-out infinite;
    }

    .card strong {
        display: block;
        font-size: 13px;
        color: #7cecff;
        margin-bottom: 6px;
    }

    .c1 { left: 3%; top: 25%; }
    .c2 { right: 3%; top: 29%; animation-delay: -1s; }
    .c3 { left: 4%; top: 52%; animation-delay: -2s; }
    .c4 { right: 3%; top: 55%; animation-delay: -1.5s; }

    /* Hero text */
    .copy {
        position: absolute;
        left: 10px;
        right: 10px;
        bottom: 28px;
        text-align: center;
        z-index: 7;
    }

    .eyebrow {
        color: #72eaff;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    h1 {
        font-size: clamp(28px, 4vw, 44px);
        line-height: 1.15;
        margin: 0;
        font-weight: 900;
    }

    .gradient {
        background: linear-gradient(90deg, #43eaff, #a48bff, #f080ff);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .subtitle {
        max-width: 550px;
        margin: 12px auto 0;
        font-size: 13px;
        line-height: 1.6;
        color: #d4e0f8;
    }

    @keyframes float {
        0%, 100% {
            transform: translate(-50%, -50%) translateY(0);
        }
        50% {
            transform: translate(-50%, -50%) translateY(-9px);
        }
    }

    @keyframes orbitSpin {
        from {
            transform: rotate(40deg) rotateX(60deg) rotateZ(0);
        }
        to {
            transform: rotate(40deg) rotateX(60deg) rotateZ(360deg);
        }
    }

    @keyframes gridRotate {
        from { transform: rotate(0); }
        to { transform: rotate(360deg); }
    }

    @keyframes cardFloat {
        0%, 100% { translate: 0 0; }
        50% { translate: 0 -5px; }
    }

    @keyframes starsMove {
        from { background-position: 0 0; }
        to { background-position: 230px 190px; }
    }

    @media (max-width: 650px) {
        .scene { height: 620px; }
        .system {
            top: 34%;
            transform: translate(-50%, -50%) scale(.75);
        }
        .card {
            width: 125px;
            padding: 9px;
            font-size: 10px;
        }
        .card strong { font-size: 11px; }
        .c1 { left: 2%; top: 18%; }
        .c2 { right: 2%; top: 22%; }
        .c3 { left: 2%; top: 47%; }
        .c4 { right: 2%; top: 50%; }
        .copy { bottom: 20px; }
        h1 { font-size: 29px; }
    }
    </style>
    </head>

    <body>
    <div class="scene">
        <div class="stars"></div>

        <div class="planet">
            <div class="planet-ring"></div>
        </div>

        <div class="system">
            <div class="orbit"></div>
            <div class="orbit two"></div>
            <div class="orbit three"></div>

            <div class="globe">
                <div class="globe-grid"></div>
                <div class="globe-label">AI</div>
            </div>
        </div>

        <div class="card c1">
            <strong>✦ AI SCREENING</strong>
            Resume Analysis
        </div>

        <div class="card c2">
            <strong>◎ SKILL MATCH</strong>
            Smart Comparison
        </div>

        <div class="card c3">
            <strong>↗ INSIGHTS</strong>
            Candidate Data
        </div>

        <div class="card c4">
            <strong>★ RANKING</strong>
            Match Score
        </div>

        <div class="copy">
            <div class="eyebrow">
                ✦ NEXT-GEN INTELLIGENT RECRUITMENT
            </div>

            <h1>
                Find the right talent.<br>
                <span class="gradient">Powered by AI.</span>
            </h1>

            <p class="subtitle">
                Intelligent resume screening, skill matching
                and candidate ranking — all in one workspace.
            </p>
        </div>
    </div>
    </body>
    </html>
    """, height=620, scrolling=False)

    st.write("")
    st.subheader("Intelligence for every hiring step")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
        <h3>📄 Resume Screening</h3>
        <p>Upload PDF resumes and extract candidate information.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
        <h3>🧠 Skill Matching</h3>
        <p>Compare resumes with job requirements.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
        <h3>🏆 Candidate Ranking</h3>
        <p>Compare match scores and skill gaps.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    if st.button("🚀 Start Analyzing", use_container_width=True):
        st.session_state.page = "Upload Resumes"
        st.rerun()


# ==================================================
# UPLOAD RESUMES
# ==================================================

elif st.session_state.page == "Upload Resumes":

    st.markdown(
        '<div class="step-label">STEP 01 · RESUME INTAKE</div>',
        unsafe_allow_html=True
    )

    st.title("📄 Upload Candidate Resumes")
    st.write("Select multiple PDF resumes to begin screening.")

    files = st.file_uploader(
        "Choose PDF resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    if files:
        st.success(f"{len(files)} PDF file(s) selected.")

        for file in files:
            st.write("📄 " + file.name)

    if st.button("Save Resumes →", type="primary"):

        if not files:
            st.error("Please select at least one PDF resume.")

        else:
            extracted = []
            errors = []

            for file in files:
                try:
                    text = extract_resume_text(file)

                    if text and text.strip():
                        extracted.append({
                            "filename": file.name,
                            "text": text
                        })
                    else:
                        errors.append(
                            f"{file.name}: No readable text found."
                        )

                except Exception as exc:
                    errors.append(f"{file.name}: {exc}")

            for error in errors:
                st.warning(error)

            if extracted:
                st.session_state.resumes = extracted
                st.session_state.results = []

                st.success(
                    f"{len(extracted)} resume(s) processed successfully."
                )

                st.session_state.page = "Job Description"
                st.rerun()


# ==================================================
# JOB DESCRIPTION
# ==================================================

elif st.session_state.page == "Job Description":

    st.markdown(
        '<div class="step-label">STEP 02 · DEFINE THE ROLE</div>',
        unsafe_allow_html=True
    )

    st.title("💼 Job Description")

    if not st.session_state.resumes:

        st.warning("Upload resumes before continuing.")

        if st.button("Go to Resume Upload"):
            st.session_state.page = "Upload Resumes"
            st.rerun()

    else:

        st.info(
            f"{len(st.session_state.resumes)} resume(s) ready for analysis."
        )

        with st.form("job_details_form"):

            title = st.text_input(
                "Job Title",
                value=st.session_state.job_title,
                placeholder="e.g. Python Developer"
            )

            description = st.text_area(
                "Full Job Description",
                value=st.session_state.job_description,
                height=220,
                placeholder="Enter skills, qualifications and responsibilities..."
            )

            submitted = st.form_submit_button(
                "Save Job Requirements →",
                type="primary"
            )

            if submitted:

                if not title.strip():
                    st.error("Please enter a job title.")

                elif len(description.strip()) < 20:
                    st.error("Please enter a detailed job description.")

                else:
                    st.session_state.job_title = title.strip()
                    st.session_state.job_description = description.strip()
                    st.session_state.results = []
                    st.session_state.page = "Analyze & Compare"
                    st.rerun()


# ==================================================
# ANALYZE & COMPARE
# ==================================================

elif st.session_state.page == "Analyze & Compare":

    st.markdown(
        '<div class="step-label">STEP 03 · CANDIDATE INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.title("📊 Analyze & Compare")

    c1, c2 = st.columns(2)

    c1.metric("Resumes Ready", len(st.session_state.resumes))
    c2.metric("Job Role", st.session_state.job_title or "Not selected")

    if not st.session_state.resumes:

        st.info("Upload candidate resumes first.")

        if st.button("📤 Upload Resumes"):
            st.session_state.page = "Upload Resumes"
            st.rerun()

    elif not st.session_state.job_description:

        st.info("Add a job description before analysis.")

        if st.button("💼 Add Job Description"):
            st.session_state.page = "Job Description"
            st.rerun()

    else:

        st.markdown(f"**Selected role:** {st.session_state.job_title}")

        with st.expander("View Job Description"):
            st.write(st.session_state.job_description)

        if st.button("⚡ Run Analysis", type="primary"):

            try:
                with st.spinner("Analyzing resumes..."):
                    st.session_state.results = rank_resumes(
                        st.session_state.resumes,
                        st.session_state.job_description
                    )

            except Exception as exc:
                st.error(f"Analysis failed: {exc}")

        results = st.session_state.results

        if results:

            results = sorted(
                results,
                key=lambda item: float(item.get("score", 0)),
                reverse=True
            )

            st.divider()
            st.subheader("🏆 Candidate Ranking")

            top_score = float(results[0].get("score", 0))

            m1, m2, m3 = st.columns(3)

            m1.metric("Candidates Analyzed", len(results))
            m2.metric("Top Match Score", f"{top_score:.1f}%")
            m3.metric("Job Role", st.session_state.job_title)

            for index, result in enumerate(results, start=1):

                score = max(
                    0.0,
                    min(float(result.get("score", 0)), 100.0)
                )

                with st.container(border=True):

                    left, right = st.columns([4, 1])

                    with left:
                        st.markdown(
                            f"### #{result.get('rank', index)} · "
                            f"{result.get('filename', 'Unknown resume')}"
                        )
                        st.progress(score / 100)

                    with right:
                        st.metric("Match", f"{score:.1f}%")

                    matched = result.get("matched_skills", [])
                    missing = result.get("missing_skills", [])

                    st.write(
                        "**Matched Skills:** " +
                        (", ".join(matched) if matched else "None detected")
                    )

                    st.write(
                        "**Missing Skills:** " +
                        (", ".join(missing) if missing else "None detected")
                    )

                    st.caption(
                        "Text similarity: "
                        f"{float(result.get('similarity', 0)):.1f}%"
                    )

            st.subheader("📋 Ranking Summary")

            df = pd.DataFrame([
                {
                    "Rank": r.get("rank", i),
                    "Resume": r.get("filename", "Unknown"),
                    "Match Score (%)": round(
                        float(r.get("score", 0)), 1
                    ),
                    "Matched Skills": len(r.get("matched_skills", [])),
                    "Missing Skills": len(r.get("missing_skills", []))
                }
                for i, r in enumerate(results, start=1)
            ])

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "⬇ Download Ranking CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="candidate_ranking.csv",
                mime="text/csv"
            )

            st.caption(
                "Match scores are estimates, not final hiring decisions. "
                "Review resumes manually."
            )

            if st.button("Start New Analysis"):

                st.session_state.resumes = []
                st.session_state.job_title = ""
                st.session_state.job_description = ""
                st.session_state.results = []
                st.session_state.page = "Upload Resumes"
                st.rerun()
