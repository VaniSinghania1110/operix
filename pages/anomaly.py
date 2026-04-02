import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="SpendGuard")

st.markdown("""
<style>
html, body, .stApp {
    background:#04080f;
    color:#e0eaf8;
}
</style>
""", unsafe_allow_html=True)

st.title("SpendGuard")
st.subheader("Cloud Spend Anomaly Detection Agent")

uploaded = st.file_uploader("Upload spend CSV", type=["csv"])

st.markdown("CSV should contain:")
st.code("service,previous_cost,current_cost")

sample = pd.DataFrame({
    "service": ["EC2", "Azure AKS", "BigQuery"],
    "previous_cost": [280000, 210000, 88000],
    "current_cost": [420000, 310000, 95000]
})

st.dataframe(sample, use_container_width=True)

if uploaded:
    df = pd.read_csv(uploaded)

    required_cols = {"service", "previous_cost", "current_cost"}

    if not required_cols.issubset(df.columns):
        st.error("CSV must contain service, previous_cost, current_cost")
    else:
        st.success("Data loaded successfully")

        if st.button("RUN ANOMALY AGENT"):

            df["spike_pct"] = (
                (df["current_cost"] - df["previous_cost"])
                / df["previous_cost"]
            ) * 100

            anomalies = df[df["spike_pct"] > 20].copy()

            anomalies["wasted_spend"] = (
                anomalies["current_cost"]
                - anomalies["previous_cost"]
            )

            total_services = len(df)
            anomaly_count = len(anomalies)

            avg_spike = round(df["spike_pct"].mean(), 1)

            total_wasted = int(
                anomalies["wasted_spend"].sum()
            ) if anomaly_count > 0 else 0

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Total Services", total_services)
            c2.metric("Anomalies", anomaly_count)
            c3.metric("Average Spike %", f"{avg_spike}%")
            c4.metric("Wasted Spend", f"₹{total_wasted}")

            st.subheader("Detected Anomalies")

            if anomaly_count == 0:
                st.success("No anomalies detected")
            else:
                st.dataframe(
                    anomalies[
                        [
                            "service",
                            "previous_cost",
                            "current_cost",
                            "spike_pct",
                            "wasted_spend"
                        ]
                    ],
                    use_container_width=True
                )

                st.subheader("Recommended Actions")

                for _, row in anomalies.iterrows():
                    st.markdown(
                        f"""
- **{row['service']}**
  - Spike: **{row['spike_pct']:.1f}%**
  - Potential waste: **₹{int(row['wasted_spend'])}**
  - Action: Investigate scaling / idle resources
"""
                    )
