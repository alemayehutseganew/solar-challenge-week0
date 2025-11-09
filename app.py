

# import streamlit as st
# import nbformat
# import os
# import glob
# import pandas as pd
# import io
# import matplotlib.pyplot as plt
# import traceback
# from typing import Dict, Any
# import sys
# import requests
# from io import BytesIO
# import re

# st.set_page_config(page_title="Solar Challenge EDA Dashboard", layout="wide")

# HEADER = "Solar Challenge EDA Dashboard — Benin / Sierra Leone / Togo / Comparison"
# st.title(HEADER)

# # Google Drive File IDs for DATA files
# GDRIVE_DATA_IDS = {
#     "benin-malanville.csv": "1YQSDdFo-PV2UAXR2_xwfpSVMIElcR14j",
#     "sierraleone-bumbuna.csv": "1ztNxJBo0Nn0xs5V6WqkAaOH_aywnow_q", 
#     "togo-dapaong_qc.csv": "1eZKayFdWNNXmBA7_y10J5j0On7tEDpMm",
#     "Benin_clean.csv": "1llMg2PlO97yN6Z9rbr4-SYuAH_T0Ehwt",
#     "Sierraleone_clean.csv": "1te7S7NvcV345Y3nmGdr7EiieoNaQtHvP",
#     "Togo_clean.csv": "1kvx4dYVvVeTgwENRBMKV_XD6WCg_TTh6"
# }

# # Google Drive File IDs for NOTEBOOK files
# GDRIVE_NOTEBOOK_IDS = {
#     "benin_eda.ipynb": "1KQtWIbOX16xwr72X9UY2zdmE3LNEtYVf",
#     "sierraleone_eda.ipynb": "1fpszb4lgfTqQRINavV9uiogHkw-p54ni",
#     "Togo_eda.ipynb": "1qSMqes0puCGrVHLOj3nsZbHkuWZciELG",
#     "compare_countries.ipynb": "1nd0EyrkNupPqkrpxpOEEx9pME39w0uoV"
# }

# NOTEBOOK_PATTERNS = [
#     "benin_eda.ipynb",
#     "sierraleone_eda.ipynb", 
#     "Togo_eda.ipynb",
#     "compare_countries.ipynb"
# ]

# @st.cache_data
# def download_from_gdrive(file_id):
#     """Download file from Google Drive and return as BytesIO object"""
#     URL = "https://drive.google.com/uc?export=download&id="
    
#     try:
#         session = requests.Session()
#         response = session.get(URL + file_id, stream=True)
        
#         if response.status_code == 200:
#             return BytesIO(response.content)
#         else:
#             st.error(f"Failed to download file {file_id}. Status code: {response.status_code}")
#             return None
#     except Exception as e:
#         st.error(f"Error downloading file {file_id}: {str(e)}")
#         return None

# @st.cache_data
# def load_csv_from_gdrive(filename):
#     """Load CSV file from Google Drive with caching"""
#     if filename in GDRIVE_DATA_IDS:
#         file_content = download_from_gdrive(GDRIVE_DATA_IDS[filename])
#         if file_content is not None:
#             try:
#                 return pd.read_csv(file_content)
#             except Exception as e:
#                 st.error(f"Error loading {filename}: {str(e)}")
#                 return None
#     return None

# @st.cache_data
# def load_notebook_from_gdrive(notebook_name):
#     """Load notebook file from Google Drive with caching"""
#     if notebook_name in GDRIVE_NOTEBOOK_IDS:
#         file_content = download_from_gdrive(GDRIVE_NOTEBOOK_IDS[notebook_name])
#         if file_content is not None:
#             try:
#                 # Read the notebook content
#                 notebook_content = file_content.read().decode('utf-8')
#                 return notebook_content
#             except Exception as e:
#                 st.error(f"Error loading notebook {notebook_name}: {str(e)}")
#     return None

# @st.cache_data
# def find_notebooks():
#     """Look for notebooks in Google Drive only"""
#     nb_paths = []
    
#     # Use Google Drive notebooks exclusively
#     for notebook_name in GDRIVE_NOTEBOOK_IDS.keys():
#         nb_paths.append(f"gdrive:{notebook_name}")
    
#     return sorted(list(set(nb_paths)))

# def extract_markdown_and_code(nb_path: str):
#     """Return (markdown_text, combined_code) from notebook file."""
#     try:
#         # This is always a Google Drive notebook now
#         notebook_name = nb_path.replace("gdrive:", "")
#         notebook_content = load_notebook_from_gdrive(notebook_name)
#         if notebook_content:
#             nb = nbformat.reads(notebook_content, as_version=4)
#         else:
#             return "", ""
#     except Exception as e:
#         st.warning(f"Could not read notebook {nb_path}: {e}")
#         return "", ""
    
#     md_cells = []
#     code_cells = []
#     for cell in nb.cells:
#         if cell.cell_type == "markdown":
#             md_cells.append(cell.source)
#         elif cell.cell_type == "code":
#             code_cells.append(cell.source)
#     return "\n\n".join(md_cells), "\n\n".join(code_cells)

# def create_safe_execution_environment():
#     """Create a completely safe execution environment with pre-loaded data"""
#     ns = {}
    
#     # Provide essential imports
#     ns['pd'] = pd
#     ns['plt'] = plt
#     ns['os'] = os
#     ns['glob'] = glob
#     ns['sys'] = sys
#     ns['st'] = st
#     ns['requests'] = requests
#     ns['BytesIO'] = BytesIO
#     ns['np'] = __import__('numpy')
    
#     # Pre-load ALL data files into the namespace
#     st.info("📥 Loading all data files from Google Drive...")
    
#     # Load Benin data
#     benin_data = load_csv_from_gdrive("benin-malanville.csv")
#     if benin_data is not None:
#         ns['benin_df'] = benin_data
#         ns['df_benin'] = benin_data
#         ns['benin_data'] = benin_data
#         st.success("✅ Benin data loaded")
    
#     # Load Sierra Leone data
#     sierra_data = load_csv_from_gdrive("sierraleone-bumbuna.csv")
#     if sierra_data is not None:
#         ns['sierraleone_df'] = sierra_data
#         ns['df_sierra'] = sierra_data
#         ns['sierra_data'] = sierra_data
#         ns['sierraleone_data'] = sierra_data
#         st.success("✅ Sierra Leone data loaded")
    
#     # Load Togo data
#     togo_data = load_csv_from_gdrive("togo-dapaong_qc.csv")
#     if togo_data is not None:
#         ns['togo_df'] = togo_data
#         ns['df_togo'] = togo_data
#         ns['togo_data'] = togo_data
#         st.success("✅ Togo data loaded")
    
#     # Load clean data versions
#     benin_clean = load_csv_from_gdrive("Benin_clean.csv")
#     if benin_clean is not None:
#         ns['benin_clean'] = benin_clean
#         ns['df_benin_clean'] = benin_clean
#         st.success("✅ Benin clean data loaded")
    
#     sierra_clean = load_csv_from_gdrive("Sierraleone_clean.csv")
#     if sierra_clean is not None:
#         ns['sierraleone_clean'] = sierra_clean
#         ns['df_sierra_clean'] = sierra_clean
#         st.success("✅ Sierra Leone clean data loaded")
    
#     togo_clean = load_csv_from_gdrive("Togo_clean.csv")
#     if togo_clean is not None:
#         ns['togo_clean'] = togo_clean
#         ns['df_togo_clean'] = togo_clean
#         st.success("✅ Togo clean data loaded")
    
#     # Add data loading functions that return the pre-loaded data
#     def load_benin_data():
#         return ns.get('benin_df')
    
#     def load_sierraleone_data():
#         return ns.get('sierraleone_df')
    
#     def load_togo_data():
#         return ns.get('togo_df')
    
#     def load_benin_clean():
#         return ns.get('benin_clean')
    
#     def load_sierraleone_clean():
#         return ns.get('sierraleone_clean')
    
#     def load_togo_clean():
#         return ns.get('togo_clean')
    
#     # Add helper functions to namespace
#     ns['load_benin_data'] = load_benin_data
#     ns['load_sierraleone_data'] = load_sierraleone_data
#     ns['load_togo_data'] = load_togo_data
#     ns['load_benin_clean'] = load_benin_clean
#     ns['load_sierraleone_clean'] = load_sierraleone_clean
#     ns['load_togo_clean'] = load_togo_clean
    
#     return ns

# def remove_file_loading_code(code: str):
#     """Remove all file loading code from the notebook and replace with comments"""
#     # Patterns to remove (file loading operations)
#     patterns_to_remove = [
#         r"pd\.read_csv\([^)]+\)",
#         r"pd\.read_excel\([^)]+\)",
#         r"pd\.read_json\([^)]+\)",
#         r"open\([^)]+\)",
#         r"with open\([^)]+\)",
#     ]
    
#     cleaned_code = code
#     for pattern in patterns_to_remove:
#         # Replace file loading operations with comments
#         cleaned_code = re.sub(
#             pattern, 
#             "# FILE LOADING REMOVED: Data is pre-loaded from Google Drive", 
#             cleaned_code, 
#             flags=re.IGNORECASE
#         )
    
#     return cleaned_code

# def exec_code_collect_dfs(code: str, notebook_name: str) -> Dict[str, Any]:
#     """Execute code in a safe environment with pre-loaded data"""
    
#     # Create safe environment with pre-loaded data
#     ns = create_safe_execution_environment()
    
#     # Remove file loading code to prevent errors
#     safe_code = remove_file_loading_code(code)
    
#     try:
#         # Execute the safe code (without file loading operations)
#         exec(safe_code, ns)
        
#     except Exception as e:
#         st.warning("Notebook code execution failed. See error details below.")
#         st.error(f"Execution error: {e}")
        
#         # Show more detailed error information
#         with st.expander("Detailed Error Traceback"):
#             st.code(traceback.format_exc())
        
#         # Show what code was executed
#         with st.expander("See Code That Was Executed"):
#             st.code(safe_code)
    
#     # collect dataframes
#     dfs = {k: v for k, v in ns.items() if isinstance(v, pd.DataFrame)}
#     return {'namespace': ns, 'dataframes': dfs, 'safe_code': safe_code}

# def list_csvs():
#     """List available CSV files from Google Drive"""
#     return list(GDRIVE_DATA_IDS.keys())

# def show_dataframe_eda(df: pd.DataFrame, name: str = 'DataFrame'):
#     st.subheader(f"{name} — Basic summary")
#     st.write('Shape:', df.shape)
    
#     with st.expander('Show first 10 rows'):
#         st.dataframe(df.head(10))
    
#     with st.expander('Describe (numerical)'):
#         st.dataframe(df.describe().T)
    
#     # Show nulls
#     nulls = df.isnull().sum()
#     if nulls.sum() > 0:
#         with st.expander('Null counts'):
#             st.dataframe(nulls[nulls > 0])
    
#     # Show column info
#     with st.expander('Column information'):
#         col_info = pd.DataFrame({
#             'Column': df.columns,
#             'Data Type': df.dtypes,
#             'Non-Null Count': df.count(),
#             'Null Count': df.isnull().sum()
#         })
#         st.dataframe(col_info)
    
#     # Simple plots
#     numeric = df.select_dtypes(include='number')
#     if numeric.shape[1] > 0:
#         st.subheader('Numeric column analysis')
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Histogram
#             hist_col = st.selectbox('Select column for histogram', 
#                                   options=list(numeric.columns), 
#                                   key=f'hist_{name}')
#             bins = st.slider('Number of bins', 5, 100, 30, key=f'bins_{name}')
            
#             fig, ax = plt.subplots()
#             ax.hist(numeric[hist_col].dropna(), bins=bins, alpha=0.7, edgecolor='black')
#             ax.set_xlabel(hist_col)
#             ax.set_ylabel('Count')
#             ax.set_title(f'Histogram of {hist_col}')
#             st.pyplot(fig)
        
#         with col2:
#             # Correlation heatmap
#             if numeric.shape[1] > 1:
#                 st.write('Correlation heatmap')
#                 corr = numeric.corr()
#                 fig2, ax2 = plt.subplots(figsize=(8, 6))
#                 im = ax2.imshow(corr, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
                
#                 # Add correlation values as text
#                 for i in range(len(corr.columns)):
#                     for j in range(len(corr.columns)):
#                         ax2.text(j, i, f'{corr.iloc[i, j]:.2f}',
#                                ha="center", va="center", color="black", fontsize=8)
                
#                 ax2.set_xticks(range(len(corr.columns)))
#                 ax2.set_yticks(range(len(corr.columns)))
#                 ax2.set_xticklabels(corr.columns, rotation=45, ha='right')
#                 ax2.set_yticklabels(corr.columns)
#                 ax2.set_title('Correlation Matrix')
#                 fig2.colorbar(im)
#                 st.pyplot(fig2)
#     else:
#         st.info('No numeric columns detected for plotting.')

# # ---- MAIN APP ----
# st.sidebar.title("Navigation")

# # Find notebooks and CSV files
# notebooks = find_notebooks()
# csv_files = list_csvs()

# # Debug information
# with st.sidebar.expander("Debug Info"):
#     st.write("Current working directory:", os.getcwd())
#     st.write("Found notebooks:", [nb.replace('gdrive:', '') for nb in notebooks])
#     st.write("Available CSV files from Google Drive:", csv_files)

# # Map simple labels for the user
# label_map = {}
# for nb in notebooks:
#     notebook_name = nb.replace("gdrive:", "")
#     base = notebook_name.lower()
        
#     if 'benin' in base:
#         label_map['Benin Analysis'] = nb
#     elif 'sierra' in base or 'sierraleone' in base:
#         label_map['Sierra Leone Analysis'] = nb
#     elif 'togo' in base:
#         label_map['Togo Analysis'] = nb
#     elif 'compare' in base:
#         label_map['Country Comparison'] = nb
#     else:
#         label_map[notebook_name] = nb

# selection = st.sidebar.selectbox('Choose analysis to view', options=list(label_map.keys()))
# nb_path = label_map[selection]

# # Display notebook source information
# notebook_name = nb_path.replace("gdrive:", "")
# st.markdown(f"**Notebook:** `{notebook_name}` (from Google Drive)")

# # Display available CSV files in sidebar
# if csv_files:
#     st.sidebar.subheader("Available Data Files (from Google Drive)")
#     for csv_file in csv_files:
#         st.sidebar.write(f"- {csv_file}")
# else:
#     st.sidebar.warning(f"No CSV files available")

# # Extract and display markdown
# md_text, code_text = extract_markdown_and_code(nb_path)
# if md_text:
#     with st.expander('Notebook markdown (click to expand)'):
#         st.markdown(md_text)

# # Show cleaned code (for debugging)
# with st.expander('Show cleaned code (for debugging)'):
#     safe_code = remove_file_loading_code(code_text)
#     st.code(safe_code)
#     st.info("Note: All file loading operations have been removed. Data is pre-loaded from Google Drive.")

# # Try to execute code and collect dataframes
# if st.button('Execute Notebook Code'):
#     with st.spinner('Loading data from Google Drive and executing notebook...'):
#         result = exec_code_collect_dfs(code_text, notebook_name)

#     dfs = result.get('dataframes', {})
    
#     # Filter out the pre-loaded dataframes to show only newly created ones
#     preloaded_names = ['benin_df', 'df_benin', 'benin_data', 'sierraleone_df', 'df_sierra', 
#                       'sierra_data', 'sierraleone_data', 'togo_df', 'df_togo', 'togo_data',
#                       'benin_clean', 'df_benin_clean', 'sierraleone_clean', 'df_sierra_clean',
#                       'togo_clean', 'df_togo_clean']
    
#     new_dfs = {k: v for k, v in dfs.items() if k not in preloaded_names}
    
#     if new_dfs:
#         st.success(f'Found {len(new_dfs)} newly created DataFrame(s) in the executed notebook.')
        
#         # Display all new dataframes in tabs
#         tab_names = list(new_dfs.keys())
#         tabs = st.tabs([f"📊 {name}" for name in tab_names])
        
#         for i, (df_name, df) in enumerate(new_dfs.items()):
#             with tabs[i]:
#                 show_dataframe_eda(df, name=df_name)
                
#                 # Add download button for each dataframe
#                 csv = df.to_csv(index=False)
#                 st.download_button(
#                     label=f"Download {df_name} as CSV",
#                     data=csv,
#                     file_name=f"{df_name}.csv",
#                     mime="text/csv",
#                     key=f"download_{df_name}_{i}"
#                 )
#     else:
#         st.info('No new DataFrame objects were created by executing the notebook.')
#         st.info('Showing pre-loaded dataframes instead:')
        
#         # Show pre-loaded dataframes
#         preloaded_dfs = {k: v for k, v in result['namespace'].items() 
#                         if k in preloaded_names and isinstance(v, pd.DataFrame)}
        
#         if preloaded_dfs:
#             tab_names = list(preloaded_dfs.keys())
#             tabs = st.tabs([f"📊 {name}" for name in tab_names])
            
#             for i, (df_name, df) in enumerate(preloaded_dfs.items()):
#                 with tabs[i]:
#                     show_dataframe_eda(df, name=df_name)

# # Quick CSV loader in sidebar
# st.sidebar.subheader("Quick CSV Loader")
# if csv_files:
#     selected_csv = st.sidebar.selectbox("Load CSV for quick EDA", 
#                                        options=[""] + csv_files)
#     if selected_csv:
#         if st.sidebar.button("Analyze this CSV"):
#             try:
#                 df_quick = load_csv_from_gdrive(selected_csv)
#                 if df_quick is not None:
#                     show_dataframe_eda(df_quick, name=selected_csv)
#                 else:
#                     st.sidebar.error(f"Failed to load: {selected_csv}")
#             except Exception as e:
#                 st.sidebar.error(f"Failed to load: {e}")

# st.markdown('---')
# st.info(f'''
# **Notes:** 
# - All notebooks and data files are loaded directly from Google Drive
# - No local file access - completely bypasses file system errors
# - Data is pre-loaded before notebook execution
# - File loading operations in notebooks are automatically removed
# - Uses cached downloads for better performance
# ''')


import streamlit as st
import nbformat
import os
import glob
import pandas as pd
import io
import matplotlib.pyplot as plt
import traceback
from typing import Dict, Any
import sys
import requests
from io import BytesIO
import re

st.set_page_config(page_title="Solar Challenge EDA Dashboard", layout="wide")

HEADER = "Solar Challenge EDA Dashboard — Benin / Sierra Leone / Togo / Comparison"
st.title(HEADER)

# Google Drive File IDs for DATA files
GDRIVE_DATA_IDS = {
    "benin-malanville.csv": "1YQSDdFo-PV2UAXR2_xwfpSVMIElcR14j",
    "sierraleone-bumbuna.csv": "1ztNxJBo0Nn0xs5V6WqkAaOH_aywnow_q", 
    "togo-dapaong_qc.csv": "1eZKayFdWNNXmBA7_y10J5j0On7tEDpMm",
    "Benin_clean.csv": "1llMg2PlO97yN6Z9rbr4-SYuAH_T0Ehwt",
    "Sierraleone_clean.csv": "1te7S7NvcV345Y3nmGdr7EiieoNaQtHvP",
    "Togo_clean.csv": "1kvx4dYVvVeTgwENRBMKV_XD6WCg_TTh6"
}

# Google Drive File IDs for NOTEBOOK files
GDRIVE_NOTEBOOK_IDS = {
    "benin_eda.ipynb": "1KQtWIbOX16xwr72X9UY2zdmE3LNEtYVf",
    "sierraleone_eda.ipynb": "1fpszb4lgfTqQRINavV9uiogHkw-p54ni",
    "Togo_eda.ipynb": "1qSMqes0puCGrVHLOj3nsZbHkuWZciELG",
    "compare_countries.ipynb": "1nd0EyrkNupPqkrpxpOEEx9pME39w0uoV"
}

NOTEBOOK_PATTERNS = [
    "benin_eda.ipynb",
    "sierraleone_eda.ipynb", 
    "Togo_eda.ipynb",
    "compare_countries.ipynb"
]

@st.cache_data
def download_from_gdrive(file_id):
    """Download file from Google Drive and return as BytesIO object"""
    URL = "https://drive.google.com/uc?export=download&id="
    
    try:
        session = requests.Session()
        response = session.get(URL + file_id, stream=True)
        
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            st.error(f"Failed to download file {file_id}. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error downloading file {file_id}: {str(e)}")
        return None

@st.cache_data
def load_csv_from_gdrive(filename):
    """Load CSV file from Google Drive with caching"""
    if filename in GDRIVE_DATA_IDS:
        file_content = download_from_gdrive(GDRIVE_DATA_IDS[filename])
        if file_content is not None:
            try:
                return pd.read_csv(file_content)
            except Exception as e:
                st.error(f"Error loading {filename}: {str(e)}")
                return None
    return None

@st.cache_data
def load_notebook_from_gdrive(notebook_name):
    """Load notebook file from Google Drive with caching"""
    if notebook_name in GDRIVE_NOTEBOOK_IDS:
        file_content = download_from_gdrive(GDRIVE_NOTEBOOK_IDS[notebook_name])
        if file_content is not None:
            try:
                # Read the notebook content
                notebook_content = file_content.read().decode('utf-8')
                return notebook_content
            except Exception as e:
                st.error(f"Error loading notebook {notebook_name}: {str(e)}")
    return None

@st.cache_data
def find_notebooks():
    """Look for notebooks in Google Drive only"""
    nb_paths = []
    
    # Use Google Drive notebooks exclusively
    for notebook_name in GDRIVE_NOTEBOOK_IDS.keys():
        nb_paths.append(f"gdrive:{notebook_name}")
    
    return sorted(list(set(nb_paths)))

def extract_markdown_and_code(nb_path: str):
    """Return (markdown_text, combined_code) from notebook file."""
    try:
        # This is always a Google Drive notebook now
        notebook_name = nb_path.replace("gdrive:", "")
        notebook_content = load_notebook_from_gdrive(notebook_name)
        if notebook_content:
            nb = nbformat.reads(notebook_content, as_version=4)
        else:
            return "", ""
    except Exception as e:
        st.warning(f"Could not read notebook {nb_path}: {e}")
        return "", ""
    
    md_cells = []
    code_cells = []
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            md_cells.append(cell.source)
        elif cell.cell_type == "code":
            code_cells.append(cell.source)
    return "\n\n".join(md_cells), "\n\n".join(code_cells)

def create_safe_execution_environment():
    """Create a completely safe execution environment with pre-loaded data"""
    ns = {}
    
    # Provide essential imports
    ns['pd'] = pd
    ns['plt'] = plt
    ns['os'] = os
    ns['glob'] = glob
    ns['sys'] = sys
    ns['st'] = st
    ns['requests'] = requests
    ns['BytesIO'] = BytesIO
    ns['np'] = __import__('numpy')
    
    # Pre-load ALL data files into the namespace
    st.info("📥 Loading all data files from Google Drive...")
    
    # Load Benin data
    benin_data = load_csv_from_gdrive("benin-malanville.csv")
    if benin_data is not None:
        ns['benin_df'] = benin_data
        ns['df_benin'] = benin_data
        ns['benin_data'] = benin_data
        st.success("✅ Benin data loaded")
    
    # Load Sierra Leone data
    sierra_data = load_csv_from_gdrive("sierraleone-bumbuna.csv")
    if sierra_data is not None:
        ns['sierraleone_df'] = sierra_data
        ns['df_sierra'] = sierra_data
        ns['sierra_data'] = sierra_data
        ns['sierraleone_data'] = sierra_data
        st.success("✅ Sierra Leone data loaded")
    
    # Load Togo data
    togo_data = load_csv_from_gdrive("togo-dapaong_qc.csv")
    if togo_data is not None:
        ns['togo_df'] = togo_data
        ns['df_togo'] = togo_data
        ns['togo_data'] = togo_data
        st.success("✅ Togo data loaded")
    
    # Load clean data versions
    benin_clean = load_csv_from_gdrive("Benin_clean.csv")
    if benin_clean is not None:
        ns['benin_clean'] = benin_clean
        ns['df_benin_clean'] = benin_clean
        st.success("✅ Benin clean data loaded")
    
    sierra_clean = load_csv_from_gdrive("Sierraleone_clean.csv")
    if sierra_clean is not None:
        ns['sierraleone_clean'] = sierra_clean
        ns['df_sierra_clean'] = sierra_clean
        st.success("✅ Sierra Leone clean data loaded")
    
    togo_clean = load_csv_from_gdrive("Togo_clean.csv")
    if togo_clean is not None:
        ns['togo_clean'] = togo_clean
        ns['df_togo_clean'] = togo_clean
        st.success("✅ Togo clean data loaded")
    
    # Add data loading functions that return the pre-loaded data
    def load_benin_data():
        return ns.get('benin_df')
    
    def load_sierraleone_data():
        return ns.get('sierraleone_df')
    
    def load_togo_data():
        return ns.get('togo_df')
    
    def load_benin_clean():
        return ns.get('benin_clean')
    
    def load_sierraleone_clean():
        return ns.get('sierraleone_clean')
    
    def load_togo_clean():
        return ns.get('togo_clean')
    
    # Add helper functions to namespace
    ns['load_benin_data'] = load_benin_data
    ns['load_sierraleone_data'] = load_sierraleone_data
    ns['load_togo_data'] = load_togo_data
    ns['load_benin_clean'] = load_benin_clean
    ns['load_sierraleone_clean'] = load_sierraleone_clean
    ns['load_togo_clean'] = load_togo_clean
    
    return ns

def remove_file_loading_code(code: str):
    """Remove all file loading code from the notebook and replace with comments"""
    lines = code.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            cleaned_lines.append(line)
            continue
            
        # Check if this line contains file loading operations
        file_loading_patterns = [
            "pd.read_csv",
            "pd.read_excel", 
            "pd.read_json",
            "open(",
            "with open(",
            "load_csv_from_gdrive",
            "download_from_gdrive",
            ".csv",  # Any reference to CSV files
            ".xlsx",
            ".json",
            "read_csv",
            "read_excel"
        ]
        
        # Also check for specific file names that we know about
        known_files = [
            "togo-dapaong_qc.csv",
            "benin-malanville.csv", 
            "sierraleone-bumbuna.csv",
            "Benin_clean.csv",
            "Sierraleone_clean.csv",
            "Togo_clean.csv"
        ]
        
        is_file_loading = any(pattern in line for pattern in file_loading_patterns)
        is_known_file = any(file in line for file in known_files)
        
        if is_file_loading or is_known_file:
            # For any line that involves file loading, comment it out
            indent = len(line) - len(line.lstrip())
            comment_prefix = "# " + (" " * indent)
            
            # Check if this looks like an assignment
            if '=' in line and not line.strip().startswith('#'):
                # Try to preserve the variable assignment with a dummy value
                parts = line.split('=')
                if len(parts) > 1:
                    var_name = parts[0].strip()
                    cleaned_lines.append(f"{' ' * indent}{var_name} = None  # FILE LOADING REMOVED: Data is pre-loaded from Google Drive")
                else:
                    cleaned_lines.append(f"# {line}  # FILE LOADING REMOVED")
            else:
                # For non-assignment lines, just comment out
                cleaned_lines.append(f"# {line}  # FILE LOADING REMOVED")
        else:
            # Keep the original line
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def exec_code_collect_dfs(code: str, notebook_name: str) -> Dict[str, Any]:
    """Execute code in a safe environment with pre-loaded data"""
    
    # Create safe environment with pre-loaded data
    ns = create_safe_execution_environment()
    
    # Remove file loading code to prevent errors
    safe_code = remove_file_loading_code(code)
    
    try:
        # Execute the safe code (without file loading operations)
        exec(safe_code, ns)
        
    except Exception as e:
        st.warning("Notebook code execution failed. See error details below.")
        st.error(f"Execution error: {e}")
        
        # Show more detailed error information
        with st.expander("Detailed Error Traceback"):
            st.code(traceback.format_exc())
        
        # Show what code was executed
        with st.expander("See Code That Was Executed"):
            st.code(safe_code)
        
        # If it's a file not found error, provide specific guidance
        if "No such file or directory" in str(e):
            st.error("""
            **File Loading Error Detected**
            
            The notebook is still trying to load files locally. This has been disabled for security.
            
            **Available pre-loaded data:**
            - `benin_df` or `df_benin` - Benin data
            - `sierraleone_df` or `df_sierra` - Sierra Leone data  
            - `togo_df` or `df_togo` - Togo data
            - `benin_clean` - Clean Benin data
            - `sierraleone_clean` - Clean Sierra Leone data
            - `togo_clean` - Clean Togo data
            
            Use these variables directly instead of file loading.
            """)
    
    # collect dataframes
    dfs = {k: v for k, v in ns.items() if isinstance(v, pd.DataFrame)}
    return {'namespace': ns, 'dataframes': dfs, 'safe_code': safe_code}

def list_csvs():
    """List available CSV files from Google Drive"""
    return list(GDRIVE_DATA_IDS.keys())

def show_dataframe_eda(df: pd.DataFrame, name: str = 'DataFrame'):
    st.subheader(f"{name} — Basic summary")
    st.write('Shape:', df.shape)
    
    with st.expander('Show first 10 rows'):
        st.dataframe(df.head(10))
    
    with st.expander('Describe (numerical)'):
        st.dataframe(df.describe().T)
    
    # Show nulls
    nulls = df.isnull().sum()
    if nulls.sum() > 0:
        with st.expander('Null counts'):
            st.dataframe(nulls[nulls > 0])
    
    # Show column info
    with st.expander('Column information'):
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes,
            'Non-Null Count': df.count(),
            'Null Count': df.isnull().sum()
        })
        st.dataframe(col_info)
    
    # Simple plots
    numeric = df.select_dtypes(include='number')
    if numeric.shape[1] > 0:
        st.subheader('Numeric column analysis')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            hist_col = st.selectbox('Select column for histogram', 
                                  options=list(numeric.columns), 
                                  key=f'hist_{name}')
            bins = st.slider('Number of bins', 5, 100, 30, key=f'bins_{name}')
            
            fig, ax = plt.subplots()
            ax.hist(numeric[hist_col].dropna(), bins=bins, alpha=0.7, edgecolor='black')
            ax.set_xlabel(hist_col)
            ax.set_ylabel('Count')
            ax.set_title(f'Histogram of {hist_col}')
            st.pyplot(fig)
        
        with col2:
            # Correlation heatmap
            if numeric.shape[1] > 1:
                st.write('Correlation heatmap')
                corr = numeric.corr()
                fig2, ax2 = plt.subplots(figsize=(8, 6))
                im = ax2.imshow(corr, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
                
                # Add correlation values as text
                for i in range(len(corr.columns)):
                    for j in range(len(corr.columns)):
                        ax2.text(j, i, f'{corr.iloc[i, j]:.2f}',
                               ha="center", va="center", color="black", fontsize=8)
                
                ax2.set_xticks(range(len(corr.columns)))
                ax2.set_yticks(range(len(corr.columns)))
                ax2.set_xticklabels(corr.columns, rotation=45, ha='right')
                ax2.set_yticklabels(corr.columns)
                ax2.set_title('Correlation Matrix')
                fig2.colorbar(im)
                st.pyplot(fig2)
    else:
        st.info('No numeric columns detected for plotting.')

# ---- MAIN APP ----
st.sidebar.title("Navigation")

# Find notebooks and CSV files
notebooks = find_notebooks()
csv_files = list_csvs()

# Debug information
with st.sidebar.expander("Debug Info"):
    st.write("Current working directory:", os.getcwd())
    st.write("Found notebooks:", [nb.replace('gdrive:', '') for nb in notebooks])
    st.write("Available CSV files from Google Drive:", csv_files)

# Map simple labels for the user
label_map = {}
for nb in notebooks:
    notebook_name = nb.replace("gdrive:", "")
    base = notebook_name.lower()
        
    if 'benin' in base:
        label_map['Benin Analysis'] = nb
    elif 'sierra' in base or 'sierraleone' in base:
        label_map['Sierra Leone Analysis'] = nb
    elif 'togo' in base:
        label_map['Togo Analysis'] = nb
    elif 'compare' in base:
        label_map['Country Comparison'] = nb
    else:
        label_map[notebook_name] = nb

selection = st.sidebar.selectbox('Choose analysis to view', options=list(label_map.keys()))
nb_path = label_map[selection]

# Display notebook source information
notebook_name = nb_path.replace("gdrive:", "")
st.markdown(f"**Notebook:** `{notebook_name}` (from Google Drive)")

# Display available CSV files in sidebar
if csv_files:
    st.sidebar.subheader("Available Data Files (from Google Drive)")
    for csv_file in csv_files:
        st.sidebar.write(f"- {csv_file}")
else:
    st.sidebar.warning(f"No CSV files available")

# Extract and display markdown
md_text, code_text = extract_markdown_and_code(nb_path)
if md_text:
    with st.expander('Notebook markdown (click to expand)'):
        st.markdown(md_text)

# Show cleaned code (for debugging)
with st.expander('Show cleaned code (for debugging)'):
    safe_code = remove_file_loading_code(code_text)
    st.code(safe_code)
    st.info("Note: All file loading operations have been removed. Data is pre-loaded from Google Drive.")

# Pre-execution check for file loading patterns
file_loading_detected = any(pattern in code_text for pattern in [
    "pd.read_csv", ".csv", "open(", "with open(", "read_csv"
])

if file_loading_detected:
    st.warning("""
    ⚠️ **File loading operations detected**
    
    The notebook contains file loading code that will be automatically disabled.
    All data is already pre-loaded from Google Drive. Use these variables:
    
    - `benin_df`, `sierraleone_df`, `togo_df` - Raw data
    - `benin_clean`, `sierraleone_clean`, `togo_clean` - Clean data
    """)

# Try to execute code and collect dataframes
if st.button('Execute Notebook Code'):
    with st.spinner('Loading data from Google Drive and executing notebook...'):
        result = exec_code_collect_dfs(code_text, notebook_name)

    dfs = result.get('dataframes', {})
    
    # Filter out the pre-loaded dataframes to show only newly created ones
    preloaded_names = ['benin_df', 'df_benin', 'benin_data', 'sierraleone_df', 'df_sierra', 
                      'sierra_data', 'sierraleone_data', 'togo_df', 'df_togo', 'togo_data',
                      'benin_clean', 'df_benin_clean', 'sierraleone_clean', 'df_sierra_clean',
                      'togo_clean', 'df_togo_clean']
    
    new_dfs = {k: v for k, v in dfs.items() if k not in preloaded_names}
    
    if new_dfs:
        st.success(f'Found {len(new_dfs)} newly created DataFrame(s) in the executed notebook.')
        
        # Display all new dataframes in tabs
        tab_names = list(new_dfs.keys())
        tabs = st.tabs([f"📊 {name}" for name in tab_names])
        
        for i, (df_name, df) in enumerate(new_dfs.items()):
            with tabs[i]:
                show_dataframe_eda(df, name=df_name)
                
                # Add download button for each dataframe
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"Download {df_name} as CSV",
                    data=csv,
                    file_name=f"{df_name}.csv",
                    mime="text/csv",
                    key=f"download_{df_name}_{i}"
                )
    else:
        st.info('No new DataFrame objects were created by executing the notebook.')
        st.info('Showing pre-loaded dataframes instead:')
        
        # Show pre-loaded dataframes
        preloaded_dfs = {k: v for k, v in result['namespace'].items() 
                        if k in preloaded_names and isinstance(v, pd.DataFrame)}
        
        if preloaded_dfs:
            tab_names = list(preloaded_dfs.keys())
            tabs = st.tabs([f"📊 {name}" for name in tab_names])
            
            for i, (df_name, df) in enumerate(preloaded_dfs.items()):
                with tabs[i]:
                    show_dataframe_eda(df, name=df_name)

# Quick CSV loader in sidebar
st.sidebar.subheader("Quick CSV Loader")
if csv_files:
    selected_csv = st.sidebar.selectbox("Load CSV for quick EDA", 
                                       options=[""] + csv_files)
    if selected_csv:
        if st.sidebar.button("Analyze this CSV"):
            try:
                df_quick = load_csv_from_gdrive(selected_csv)
                if df_quick is not None:
                    show_dataframe_eda(df_quick, name=selected_csv)
                else:
                    st.sidebar.error(f"Failed to load: {selected_csv}")
            except Exception as e:
                st.sidebar.error(f"Failed to load: {e}")

st.markdown('---')
st.info(f'''
**Notes:** 
- All notebooks and data files are loaded directly from Google Drive
- No local file access - completely bypasses file system errors
- Data is pre-loaded before notebook execution
- File loading operations in notebooks are automatically removed
- Uses cached downloads for better performance
''')