import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# App Configuration
st.set_page_config(page_title="Spectral Analysis", layout="centered")
st.title("📈 Spectral Analysis Program For Group 3")
st.markdown("### 👨‍💻 Developed by **Incrisz**")

# File Upload
uploaded_file = st.file_uploader("📤 Upload your Excel file (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Filter numeric columns only
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

        if len(numeric_columns) < 2:
            st.error("❌ The uploaded file must contain at least two numeric columns.")
        else:
            # Column selection
            x_column = st.selectbox("🔢 Select X-axis column", numeric_columns)
            y_column = st.selectbox("🔢 Select Y-axis column", numeric_columns, index=1)

            x = pd.to_numeric(df[x_column], errors='coerce')
            y = pd.to_numeric(df[y_column], errors='coerce')
            valid_data = df[(~x.isna()) & (~y.isna())]

            x = valid_data[x_column].values.reshape(-1, 1)
            y = valid_data[y_column].values

            # Optional Display
            if st.checkbox("👁️ Show Raw Data"):
                st.dataframe(df.head())

            if st.checkbox("👁️ Show Cleaned Data"):
                st.dataframe(valid_data[[x_column, y_column]].head())

            # Plot Settings
            plot_title = st.text_input("📌 Enter Plot Title", "Spectral Analysis Plot")
            x_label = st.text_input("🧭 X-axis Label", x_column)
            y_label = st.text_input("🧭 Y-axis Label", y_column)
            line_color = st.color_picker("🎨 Pick a line color", "#0000FF")
            line_style = st.selectbox("📈 Select line style", ["-", "--", "-.", ":"])
            show_regression = st.checkbox("📐 Show Linear Regression Line")

            # Plotting
            fig, ax = plt.subplots()
            ax.plot(x, y, marker='o', linestyle=line_style, color=line_color, label='Data')

            # Regression Line
            if show_regression:
                model = LinearRegression()
                model.fit(x, y)
                y_pred = model.predict(x)
                slope = model.coef_[0]
                intercept = model.intercept_

                ax.plot(x, y_pred, color='red', linestyle='--', label=f'Regression line\ny={slope:.4f}x+{intercept:.4f}')
                ax.legend()

                st.subheader("📐 Linear Regression Results")
                st.write(f"**Slope (m):** `{slope:.4f}`")
                st.write(f"**Intercept (b):** `{intercept:.4f}`")

            ax.set_title(plot_title)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.grid(True)
            st.subheader("📊 Plot")
            st.pyplot(fig)

            # Statistics
            st.subheader("📉 Summary Statistics")
            st.write(valid_data[[x_column, y_column]].describe())

    except Exception as e:
        st.error(f"❌ An error occurred while processing the file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
