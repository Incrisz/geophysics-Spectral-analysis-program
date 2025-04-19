import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'DejaVu Sans'  # Or try a system emoji font if available
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

                # Show working for slope using first and last point
                x1 = x[0][0]
                x2 = x[-1][0]
                y1 = y[0]
                y2 = y[-1]
                manual_slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')

                # st.markdown("### 🧮 Slope Calculation (Manual Working)")
                st.write(f"Let the first point be (x₁, y₁) = ({x1:.4f}, {y1:.4f})")
                st.write(f"Let the last point be (x₂, y₂) = ({x2:.4f}, {y2:.4f})")

                st.latex(r"""
                m = \frac{y_2 - y_1}{x_2 - x_1}
                """)
                st.latex(r"""
                m = \frac{%0.4f - %0.4f}{%0.4f - %0.4f}
                """ % (y2, y1, x2, x1))
                st.latex(r"""
                m = %0.4f
                """ % manual_slope)

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

            # -------------------------------
            # 📡 Spectral Analysis (FFT)
            # -------------------------------
            st.subheader("📡 Spectral Analysis (FFT)")

            # Sampling interval input (time between data points)
            sampling_interval = st.number_input("🕒 Sampling Interval (e.g., 1 for unit steps)", min_value=0.0001, value=1.0, step=0.1, format="%.4f")

            # FFT Calculation
            N = len(y)
            T = sampling_interval
            yf = np.fft.fft(y)
            xf = np.fft.fftfreq(N, T)[:N // 2]

            # Frequency domain plot
            fig_fft, ax_fft = plt.subplots()
            ax_fft.plot(xf, 2.0 / N * np.abs(yf[:N // 2]), color='green')
            ax_fft.set_title("🧠 Frequency Spectrum")
            ax_fft.set_xlabel("Frequency (Hz)")
            ax_fft.set_ylabel("Magnitude")
            ax_fft.grid(True)
            st.pyplot(fig_fft)

            # Optional: Frequency components table
            if st.checkbox("📄 Show Frequency Components Table"):
                freq_data = pd.DataFrame({
                    "Frequency (Hz)": xf,
                    "Magnitude": 2.0 / N * np.abs(yf[:N // 2])
                })
                st.dataframe(freq_data.head(20))

            # Optional: Show as wavelength
            if st.checkbox("🔁 Show Wavelength Instead of Frequency"):
                # Avoid division by zero
                safe_xf = np.where(xf == 0, np.nan, xf)
                wavelength = 1 / safe_xf
                fig_wave, ax_wave = plt.subplots()
                ax_wave.plot(wavelength, 2.0 / N * np.abs(yf[:N // 2]), color='purple')
                ax_wave.set_title("🔬 Spectrum by Wavelength")
                ax_wave.set_xlabel("Wavelength")
                ax_wave.set_ylabel("Magnitude")
                ax_wave.grid(True)
                st.pyplot(fig_wave)


    except Exception as e:
        st.error(f"❌ An error occurred while processing the file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
