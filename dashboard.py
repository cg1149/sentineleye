import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "data/sentineleye.db"

def get_scans():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM scans ORDER BY timestamp DESC", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df

st.set_page_config(page_title="SentinelEye", page_icon="🛡️", layout="wide")
st.title("🛡️ SentinelEye Dashboard")
st.subheader("Real-time AI Security Monitor")

df = get_scans()

if df.empty:
    st.warning("No scans yet. Run main.py first!")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Scans", len(df))
    with col2:
        high = len(df[df["threat_level"] == "HIGH"])
        st.metric("HIGH Threats", high)
    with col3:
        medium = len(df[df["threat_level"] == "MEDIUM"])
        st.metric("MEDIUM Threats", medium)
    with col4:
        if "confidence" in df.columns:
            avg_conf = int(df["confidence"].mean())
            st.metric("Avg Confidence", f"{avg_conf}%")

    st.divider()

    st.subheader("Threat Level Breakdown")
    threat_counts = df["threat_level"].value_counts()
    st.bar_chart(threat_counts)

    st.divider()

    st.subheader("Recent Scans")
    for _, row in df.head(10).iterrows():
        if row["threat_level"] == "HIGH":
            color = "🔴"
        elif row["threat_level"] == "MEDIUM":
            color = "🟡"
        else:
            color = "🟢"

        conf = row.get("confidence", "N/A")
        with st.expander(f"{color} {row['threat_level']} — {row['timestamp']} — Confidence: {conf}%"):
            st.write(f"**Type:** {row['threat_type']}")
            st.write(f"**Description:** {row['description']}")
            if "reason" in row and row["reason"]:
                st.write(f"**Reason:** {row['reason']}")
            st.write(f"**Action:** {row['action']}")
