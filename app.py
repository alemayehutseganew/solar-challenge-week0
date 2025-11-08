<<<<<<< HEAD
# import streamlit as st
# import nbformat
# import os
# import pandas as pd
# import glob
# import matplotlib
# matplotlib.use("Agg")   # Important for Streamlit Cloud
# import matplotlib.pyplot as plt

# st.set_page_config(page_title="Solar Challenge EDA Dashboard", layout="wide")
# st.title("Solar Data Discovery Dashboard — Benin / Sierra Leone / Togo / Comparison")

# # === Directory Constants ===
# NOTEBOOK_DIR = "notebooks"
# DATA_DIR = "data"

# NOTEBOOK_FILES = {
#     "Benin Analysis": "benin_eda.ipynb",
#     "Sierra Leone Analysis": "sierraleone_eda.ipynb",
#     "Togo Analysis": "Togo_eda.ipynb",
#     "Country Comparison": "compare_countries.ipynb"
# }


# def read_notebook_markdown(nb_path):
#     """Extract markdown content only (safe for Streamlit Cloud)"""
#     nb = nbformat.read(nb_path, as_version=4)
#     md_parts = [cell.source for cell in nb.cells if cell.cell_type == "markdown"]
#     return "\n\n".join(md_parts)


# def load_available_csvs():
#     return sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))


# def show_dataframe(df, title):
#     st.subheader(f"📊 {title}")
#     st.write("Shape:", df.shape)
#     st.dataframe(df.head())

#     if df.select_dtypes(include="number").shape[1] > 0:
#         col = st.selectbox(f"Select a numeric column to plot for {title}", df.select_dtypes(include="number").columns)
#         fig, ax = plt.subplots()
#         ax.hist(df[col].dropna())
#         st.pyplot(fig)


# # === SIDEBAR NAVIGATION ===
# selection = st.sidebar.radio("Choose Analysis", list(NOTEBOOK_FILES.keys()))

# notebook_path = os.path.join(NOTEBOOK_DIR, NOTEBOOK_FILES[selection])

# if not os.path.exists(notebook_path):
#     st.error(f"Notebook not found: {notebook_path}")
#     st.stop()

# st.success(f"Loaded Notebook: `{NOTEBOOK_FILES[selection]}`")

# # === DISPLAY NOTEBOOK MARKDOWN ===
# with st.expander("📘 Notebook Summary (Markdown)"):
#     markdown_content = read_notebook_markdown(notebook_path)
#     st.markdown(markdown_content)

# # === SHOW RELATED DATA ===
# st.markdown("---")
# st.subheader("📂 Related Data Files")

# data_files = load_available_csvs()

# if not data_files:
#     st.warning(f"No CSV files found inside `{DATA_DIR}` directory.")
# else:
#     file_choice = st.selectbox("Select a CSV file to preview:", [""] + [os.path.basename(f) for f in data_files])

#     if file_choice:
#         df = pd.read_csv(os.path.join(DATA_DIR, file_choice))
#         show_dataframe(df, file_choice)

# st.markdown("---")
# st.info("""
# **About this Dashboard**
# - Built by *Alemayehu Tseganew* for Week 0 Solar Data Exploration.
# - Notebooks are displayed as readable summaries.
# - Data Preview and EDA tools are interactive.
# """)

# """app.py - Advanced Streamlit Dashboard (deployment-ready, works without large CSVs)

# Features:
# - Discovers notebooks in ./notebooks (if present) and extracts markdown & code
# - Safe notebook rendering (markdown), code preview (no automatic execution)
# - Smart insight extraction & keyword frequency
# - Global keyword search across notebooks
# - Text-based "Country Comparison" scorecards derived from notebook text
# - Synthetic data generator for interactive visualizations when CSVs are not present
# - Downloadable insight reports and synthetic sample CSV
# - Clean tabbed UI with sidebar controls

# Notes:
# - This app intentionally DOES NOT execute notebook code to remain safe in deployment.
# - If you have notebooks in the "notebooks" folder they will be used; otherwise the app
#   falls back to synthetic demo content.

# Recommended: deploy this to Streamlit Cloud as your app's `app.py`.

# """








=======
>>>>>>> a96ed0d (Week0)

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

st.set_page_config(page_title="Solar Challenge EDA Dashboard", layout="wide")

HEADER = "Solar Data Discovery: Week 0 Challenge Dashboard — Benin / Sierra Leone / Togo and  Comparison for those countris"
st.title(HEADER)
<<<<<<< HEAD

# Directory constants - UPDATED TO USE YOUR CONSTANTS
NOTEBOOK_DIR = "notebooks"
DATA_DIR = "data"

# UPDATED TO USE YOUR DICTIONARY
NOTEBOOK_FILES = {
    "Benin Analysis": "benin_eda.ipynb",
    "Sierra Leone Analysis": "sierraleone_eda.ipynb",
    "Togo Analysis": "Togo_eda.ipynb",
    "Country Comparison": "compare_countries.ipynb"
}

@st.cache_data
def find_notebooks(base_dir: str = NOTEBOOK_DIR):
    """Look for notebooks in the notebooks directory using the NOTEBOOK_FILES mapping"""
    nb_paths = []
    for display_name, notebook_file in NOTEBOOK_FILES.items():
        full_path = os.path.join(base_dir, notebook_file)
        if os.path.exists(full_path):
            nb_paths.append((display_name, full_path))
        else:
            st.warning(f"Notebook not found: {full_path}")
    
    # If no notebooks found with exact patterns, search for any .ipynb files
    if not nb_paths:
        all_nb_paths = glob.glob(os.path.join(base_dir, "*.ipynb"))
        nb_paths = [(os.path.splitext(os.path.basename(path))[0], path) for path in all_nb_paths]
    
    return sorted(nb_paths, key=lambda x: x[0])

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
        # Handle paths with ./data/ prefix (in case notebooks already use them)
        ("'./data/benin-malanville.csv'", f"'{DATA_DIR}/benin-malanville.csv'"),
        ("'./data/sierraleone-bumbuna.csv'", f"'{DATA_DIR}/sierraleone-bumbuna.csv'"),
        ("'./data/togo-dapaong_qc.csv'", f"'{DATA_DIR}/togo-dapaong_qc.csv'"),
        ("'./data/Benin_clean.csv'", f"'{DATA_DIR}/Benin_clean.csv'"),
        ("'./data/Sierraleone_clean.csv'", f"'{DATA_DIR}/Sierraleone_clean.csv'"),
        ("'./data/Togo_clean.csv'", f"'{DATA_DIR}/Togo_clean.csv'"),
    ]
    
    fixed_code = code
    for old, new in fixes:
        fixed_code = fixed_code.replace(old, new)
    
    return fixed_code

def exec_code_collect_dfs(code: str, notebook_name: str) -> Dict[str, Any]:
    
    ns: Dict[str, Any] = {}
    
    # Provide essential imports
    ns['pd'] = pd
    ns['plt'] = plt
    ns['os'] = os
    ns['glob'] = glob
    ns['sys'] = sys
    
    # Fix data paths in the code before execution
    fixed_code = fix_data_paths_in_code(code)
    
    # Add data loading helper functions to namespace
    def load_benin_data():
        return pd.read_csv(f'{DATA_DIR}/benin-malanville.csv')
    
    def load_sierraleone_data():
        return pd.read_csv(f'{DATA_DIR}/sierraleone-bumbuna.csv')
    
    def load_togo_data():
        return pd.read_csv(f'{DATA_DIR}/togo-dapaong_qc.csv')
    
    def load_benin_clean():
        return pd.read_csv(f'{DATA_DIR}/Benin_clean.csv')
    
    def load_sierraleone_clean():
        return pd.read_csv(f'{DATA_DIR}/Sierraleone_clean.csv')
    
    def load_togo_clean():
        return pd.read_csv(f'{DATA_DIR}/Togo_clean.csv')
    
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

def list_csvs(base_dir: str = DATA_DIR):
    """Look for CSV files in the data directory"""
    csv_files = glob.glob(os.path.join(base_dir, '*.csv'))
    return sorted(csv_files)

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

if not notebooks:
    st.error(f'No notebooks found in the {NOTEBOOK_DIR} directory. Looking for: {list(NOTEBOOK_FILES.values())}')
=======

# Directory constants
NOTEBOOK_DIR = "./notebooks"
DATA_DIR = "./data"

NOTEBOOK_PATTERNS = [
    "benin_eda.ipynb",
    "sierraleone_eda.ipynb",
    "Togo_eda.ipynb",
    "compare_countries.ipynb"
]

@st.cache_data
def find_notebooks(base_dir: str = NOTEBOOK_DIR):
    """Look for notebooks in the notebooks directory"""
    nb_paths = []
    for pat in NOTEBOOK_PATTERNS:
        full_path = os.path.join(base_dir, pat)
        if os.path.exists(full_path):
            nb_paths.append(full_path)
    
    # If no notebooks found with exact patterns, search for any .ipynb files
    if not nb_paths:
        nb_paths = glob.glob(os.path.join(base_dir, "*.ipynb"))
    
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
        # Handle paths with ./data/ prefix (in case notebooks already use them)
        ("'./data/benin-malanville.csv'", f"'{DATA_DIR}/benin-malanville.csv'"),
        ("'./data/sierraleone-bumbuna.csv'", f"'{DATA_DIR}/sierraleone-bumbuna.csv'"),
        ("'./data/togo-dapaong_qc.csv'", f"'{DATA_DIR}/togo-dapaong_qc.csv'"),
        ("'./data/Benin_clean.csv'", f"'{DATA_DIR}/Benin_clean.csv'"),
        ("'./data/Sierraleone_clean.csv'", f"'{DATA_DIR}/Sierraleone_clean.csv'"),
        ("'./data/Togo_clean.csv'", f"'{DATA_DIR}/Togo_clean.csv'"),
    ]
    
    fixed_code = code
    for old, new in fixes:
        fixed_code = fixed_code.replace(old, new)
    
    return fixed_code

def exec_code_collect_dfs(code: str, notebook_name: str) -> Dict[str, Any]:
    
    ns: Dict[str, Any] = {}
    
    # Provide essential imports
    ns['pd'] = pd
    ns['plt'] = plt
    ns['os'] = os
    ns['glob'] = glob
    ns['sys'] = sys
    
    # Fix data paths in the code before execution
    fixed_code = fix_data_paths_in_code(code)
    
    # Add data loading helper functions to namespace
    def load_benin_data():
        return pd.read_csv(f'{DATA_DIR}/benin-malanville.csv')
    
    def load_sierraleone_data():
        return pd.read_csv(f'{DATA_DIR}/sierraleone-bumbuna.csv')
    
    def load_togo_data():
        return pd.read_csv(f'{DATA_DIR}/togo-dapaong_qc.csv')
    
    def load_benin_clean():
        return pd.read_csv(f'{DATA_DIR}/Benin_clean.csv')
    
    def load_sierraleone_clean():
        return pd.read_csv(f'{DATA_DIR}/Sierraleone_clean.csv')
    
    def load_togo_clean():
        return pd.read_csv(f'{DATA_DIR}/Togo_clean.csv')
    
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

def list_csvs(base_dir: str = DATA_DIR):
    """Look for CSV files in the data directory"""
    csv_files = glob.glob(os.path.join(base_dir, '*.csv'))
    return sorted(csv_files)

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

if not notebooks:
    st.error(f'No notebooks found in the {NOTEBOOK_DIR} directory. Looking for: {NOTEBOOK_PATTERNS}')
>>>>>>> a96ed0d (Week0)
    
    # Show available files for debugging
    st.info(f"Available files in {NOTEBOOK_DIR} directory:")
    if os.path.exists(NOTEBOOK_DIR):
        notebook_files = os.listdir(NOTEBOOK_DIR)
        for f in notebook_files:
            st.write(f"- {f}")
    st.stop()

<<<<<<< HEAD
# Create label map from found notebooks
label_map = {display_name: path for display_name, path in notebooks}
=======
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
>>>>>>> a96ed0d (Week0)

selection = st.sidebar.selectbox('Choose analysis to view', options=list(label_map.keys()))
nb_path = label_map[selection]
st.markdown(f"**Notebook:** `{os.path.basename(nb_path)}`")

# Display available CSV files in sidebar
if csv_files:
    st.sidebar.subheader("Available Data Files")
    for csv_file in csv_files:
        st.sidebar.write(f"- {os.path.basename(csv_file)}")
else:
    st.sidebar.warning(f"No CSV files found in {DATA_DIR} directory")

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
    with st.spinner('Executing notebook code ...'):
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
        st.info('Trying to load data files directly...')
        
        if 'benin' in selection.lower():
            csv_files_to_try = [f'{DATA_DIR}/benin-malanville.csv', f'{DATA_DIR}/Benin_clean.csv']
        elif 'sierra' in selection.lower():
            csv_files_to_try = [f'{DATA_DIR}/sierraleone-bumbuna.csv', f'{DATA_DIR}/Sierraleone_clean.csv']
        elif 'togo' in selection.lower():
            csv_files_to_try = [f'{DATA_DIR}/togo-dapaong_qc.csv', f'{DATA_DIR}/Togo_clean.csv']
        else:
            csv_files_to_try = [f for f in csv_files]
        
        loaded = False
        for csv_file in csv_files_to_try:
            if os.path.exists(csv_file):
                try:
                    df_csv = pd.read_csv(csv_file)
                    st.success(f"Loaded: {os.path.basename(csv_file)}")
                    show_dataframe_eda(df_csv, name=os.path.basename(csv_file))
                    loaded = True
                    break
                except Exception as e:
                    st.error(f"Failed to load {csv_file}: {e}")
        
        if not loaded and csv_files:
            st.warning("Could not load specific files. Try loading any available CSV:")
            for csv_file in csv_files:
                try:
                    df_csv = pd.read_csv(csv_file)
                    st.success(f"Loaded: {os.path.basename(csv_file)}")
                    show_dataframe_eda(df_csv, name=os.path.basename(csv_file))
                    break
                except Exception as e:
                    st.error(f"Failed to load {csv_file}: {e}")

# Quick CSV loader in sidebar
st.sidebar.subheader("Quick CSV Loader")
if csv_files:
    selected_csv = st.sidebar.selectbox("Load CSV for quick EDA", 
                                       options=[""] + [os.path.basename(f) for f in csv_files])
    if selected_csv:
        csv_path = os.path.join(DATA_DIR, selected_csv)
        try:
            df_quick = pd.read_csv(csv_path)
            st.sidebar.success(f"Loaded: {selected_csv}")
            if st.sidebar.button("Analyze this CSV"):
                show_dataframe_eda(df_quick, name=selected_csv)
        except Exception as e:
            st.sidebar.error(f"Failed to load: {e}")

# Display directory information
with st.sidebar.expander("Directory Info"):
    st.write(f"**Notebook Directory:** {NOTEBOOK_DIR}")
    st.write(f"**Data Directory:** {DATA_DIR}")
    st.write(f"**Found Notebooks:** {len(notebooks)}")
    st.write(f"**Found CSV Files:** {len(csv_files)}")

st.markdown('---')
st.info(f'''
**Notes:** 

Alemayehu Tseganew
- This app demonistrates for understanding, exploring, and analyzing solar farm data from Benin, Sierra Leone, and Togo.
- Notebooks are loaded from: `{NOTEBOOK_DIR}`
- Data files are loaded from: `{DATA_DIR}`
- Streamlit is an open source Python framework for creating interactive web applications
<<<<<<< HEAD
''')
=======
''')
>>>>>>> a96ed0d (Week0)
