import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from sklearn.ensemble import IsolationForest
from matplotlib.colors import Normalize

st.set_page_config(page_title="Radiometric Grid Map", layout="wide")
st.title("🌍 Radiometric Grid Map Viewer")

uploaded_file = st.file_uploader("📤 Upload Excel file with radiometric data", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_columns) >= 3:
        st.subheader("🗺️ Grid Map Visualization")

        x_grid_col = st.selectbox("🧭 Select X (Grid)", numeric_columns, key="x_grid")
        y_grid_col = st.selectbox("🧭 Select Y (Grid)", numeric_columns, key="y_grid")
        z_grid_col = st.selectbox("📊 Select Z (Value)", numeric_columns, key="z_grid")

        grid_data = df[[x_grid_col, y_grid_col, z_grid_col]].dropna()

        try:
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
                heatmap = ax_map.imshow(Z, aspect='auto', origin='lower',
                                        extent=[X.min(), X.max(), Y.min(), Y.max()],
                                        cmap=cmap, norm=norm)
                fig_map.colorbar(heatmap, ax=ax_map)

            ax_map.set_xlabel(x_grid_col)
            ax_map.set_ylabel(y_grid_col)
            ax_map.set_title(f"Grid Map of {z_grid_col}")
            ax_map.grid(True)

            st.pyplot(fig_map)

            # ZONE CLASSIFICATION
            z_min, z_max = np.nanmin(Z), np.nanmax(Z)
            z_range = z_max - z_min

            low_thresh = z_min + 0.33 * z_range
            med_thresh = z_min + 0.66 * z_range

            st.markdown("#### 🔍 Zone Classification (based on Z-value ranges):")
            st.markdown(f"""
            - 🟦 **Low Zone:** ≤ {low_thresh:.2f}  
            - 🟨 **Medium Zone:** > {low_thresh:.2f} and ≤ {med_thresh:.2f}  
            - 🟥 **High Zone:** > {med_thresh:.2f}
            """)

            # Hover Simulation
            hover_x = st.slider("📍 Simulate Hover - X", float(X.min()), float(X.max()), float((X.min() + X.max()) / 2))
            hover_y = st.slider("📍 Simulate Hover - Y", float(Y.min()), float(Y.max()), float((Y.min() + Y.max()) / 2))

            x_idx = (np.abs(pivot_table.columns - hover_x)).argmin()
            y_idx = (np.abs(pivot_table.index - hover_y)).argmin()
            hover_value = Z[y_idx, x_idx]

            st.info(f"🧭 At (X={pivot_table.columns[x_idx]:.2f}, Y={pivot_table.index[y_idx]:.2f}) → {z_grid_col} = {hover_value:.2f}")

            ax_map.plot(pivot_table.columns[x_idx], pivot_table.index[y_idx], 'ko', markersize=6, label='Selected Point')
            ax_map.legend(loc='upper right')

            st.pyplot(fig_map)

            # INTERPRETATION
            st.subheader("🧠 Interpretation")

            z_mean = np.nanmean(Z)

            st.markdown(f"""
            - **Minimum {z_grid_col}**: {z_min:.2f}  
            - **Maximum {z_grid_col}**: {z_max:.2f}  
            - **Average {z_grid_col}**: {z_mean:.2f}  
            """)

            if "eTh/K" in z_grid_col or "radiometric" in z_grid_col.lower():
                st.markdown("""
                #### Radiometric Interpretation:

                - **Red/Hot Colors (High Values):** Suggest elevated concentrations of radioactive elements (like Thorium or Potassium).
                - **Blue/Cold Colors (Low Values):** Indicate regions with low radiometric response — often associated with less mineralized or sedimentary zones.
                - **Transition Zones (Green/Yellow):** Could mark boundaries, geological contacts, or zones of interest for exploration.
                """)
            else:
                st.markdown(f"""
                #### General Interpretation:

                - The grid shows spatial variation of **{z_grid_col}**.
                - Regions with **high values** are seen in warmer colors (red/yellow).
                - Regions with **low values** are shown in cooler tones (blue/green).
                - This can indicate zones of interest, anomalies, or spatial trends in your dataset.
                """)

            # AI-BASED ANOMALY ZONES
            st.subheader("🤖 AI-based Pattern Detection (Anomaly Zones)")

            model = IsolationForest(contamination=0.1)
            anomalies = model.fit_predict(Z.reshape(-1, 1))
            anomaly_grid = anomalies.reshape(Z.shape)

            fig_anomaly, ax_anomaly = plt.subplots()
            ax_anomaly.imshow(anomaly_grid, aspect='auto', origin='lower',
                              extent=[X.min(), X.max(), Y.min(), Y.max()],
                              cmap="coolwarm")
            ax_anomaly.set_title("Anomaly Zones")
            ax_anomaly.set_xlabel(x_grid_col)
            ax_anomaly.set_ylabel(y_grid_col)

            st.pyplot(fig_anomaly)

  

        except Exception as e:
            st.error(f"❌ Could not generate grid map: {e}")

    else:
        st.warning("You need at least 3 numeric columns: X, Y, Z.")
