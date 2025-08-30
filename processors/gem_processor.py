import streamlit as st
from .base import Processor

class GemProcessor(Processor):
    def process(self):
        st.info(f"Processing GEM file: {self.uploaded_file.name}")
        st.info("Support for this file type is coming soon.")
