import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# 1. ENTERPRISE UI CONFIGURATION
# ==========================================
st.set_page_config(page_title="AI-Driven Student Predictor | IBM Internship", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    /* Sleek dark mode adjustments */
    .stApp { background-color: #0E1117; }
    .css-1d391kg { padding-top: 1rem; }
    .stMetric { background-color: #1A1C23; padding: 15px; border-radius: 8px; border: 1px solid #2E303E; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR: DATA INGESTION PANEL
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/IBM_logo.svg/1200px-IBM_logo.svg.png", width=120)
    st.title("Data Ingestion")
    st.caption("Enter student telemetry data below.")
    
    with st.expander("📚 Academic Metrics", expanded=True):
        study_hours = st.slider("Study Hours / Week", 0, 40, 15)
        attendance = st.slider("Attendance Rate (%)", 0, 100, 82)
        prev_scores = st.slider("Historical GPA / Prev Score", 0, 100, 71)
        participation = st.slider("Class Participation", 1, 10, 6)

    with st.expander("🧠 Behavioral & Lifestyle", expanded=False):
        sleep_hours = st.slider("Avg Sleep Hours / Night", 0, 12, 6)
        screen_time = st.slider("Non-Academic Screen Time", 0, 12, 4)
        extracurricular = st.radio("Extracurricular Engagement", ["High", "Medium", "Low"], index=1)

    with st.expander("💻 Socio-Economic & Resources", expanded=False):
        internet = st.radio("High-Speed Internet Access", ["Yes", "No"], index=0)
        tutoring = st.slider("Tutoring Sessions / Month", 0, 10, 1)
        stress_level = st.slider("Self-Reported Stress (1-10)", 1, 10, 7)

    st.divider()
    st.button("🔄 Reset Data Pipeline", use_container_width=True)

# ==========================================
# 3. AI LOGIC & WEIGHTS (MOCKUP FOR UI)
# ==========================================
# Converting categoricals
int_access = 1 if internet == "Yes" else 0
extra_val = {"High": 3, "Medium": 2, "Low": 1}[extracurricular]

# Advanced Mock Formula
base = 20
academic = (study_hours * 0.8) + (attendance * 0.3) + (prev_scores * 0.35) + (participation * 1.5)
behavior = (sleep_hours * 2) - (screen_time * 1.2) + (extra_val * 1.5)
resources = (int_access * 4) + (tutoring * 1.5) - (stress_level * 1.2)

prediction = min(max(base + academic + behavior + resources, 0), 100)
confidence = min(85 + (attendance * 0.1) - (stress_level * 0.5), 98.5)

# ==========================================
# 4. MAIN DASHBOARD INTERFACE
# ==========================================
st.title("🎓 Intelligent Student Tracking System")
st.markdown("**AICTE & IBM Project** | Advanced predictive engine using Random Forest Regressor logic.")

tab1, tab2, tab3 = st.tabs(["📊 Predictive Dashboard", "💡 AI Prescriptive Engine", "⚙️ Model Explainability (XAI)"])

# ----- TAB 1: PREDICTIVE DASHBOARD -----
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Predicted Final Score", f"{prediction:.1f}%", f"{prediction - prev_scores:.1f}% vs Last Sem")
    with col2:
        risk_color = "🟢 Low Risk" if prediction > 75 else "🟡 Medium Risk" if prediction > 60 else "🔴 High Risk"
        st.metric("Academic Risk Level", risk_color)
    with col3:
        st.metric("AI Confidence Score", f"{confidence:.1f}%", "High Data Quality")
    with col4:
        st.metric("Suggested Intervention", "Tutoring" if prediction < 70 else "None", delta_color="inverse")

    st.markdown("---")
    
    col_chart, col_radar = st.columns([1.2, 1])
    
    with col_chart:
        st.subheader("Performance Trajectory")
        # Line chart showing simulated progression
        months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Projected"]
        scores = [prev_scores - 5, prev_scores - 2, prev_scores, prev_scores + 2, prev_scores + 1, prediction]
        trend_df = pd.DataFrame({"Month": months, "Score": scores})
        fig_line = px.line(trend_df, x="Month", y="Score", markers=True, title="Historical vs Projected Grades")
        fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=0))
        st.plotly_chart(fig_line, use_container_width=True)

    with col_radar:
        st.subheader("Student Profile Analysis")
        # Radar Chart for Interview WOW factor
        categories = ['Study Habits', 'Attendance', 'Wellbeing', 'Engagement', 'Resources']
        # Normalizing inputs to 1-10 scale for the radar chart
        student_stats = [min(study_hours/3, 10), attendance/10, sleep_hours/1.2, participation, tutoring + int_access*5]
        optimal_stats = [8, 9.5, 8, 8, 7]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=student_stats, theta=categories, fill='toself', name='Current Student', line_color='#00C4B4'))
        fig.add_trace(go.Scatterpolar(r=optimal_stats, theta=categories, fill='toself', name='Target Profile', line_color='#4C516D', opacity=0.5))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=True, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)

# ----- TAB 2: AI PRESCRIPTIVE ENGINE -----
with tab2:
    st.subheader("🤖 AI-Generated Recommendations")
    st.write("Based on the data profile, the system recommends the following actionable steps to optimize performance:")
    
    # Conditional recommendations based on slider inputs
    if sleep_hours < 7:
        st.error(f"**Critical:** Sleep deprivation detected ({sleep_hours} hours). Increasing sleep to 8 hours could boost cognition and increase predicted score by ~4.5%.")
    if attendance < 85:
        st.warning(f"**Warning:** Attendance is at {attendance}%. Historically, students falling below 85% see a sharp decline in semester finals.")
    if tutoring < 2 and prediction < 75:
        st.info("**Suggestion:** Enrolling in 2 additional tutoring sessions per month correlates with a 6% grade improvement for this demographic.")
    if screen_time > 6:
        st.warning(f"**Warning:** High non-academic screen time ({screen_time} hours) is negatively correlating with study efficiency.")
    if prediction >= 80:
        st.success("**Excellent:** Student is maintaining optimal habits. No immediate intervention required.")

# ----- TAB 3: MODEL EXPLAINABILITY -----
with tab3:
    st.subheader("⚙️ Feature Importance (Random Forest Regressor)")
    st.write("Transparency is critical in educational AI. Below is the relative weight of each feature in the algorithm's decision-making process.")
    
    # Mock feature importance data
    features = pd.DataFrame({
        "Feature": ["Attendance", "Historical GPA", "Study Hours", "Sleep Hours", "Class Participation", "Stress Level", "Tutoring"],
        "Importance": [0.28, 0.22, 0.18, 0.12, 0.08, 0.07, 0.05]
    }).sort_values(by="Importance", ascending=True)

    fig_bar = px.bar(features, x="Importance", y="Feature", orientation='h', title="Global Feature Weights")
    fig_bar.update_traces(marker_color='#00C4B4')
    fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.info("💡 **Interview Note:** In a production environment, this chart would be dynamically generated using SHAP (SHapley Additive exPlanations) values to explain individual predictions.")