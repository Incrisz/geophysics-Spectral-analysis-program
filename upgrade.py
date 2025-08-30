import streamlit as st
from processors.excel_processor import ExcelProcessor
from processors.excel_grid_processor import ExcelGridProcessor
from processors.segy_processor import SegyProcessor
from processors.grd_processor import GrdProcessor
from processors.xyz_processor import XyzProcessor
from processors.las_processor import LasProcessor
from processors.dlis_processor import DlisProcessor
from processors.tif_processor import TifProcessor
from processors.nc_processor import NcProcessor
from processors.h5_processor import H5Processor
from processors.gem_processor import GemProcessor

PROCESSOR_MAP = {
    'xls': ExcelProcessor,
    'xlsx': ExcelProcessor,
    'segy': SegyProcessor,
    'sgy': SegyProcessor,
    'grd': GrdProcessor,
    'xyz': XyzProcessor,
    'las': LasProcessor,
    'dlis': DlisProcessor,
    'tif': TifProcessor,
    'nc': NcProcessor,
    'h5': H5Processor,
    'hdf5': H5Processor,
    'gem': GemProcessor,
}

def main():
    st.set_page_config(page_title="Spectral Analysis", layout="centered")
    st.title("📈 Spectral Analysis Program")
    st.markdown("### 👨‍💻 Developed by **Incrisz**")

    allowed_extensions = list(PROCESSOR_MAP.keys())
    uploaded_file = st.file_uploader(f"📤 Upload your data file", type=allowed_extensions)

    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension in ['xls', 'xlsx']:
            analysis_type = st.radio("Select analysis type:", ("Spectral Analysis", "Grid Map Visualization"))
            if analysis_type == "Spectral Analysis":
                processor_class = PROCESSOR_MAP[file_extension]
            else:
                processor_class = ExcelGridProcessor
        else:
            processor_class = PROCESSOR_MAP.get(file_extension)

        if processor_class:
            processor = processor_class(uploaded_file)
            processor.process()
        else:
            st.error(f"Unsupported file type: .{file_extension}")
    else:
        st.info("Please upload a data file to begin.")

if __name__ == "__main__":
    main()
