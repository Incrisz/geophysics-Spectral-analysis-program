import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import Rectangle
from matplotlib.widgets import Cursor

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

            if plot_type == "Contour Map":
                contour = ax_map.contourf(X, Y, Z, levels=20, cmap=cmap)
                fig_map.colorbar(contour, ax=ax_map)
            else:
                heatmap = ax_map.imshow(Z, aspect='auto', origin='lower',
                                        extent=[X.min(), X.max(), Y.min(), Y.max()], cmap=cmap)
                fig_map.colorbar(heatmap, ax=ax_map)

            ax_map.set_xlabel(x_grid_col)
            ax_map.set_ylabel(y_grid_col)
            ax_map.set_title(f"Grid Map of {z_grid_col}")
            ax_map.grid(True)

            st.pyplot(fig_map)

            # 🔍 Interpretation Section
            st.subheader("🧠 Interpretation")

            z_min = np.nanmin(Z)
            z_max = np.nanmax(Z)
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

                These patterns can highlight potential mineralization zones, structural trends, or lithological variations.
                """)
            else:
                st.markdown(f"""
                #### General Interpretation:

                - The grid shows spatial variation of **{z_grid_col}**.
                - Regions with **high values** are seen in warmer colors (red/yellow).
                - Regions with **low values** are shown in cooler tones (blue/green).
                - This can indicate zones of interest, anomalies, or spatial trends in your dataset.
                """)

        except Exception as e:
            st.error(f"❌ Could not generate grid map: {e}")


    else:
        st.warning("You need at least 3 numeric columns: X, Y, Z.")
