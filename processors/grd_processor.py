import streamlit as st
import rioxarray
import plotly.graph_objects as go
import numpy as np

from .base import Processor

class GrdProcessor(Processor):
    def process(self):
        st.info(f"Processing GRD file: {self.uploaded_file.name}")
        try:
            rds = rioxarray.open_rasterio(self.uploaded_file)

            # Squeeze the data to remove the band dimension for plotting
            rds_squeezed = rds.squeeze()

            # Coarsen the data to reduce the size
            coarsened_rds = rds_squeezed.coarsen(x=10, y=10, boundary='trim').mean()
            data = coarsened_rds.values

            fig = go.Figure(data=go.Heatmap(z=data, colorscale='Viridis'))

            fig.update_layout(
                title="Click on two points to draw a line",
                xaxis_title="X-axis",
                yaxis_title="Y-axis",
            )

            st.plotly_chart(fig, use_container_width=True)

            st.warning("Due to limitations in Streamlit, true click events are not available. As an alternative, please use the sliders below to define the line.")

            st.sidebar.title("Line controls")
            slope = st.sidebar.slider("Slope (m)", -10.0, 10.0, 1.0, 0.1)
            intercept = st.sidebar.slider("Intercept (b)", -10.0, 10.0, 0.0, 0.1)

            fig_with_line = go.Figure(data=go.Heatmap(z=data, colorscale='Viridis'))

            x = np.linspace(0, data.shape[1], 100)
            y = slope * x + intercept

            fig_with_line.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'y = {slope:.1f}x + {intercept:.1f}', line=dict(color='red')))

            fig_with_line.update_layout(
                title="GRD data with interactive line",
                xaxis_title="X-axis",
                yaxis_title="Y-axis",
                xaxis_range=[0, data.shape[1]],
                yaxis_range=[0, data.shape[0]],
            )

            st.plotly_chart(fig_with_line, use_container_width=True)


        except Exception as e:
            st.error(f"Error opening or processing GRD file: {e}")
            return
