import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Spectral Analysis Program
# Developed by Incrisz
# https://github.com/Incrisz/geophysics-Spectral-analysis-program

st.set_page_config(page_title="Spectral Analysis", layout="centered")
st.title("📈 Spectral Analysis Program For Group 3")
st.markdown("### 👨‍💻 Developed by **Incrisz**")

uploaded_file = st.file_uploader("📤 Upload your Excel file (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("🧾 Raw Data")
        st.dataframe(df.head())

        x = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        y = pd.to_numeric(df.iloc[:, 1], errors='coerce')
        valid_data = df[(~x.isna()) & (~y.isna())]
        x = valid_data.iloc[:, 0]
        y = valid_data.iloc[:, 1]

        st.subheader("✅ Cleaned Data")
        st.dataframe(valid_data.head())

        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o', linestyle='-', color='blue')
        ax.set_title("Spectral Analysis Plot")
        ax.set_xlabel("X (CYC/K_unit) - 2-D RADIALLY")
        ax.set_ylabel("Y (Ln_P) - SPECTRUM")
        ax.grid(True)

        st.subheader("📊 Plot")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"❌ An error occurred while processing the file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
