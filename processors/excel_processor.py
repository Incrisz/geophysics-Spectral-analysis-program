import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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

            if 'points' not in st.session_state:
                st.session_state.points = []

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='markers', name='Data'))

            st.write("Click on two points on the plot to draw a line.")

            slope = 0
            intercept = 0

            if len(st.session_state.points) == 2:
                p1 = st.session_state.points[0]
                p2 = st.session_state.points[1]

                # Calculate slope and intercept
                if (p2[0] - p1[0]) == 0:
                    slope = np.inf
                    intercept = p1[0]
                else:
                    slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
                    intercept = p1[1] - slope * p1[0]

                # Add line to plot
                x_line = np.array([min(x_vals), max(x_vals)])
                y_line = slope * x_line + intercept
                fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name=f'y={slope:.2f}x+{intercept:.2f}'))

            selected_points = plotly_events(fig, key="plotly_events")

            if selected_points:
                point = (selected_points[0]['x'], selected_points[0]['y'])
                if point not in st.session_state.points:
                    st.session_state.points.append(point)
                    st.experimental_rerun()

            if st.button("Clear selected points"):
                st.session_state.points = []
                st.experimental_rerun()

            st.write(f"Selected points: {len(st.session_state.points)}/2")

            if len(st.session_state.points) == 2:
                st.subheader("📐 Calculated Line")
                st.write(f"**Slope (m):** `{slope:.4f}`")
                st.write(f"**Intercept (b):** `{intercept:.4f}`")

                # Clear points for next line after displaying results
                st.session_state.points = []


        except Exception as e:
            st.error(f"❌ An error occurred while processing the Excel file: {e}")
