import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_plotly_events import plotly_events
from .base import Processor

class ExcelProcessor(Processor):
    def process(self):
        st.subheader("Excel File (.xls, .xlsx) - Interactive Spectral Analysis")

        try:
            df = pd.read_excel(self.uploaded_file)
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

            if len(numeric_columns) < 2:
                st.error("❌ The uploaded file must contain at least two numeric columns.")
                return

            x_column = st.selectbox("🔢 Select X-axis column", numeric_columns)
            y_column = st.selectbox("🔢 Select Y-axis column", numeric_columns, index=1 if len(numeric_columns) > 1 else 0)

            df_clean = df[[x_column, y_column]].dropna()
            x_vals = df_clean[x_column].values
            y_vals = df_clean[y_column].values

            st.subheader("📊 Interactive Plot")
            plot_title = st.text_input("📌 Enter Plot Title", "Interactive Plot")
            x_label = st.text_input("🧭 X-axis Label", x_column)
            y_label = st.text_input("🧭 Y-axis Label", y_column)

            if 'points' not in st.session_state:
                st.session_state.points = []

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='markers', name='Data'))
            fig.update_layout(title=plot_title, xaxis_title=x_label, yaxis_title=y_label)

            if len(st.session_state.points) == 2:
                p1 = st.session_state.points[0]
                p2 = st.session_state.points[1]

                if (p2[0] - p1[0]) == 0:
                    slope = np.inf
                    intercept = p1[0]
                else:
                    slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
                    intercept = p1[1] - slope * p1[0]

                x_line = np.array([min(x_vals), max(x_vals)])
                y_line = slope * x_line + intercept
                fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name=f'y={slope:.2f}x+{intercept:.2f}'))

                st.subheader("📐 Calculated Line")
                st.write(f"**Slope (m):** `{slope:.4f}`")
                st.write(f"**Intercept (b):** `{intercept:.4f}`")

            # The main plot area
            if len(st.session_state.points) < 2:
                st.write("Click on two points on the plot to draw a line.")
                selected_points = plotly_events(fig, key="plotly_events")
                if selected_points:
                    point = (selected_points[0]['x'], selected_points[0]['y'])
                    if point not in st.session_state.points:
                        st.session_state.points.append(point)
                        st.rerun()
            else:
                st.plotly_chart(fig)

            if st.button("Clear selected points"):
                st.session_state.points = []
                st.rerun()

            st.write(f"Selected points: {len(st.session_state.points)}/2")

            # --- Summary Statistics Section ---
            st.subheader("📉 Summary Statistics")
            st.write(df_clean.describe())

            # --- FFT Plot Section ---
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
