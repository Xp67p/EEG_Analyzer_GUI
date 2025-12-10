import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from main import closed_avg_band, open_avg_band, bandpass, compute_power

#Headersection

st.set_page_config(page_title="EEG Analyzer", page_icon="🧠", layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>🧠 EEG Analyzer Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Simple EEG viewer and band comparison tool</h4>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='text-align:center; font-size:17px; margin-top:10px;'>
        <b>Done by:</b> Abdullah Aburous & Asem Abueisa<br>
        <b>Under Supervision Of:</b> Dr. Mahmoud Al Sarayrah
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")


#Sidebar navigation

st.sidebar.header("Menu")
page = st.sidebar.radio("Select page", ["Overview", "Band Comparison", "Upload & View"])



if page == "Overview":
    st.subheader("What this program does")
    st.write("""
    • Loads EEG signals  
    • Computes band power (Delta → Gamma)  
    • Compares open vs closed eyes  
    • Lets you upload your own file and view EEG channels  
    """)



# Band comparison page

elif page == "Band Comparison":

    st.subheader("Dataset Band Comparison")

    bands = list(closed_avg_band.keys())
    closed_vals = [closed_avg_band[b] for b in bands]
    open_vals   = [open_avg_band[b] for b in bands]

    col1, col2 = st.columns(2)
    col1.metric("Closed Avg Alpha", f"{closed_avg_band['Alpha']:.2f}")
    col2.metric("Open Avg Alpha", f"{open_avg_band['Alpha']:.2f}")

    fig, ax = plt.subplots(figsize=(6,3))
    x = np.arange(len(bands))
    width = 0.25

    ax.bar(x - width/2, closed_vals, width, label="Closed", color="skyblue")
    ax.bar(x + width/2, open_vals, width, label="Open", color="orange")

    ax.set_xticks(x)
    ax.set_xticklabels(bands)
    ax.set_ylabel("Power")
    ax.set_title("Band Power (Closed vs Open)")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    plt.tight_layout()

    st.pyplot(fig)

    df_table = pd.DataFrame({
        "Band": bands,
        "Closed Power": closed_vals,
        "Open Power": open_vals
    })
    st.dataframe(df_table)



# Upload page

elif page == "Upload & View":

    st.subheader("Upload EEG CSV File")
    uploaded = st.file_uploader("Select CSV file", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)

        st.write("Preview:")
        st.dataframe(df.head())

        channels = df.columns.tolist()
        selected_ch = st.selectbox("Select channel", channels)

        sig = df[selected_ch].values

        st.write(f"Raw signal ({selected_ch})")
        fig2, ax2 = plt.subplots(figsize=(9,2.8))
        ax2.plot(sig[:1000], color="purple")
        ax2.set_xlabel("Samples")
        ax2.set_ylabel("Amplitude")
        st.pyplot(fig2)

        st.success("Signal displayed.")

        st.subheader("Band Filter")

        bands = {
            "Delta (0.5–4 Hz)": (0.5, 4),
            "Theta (4–8 Hz)": (4, 8),
            "Alpha (8–13 Hz)": (8, 13),
            "Beta (13–30 Hz)": (13, 30),
            "Gamma (30–45 Hz)": (30, 45)
        }

        band_name = st.selectbox("Select band to filter", list(bands.keys()))
        low, high = bands[band_name]

        if st.button("Apply Filter"):
            filtered = bandpass(sig, low, high)
            pwr = compute_power(filtered)

            st.write(f"Band power = **{pwr:.2f}**")

            fig3, ax3 = plt.subplots(figsize=(9,2.8))
            ax3.plot(filtered[:1000], color="green")
            ax3.set_xlabel("Samples")
            ax3.set_ylabel("Filtered amplitude")
            ax3.set_title(f"{band_name} filtered signal")
            st.pyplot(fig3)
