import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DARK DASHBOARD STYLE
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background: #0B1120;
        color: #E5E7EB;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .main-title {
        color: #F8FAFC !important;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .main-subtitle {
        color: #94A3B8 !important;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .section-title {
        color: #F8FAFC !important;
        font-size: 25px;
        font-weight: 750;
        margin-top: 28px;
        margin-bottom: 16px;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background: #111827 !important;
        border: 1px solid #273449 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 6px 18px rgba(0,0,0,.25);
    }

    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 800 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827 !important;
        border-right: 1px solid #273449;
    }

    section[data-testid="stSidebar"] * {
        color: #E5E7EB;
    }

    /* Insight cards - strong selectors prevent white cards */
    div.insight-card {
        background-color: #111827 !important;
        background: #111827 !important;
        border: 1px solid #273449 !important;
        border-left: 5px solid #6366F1 !important;
        border-radius: 14px !important;
        padding: 20px !important;
        min-height: 145px;
        margin-bottom: 16px;
        box-shadow: 0 6px 18px rgba(0,0,0,.22);
    }

    div.insight-card .insight-title {
        color: #F8FAFC !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }

    div.insight-card .insight-text {
        color: #CBD5E1 !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    div.insight-card .insight-text b {
        color: #FFFFFF !important;
    }

    div[data-testid="stExpander"] {
        background: #111827 !important;
        border: 1px solid #273449 !important;
        border-radius: 12px !important;
    }

    hr {
        border-color: #273449 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv("data/cleaned_student_data.csv")

# ============================================================
# LABELS
# ============================================================
studytime_labels = {
    1: "< 2 hours",
    2: "2–5 hours",
    3: "5–10 hours",
    4: "> 10 hours",
}

mother_education_labels = {
    0: "None",
    1: "Primary",
    2: "5th–9th Grade",
    3: "Secondary",
    4: "Higher Education",
}

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.markdown(
    """
    <h1 style="color:#F8FAFC;">🔎 Dashboard Filters</h1>
    <p style="color:#94A3B8;">Use the filters to explore different student groups.</p>
    """,
    unsafe_allow_html=True,
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["sex"].dropna().unique()),
    default=sorted(df["sex"].dropna().unique()),
    format_func=lambda x: {"F": "Female", "M": "Male"}.get(x, str(x)),
)

selected_school = st.sidebar.multiselect(
    "School",
    options=sorted(df["school"].dropna().unique()),
    default=sorted(df["school"].dropna().unique()),
    format_func=lambda x: {
        "GP": "Gabriel Pereira",
        "MS": "Mousinho da Silveira",
    }.get(x, str(x)),
)

studytime_options = sorted(df["studytime"].dropna().unique())
selected_studytime = st.sidebar.multiselect(
    "Study Time",
    options=studytime_options,
    default=studytime_options,
    format_func=lambda x: studytime_labels.get(x, str(x)),
)

# ============================================================
# FILTER DATA
# ============================================================
filtered_df = df[
    df["sex"].isin(selected_gender)
    & df["school"].isin(selected_school)
    & df["studytime"].isin(selected_studytime)
].copy()

if filtered_df.empty:
    st.warning("⚠️ No students match the selected filters.")
    st.stop()

# ============================================================
# COMMON PLOT STYLE
# ============================================================
PLOT_BG = "#111827"
GRID = "#374151"
TEXT = "#CBD5E1"
TITLE = "#F8FAFC"
PRIMARY = "#6366F1"
SECONDARY = "#8B5CF6"
CYAN = "#22D3EE"


def style_figure(fig, height=430, title_size=18, bottom=65):
    fig.update_layout(
        height=height,
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT, size=13),
        title=dict(font=dict(color=TITLE, size=title_size), x=0),
        margin=dict(l=55, r=25, t=70, b=bottom),
        legend=dict(font=dict(color=TEXT)),
    )
    fig.update_xaxes(
        color=TEXT,
        gridcolor=GRID,
        zerolinecolor=GRID,
        title_font=dict(color=TEXT),
    )
    fig.update_yaxes(
        color=TEXT,
        gridcolor=GRID,
        zerolinecolor=GRID,
        title_font=dict(color=TEXT),
    )
    return fig

# ============================================================
# HEADER
# ============================================================
st.markdown(
    '<div class="main-title">🎓 Student Performance Analytics</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="main-subtitle">Interactive dashboard for analysing academic performance, study habits, attendance and student characteristics.</div>',
    unsafe_allow_html=True,
)

# ============================================================
# KPI SECTION
# ============================================================
st.markdown(
    '<div class="section-title">📊 Performance Overview</div>',
    unsafe_allow_html=True,
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("👥 Total Students", len(filtered_df))
with k2:
    st.metric("📈 Average Final Grade", f"{filtered_df['G3'].mean():.2f}")
with k3:
    st.metric("🏆 Highest Final Grade", int(filtered_df["G3"].max()))
with k4:
    st.metric("📉 Lowest Final Grade", int(filtered_df["G3"].min()))

# ============================================================
# ACADEMIC PERFORMANCE
# ============================================================
st.markdown(
    '<div class="section-title">📚 Academic Performance Analysis</div>',
    unsafe_allow_html=True,
)

# 1. FINAL GRADE - BAR GRAPH
# This replaces the old histogram with one bar for every final grade.
grade_counts = (
    filtered_df["G3"]
    .value_counts()
    .sort_index()
    .rename_axis("Final Grade")
    .reset_index(name="Number of Students")
)

fig1 = px.bar(
    grade_counts,
    x="Final Grade",
    y="Number of Students",
    text="Number of Students",
    title="Final Grade Distribution",
)
fig1.update_traces(
    marker_color=PRIMARY,
    textposition="outside",
    cliponaxis=False,
)
style_figure(fig1, height=430, title_size=20, bottom=60)
fig1.update_xaxes(dtick=1, title="Final Grade")
fig1.update_yaxes(title="Number of Students")

st.plotly_chart(fig1, use_container_width=True, key="grade_distribution")

# ============================================================
# STUDY TIME + PREVIOUS FAILURES
# ============================================================
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    studytime_avg = (
        filtered_df.groupby("studytime", as_index=False)["G3"]
        .mean()
        .sort_values("studytime")
    )
    studytime_avg["Study Time"] = studytime_avg["studytime"].map(studytime_labels)

    fig2 = px.bar(
        studytime_avg,
        x="Study Time",
        y="G3",
        text="G3",
        title="Average Grade by Study Time",
    )
    fig2.update_traces(
        marker_color=CYAN,
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False,
    )
    style_figure(fig2, bottom=75)
    fig2.update_yaxes(title="Average Final Grade")
    fig2.update_xaxes(title="Study Time")
    st.plotly_chart(fig2, use_container_width=True, key="studytime_chart")

with chart_col2:
    failure_avg = (
        filtered_df.groupby("failures", as_index=False)["G3"]
        .mean()
        .sort_values("failures")
    )
    failure_avg["Failure Category"] = failure_avg["failures"].apply(
        lambda x: "None" if x == 0 else f"{int(x)} failure" if x == 1 else f"{int(x)} failures"
    )

    fig3 = px.bar(
        failure_avg,
        x="Failure Category",
        y="G3",
        text="G3",
        title="Average Grade by Previous Failures",
    )
    fig3.update_traces(
        marker_color=SECONDARY,
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False,
    )
    style_figure(fig3, bottom=75)
    fig3.update_yaxes(title="Average Final Grade")
    fig3.update_xaxes(title="Previous Failures")
    st.plotly_chart(fig3, use_container_width=True, key="failures_chart")

# ============================================================
# ATTENDANCE / STUDENT CHARACTERISTICS
# ============================================================
st.markdown(
    '<div class="section-title">📅 Attendance & Student Characteristics</div>',
    unsafe_allow_html=True,
)

# 4. ABSENCES VS FINAL GRADE - SCATTER
fig4 = px.scatter(
    filtered_df,
    x="absences",
    y="G3",
    title="Absences vs Final Grade",
    labels={"absences": "Number of Absences", "G3": "Final Grade"},
    opacity=0.75,
)
fig4.update_traces(
    marker=dict(size=9, color=CYAN, line=dict(width=1, color="#A5F3FC"))
)
style_figure(fig4, height=430, title_size=20, bottom=60)
st.plotly_chart(fig4, use_container_width=True, key="absences_chart")

# 5 + 6. GENDER / MOTHER EDUCATION
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    gender_avg = (
        filtered_df.groupby("sex", as_index=False)["G3"]
        .mean()
    )
    gender_avg["Gender"] = gender_avg["sex"].map({"F": "Female", "M": "Male"})

    fig5 = px.bar(
        gender_avg,
        x="Gender",
        y="G3",
        text="G3",
        title="Average Grade by Gender",
    )
    fig5.update_traces(
        marker_color=PRIMARY,
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False,
    )
    style_figure(fig5, bottom=65)
    fig5.update_yaxes(title="Average Final Grade")
    fig5.update_xaxes(title="Gender")
    st.plotly_chart(fig5, use_container_width=True, key="gender_chart")

with chart_col4:
    mother_avg = (
        filtered_df.groupby("Medu", as_index=False)["G3"]
        .mean()
        .sort_values("Medu")
    )
    mother_avg["Mother's Education"] = mother_avg["Medu"].map(mother_education_labels)

    fig6 = px.bar(
        mother_avg,
        x="Mother's Education",
        y="G3",
        text="G3",
        title="Average Grade by Mother's Education",
    )
    fig6.update_traces(
        marker_color=SECONDARY,
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False,
    )
    style_figure(fig6, bottom=95)
    fig6.update_yaxes(title="Average Final Grade")
    fig6.update_xaxes(title="Mother's Education", tickangle=-20)
    st.plotly_chart(fig6, use_container_width=True, key="parent_education_chart")

# ============================================================
# KEY INSIGHTS
# ============================================================
st.markdown(
    '<div class="section-title">💡 Key Insights</div>',
    unsafe_allow_html=True,
)

overall_avg = filtered_df["G3"].mean()

studytime_avg_insight = filtered_df.groupby("studytime")["G3"].mean()
best_studytime = studytime_avg_insight.idxmax()
best_studytime_grade = studytime_avg_insight.max()

if filtered_df["absences"].nunique() > 1:
    absence_corr = filtered_df["absences"].corr(filtered_df["G3"])
else:
    absence_corr = 0.0

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">📊 Overall Performance</div>
            <div class="insight-text">
                The average final grade for the selected students is
                <b>{overall_avg:.2f}</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with insight_col2:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">📉 Attendance Relationship</div>
            <div class="insight-text">
                The correlation between absences and final grade is
                <b>{absence_corr:.2f}</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

insight_col3, insight_col4 = st.columns(2)

with insight_col3:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">📚 Study Time</div>
            <div class="insight-text">
                The <b>{studytime_labels.get(best_studytime, best_studytime)}</b>
                group has the highest average final grade of
                <b>{best_studytime_grade:.2f}</b> among the selected groups.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with insight_col4:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">🔎 Dynamic Analysis</div>
            <div class="insight-text">
                These insights automatically update whenever the dashboard filters are changed.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# FILTERED DATA
# ============================================================
with st.expander("📋 View Filtered Student Data"):
    st.dataframe(filtered_df, use_container_width=True, height=420)

# ============================================================
# PROJECT INFORMATION
# ============================================================
st.markdown("---")

info1, info2, info3 = st.columns(3)

with info1:
    st.markdown(
        """
        <h2 style="color:#F8FAFC;">🎯 Project</h2>
        <p style="color:#CBD5E1;">Student Performance Analysis Dashboard</p>
        <p style="color:#94A3B8;">Interactive analysis of academic performance and student characteristics.</p>
        """,
        unsafe_allow_html=True,
    )

with info2:
    st.markdown(
        """
        <h2 style="color:#F8FAFC;">🛠️ Technologies</h2>
        <p style="color:#CBD5E1;">Python • Pandas • Plotly • Streamlit</p>
        <p style="color:#94A3B8;">Git & GitHub used for version control and open-source workflow.</p>
        """,
        unsafe_allow_html=True,
    )

with info3:
    st.markdown(
        """
        <h2 style="color:#F8FAFC;">📁 Dataset</h2>
        <p style="color:#CBD5E1;">UCI Student Performance Dataset</p>
        <p style="color:#94A3B8;">The dashboard uses cleaned student performance data for analysis.</p>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div style="text-align:center; color:#64748B; margin-top:35px; font-size:13px;">
        Student Performance Analytics Dashboard • Academic Project
    </div>
    """,
    unsafe_allow_html=True,
)
