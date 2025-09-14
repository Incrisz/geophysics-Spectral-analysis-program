import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App Configuration
st.set_page_config(page_title="Spectral Analysis", layout="centered")
st.title("📈 Spectral Analysis Program (500L project)")
st.markdown("### 👨‍💻 Developed by **Incrisz**")

# File Upload
uploaded_file = st.file_uploader(
    "📤 Upload your data file (.xlsx or .txt)",
    type=["xlsx", "txt"],
)

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".txt"):
            df = pd.read_csv(uploaded_file, sep=None, engine="python")
        else:
            df = pd.read_excel(uploaded_file)

        # Clean the data
        x = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        y = pd.to_numeric(df.iloc[:, 1], errors='coerce')
        valid_data = df[(~x.isna()) & (~y.isna())]
        x = valid_data.iloc[:, 0]
        y = valid_data.iloc[:, 1]

        # Optional Display
        if st.checkbox("👁️ Show Raw Data"):
            st.dataframe(df.head())

        if st.checkbox("👁️ Show Cleaned Data"):
            st.dataframe(valid_data.head())

        # Plot Settings
        plot_title = st.text_input("📌 Enter Plot Title", "Spectral Analysis Plot")
        x_label = st.text_input("🧭 X-axis Label", "X (CYC/K_unit) - 2D RADIALLY")
        y_label = st.text_input("🧭 Y-axis Label", "Y (Ln_P) - SPECTRUM")
        line_color = st.color_picker("🎨 Pick a line color", "#0000FF")
        line_style = st.selectbox("📈 Select line style", ["-", "--", "-.", ":"])

        # Plotting
        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o', linestyle=line_style, color=line_color)
        ax.set_title(plot_title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(True)
        st.subheader("📊 Plot")
        st.pyplot(fig)

        # Statistics
        st.subheader("📉 Summary Statistics")
        st.write(valid_data.describe())

    except Exception as e:
        st.error(f"❌ An error occurred while processing the file: {e}")
else:
    st.info("Please upload an Excel or text file to begin.")
