import streamlit as st
from .base import Processor

class H5Processor(Processor):
    def process(self):
        st.info(f"Processing HDF5 file: {self.uploaded_file.name}")
        st.info("Support for this file type is coming soon.")
