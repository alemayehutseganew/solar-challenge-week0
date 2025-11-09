

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
import numpy as np

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
    """Load CSV file from Google Drive with caching and proper dtype handling"""
    if filename in GDRIVE_DATA_IDS:
        file_content = download_from_gdrive(GDRIVE_DATA_IDS[filename])
        if file_content is not None:
            try:
                # Load with explicit dtype specification to avoid PyArrow issues
                df = pd.read_csv(
                    file_content,
                    low_memory=False
                )
                
                # Fix problematic dtypes
                for col in df.columns:
                    # Convert object columns that should be numeric
                    if df[col].dtype == 'object':
                        try:
                            # Try to convert to numeric first
                            df[col] = pd.to_numeric(df[col], errors='ignore')
                        except:
                            pass
                    
                    # Fix datetime columns
                    if 'date' in col.lower() or 'time' in col.lower():
                        try:
                            df[col] = pd.to_datetime(df[col], errors='ignore')
                        except:
                            pass
                
                return df
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
    ns['np'] = np
    
    # Pre-load ALL data files into the namespace
    st.info("📥 Loading all data files from Google Drive...")
    
    # Load Benin data
    benin_data = load_csv_from_gdrive("benin-malanville.csv")
    if benin_data is not None:
        ns['benin_df'] = benin_data
        ns['df_benin'] = benin_data
        ns['benin_data'] = benin_data
        ns['df'] = benin_data  # Common generic name
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

def remove_file_loading_code(code: str, notebook_name: str):
    """Intelligently replace file loading code with proper data references"""
    
    # Define mapping of what the notebook is trying to load vs what we have pre-loaded
    file_mappings = {
        "benin.csv": "benin_df",
        "benin-malanville.csv": "benin_df", 
        "sierraleone-bumbuna.csv": "sierraleone_df",
        "togo-dapaong_qc.csv": "togo_df",
        "Benin_clean.csv": "benin_clean",
        "Sierraleone_clean.csv": "sierraleone_clean", 
        "Togo_clean.csv": "togo_clean"
    }
    
    cleaned_code = code
    
    # Replace specific file patterns with pre-loaded dataframe variables
    for file_pattern, df_variable in file_mappings.items():
        # Handle df = pd.read_csv("filename.csv") patterns
        assignment_pattern = r'(\w+)\s*=\s*pd\.read_csv\([\'"]' + re.escape(file_pattern) + r'[\'"]\)'
        replacement = r'\1 = ' + df_variable
        cleaned_code = re.sub(assignment_pattern, replacement, cleaned_code, flags=re.IGNORECASE)
        
        # Handle direct pd.read_csv("filename.csv") calls
        direct_pattern = r'pd\.read_csv\([\'"]' + re.escape(file_pattern) + r'[\'"]\)'
        cleaned_code = re.sub(direct_pattern, df_variable, cleaned_code, flags=re.IGNORECASE)
    
    # Handle URL patterns
    url_patterns = [
        (r'pd\.read_csv\([\'"]http://benin-malanville\.cs\.york\.ac\.uk[^\'"]*[\'"]\)', 'benin_df'),
        (r'pd\.read_csv\([\'"]http://sierraleone-bumbuna\.cs\.york\.ac\.uk[^\'"]*[\'"]\)', 'sierraleone_df'),
        (r'pd\.read_csv\([\'"]http://togo-dapaong\.cs\.york\.ac\.uk[^\'"]*[\'"]\)', 'togo_df'),
    ]
    
    for pattern, replacement in url_patterns:
        cleaned_code = re.sub(pattern, replacement, cleaned_code, flags=re.IGNORECASE)
    
    # For any remaining file loading operations, replace with safe code
    generic_patterns = [
        # Handle assignment patterns with any variable name
        (r'(\w+)\s*=\s*pd\.read_csv\([^)]+\)', r'\1 = None  # FILE LOADING: Data pre-loaded from Google Drive'),
        # Handle direct calls without assignment
        (r'pd\.read_csv\([^)]+\)', 'None  # FILE LOADING: Use pre-loaded data'),
        # Handle other file reading methods
        (r'pd\.read_excel\([^)]+\)', 'None  # FILE LOADING: Use pre-loaded data'),
        (r'pd\.read_json\([^)]+\)', 'None  # FILE LOADING: Use pre-loaded data'),
        (r'open\([^)]+\)', 'None  # FILE LOADING: Use pre-loaded data'),
    ]
    
    for pattern, replacement in generic_patterns:
        cleaned_code = re.sub(pattern, replacement, cleaned_code, flags=re.IGNORECASE)
    
    return cleaned_code

def exec_code_collect_dfs(code: str, notebook_name: str) -> Dict[str, Any]:
    """Execute code in a safe environment with pre-loaded data"""
    
    # Create safe environment with pre-loaded data
    ns = create_safe_execution_environment()
    
    # Remove file loading code to prevent errors - pass notebook_name for better mapping
    safe_code = remove_file_loading_code(code, notebook_name)
    
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
    
    # collect dataframes
    dfs = {k: v for k, v in ns.items() if isinstance(v, pd.DataFrame)}
    return {'namespace': ns, 'dataframes': dfs, 'safe_code': safe_code}

def list_csvs():
    """List available CSV files from Google Drive"""
    return list(GDRIVE_DATA_IDS.keys())

def fix_dataframe_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dataframe to avoid PyArrow datetime conversion issues"""
    df_fixed = df.copy()
    
    # Convert datetime columns to string for display to avoid PyArrow issues
    for col in df_fixed.columns:
        if pd.api.types.is_datetime64_any_dtype(df_fixed[col]):
            df_fixed[col] = df_fixed[col].astype(str)
        # Handle problematic object dtypes
        elif df_fixed[col].dtype == 'object':
            # Try to identify if it's actually numeric data stored as object
            try:
                # Sample a few values to check if they're numeric
                sample_values = df_fixed[col].dropna().head(10)
                if all(pd.to_numeric(sample_values, errors='coerce').notna()):
                    df_fixed[col] = pd.to_numeric(df_fixed[col], errors='coerce')
            except:
                pass
    
    return df_fixed

def get_numeric_columns(df: pd.DataFrame):
    """Safely get numeric columns from dataframe"""
    numeric_cols = []
    for col in df.columns:
        try:
            # Check if column can be converted to numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                numeric_cols.append(col)
            else:
                # Try to convert and check
                temp_series = pd.to_numeric(df[col], errors='coerce')
                if temp_series.notna().any():  # If any values successfully converted
                    numeric_cols.append(col)
        except:
            continue
    return numeric_cols

def show_dataframe_eda(df: pd.DataFrame, name: str = 'DataFrame'):
    st.subheader(f"{name} — Basic summary")
    st.write('Shape:', df.shape)
    
    # Fix dataframe for display to avoid PyArrow issues
    df_display = fix_dataframe_for_display(df)
    
    with st.expander('Show first 10 rows'):
        st.dataframe(df_display.head(10), width='stretch')
    
    with st.expander('Describe (numerical)'):
        # Safely get numeric columns for describe
        numeric_cols = get_numeric_columns(df)
        if numeric_cols:
            numeric_df = df[numeric_cols]
            desc_df = numeric_df.describe().T
            desc_df_fixed = fix_dataframe_for_display(desc_df)
            st.dataframe(desc_df_fixed, width='stretch')
        else:
            st.info('No numeric columns available for description')
    
    # Show nulls
    nulls = df.isnull().sum()
    if nulls.sum() > 0:
        with st.expander('Null counts'):
            nulls_df = pd.DataFrame({'Null Count': nulls[nulls > 0]})
            st.dataframe(nulls_df, width='stretch')
    
    # Show column info
    with st.expander('Column information'):
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.astype(str),  # Convert to string to avoid dtype issues
            'Non-Null Count': df.count(),
            'Null Count': df.isnull().sum()
        })
        st.dataframe(col_info, width='stretch')
    
    # Simple plots - only if we have numeric columns
    numeric_cols = get_numeric_columns(df)
    if numeric_cols:
        st.subheader('Numeric column analysis')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            hist_col = st.selectbox('Select column for histogram', 
                                  options=numeric_cols, 
                                  key=f'hist_{name}')
            
            if hist_col in df.columns:
                # Safely get numeric data for histogram
                hist_data = pd.to_numeric(df[hist_col], errors='coerce').dropna()
                if len(hist_data) > 0:
                    bins = st.slider('Number of bins', 5, 100, 30, key=f'bins_{name}')
                    
                    fig, ax = plt.subplots()
                    ax.hist(hist_data, bins=bins, alpha=0.7, edgecolor='black')
                    ax.set_xlabel(hist_col)
                    ax.set_ylabel('Count')
                    ax.set_title(f'Histogram of {hist_col}')
                    st.pyplot(fig)
                else:
                    st.warning(f"No numeric data available for {hist_col}")
            else:
                st.warning(f"Column {hist_col} not found in dataframe")
        
        with col2:
            # Correlation heatmap - only if we have multiple numeric columns
            if len(numeric_cols) > 1:
                st.write('Correlation heatmap')
                try:
                    # Safely create correlation matrix
                    numeric_data = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
                    corr = numeric_data.corr()
                    
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
                except Exception as e:
                    st.error(f"Could not create correlation heatmap: {e}")
            else:
                st.info('Need at least 2 numeric columns for correlation heatmap')
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
    safe_code = remove_file_loading_code(code_text, notebook_name)
    st.code(safe_code)
    st.info("Note: File loading operations have been replaced with pre-loaded data references.")

# Try to execute code and collect dataframes
if st.button('Execute Notebook Code'):
    with st.spinner('Loading data from Google Drive and executing notebook...'):
        result = exec_code_collect_dfs(code_text, notebook_name)

    dfs = result.get('dataframes', {})
    
    # Filter out the pre-loaded dataframes to show only newly created ones
    preloaded_names = ['benin_df', 'df_benin', 'benin_data', 'sierraleone_df', 'df_sierra', 
                      'sierra_data', 'sierraleone_data', 'togo_df', 'df_togo', 'togo_data',
                      'benin_clean', 'df_benin_clean', 'sierraleone_clean', 'df_sierra_clean',
                      'togo_clean', 'df_togo_clean', 'df']  # Added 'df' as common generic name
    
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
                    key=f"download_{df_name}_{i}",
                    width='stretch'
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
        if st.sidebar.button("Analyze this CSV", width='stretch'):
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
- File loading operations in notebooks are automatically replaced with pre-loaded data references
- Uses cached downloads for better performance
- Enhanced data type handling to avoid NumPy object dtype issues
''')