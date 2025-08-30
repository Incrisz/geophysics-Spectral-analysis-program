import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from sklearn.ensemble import IsolationForest
from .base import Processor

class ExcelGridProcessor(Processor):
    def process(self):
        st.subheader("Grid Data Visualization from Excel")
        try:
            df = pd.read_excel(self.uploaded_file)
            numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

            if len(numeric_columns) < 3:
                st.warning("You need at least 3 numeric columns for grid visualization: X, Y, Z.")
                return

            st.subheader("🗺️ Grid Map Visualization")
            x_grid_col = st.selectbox("🧭 Select X (Grid)", numeric_columns, key="x_grid")
            y_grid_col = st.selectbox("🧭 Select Y (Grid)", numeric_columns, key="y_grid", index=1 if len(numeric_columns) > 1 else 0)
            z_grid_col = st.selectbox("📊 Select Z (Value)", numeric_columns, key="z_grid", index=2 if len(numeric_columns) > 2 else 0)

            grid_data = df[[x_grid_col, y_grid_col, z_grid_col]].dropna()

            if len(grid_data) == 0:
                st.error("❌ No valid data to display.")
                return

            pivot_table = grid_data.pivot_table(index=y_grid_col, columns=x_grid_col, values=z_grid_col)
            X, Y = np.meshgrid(pivot_table.columns, pivot_table.index)
            Z = pivot_table.values

            fig_map, ax_map = plt.subplots()
            cmap = st.selectbox("🎨 Select Color Map", plt.colormaps(), index=plt.colormaps().index("viridis"))
            plot_type = st.radio("📈 Choose Grid Map Type", ["Contour Map", "Heatmap"])
            norm = Normalize(vmin=np.nanmin(Z), vmax=np.nanmax(Z))

            if plot_type == "Contour Map":
                contour = ax_map.contourf(X, Y, Z, levels=20, cmap=cmap, norm=norm)
                fig_map.colorbar(contour, ax=ax_map)
            else:
                heatmap = ax_map.imshow(Z, aspect='auto', origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()], cmap=cmap, norm=norm)
                fig_map.colorbar(heatmap, ax=ax_map)

            ax_map.set_xlabel(x_grid_col)
            ax_map.set_ylabel(y_grid_col)
            ax_map.set_title(f"Grid Map of {z_grid_col}")
            ax_map.grid(True)
            st.pyplot(fig_map)

            st.subheader("🧠 Interpretation")
            z_min, z_max, z_mean = np.nanmin(Z), np.nanmax(Z), np.nanmean(Z)
            st.markdown(f"- **Minimum {z_grid_col}**: {z_min:.2f}\n- **Maximum {z_grid_col}**: {z_max:.2f}\n- **Average {z_grid_col}**: {z_mean:.2f}")

            st.subheader("🤖 AI-based Pattern Detection (Anomaly Zones)")
            model = IsolationForest(contamination=0.1)
            anomalies = model.fit_predict(Z.reshape(-1, 1))
            anomaly_grid = anomalies.reshape(Z.shape)
            fig_anomaly, ax_anomaly = plt.subplots()
            ax_anomaly.imshow(anomaly_grid, aspect='auto', origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()], cmap="coolwarm")
            ax_anomaly.set_title("Anomaly Zones")
            ax_anomaly.set_xlabel(x_grid_col)
            ax_anomaly.set_ylabel(y_grid_col)
            st.pyplot(fig_anomaly)

        except Exception as e:
            st.error(f"❌ Could not generate grid map: {e}")
