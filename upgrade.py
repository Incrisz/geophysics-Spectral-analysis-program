import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy.interpolate import interp1d


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
            x_flat = x.flatten()

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
            dash_styles = {"-": "solid", "--": "dash", "-.": "dashdot", ":": "dot"}
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=x_flat,
                    y=y,
                    mode='lines+markers',
                    line=dict(color=line_color, dash=dash_styles.get(line_style, 'solid')),
                    name='Data'
                )
            )

            # Interpolation 
            if st.checkbox("🔧 Apply Interpolation"):
                interp_type = st.selectbox("📐 Select Interpolation Type", ['linear', 'quadratic', 'cubic'])

                try:
                    f_interp = interp1d(x_flat, y, kind=interp_type)
                    x_interp = np.linspace(x_flat.min(), x_flat.max(), 500)
                    y_interp = f_interp(x_interp)

                    fig.add_trace(
                        go.Scatter(
                            x=x_interp,
                            y=y_interp,
                            mode='lines',
                            line=dict(color='orange', dash='dot'),
                            name=f'{interp_type.capitalize()} Interpolation'
                        )
                    )

                    st.success(f"{interp_type.capitalize()} interpolation applied and plotted.")
                except Exception as e:
                    st.error(f"Interpolation error: {e}")

            # Regression Line
            if show_regression:
                model = LinearRegression()
                model.fit(x, y)
                y_pred = model.predict(x)
                slope = model.coef_[0]
                intercept = model.intercept_

                fig.add_trace(
                    go.Scatter(
                        x=x_flat,
                        y=y_pred,
                        mode='lines',
                        line=dict(color='red', dash='dash'),
                        name=f'Regression line\\ny={slope:.4f}x+{intercept:.4f}'
                    )
                )

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

                # st.latex(r"""
                # m = \frac{y_2 - y_1}{x_2 - x_1}
                # """)
                # st.latex(r"""
                # m = \frac{%0.4f - %0.4f}{%0.4f - %0.4f}
                # """ % (y2, y1, x2, x1))
                # st.latex(r"""
                # m = %0.4f
                # """ % manual_slope)

                st.write(f"**Slope (m):** `{slope:.4f}`")
                st.write(f"**Intercept (b):** `{intercept:.4f}`")

            fig.update_layout(
                title=plot_title,
                xaxis_title=x_label,
                yaxis_title=y_label
            )
            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)
            st.subheader("📊 Plot")
            st.plotly_chart(fig, use_container_width=True)

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
            fig_fft = go.Figure()
            fig_fft.add_trace(
                go.Scatter(
                    x=xf,
                    y=2.0 / N * np.abs(yf[:N // 2]),
                    mode='lines',
                    line=dict(color='green')
                )
            )
            fig_fft.update_layout(
                title="🧠 Frequency Spectrum",
                xaxis_title="Frequency (Hz)",
                yaxis_title="Magnitude"
            )
            fig_fft.update_xaxes(showgrid=True)
            fig_fft.update_yaxes(showgrid=True)
            st.plotly_chart(fig_fft, use_container_width=True)

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
                fig_wave = go.Figure()
                fig_wave.add_trace(
                    go.Scatter(
                        x=wavelength,
                        y=2.0 / N * np.abs(yf[:N // 2]),
                        mode='lines',
                        line=dict(color='purple')
                    )
                )
                fig_wave.update_layout(
                    title="🔬 Spectrum by Wavelength",
                    xaxis_title="Wavelength",
                    yaxis_title="Magnitude"
                )
                fig_wave.update_xaxes(showgrid=True)
                fig_wave.update_yaxes(showgrid=True)
                st.plotly_chart(fig_wave, use_container_width=True)


    except Exception as e:
        st.error(f"❌ An error occurred while processing the file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
