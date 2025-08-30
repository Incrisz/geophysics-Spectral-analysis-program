import streamlit as st
from .base import Processor

class SegyProcessor(Processor):
    def process(self):
        st.info(f"Processing SEG-Y file: {self.uploaded_file.name}")
        st.info("Support for this file type is coming soon.")
