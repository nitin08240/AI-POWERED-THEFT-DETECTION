
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import warnings


# Suppress scikit-learn version warnings
warnings.filterwarnings('ignore', category=UserWarning)

st.set_page_config(
    page_title="AI Electricity Theft Prevention",
    layout="wide"
)

# Load models
model = joblib.load("electricity_theft_model (1).pkl")
scaler = joblib.load("scaler (1).pkl")

# Load dashboard data - Fixed filename (removed extra space)
dashboard_df = pd.read_csv("dashboard_data .csv")
df = dashboard_df.copy()

tab1, tab2 = st.tabs([
    "📊 Strategic Dashboard",
    "🔮 Live Prediction"
])

with tab1:
    # ================= SIDEBAR =================
    st.sidebar.title("⚙️ Control Panel")

    area_filter = st.sidebar.multiselect(
        "Select Area",
        df['AREA_ID'].unique(),
        default=df['AREA_ID'].unique()
    )

    risk_filter = st.sidebar.multiselect(
        "Select Risk Level",
        df['risk_level'].unique(),
        default=df['risk_level'].unique()
    )

    df_filtered = df[
        (df['AREA_ID'].isin(area_filter)) &
        (df['risk_level'].isin(risk_filter))
    ]

    # ================= HEADER =================
    st.title("⚡ AI-Powered Electricity Theft Prevention System")
    st.markdown(
        "An intelligent decision-support platform for power utilities"
    )

    # ================= KPIs =================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Consumers", len(df_filtered))
    col2.metric("High Risk Cases", len(df_filtered[df_filtered['risk_level']=="High"]))
    col3.metric("Total Estimated Loss (₹)", int(df_filtered['estimated_loss'].sum()))
    col4.metric("Areas Monitored", df_filtered['AREA_ID'].nunique())

    # ================= AREA ANALYSIS =================
    st.subheader("📍 Area-Wise Risk Overview")

    area_summary = df_filtered.groupby('AREA_ID').agg({
        'risk_score':'mean',
        'estimated_loss':'sum'
    })

    st.bar_chart(area_summary)

    # ================= HIGH RISK TABLE =================
    st.subheader("🚨 High Priority Consumers")

    high_risk = df_filtered[df_filtered['risk_level']=="High"].sort_values(
        by='estimated_loss', ascending=False
    )

    st.dataframe(
        high_risk[[
            'CONS_NO','AREA_ID','risk_score',
            'estimated_loss','theft_reason'
        ]]
    )

    # ================= INSPECTION PRIORITY =================
    st.subheader("🛠 Inspection Priority List")

    df_filtered['inspection_priority'] = df_filtered['risk_score'] * df_filtered['estimated_loss']

    priority = df_filtered.sort_values(
        by='inspection_priority', ascending=False
    ).head(10)

    st.table(
        priority[['CONS_NO','AREA_ID','inspection_priority']]
    )

    # ================= EXPLAINABLE AI =================
    st.subheader("🧠 Explainable AI – Why is this flagged?")

    selected = st.selectbox(
        "Select Consumer ID",
        df['CONS_NO'].unique()
    )

    selected_data = df[df['CONS_NO']==selected]
    if not selected_data.empty:
        reason = selected_data['theft_reason'].values[0]
        st.info(reason)
    else:
        st.warning("No data available for selected consumer")

    # ================= FOOTER =================
    st.markdown("---")
    st.caption("Built for Smart Utilities | AI + Decision Intelligence")

with tab2:
    st.title("🔮 Real-Time Theft Prediction")

    uploaded = st.file_uploader(
        "Upload New Consumer Usage CSV",
        type=["csv"]
    )

    if uploaded:
        new_df = pd.read_csv(uploaded)

        # -------- Feature Engineering --------
        X_time = new_df.iloc[:, 2:]
        X_time = X_time.apply(
            pd.to_numeric, errors='coerce'
        ).fillna(0)

        new_df['mean_usage'] = X_time.mean(axis=1)
        new_df['std_usage']  = X_time.std(axis=1)
        new_df['min_usage']  = X_time.min(axis=1)
        new_df['max_usage']  = X_time.max(axis=1)
        new_df['usage_drop'] = X_time.diff(axis=1).abs().mean(axis=1)
        new_df['zero_ratio'] = (
            X_time == 0
        ).sum(axis=1) / X_time.shape[1]

        # Area neutral assumption
        new_df['AREA_USAGE_RATIO'] = 1

        features = [
            'mean_usage','std_usage','min_usage',
            'max_usage','usage_drop',
            'zero_ratio','AREA_USAGE_RATIO'
        ]

        X = scaler.transform(new_df[features])

        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1]

        if prediction == 1:
            st.error(
                f"⚠️ Theft Risk Detected "
                f"(Confidence: {probability:.2f})"
            )
        else:
            st.success(
                f"✅ Normal Usage "
                f"(Confidence: {1-probability:.2f})"
            )