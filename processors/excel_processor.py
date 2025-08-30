import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.interpolate import interp1d
from .base import Processor

class ExcelProcessor(Processor):
    def process(self):
        st.subheader("Excel File (.xls, .xlsx) - Spectral Analysis")
        try:
            df = pd.read_excel(self.uploaded_file)

            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

            if len(numeric_columns) < 2:
                st.error("❌ The uploaded file must contain at least two numeric columns for spectral analysis.")
                return

            x_column = st.selectbox("🔢 Select X-axis column", numeric_columns)
            y_column = st.selectbox("🔢 Select Y-axis column", numeric_columns, index=1 if len(numeric_columns) > 1 else 0)

            x = pd.to_numeric(df[x_column], errors='coerce')
            y = pd.to_numeric(df[y_column], errors='coerce')
            valid_data = df[(~x.isna()) & (~y.isna())]

            if len(valid_data) < 2:
                st.error("❌ Not enough valid data for analysis.")
                return

            x_vals = valid_data[x_column].values.reshape(-1, 1)
            y_vals = valid_data[y_column].values

            if st.checkbox("👁️ Show Raw Data"):
                st.dataframe(df.head())

            if st.checkbox("👁️ Show Cleaned Data"):
                st.dataframe(valid_data[[x_column, y_column]].head())

            plot_title = st.text_input("📌 Enter Plot Title", "Spectral Analysis Plot")
            x_label = st.text_input("🧭 X-axis Label", x_column)
            y_label = st.text_input("🧭 Y-axis Label", y_column)
            line_color = st.color_picker("🎨 Pick a line color", "#0000FF")
            line_style = st.selectbox("📈 Select line style", ["-", "--", "-.", ":"])

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, marker='o', linestyle=line_style, color=line_color, label='Data')

            if st.checkbox("🔧 Apply Interpolation"):
                interp_type = st.selectbox("📐 Select Interpolation Type", ['linear', 'quadratic', 'cubic'])
                x_flat = x_vals.flatten()
                try:
                    f_interp = interp1d(x_flat, y_vals, kind=interp_type, fill_value="extrapolate")
                    x_interp = np.linspace(x_flat.min(), x_flat.max(), 500)
                    y_interp = f_interp(x_interp)
                    ax.plot(x_interp, y_interp, color='orange', linestyle=':', label=f'{interp_type.capitalize()} Interpolation')
                except Exception as e:
                    st.error(f"Interpolation error: {e}")

            if st.checkbox("📐 Show Linear Regression Line"):
                model = LinearRegression()
                model.fit(x_vals, y_vals)
                y_pred = model.predict(x_vals)
                slope = model.coef_[0]
                intercept = model.intercept_
                ax.plot(x_vals, y_pred, color='red', linestyle='--', label=f'Regression line\ny={slope:.4f}x+{intercept:.4f}')
                st.subheader("📐 Linear Regression Results")
                st.write(f"**Slope (m):** `{slope:.4f}`")
                st.write(f"**Intercept (b):** `{intercept:.4f}`")

            ax.set_title(plot_title)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.grid(True)
            ax.legend()
            st.subheader("📊 Plot")
            st.pyplot(fig)

            st.subheader("📉 Summary Statistics")
            st.write(valid_data[[x_column, y_column]].describe())

            st.subheader("📡 Spectral Analysis (FFT)")
            sampling_interval = st.number_input("🕒 Sampling Interval", min_value=0.0001, value=1.0, step=0.1, format="%.4f")
            N = len(y_vals)
            T = sampling_interval
            yf = np.fft.fft(y_vals)
            xf = np.fft.fftfreq(N, T)[:N//2]
            fig_fft, ax_fft = plt.subplots()
            ax_fft.plot(xf, 2.0/N * np.abs(yf[0:N//2]), color='green')
            ax_fft.set_title("Frequency Spectrum")
            ax_fft.set_xlabel("Frequency (Hz)")
            ax_fft.set_ylabel("Magnitude")
            ax_fft.grid(True)
            st.pyplot(fig_fft)

        except Exception as e:
            st.error(f"❌ An error occurred while processing the Excel file: {e}")
