import streamlit as st
from .base import Processor

class TifProcessor(Processor):
    def process(self):
        st.info(f"Processing GeoTIFF file: {self.uploaded_file.name}")
        st.info("Support for this file type is coming soon.")
