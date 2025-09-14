import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# App Configuration
st.set_page_config(page_title="Spectral Analysis", layout="centered")
st.title("📈 Spectral Analysis Program")
st.markdown("### 👨‍💻 Developed by **Incrisz**")

# File Upload
uploaded_file = st.file_uploader("📤 Upload your Excel file (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Clean the data
        x = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        y = pd.to_numeric(df.iloc[:, 1], errors='coerce')
        valid_data = df[(~x.isna()) & (~y.isna())]
        x = valid_data.iloc[:, 0]
        y = valid_data.iloc[:, 1]

        # Optional Display
        if st.checkbox("👁️ Show Raw Data"):
            st.dataframe(df.head())

        if st.checkbox("👁️ Show Cleaned Data"):
            st.dataframe(valid_data.head())

        # Plot Settings
        plot_title = st.text_input("📌 Enter Plot Title", "Spectral Analysis Plot")
        x_label = st.text_input("🧭 X-axis Label", "X (CYC/K_unit) - 2D RADIALLY")
        y_label = st.text_input("🧭 Y-axis Label", "Y (Ln_P) - SPECTRUM")
        line_color = st.color_picker("🎨 Pick a line color", "#0000FF")
        line_style = st.selectbox("📈 Select line style", ["-", "--", "-.", ":"])

        # Plotting
        plot_df = pd.DataFrame({'x': x, 'y': y})
        dash_styles = {"-": "solid", "--": "dash", "-.": "dashdot", ":": "dot"}
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=plot_df['x'],
                y=plot_df['y'],
                mode='lines+markers',
                line=dict(color=line_color, dash=dash_styles.get(line_style, 'solid'))
            )
        )
        fig.update_layout(
            title=plot_title,
            xaxis_title=x_label,
            yaxis_title=y_label
        )
        st.subheader("📊 Plot")
        st.plotly_chart(fig, use_container_width=True)

        # Statistics
        st.subheader("📉 Summary Statistics")
        st.write(valid_data.describe())

    except Exception as e:
        st.error(f"❌ An error occurred while processing the file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
