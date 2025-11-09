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

# st.set_page_config(page_title="Solar Challenge EDA Dashboard", layout="wide")

# HEADER = "Solar Challenge EDA Dashboard — Benin / Sierra Leone / Togo / Comparison"
# st.title(HEADER)

# # Directory constants - adjusted based on your git status
# NOTEBOOK_DIR = "."  # Current directory since Togo_eda.ipynb is in parent
# DATA_DIR = "./data"

# NOTEBOOK_PATTERNS = [
#     "benin_eda.ipynb",
#     "sierraleone_eda.ipynb", 
#     "Togo_eda.ipynb",
#     "compare_countries.ipynb"
# ]

# @st.cache_data
# def find_notebooks(base_dir: str = NOTEBOOK_DIR):
#     """Look for notebooks in the specified directory"""
#     nb_paths = []
    
#     # First try exact patterns
#     for pat in NOTEBOOK_PATTERNS:
#         # Try in current directory
#         full_path = os.path.join(base_dir, pat)
#         if os.path.exists(full_path):
#             nb_paths.append(full_path)
#         # Also try in parent directory (based on git status)
#         parent_path = os.path.join("..", pat)
#         if os.path.exists(parent_path):
#             nb_paths.append(parent_path)
    
#     # If no notebooks found with exact patterns, search broadly
#     if not nb_paths:
#         # Search current directory
#         nb_paths.extend(glob.glob(os.path.join(base_dir, "*.ipynb")))
#         # Search parent directory
#         nb_paths.extend(glob.glob(os.path.join("..", "*.ipynb")))
    
#     return sorted(list(set(nb_paths)))

# def extract_markdown_and_code(nb_path: str):
#     """Return (markdown_text, combined_code) from notebook file."""
#     try:
#         nb = nbformat.read(nb_path, as_version=4)
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

# def fix_data_paths_in_code(code: str):
#     """Fix common data path patterns in notebook code"""
#     # Replace common relative path patterns with correct DATA_DIR paths
#     fixes = [
#         ("'benin-malanville.csv'", f"'{DATA_DIR}/benin-malanville.csv'"),
#         ("'sierraleone-bumbuna.csv'", f"'{DATA_DIR}/sierraleone-bumbuna.csv'"),
#         ("'togo-dapaong_qc.csv'", f"'{DATA_DIR}/togo-dapaong_qc.csv'"),
#         ("'Benin_clean.csv'", f"'{DATA_DIR}/Benin_clean.csv'"),
#         ("'Sierraleone_clean.csv'", f"'{DATA_DIR}/Sierraleone_clean.csv'"),
#         ("'Togo_clean.csv'", f"'{DATA_DIR}/Togo_clean.csv'"),
#         ('"benin-malanville.csv"', f'"{DATA_DIR}/benin-malanville.csv"'),
#         ('"sierraleone-bumbuna.csv"', f'"{DATA_DIR}/sierraleone-bumbuna.csv"'),
#         ('"togo-dapaong_qc.csv"', f'"{DATA_DIR}/togo-dapaong_qc.csv"'),
#         ('"Benin_clean.csv"', f'"{DATA_DIR}/Benin_clean.csv"'),
#         ('"Sierraleone_clean.csv"', f'"{DATA_DIR}/Sierraleone_clean.csv"'),
#         ('"Togo_clean.csv"', f'"{DATA_DIR}/Togo_clean.csv"'),
#         # Handle various path patterns
#         ("'../data/benin-malanville.csv'", f"'{DATA_DIR}/benin-malanville.csv'"),
#         ("'../data/sierraleone-bumbuna.csv'", f"'{DATA_DIR}/sierraleone-bumbuna.csv'"),
#         ("'../data/togo-dapaong_qc.csv'", f"'{DATA_DIR}/togo-dapaong_qc.csv'"),
#         ("'./benin-malanville.csv'", f"'{DATA_DIR}/benin-malanville.csv'"),
#         ("'./sierraleone-bumbuna.csv'", f"'{DATA_DIR}/sierraleone-bumbuna.csv'"),
#         ("'./togo-dapaong_qc.csv'", f"'{DATA_DIR}/togo-dapaong_qc.csv'"),
#     ]
    
#     fixed_code = code
#     for old, new in fixes:
#         fixed_code = fixed_code.replace(old, new)
    
#     return fixed_code

# def exec_code_collect_dfs(code: str, notebook_name: str) -> Dict[str, Any]:
#     """Execute code in a restricted namespace and collect pandas DataFrames."""
#     ns: Dict[str, Any] = {}
    
#     # Provide essential imports
#     ns['pd'] = pd
#     ns['plt'] = plt
#     ns['os'] = os
#     ns['glob'] = glob
#     ns['sys'] = sys
    
#     # Fix data paths in the code before execution
#     fixed_code = fix_data_paths_in_code(code)
    
#     # Add data loading helper functions to namespace
#     def load_benin_data():
#         return pd.read_csv(f'{DATA_DIR}/benin-malanville.csv')
    
#     def load_sierraleone_data():
#         return pd.read_csv(f'{DATA_DIR}/sierraleone-bumbuna.csv')
    
#     def load_togo_data():
#         return pd.read_csv(f'{DATA_DIR}/togo-dapaong_qc.csv')
    
#     def load_benin_clean():
#         return pd.read_csv(f'{DATA_DIR}/Benin_clean.csv')
    
#     def load_sierraleone_clean():
#         return pd.read_csv(f'{DATA_DIR}/Sierraleone_clean.csv')
    
#     def load_togo_clean():
#         return pd.read_csv(f'{DATA_DIR}/Togo_clean.csv')
    
#     # Add helper functions to namespace
#     ns['load_benin_data'] = load_benin_data
#     ns['load_sierraleone_data'] = load_sierraleone_data
#     ns['load_togo_data'] = load_togo_data
#     ns['load_benin_clean'] = load_benin_clean
#     ns['load_sierraleone_clean'] = load_sierraleone_clean
#     ns['load_togo_clean'] = load_togo_clean
    
#     # Add directory constants to namespace
#     ns['NOTEBOOK_DIR'] = NOTEBOOK_DIR
#     ns['DATA_DIR'] = DATA_DIR
    
#     try:
#         # Execute the fixed code
#         exec(fixed_code, ns)
        
#     except Exception as e:
#         st.warning("Notebook code execution failed. See error details below.")
#         st.error(f"Execution error: {e}")
#         st.text(traceback.format_exc())
    
#     # collect dataframes
#     dfs = {k: v for k, v in ns.items() if isinstance(v, pd.DataFrame)}
#     return {'namespace': ns, 'dataframes': dfs, 'fixed_code': fixed_code}

# def list_csvs(base_dir: str = DATA_DIR):
#     """Look for CSV files in the data directory"""
#     csv_files = []
    
#     # Try primary data directory
#     if os.path.exists(base_dir):
#         csv_files.extend(glob.glob(os.path.join(base_dir, '*.csv')))
    
#     # Also try parent data directory
#     parent_data_dir = os.path.join("..", "data")
#     if os.path.exists(parent_data_dir):
#         csv_files.extend(glob.glob(os.path.join(parent_data_dir, '*.csv')))
    
#     return sorted(list(set(csv_files)))

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
#     st.write("Found notebooks:", [os.path.basename(nb) for nb in notebooks])
#     st.write("Found CSV files:", [os.path.basename(csv) for csv in csv_files])

# if not notebooks:
#     st.error(f'No notebooks found. Looking for: {NOTEBOOK_PATTERNS}')
    
#     # Show directory contents for debugging
#     st.info("Current directory contents:")
#     for item in os.listdir("."):
#         st.write(f"- {item}")
    
#     st.info("Parent directory contents:")
#     for item in os.listdir(".."):
#         st.write(f"- {item}")
#     st.stop()

# # Map simple labels for the user
# label_map = {}
# for nb in notebooks:
#     base = os.path.basename(nb).lower()
#     if 'benin' in base:
#         label_map['Benin Analysis'] = nb
#     elif 'sierra' in base or 'sierraleone' in base:
#         label_map['Sierra Leone Analysis'] = nb
#     elif 'togo' in base:
#         label_map['Togo Analysis'] = nb
#     elif 'compare' in base:
#         label_map['Country Comparison'] = nb
#     else:
#         label_map[os.path.splitext(os.path.basename(nb))[0]] = nb

# selection = st.sidebar.selectbox('Choose analysis to view', options=list(label_map.keys()))
# nb_path = label_map[selection]
# st.markdown(f"**Notebook:** `{os.path.basename(nb_path)}` (from `{os.path.dirname(nb_path) or 'current dir'}`)")

# # Display available CSV files in sidebar
# if csv_files:
#     st.sidebar.subheader("Available Data Files")
#     for csv_file in csv_files:
#         st.sidebar.write(f"- {os.path.basename(csv_file)}")
# else:
#     st.sidebar.warning(f"No CSV files found in data directories")

# # Extract and display markdown
# md_text, code_text = extract_markdown_and_code(nb_path)
# if md_text:
#     with st.expander('Notebook markdown (click to expand)'):
#         st.markdown(md_text)

# # Show fixed code (for debugging)
# with st.expander('Show fixed code (for debugging)'):
#     fixed_code = fix_data_paths_in_code(code_text)
#     st.code(fixed_code)

# # Try to execute code and collect dataframes
# if st.button('Execute Notebook Code'):
#     with st.spinner('Executing notebook code (with path fixes)...'):
#         result = exec_code_collect_dfs(code_text, os.path.basename(nb_path))

#     dfs = result.get('dataframes', {})
#     if dfs:
#         st.success(f'Found {len(dfs)} DataFrame(s) in the executed notebook.')
        
#         # Display all dataframes in tabs
#         tab_names = list(dfs.keys())
#         tabs = st.tabs([f"📊 {name}" for name in tab_names])
        
#         for i, (df_name, df) in enumerate(dfs.items()):
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
#         st.info('No DataFrame objects were created by executing the notebook.')
        
#         # Fallback: Load data based on selected notebook
#         st.info('Trying to load data files directly...')
        
#         # Map notebook types to possible data files
#         notebook_data_map = {
#             'benin': ['benin-malanville.csv', 'Benin_clean.csv'],
#             'sierra': ['sierraleone-bumbuna.csv', 'Sierraleone_clean.csv'],
#             'togo': ['togo-dapaong_qc.csv', 'Togo_clean.csv']
#         }
        
#         loaded = False
#         for key, files in notebook_data_map.items():
#             if key in selection.lower():
#                 for data_file in files:
#                     # Try multiple possible locations
#                     possible_paths = [
#                         os.path.join(DATA_DIR, data_file),
#                         os.path.join("..", "data", data_file),
#                         data_file  # current directory
#                     ]
                    
#                     for csv_path in possible_paths:
#                         if os.path.exists(csv_path):
#                             try:
#                                 df_csv = pd.read_csv(csv_path)
#                                 st.success(f"Loaded: {os.path.basename(csv_path)}")
#                                 show_dataframe_eda(df_csv, name=os.path.basename(csv_path))
#                                 loaded = True
#                                 break
#                             except Exception as e:
#                                 st.error(f"Failed to load {csv_path}: {e}")
        
#         if not loaded and csv_files:
#             st.warning("Could not load specific files. Try loading any available CSV:")
#             for csv_file in csv_files[:3]:  # Try first 3 CSVs
#                 try:
#                     df_csv = pd.read_csv(csv_file)
#                     st.success(f"Loaded: {os.path.basename(csv_file)}")
#                     show_dataframe_eda(df_csv, name=os.path.basename(csv_file))
#                     break
#                 except Exception as e:
#                     st.error(f"Failed to load {csv_file}: {e}")

# # Quick CSV loader in sidebar
# st.sidebar.subheader("Quick CSV Loader")
# if csv_files:
#     selected_csv = st.sidebar.selectbox("Load CSV for quick EDA", 
#                                        options=[""] + [os.path.basename(f) for f in csv_files])
#     if selected_csv:
#         # Find the full path for the selected CSV
#         csv_path = None
#         for csv_file in csv_files:
#             if os.path.basename(csv_file) == selected_csv:
#                 csv_path = csv_file
#                 break
        
#         if csv_path and st.sidebar.button("Analyze this CSV"):
#             try:
#                 df_quick = pd.read_csv(csv_path)
#                 show_dataframe_eda(df_quick, name=selected_csv)
#             except Exception as e:
#                 st.sidebar.error(f"Failed to load: {e}")

# st.markdown('---')
# st.info(f'''
# **Notes:** 
# - This app searches for notebooks in current and parent directories
# - Data files are loaded from: `{DATA_DIR}` and parent data directory
# - Path issues are automatically fixed during execution
# - Use the Quick CSV Loader if notebook execution fails
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

st.set_page_config(page_title="Solar Challenge EDA Dashboard", layout="wide")

HEADER = "Solar Challenge EDA Dashboard — Benin / Sierra Leone / Togo / Comparison"
st.title(HEADER)

# Directory constants - adjusted based on your git status
NOTEBOOK_DIR = "."  # Current directory since Togo_eda.ipynb is in parent
DATA_DIR = "./data"

# Google Drive File IDs extracted from your links
GDRIVE_FILE_IDS = {
    "benin-malanville.csv": "1YQSDdFo-PV2UAXR2_xwfpSVMIElcR14j",
    "sierraleone-bumbuna.csv": "1ztNxJBo0Nn0xs5V6WqkAaOH_aywnow_q", 
    "togo-dapaong_qc.csv": "1eZKayFdWNNXmBA7_y10J5j0On7tEDpMm",
    "Benin_clean.csv": "1llMg2PlO97yN6Z9rbr4-SYuAH_T0Ehwt",
    "Sierraleone_clean.csv": "1te7S7NvcV345Y3nmGdr7EiieoNaQtHvP",
    "Togo_clean.csv": "1kvx4dYVvVeTgwENRBMKV_XD6WCg_TTh6"
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
    if filename in GDRIVE_FILE_IDS:
        file_content = download_from_gdrive(GDRIVE_FILE_IDS[filename])
        if file_content is not None:
            try:
                return pd.read_csv(file_content)
            except Exception as e:
                st.error(f"Error loading {filename}: {str(e)}")
    return None

@st.cache_data
def find_notebooks(base_dir: str = NOTEBOOK_DIR):
    """Look for notebooks in the specified directory"""
    nb_paths = []
    
    # First try exact patterns
    for pat in NOTEBOOK_PATTERNS:
        # Try in current directory
        full_path = os.path.join(base_dir, pat)
        if os.path.exists(full_path):
            nb_paths.append(full_path)
        # Also try in parent directory (based on git status)
        parent_path = os.path.join("..", pat)
        if os.path.exists(parent_path):
            nb_paths.append(parent_path)
    
    # If no notebooks found with exact patterns, search broadly
    if not nb_paths:
        # Search current directory
        nb_paths.extend(glob.glob(os.path.join(base_dir, "*.ipynb")))
        # Search parent directory
        nb_paths.extend(glob.glob(os.path.join("..", "*.ipynb")))
    
    return sorted(list(set(nb_paths)))

def extract_markdown_and_code(nb_path: str):
    """Return (markdown_text, combined_code) from notebook file."""
    try:
        nb = nbformat.read(nb_path, as_version=4)
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

def fix_data_paths_in_code(code: str):
    """Fix common data path patterns in notebook code"""
    # Replace common relative path patterns with correct DATA_DIR paths
    fixes = [
        ("'benin-malanville.csv'", f"'{DATA_DIR}/benin-malanville.csv'"),
        ("'sierraleone-bumbuna.csv'", f"'{DATA_DIR}/sierraleone-bumbuna.csv'"),
        ("'togo-dapaong_qc.csv'", f"'{DATA_DIR}/togo-dapaong_qc.csv'"),
        ("'Benin_clean.csv'", f"'{DATA_DIR}/Benin_clean.csv'"),
        ("'Sierraleone_clean.csv'", f"'{DATA_DIR}/Sierraleone_clean.csv'"),
        ("'Togo_clean.csv'", f"'{DATA_DIR}/Togo_clean.csv'"),
        ('"benin-malanville.csv"', f'"{DATA_DIR}/benin-malanville.csv"'),
        ('"sierraleone-bumbuna.csv"', f'"{DATA_DIR}/sierraleone-bumbuna.csv"'),
        ('"togo-dapaong_qc.csv"', f'"{DATA_DIR}/togo-dapaong_qc.csv"'),
        ('"Benin_clean.csv"', f'"{DATA_DIR}/Benin_clean.csv"'),
        ('"Sierraleone_clean.csv"', f'"{DATA_DIR}/Sierraleone_clean.csv"'),
        ('"Togo_clean.csv"', f'"{DATA_DIR}/Togo_clean.csv"'),
        # Handle various path patterns
        ("'../data/benin-malanville.csv'", f"'{DATA_DIR}/benin-malanville.csv'"),
        ("'../data/sierraleone-bumbuna.csv'", f"'{DATA_DIR}/sierraleone-bumbuna.csv'"),
        ("'../data/togo-dapaong_qc.csv'", f"'{DATA_DIR}/togo-dapaong_qc.csv'"),
        ("'./benin-malanville.csv'", f"'{DATA_DIR}/benin-malanville.csv'"),
        ("'./sierraleone-bumbuna.csv'", f"'{DATA_DIR}/sierraleone-bumbuna.csv'"),
        ("'./togo-dapaong_qc.csv'", f"'{DATA_DIR}/togo-dapaong_qc.csv'"),
    ]
    
    fixed_code = code
    for old, new in fixes:
        fixed_code = fixed_code.replace(old, new)
    
    return fixed_code

def exec_code_collect_dfs(code: str, notebook_name: str) -> Dict[str, Any]:
    """Execute code in a restricted namespace and collect pandas DataFrames."""
    ns: Dict[str, Any] = {}
    
    # Provide essential imports
    ns['pd'] = pd
    ns['plt'] = plt
    ns['os'] = os
    ns['glob'] = glob
    ns['sys'] = sys
    ns['st'] = st
    ns['requests'] = requests
    ns['BytesIO'] = BytesIO
    
    # Fix data paths in the code before execution
    fixed_code = fix_data_paths_in_code(code)
    
    # Add data loading helper functions to namespace that use Google Drive
    def load_benin_data():
        return load_csv_from_gdrive("benin-malanville.csv")
    
    def load_sierraleone_data():
        return load_csv_from_gdrive("sierraleone-bumbuna.csv")
    
    def load_togo_data():
        return load_csv_from_gdrive("togo-dapaong_qc.csv")
    
    def load_benin_clean():
        return load_csv_from_gdrive("Benin_clean.csv")
    
    def load_sierraleone_clean():
        return load_csv_from_gdrive("Sierraleone_clean.csv")
    
    def load_togo_clean():
        return load_csv_from_gdrive("Togo_clean.csv")
    
    # Add helper functions to namespace
    ns['load_benin_data'] = load_benin_data
    ns['load_sierraleone_data'] = load_sierraleone_data
    ns['load_togo_data'] = load_togo_data
    ns['load_benin_clean'] = load_benin_clean
    ns['load_sierraleone_clean'] = load_sierraleone_clean
    ns['load_togo_clean'] = load_togo_clean
    
    # Add directory constants to namespace
    ns['NOTEBOOK_DIR'] = NOTEBOOK_DIR
    ns['DATA_DIR'] = DATA_DIR
    
    # Add Google Drive file IDs to namespace
    ns['GDRIVE_FILE_IDS'] = GDRIVE_FILE_IDS
    ns['download_from_gdrive'] = download_from_gdrive
    ns['load_csv_from_gdrive'] = load_csv_from_gdrive
    
    try:
        # Execute the fixed code
        exec(fixed_code, ns)
        
    except Exception as e:
        st.warning("Notebook code execution failed. See error details below.")
        st.error(f"Execution error: {e}")
        st.text(traceback.format_exc())
    
    # collect dataframes
    dfs = {k: v for k, v in ns.items() if isinstance(v, pd.DataFrame)}
    return {'namespace': ns, 'dataframes': dfs, 'fixed_code': fixed_code}

def list_csvs():
    """List available CSV files from Google Drive"""
    return list(GDRIVE_FILE_IDS.keys())

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
    st.write("Found notebooks:", [os.path.basename(nb) for nb in notebooks])
    st.write("Available CSV files from Google Drive:", csv_files)

if not notebooks:
    st.error(f'No notebooks found. Looking for: {NOTEBOOK_PATTERNS}')
    
    # Show directory contents for debugging
    st.info("Current directory contents:")
    for item in os.listdir("."):
        st.write(f"- {item}")
    
    st.info("Parent directory contents:")
    for item in os.listdir(".."):
        st.write(f"- {item}")
    st.stop()

# Map simple labels for the user
label_map = {}
for nb in notebooks:
    base = os.path.basename(nb).lower()
    if 'benin' in base:
        label_map['Benin Analysis'] = nb
    elif 'sierra' in base or 'sierraleone' in base:
        label_map['Sierra Leone Analysis'] = nb
    elif 'togo' in base:
        label_map['Togo Analysis'] = nb
    elif 'compare' in base:
        label_map['Country Comparison'] = nb
    else:
        label_map[os.path.splitext(os.path.basename(nb))[0]] = nb

selection = st.sidebar.selectbox('Choose analysis to view', options=list(label_map.keys()))
nb_path = label_map[selection]
st.markdown(f"**Notebook:** `{os.path.basename(nb_path)}` (from `{os.path.dirname(nb_path) or 'current dir'}`)")

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

# Show fixed code (for debugging)
with st.expander('Show fixed code (for debugging)'):
    fixed_code = fix_data_paths_in_code(code_text)
    st.code(fixed_code)

# Try to execute code and collect dataframes
if st.button('Execute Notebook Code'):
    with st.spinner('Executing notebook code (with Google Drive data)...'):
        result = exec_code_collect_dfs(code_text, os.path.basename(nb_path))

    dfs = result.get('dataframes', {})
    if dfs:
        st.success(f'Found {len(dfs)} DataFrame(s) in the executed notebook.')
        
        # Display all dataframes in tabs
        tab_names = list(dfs.keys())
        tabs = st.tabs([f"📊 {name}" for name in tab_names])
        
        for i, (df_name, df) in enumerate(dfs.items()):
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
        st.info('No DataFrame objects were created by executing the notebook.')
        
        # Fallback: Load data based on selected notebook
        st.info('Trying to load data files directly from Google Drive...')
        
        # Map notebook types to possible data files
        notebook_data_map = {
            'benin': ['benin-malanville.csv', 'Benin_clean.csv'],
            'sierra': ['sierraleone-bumbuna.csv', 'Sierraleone_clean.csv'],
            'togo': ['togo-dapaong_qc.csv', 'Togo_clean.csv']
        }
        
        loaded = False
        for key, files in notebook_data_map.items():
            if key in selection.lower():
                for data_file in files:
                    if data_file in GDRIVE_FILE_IDS:
                        try:
                            df_csv = load_csv_from_gdrive(data_file)
                            if df_csv is not None:
                                st.success(f"Loaded from Google Drive: {data_file}")
                                show_dataframe_eda(df_csv, name=data_file)
                                loaded = True
                        except Exception as e:
                            st.error(f"Failed to load {data_file}: {e}")
        
        if not loaded and csv_files:
            st.warning("Could not load specific files. Try loading any available CSV:")
            for csv_file in csv_files[:3]:  # Try first 3 CSVs
                try:
                    df_csv = load_csv_from_gdrive(csv_file)
                    if df_csv is not None:
                        st.success(f"Loaded: {csv_file}")
                        show_dataframe_eda(df_csv, name=csv_file)
                        break
                except Exception as e:
                    st.error(f"Failed to load {csv_file}: {e}")

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
- This app searches for notebooks in current and parent directories
- Data files are loaded from Google Drive (bypassing GitHub size limits)
- Path issues are automatically fixed during execution
- Use the Quick CSV Loader if notebook execution fails
- Google Drive files are cached for better performance
''')