import streamlit as st
from .base import Processor

class LasProcessor(Processor):
    def process(self):
        st.info(f"Processing LAS file: {self.uploaded_file.name}")
        st.info("Support for this file type is coming soon.")
