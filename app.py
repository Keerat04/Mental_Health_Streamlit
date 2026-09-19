import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Mental Health Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 17px;
    margin-bottom: 25px;
}

.kpi-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
}

.kpi-title {
    color: #6b7280;
    font-size: 14px;
    font-weight: 600;
}

.kpi-value {
    font-size: 30px;
    font-weight: 750;
    margin-top: 5px;
}

.section-header {
    font-size: 25px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 12px;
}

.insight-box {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border-left: 5px solid #6366f1;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-title">🧠 Mental Health in Tech</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive Mental Health Survey Analytics Dashboard'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DATA UPLOAD
# =========================================================

st.sidebar.title("⚙️ Dashboard Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload survey.csv",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

else:
    try:
        df = pd.read_csv("survey.csv")
    except:
        st.info("👈 Upload survey.csv from the sidebar to start.")
        st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================

df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 19, 29, 39, 100],
    labels=["Under 20", "20-29", "30-39", "40+"]
)

# Remove obvious invalid ages
df_clean = df[
    (df["Age"].isna()) |
    ((df["Age"] >= 18) & (df["Age"] <= 100))
].copy()


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🔎 Filters")

# Country
country_list = sorted(
    df_clean["Country"].dropna().unique().tolist()
)

selected_country = st.sidebar.multiselect(
    "🌍 Country",
    country_list,
    default=country_list
)

# Gender
gender_list = sorted(
    df_clean["Gender"].dropna().unique().tolist()
)

selected_gender = st.sidebar.multiselect(
    "👤 Gender",
    gender_list,
    default=gender_list
)

# Treatment
treatment_list = sorted(
    df_clean["treatment"].dropna().unique().tolist()
)

selected_treatment = st.sidebar.multiselect(
    "🧠 Treatment",
    treatment_list,
    default=treatment_list
)

# Remote work
remote_list = sorted(
    df_clean["remote_work"].dropna().unique().tolist()
)

selected_remote = st.sidebar.multiselect(
    "💻 Remote Work",
    remote_list,
    default=remote_list
)

# Tech company
tech_list = sorted(
    df_clean["tech_company"].dropna().unique().tolist()
)

selected_tech = st.sidebar.multiselect(
    "🏢 Tech Company",
    tech_list,
    default=tech_list
)

# Family history
family_list = sorted(
    df_clean["family_history"].dropna().unique().tolist()
)

selected_family = st.sidebar.multiselect(
    "👨‍👩‍👧 Family History",
    family_list,
    default=family_list
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered = df_clean[
    df_clean["Country"].isin(selected_country)
    & df_clean["Gender"].isin(selected_gender)
    & df_clean["treatment"].isin(selected_treatment)
    & df_clean["remote_work"].isin(selected_remote)
    & df_clean["tech_company"].isin(selected_tech)
    & df_clean["family_history"].isin(selected_family)
].copy()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_people = len(filtered)

if total_people > 0:

    treatment_rate = (
        filtered["treatment"].eq("Yes").mean() * 100
    )

    remote_rate = (
        filtered["remote_work"].eq("Yes").mean() * 100
    )

    tech_rate = (
        filtered["tech_company"].eq("Yes").mean() * 100
    )

    family_rate = (
        filtered["family_history"].eq("Yes").mean() * 100
    )

    avg_age = filtered["Age"].mean()

else:

    treatment_rate = 0
    remote_rate = 0
    tech_rate = 0
    family_rate = 0
    avg_age = 0


# =========================================================
# KPI CARDS
# =========================================================

st.markdown(
    '<div class="section-header">📌 Executive Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-title">TOTAL RESPONDENTS</div>
        <div class="kpi-value">{total_people:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-title">TREATMENT RATE</div>
        <div class="kpi-value">{treatment_rate:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-title">REMOTE WORK</div>
        <div class="kpi-value">{remote_rate:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-title">TECH COMPANY</div>
        <div class="kpi-value">{tech_rate:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c5:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-title">AVERAGE AGE</div>
        <div class="kpi-value">{avg_age:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.caption(
    f"Showing {len(filtered):,} respondents from {len(df_clean):,} available records."
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "🧠 Treatment",
    "🏢 Workplace",
    "🌍 Demographics",
    "🔗 Relationships",
    "📋 Data Explorer"
])


# =========================================================
# TAB 1 - OVERVIEW
# =========================================================

with tab1:

    st.markdown(
        '<div class="section-header">📊 Survey Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # Treatment pie
    with col1:

        treatment_data = (
            filtered["treatment"]
            .value_counts()
            .reset_index()
        )

        treatment_data.columns = [
            "Treatment",
            "Count"
        ]

        fig = px.pie(
            treatment_data,
            names="Treatment",
            values="Count",
            hole=0.45,
            title="Mental Health Treatment"
        )

        fig.update_layout(
            margin=dict(t=60, b=20, l=20, r=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Gender
    with col2:

        gender_data = (
            filtered["Gender"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        gender_data.columns = [
            "Gender",
            "Count"
        ]

        fig = px.bar(
            gender_data,
            x="Gender",
            y="Count",
            title="Gender Distribution",
            text="Count"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Age
    st.markdown("### 👥 Age Distribution")

    age_data = filtered[
        filtered["Age"].notna()
    ]

    fig = px.histogram(
        age_data,
        x="Age",
        nbins=25,
        title="Respondent Age Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Remote + Tech
    col1, col2 = st.columns(2)

    with col1:

        remote_data = (
            filtered["remote_work"]
            .value_counts()
            .reset_index()
        )

        remote_data.columns = [
            "Remote Work",
            "Count"
        ]

        fig = px.bar(
            remote_data,
            x="Remote Work",
            y="Count",
            title="Remote Work"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        tech_data = (
            filtered["tech_company"]
            .value_counts()
            .reset_index()
        )

        tech_data.columns = [
            "Tech Company",
            "Count"
        ]

        fig = px.pie(
            tech_data,
            names="Tech Company",
            values="Count",
            hole=0.4,
            title="Tech Company Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 2 - TREATMENT
# =========================================================

with tab2:

    st.markdown(
        '<div class="section-header">🧠 Mental Health Treatment Analysis</div>',
        unsafe_allow_html=True
    )

    # Treatment chart
    treatment_cross = pd.crosstab(
        filtered["family_history"],
        filtered["treatment"],
        normalize="index"
    ) * 100

    treatment_cross = treatment_cross.reset_index()

    available_cols = [
        c for c in ["No", "Yes"]
        if c in treatment_cross.columns
    ]

    fig = px.bar(
        treatment_cross,
        x="family_history",
        y=available_cols,
        barmode="group",
        title="Family History vs Treatment (%)",
        labels={
            "family_history": "Family History",
            "value": "Percentage"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Work interference
    st.markdown("### 💼 Work Interference")

    work_cross = pd.crosstab(
        filtered["work_interfere"],
        filtered["treatment"],
        normalize="index"
    ) * 100

    work_cross = work_cross.reset_index()

    available_cols = [
        c for c in ["No", "Yes"]
        if c in work_cross.columns
    ]

    fig = px.bar(
        work_cross,
        x="work_interfere",
        y=available_cols,
        barmode="group",
        title="Work Interference vs Treatment (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Benefits
    st.markdown("### 🏥 Mental Health Benefits")

    benefits_cross = pd.crosstab(
        filtered["benefits"],
        filtered["treatment"],
        normalize="index"
    ) * 100

    benefits_cross = benefits_cross.reset_index()

    available_cols = [
        c for c in ["No", "Yes"]
        if c in benefits_cross.columns
    ]

    fig = px.bar(
        benefits_cross,
        x="benefits",
        y=available_cols,
        barmode="group",
        title="Benefits vs Treatment (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Care options
    st.markdown("### 🩺 Care Options")

    care_cross = pd.crosstab(
        filtered["care_options"],
        filtered["treatment"],
        normalize="index"
    ) * 100

    care_cross = care_cross.reset_index()

    available_cols = [
        c for c in ["No", "Yes"]
        if c in care_cross.columns
    ]

    fig = px.bar(
        care_cross,
        x="care_options",
        y=available_cols,
        barmode="group",
        title="Care Options vs Treatment (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Consequences
    st.markdown("### ⚠️ Mental Health Consequences")

    consequence_cross = pd.crosstab(
        filtered["mental_health_consequence"],
        filtered["treatment"],
        normalize="index"
    ) * 100

    consequence_cross = consequence_cross.reset_index()

    available_cols = [
        c for c in ["No", "Yes"]
        if c in consequence_cross.columns
    ]

    fig = px.bar(
        consequence_cross,
        x="mental_health_consequence",
        y=available_cols,
        barmode="group",
        title="Mental Health Consequence vs Treatment (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TAB 3 - WORKPLACE
# =========================================================

with tab3:

    st.markdown(
        '<div class="section-header">🏢 Workplace Environment</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # Benefits
    with col1:

        data = filtered["benefits"].value_counts().reset_index()
        data.columns = ["Benefits", "Count"]

        fig = px.pie(
            data,
            names="Benefits",
            values="Count",
            hole=0.45,
            title="Mental Health Benefits"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Wellness
    with col2:

        data = (
            filtered["wellness_program"]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "Wellness Program",
            "Count"
        ]

        fig = px.bar(
            data,
            x="Wellness Program",
            y="Count",
            title="Workplace Wellness Programs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Seek help
    data = (
        filtered["seek_help"]
        .value_counts()
        .reset_index()
    )

    data.columns = [
        "Seek Help",
        "Count"
    ]

    fig = px.bar(
        data,
        x="Seek Help",
        y="Count",
        title="Workplace Support for Seeking Help"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Anonymity
    col1, col2 = st.columns(2)

    with col1:

        data = (
            filtered["anonymity"]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "Anonymity",
            "Count"
        ]

        fig = px.bar(
            data,
            x="Anonymity",
            y="Count",
            title="Perceived Anonymity"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        data = (
            filtered["leave"]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "Leave",
            "Count"
        ]

        fig = px.bar(
            data,
            x="Leave",
            y="Count",
            title="Ease of Taking Mental Health Leave"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Coworkers / supervisors
    col1, col2 = st.columns(2)

    with col1:

        data = (
            filtered["coworkers"]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "Coworkers",
            "Count"
        ]

        fig = px.bar(
            data,
            x="Coworkers",
            y="Count",
            title="Talking to Coworkers"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        data = (
            filtered["supervisor"]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "Supervisor",
            "Count"
        ]

        fig = px.bar(
            data,
            x="Supervisor",
            y="Count",
            title="Talking to Supervisors"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 4 - DEMOGRAPHICS
# =========================================================

with tab4:

    st.markdown(
        '<div class="section-header">🌍 Demographic Analysis</div>',
        unsafe_allow_html=True
    )

    # Age groups
    age_group_data = (
        filtered["Age_Group"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    age_group_data.columns = [
        "Age Group",
        "Count"
    ]

    fig = px.bar(
        age_group_data,
        x="Age Group",
        y="Count",
        text="Count",
        title="Respondents by Age Group"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Age vs treatment
    age_treatment = pd.crosstab(
        filtered["Age_Group"],
        filtered["treatment"]
    ).reset_index()

    available_cols = [
        c for c in ["No", "Yes"]
        if c in age_treatment.columns
    ]

    fig = px.bar(
        age_treatment,
        x="Age_Group",
        y=available_cols,
        barmode="group",
        title="Age Group vs Treatment"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Gender vs treatment
    gender_treatment = pd.crosstab(
        filtered["Gender"],
        filtered["treatment"]
    ).reset_index()

    available_cols = [
        c for c in ["No", "Yes"]
        if c in gender_treatment.columns
    ]

    fig = px.bar(
        gender_treatment,
        x="Gender",
        y=available_cols,
        barmode="group",
        title="Gender vs Treatment"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Country
    country_data = filtered["Country"].value_counts().head(15)

    country_data = country_data.reset_index()

    country_data.columns = [
        "Country",
        "Respondents"
    ]

    fig = px.bar(
        country_data,
        x="Respondents",
        y="Country",
        orientation="h",
        title="Top Countries by Respondents"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TAB 5 - RELATIONSHIPS
# =========================================================

with tab5:

    st.markdown(
        '<div class="section-header">🔗 Relationship Analysis</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore how different survey variables relate to mental health treatment."
    )


    # Family history treatment rate
    family_rate = (
        filtered.groupby("family_history")["treatment"]
        .apply(lambda x: (x == "Yes").mean() * 100)
        .reset_index()
    )

    family_rate.columns = [
        "Family History",
        "Treatment Rate"
    ]

    fig = px.bar(
        family_rate,
        x="Family History",
        y="Treatment Rate",
        text="Treatment Rate",
        title="Treatment Rate by Family History"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Work interference treatment rate
    work_rate = (
        filtered.groupby("work_interfere")["treatment"]
        .apply(lambda x: (x == "Yes").mean() * 100)
        .reset_index()
    )

    work_rate.columns = [
        "Work Interference",
        "Treatment Rate"
    ]

    fig = px.bar(
        work_rate,
        x="Work Interference",
        y="Treatment Rate",
        text="Treatment Rate",
        title="Treatment Rate by Work Interference"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Remote work treatment
    remote_treatment = (
        filtered.groupby("remote_work")["treatment"]
        .apply(lambda x: (x == "Yes").mean() * 100)
        .reset_index()
    )

    remote_treatment.columns = [
        "Remote Work",
        "Treatment Rate"
    ]

    fig = px.bar(
        remote_treatment,
        x="Remote Work",
        y="Treatment Rate",
        text="Treatment Rate",
        title="Treatment Rate by Remote Work"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Family history + treatment table
    st.markdown("### 📊 Treatment Cross-Tabulation")

    cross = pd.crosstab(
        filtered["family_history"],
        filtered["treatment"]
    )

    st.dataframe(
        cross,
        use_container_width=True
    )


# =========================================================
# TAB 6 - DATA EXPLORER
# =========================================================

with tab6:

    st.markdown(
        '<div class="section-header">📋 Data Explorer</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore the filtered survey records."
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        height=550
    )


    # Download
    csv_data = filtered.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Filtered Dataset",
        data=csv_data,
        file_name="mental_health_filtered.csv",
        mime="text/csv"
    )


# =========================================================
# DATA QUALITY
# =========================================================

with st.expander("🔍 Data Quality Information"):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rows",
            len(df)
        )

    with col2:
        st.metric(
            "Columns",
            len(df.columns)
        )

    with col3:
        st.metric(
            "Duplicate Rows",
            df.duplicated().sum()
        )

    missing = (
        df.isnull()
        .sum()
        .sort_values(ascending=False)
    )

    missing = missing[
        missing > 0
    ]

    st.subheader("Missing Values")

    if len(missing) > 0:
        st.dataframe(
            missing.rename("Missing Values"),
            use_container_width=True
        )
    else:
        st.success("No missing values.")


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Mental Health in Tech Survey • Interactive EDA Dashboard"
)