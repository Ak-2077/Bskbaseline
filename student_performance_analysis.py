import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import random
import os
import glob
import re

# Set page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="School Performance Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Windsurf-style professional theme
st.markdown("""
<style>
    .main > div {
        padding: 2rem 3rem;
        max-width: none;
        margin: 0;
        background-color: #f5f4f0;
    }
    .stApp {
        background-color: #f5f4f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Header/Navbar styling */
    header[data-testid="stHeader"] {
        background-color: #f5f4f0 !important;
        border-bottom: 1px solid #e0e0e0 !important;
    }
    .stApp > header {
        background-color: #f5f4f0 !important;
    }
    /* Navbar text styling */
    header[data-testid="stHeader"] * {
        color: #000000 !important;
    }
    header[data-testid="stHeader"] button {
        color: #000000 !important;
        background-color: transparent !important;
    }
    header[data-testid="stHeader"] svg {
        fill: #000000 !important;
    }
    /* Table styling */
    .stDataFrame {
        background-color: #f5f4f0 !important;
    }
    .stDataFrame table {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    .stDataFrame thead th {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
        border-bottom: 2px solid #e0e0e0 !important;
    }
    .stDataFrame tbody td {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
        border-bottom: 1px solid #e0e0e0 !important;
    }
    .stDataFrame tbody tr:hover {
        background-color: #ede9e3 !important;
    }
    /* Alternative table selectors */
    div[data-testid="stDataFrame"] {
        background-color: #f5f4f0 !important;
    }
    div[data-testid="stDataFrame"] table {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    div[data-testid="stDataFrame"] th {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    div[data-testid="stDataFrame"] td {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    /* More aggressive table styling with higher specificity */
    .stApp .stDataFrame,
    .stApp div[data-testid="stDataFrame"],
    .stApp .dataframe,
    .main .stDataFrame,
    .main div[data-testid="stDataFrame"] {
        background-color: #f5f4f0 !important;
    }
    
    .stApp .stDataFrame table,
    .stApp div[data-testid="stDataFrame"] table,
    .main .stDataFrame table,
    .main div[data-testid="stDataFrame"] table,
    .stApp table,
    .main table {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    .stApp .stDataFrame th,
    .stApp div[data-testid="stDataFrame"] th,
    .main .stDataFrame th,
    .main div[data-testid="stDataFrame"] th,
    .stApp th,
    .main th {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    .stApp .stDataFrame td,
    .stApp div[data-testid="stDataFrame"] td,
    .main .stDataFrame td,
    .main div[data-testid="stDataFrame"] td,
    .stApp td,
    .main td {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    /* Target any table elements directly */
    table {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    table th {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    table td {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    /* Ultra-specific table selectors with maximum CSS specificity */
    .stApp .main .block-container div[data-testid="stDataFrame"] {
        background-color: #f5f4f0 !important;
    }
    
    .stApp .main .block-container div[data-testid="stDataFrame"] > div {
        background-color: #f5f4f0 !important;
    }
    
    .stApp .main .block-container div[data-testid="stDataFrame"] > div > div {
        background-color: #f5f4f0 !important;
    }
    
    .stApp .main .block-container div[data-testid="stDataFrame"] table {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    .stApp .main .block-container div[data-testid="stDataFrame"] table thead {
        background-color: #f5f4f0 !important;
    }
    
    .stApp .main .block-container div[data-testid="stDataFrame"] table thead tr {
        background-color: #f5f4f0 !important;
    }
    
    .stApp .main .block-container div[data-testid="stDataFrame"] table thead tr th {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    .stApp .main .block-container div[data-testid="stDataFrame"] table tbody {
        background-color: #f5f4f0 !important;
    }
    
    .stApp .main .block-container div[data-testid="stDataFrame"] table tbody tr {
        background-color: #f5f4f0 !important;
    }
    
    .stApp .main .block-container div[data-testid="stDataFrame"] table tbody tr td {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    /* Even more specific with element IDs and classes */
    div[data-testid="stDataFrame"][data-baseweb="data-table"] {
        background-color: #f5f4f0 !important;
    }
    
    div[data-testid="stDataFrame"][data-baseweb="data-table"] table {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    div[data-testid="stDataFrame"][data-baseweb="data-table"] th {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    div[data-testid="stDataFrame"][data-baseweb="data-table"] td {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    /* Target specific Streamlit table classes */
    .element-container div[data-testid="stDataFrame"] {
        background-color: #f5f4f0 !important;
    }
    
    .element-container div[data-testid="stDataFrame"] table {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    .element-container div[data-testid="stDataFrame"] th {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    .element-container div[data-testid="stDataFrame"] td {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    /* Force override any dark theme table styling */
    [data-theme="dark"] div[data-testid="stDataFrame"] table,
    [data-theme="dark"] div[data-testid="stDataFrame"] th,
    [data-theme="dark"] div[data-testid="stDataFrame"] td {
        background-color: #f5f4f0 !important;
        color: #000000 !important;
    }
    
    /* Override any CSS custom properties/variables */
    div[data-testid="stDataFrame"] {
        --background-color: #f5f4f0 !important;
        --text-color: #000000 !important;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f5f4f0 !important;
        border-right: 1px solid #e0e0e0;
        width: 300px !important;
        min-width: 300px !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        height: 100vh !important;
        z-index: 999 !important;
    }
    section[data-testid="stSidebar"] > div {
        background-color: #f5f4f0 !important;
        padding-top: 2rem;
        width: 100% !important;
    }
    
    /* Hide sidebar close button */
    section[data-testid="stSidebar"] button[kind="header"] {
        display: none !important;
    }
    section[data-testid="stSidebar"] .css-1d391kg {
        display: none !important;
    }
    section[data-testid="stSidebar"] [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Adjust main content to account for fixed sidebar */
    .main .block-container {
        margin-left: 300px !important;
        max-width: calc(100% - 300px) !important;
    }
    
    /* Media query for desktop only */
    @media (min-width: 768px) {
        section[data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
        }
    }
    /* Force sidebar text visibility with high specificity */
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    section[data-testid="stSidebar"] .metric-value {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .metric-label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    .stSidebar h1, .stSidebar h2, .stSidebar h3 {
        color: #000000 !important;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .stSidebar h1, .stSidebar h2, .stSidebar h3 {
        color: #2c3e50 !important;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .stSidebar .stMetric {
        background-color: #ffffff;
        border: 1px solid #d0cdc4;
        border-radius: 6px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stSidebar .stMetric label {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    .stSidebar .stMetric div {
        color: #2c3e50 !important;
    }
    .stSidebar .stSelectbox > div > div {
        background-color: #ffffff;
        border: 1px solid #d0cdc4;
        border-radius: 6px;
        font-size: 0.9rem;
        color: #2c3e50 !important;
    }
    .stSidebar .stMarkdown {
        color: #2c3e50 !important;
        font-size: 0.85rem;
        line-height: 1.4;
        font-weight: 500;
    }
    .stSidebar .stMarkdown p {
        color: #2c3e50 !important;
    }
    .stSidebar .stInfo {
        background-color: #f8f9fa;
        border: 1px solid #d0cdc4;
        border-radius: 6px;
        padding: 0.5rem;
        font-size: 0.8rem;
        color: #2c3e50 !important;
    }
    .stSidebar label {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    .stSidebar p {
        color: #2c3e50 !important;
    }
    .stSelectbox > div > div, .stDataFrame {
        background-color: #ffffff;
        border: 1px solid #d0cdc4;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1 {
        color: #2c3e50;
        font-weight: 600;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    h2 {
        color: #2c3e50;
        font-weight: 500;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    h3 {
        color: #2c3e50;
        font-weight: 500;
        font-size: 1.4rem;
        margin-bottom: 0.75rem;
    }
    .metric-container {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #d0cdc4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        font-size: 0.9rem;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
    .stDataFrame > div {
        background-color: #ffffff !important;
        border-radius: 8px;
    }
    .stDataFrame table {
        background-color: #ffffff !important;
        font-size: 0.9rem;
    }
    .stDataFrame thead tr th {
        background-color: #f8f9fa !important;
        color: #5a5a5a !important;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    .stDataFrame tbody tr td {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border-bottom: 1px solid #f0f0f0;
    }
    .stMarkdown p {
        color: #6a6a6a;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    /* Force sidebar text visibility with high specificity */
    section[data-testid="stSidebar"] * {
        color: #2c3e50 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label {
        color: #2c3e50 !important;
        font-weight: 500 !important;
    }
    section[data-testid="stSidebar"] .metric-value {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .metric-label {
        color: #2c3e50 !important;
        font-weight: 500 !important;
    }
    .stSidebar h1, .stSidebar h2, .stSidebar h3 {
        color: #2c3e50 !important;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript-based CSS injection for tables
st.components.v1.html("""
<script>
function forceTableStyling() {
    // Wait for tables to load
    setTimeout(function() {
        // Find all dataframe elements
        const dataframes = document.querySelectorAll('[data-testid="stDataFrame"]');
        
        dataframes.forEach(function(df) {
            // Style the container
            df.style.backgroundColor = '#f5f4f0';
            
            // Find and style all nested elements
            const allElements = df.querySelectorAll('*');
            allElements.forEach(function(el) {
                if (el.tagName === 'TABLE' || el.tagName === 'THEAD' || 
                    el.tagName === 'TBODY' || el.tagName === 'TR' || 
                    el.tagName === 'TH' || el.tagName === 'TD') {
                    el.style.backgroundColor = '#f5f4f0';
                    el.style.color = '#000000';
                }
            });
        });
        
        // Also target any table elements directly
        const tables = document.querySelectorAll('table');
        tables.forEach(function(table) {
            table.style.backgroundColor = '#f5f4f0';
            table.style.color = '#000000';
            
            const cells = table.querySelectorAll('th, td');
            cells.forEach(function(cell) {
                cell.style.backgroundColor = '#f5f4f0';
                cell.style.color = '#000000';
            });
        });
    }, 100);
}

// Run immediately and on DOM changes
forceTableStyling();

// Create observer for dynamic content
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.addedNodes.length > 0) {
            forceTableStyling();
        }
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});
</script>
""", height=0)

# Initialize session state for navigation and selections
if 'current_level' not in st.session_state:
    st.session_state.current_level = 'school'
if 'selected_school' not in st.session_state:
    st.session_state.selected_school = None
if 'selected_grade' not in st.session_state:
    st.session_state.selected_grade = None
if 'selected_section' not in st.session_state:
    st.session_state.selected_section = None
if 'subject_type' not in st.session_state:
    st.session_state.subject_type = 'Communication'

# Sidebar for navigation and subject selection
with st.sidebar:
    st.markdown("###  Analysis Dashboard")
    
    # Subject Selection
    st.markdown("####  Subject Type")
    subject_type = st.selectbox(
        "Select Subject for Analysis:",
        ["Communication", "STEM"],
        index=0 if st.session_state.subject_type == 'Communication' else 1,
        key="subject_selector"
    )
    st.session_state.subject_type = subject_type

def determine_school_type(school_name):
    """Determine school type based on school name"""
    school_name_lower = school_name.lower()
    if any(word in school_name_lower for word in ['international', 'apex']):
        return 'International'
    elif any(word in school_name_lower for word in ['billabong', 'dominic', 'horizon']):
        return 'Private'
    elif any(word in school_name_lower for word in ['unicent', 'nathella']):
        return 'Semi-Government'
    else:
        return 'Government'

def determine_city(school_name):
    """Determine city based on school name"""
    city_mapping = {
        'apex': 'Mumbai',
        'nathella': 'Chennai', 
        'unicent': 'Hyderabad',
        'billabong': 'Mumbai',
        'dominic': 'Bangalore',
        'horizon': 'Bangalore',
        'nkt': 'Delhi',
        'rklgis': 'Kolkata',
        'rkl': 'Kolkata',
        'cambria': 'Pune'
    }
    
    school_name_lower = school_name.lower()
    for key, city in city_mapping.items():
        if key in school_name_lower:
            return city
    return 'Unknown'

# Load real school data from CSV files
@st.cache_data
def load_school_data(subject_type='Communication'):
    """Load and process school data based on subject type"""
    data_dir = "data"
    all_data = []
    
    # Define column mappings for different subjects
    if subject_type == 'Communication':
        # Communication subject columns
        expected_columns = ['Grade', 'Section', 'StudentName', 'Articulation', 'StructuredThinking', 
                          'BodyLanguage', 'AudienceEngagement', 'AbilityToSpeak', 'AbilityToEngage']
        file_pattern = '_Comm_'
    else:  # STEM
        # STEM subject columns  
        expected_columns = ['Grade', 'Section', 'StudentName', 'Logical Reasoning  %', 'Critical Thinking %',
                          'Creative Thinking %', 'Real Life Application %', 'Computational Thinking %', 'Creative Thinking Skills %']
        file_pattern = '_STEM_'
    
    # School mapping based on file names
    school_mapping = {
        'RKL': 'RKL Government School',
        'Unicent Miyapur': 'Unicent International School - Miyapur',
        'Unicent Bachupally': 'Unicent International School - Bachupally', 
        'Apex': 'Apex International School',
        'Billabong _ Juhu': 'Billabong High School - Juhu',
        'Billabong _ Mulund': 'Billabong High School - Mulund',
        'Nathella': 'Nathella Vidyodaya School',
        'New Horizon': 'New Horizon Public School',
        'St Dominic': 'St Dominic Savio High School',
        'Cambria': 'Cambria International School',
        'NKT': 'NKT English Medium School'
    }
    
    # Process files based on subject type
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv') and file_pattern in filename:
            try:
                file_path = os.path.join(data_dir, filename)
                df = pd.read_csv(file_path)
                
                # Extract school name from filename
                school_name = None
                for key, value in school_mapping.items():
                    if key in filename:
                        school_name = value
                        break
                
                if school_name is None:
                    continue
                
                # Clean and standardize column names
                df.columns = df.columns.str.strip()
                
                if subject_type == 'Communication':
                    # Communication data processing
                    column_mapping = {
                        'Grade': 'Grade',
                        'Div': 'Section', 'Section': 'Section',
                        'Name': 'StudentName', 'Student Name': 'StudentName',
                        'Articulation %': 'Articulation', 'Articulation': 'Articulation',
                        'Structured Thinking %': 'StructuredThinking', 'Structured Thinking': 'StructuredThinking',
                        'Body Language %': 'BodyLanguage', 'Body Language': 'BodyLanguage', 
                        'Audience Engagement %': 'AudienceEngagement', 'Audience Engagement': 'AudienceEngagement',
                        'Ability to Speak %': 'AbilityToSpeak', 'Ability to Speak': 'AbilityToSpeak',
                        'Ability to Engage %': 'AbilityToEngage', 'Ability to Engage': 'AbilityToEngage'
                    }
                else:  # STEM
                    # STEM data processing
                    column_mapping = {
                        'Grade': 'Grade',
                        'Div': 'Section', 'Section': 'Section',
                        'Name': 'StudentName', 'Student Name': 'StudentName',
                        # Handle various formats of Logical Reasoning column
                        'Logical Reasoning  %': 'Logical Reasoning  %', 
                        'Logical Reasoning %': 'Logical Reasoning  %',
                        'Logical Reasoning  ': 'Logical Reasoning  %', 
                        'Logical Reasoning': 'Logical Reasoning  %',
                        # Handle various formats of Critical Thinking column
                        'Critical Thinking %': 'Critical Thinking %', 
                        'Critical Thinking  ': 'Critical Thinking %',
                        'Critical Thinking': 'Critical Thinking %',
                        # Handle various formats of Creative Thinking column
                        'Creative Thing %': 'Creative Thinking %', 
                        'Creative Thinking %': 'Creative Thinking %',
                        'Creative Thing ': 'Creative Thinking %', 
                        'Creative Thing': 'Creative Thinking %',
                        'Creative Thinking ': 'Creative Thinking %', 
                        'Creative Thinking': 'Creative Thinking %',
                        # Handle various formats of Real Life Application column
                        'Real life Application %': 'Real Life Application %', 
                        'Real life Application ': 'Real Life Application %',
                        'Real life Application': 'Real Life Application %', 
                        'Real Life Application %': 'Real Life Application %',
                        # Handle various formats of Computational Thinking column
                        'Computational Thinking %': 'Computational Thinking %', 
                        'Computational Thinking ': 'Computational Thinking %',
                        'Computational Thinking': 'Computational Thinking %',
                        # Handle various formats of Creative Thinking Skills column
                        'Creative Thinking Skills %': 'Creative Thinking Skills %', 
                        'Creative Thinking Skills ': 'Creative Thinking Skills %',
                        'Creative Thinking Skills': 'Creative Thinking Skills %'
                    }
                
                # Apply column mapping
                df = df.rename(columns=column_mapping)
                
                # Add school information
                df['SchoolName'] = school_name
                df['SchoolType'] = determine_school_type(school_name)
                df['City'] = determine_city(school_name)
                
                # Convert percentage columns to numeric
                numeric_columns = [col for col in expected_columns if col not in ['Grade', 'Section', 'StudentName']]
                for col in numeric_columns:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Calculate composite scores based on subject type
                if subject_type == 'Communication':
                    df['AbilityToSpeak'] = df[['Articulation', 'StructuredThinking']].mean(axis=1)
                    df['AbilityToEngage'] = df[['BodyLanguage', 'AudienceEngagement']].mean(axis=1)
                else:  # STEM
                    df['AbilityToSpeak'] = df[['Logical Reasoning  %', 'Critical Thinking %']].mean(axis=1)
                    df['AbilityToEngage'] = df[['Creative Thinking %', 'Real Life Application %']].mean(axis=1)
                
                # Select only the expected columns that exist
                available_columns = [col for col in expected_columns if col in df.columns] + ['SchoolName', 'SchoolType', 'City']
                df = df[available_columns]
                
                all_data.append(df)
                
            except Exception as e:
                st.warning(f"Error processing {filename}: {str(e)}")
                continue
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df.dropna()
        return combined_df
    else:
        st.error(f"No {subject_type} data files found or processed successfully.")
        return pd.DataFrame()

# Load data based on selected subject type
df = load_school_data(st.session_state.subject_type)

# Add callback to reload data when subject type changes
if 'previous_subject_type' not in st.session_state:
    st.session_state.previous_subject_type = st.session_state.subject_type

if st.session_state.previous_subject_type != st.session_state.subject_type:
    st.session_state.previous_subject_type = st.session_state.subject_type
    st.cache_data.clear()  # Clear cache to reload data
    df = load_school_data(st.session_state.subject_type)
    st.rerun()

# Custom HTML table function
def create_custom_table(data, height=300):
    """Create a custom HTML table with beige background and black text"""
    # Create header cells with conditional left border
    header_cells = []
    for i, col in enumerate(data.columns):
        if i == 0:
            header_cells.append(f'<th style="background-color: #f5f4f0; color: #000000; border-bottom: 2px solid #e0e0e0; padding: 12px 15px; text-align: left;">{col}</th>')
        else:
            header_cells.append(f'<th style="background-color: #f5f4f0; color: #000000; border-bottom: 2px solid #e0e0e0; border-left: 1px solid #e0e0e0; padding: 12px 15px; text-align: left;">{col}</th>')
    
    # Create data rows with conditional left border
    data_rows = []
    for row in data.values:
        row_cells = []
        for i, val in enumerate(row):
            if i == 0:
                row_cells.append(f'<td style="background-color: inherit; color: #000000; border-bottom: 1px solid #e0e0e0; padding: 12px 15px;">{val}</td>')
            else:
                row_cells.append(f'<td style="background-color: inherit; color: #000000; border-bottom: 1px solid #e0e0e0; border-left: 1px solid #e0e0e0; padding: 12px 15px;">{val}</td>')
        data_rows.append(f'<tr style="background-color: #f5f4f0; color: #000000;" onmouseover="this.style.backgroundColor=\'#ede9e3\'" onmouseout="this.style.backgroundColor=\'#f5f4f0\'">{"".join(row_cells)}</tr>')
    
    html = f"""
    <div style="overflow-x: auto; max-height: {height}px; overflow-y: auto; border: 1px solid #e0e0e0; border-radius: 8px;">
        <table style="width: 100%; border-collapse: collapse; background-color: #f5f4f0; color: #000000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <thead>
                <tr style="background-color: #f5f4f0; color: #000000; font-weight: 600; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; position: sticky; top: 0;">
                    {"".join(header_cells)}
                </tr>
            </thead>
            <tbody>
                {"".join(data_rows)}
            </tbody>
        </table>
    </div>
    """
    return html

# Show data loading status
if not df.empty:
    st.sidebar.success(f" Loaded {st.session_state.subject_type} data from {df['SchoolName'].nunique()} schools")
    st.sidebar.info(f" Total students: {len(df)}")
else:
    st.sidebar.error(" No data loaded")

# Navigation functions
def reset_to_school():
    st.session_state.current_level = 'school'
    st.session_state.selected_school = None
    st.session_state.selected_grade = None
    st.session_state.selected_section = None

def go_to_grade(school_name):
    st.session_state.current_level = 'grade'
    st.session_state.selected_school = school_name
    st.session_state.selected_grade = None
    st.session_state.selected_section = None

def go_to_section(grade):
    st.session_state.current_level = 'section'
    st.session_state.selected_grade = grade
    st.session_state.selected_section = None

def go_to_student(section):
    st.session_state.current_level = 'student'
    st.session_state.selected_section = section

# Dashboard title with navigation breadcrumb
st.title(" Interactive Drill-Down School Analysis Dashboard")
st.markdown("*Analyzing real student performance data from multiple schools*")

# Navigation breadcrumb
breadcrumb_parts = ["Schools"]
if st.session_state.selected_school:
    breadcrumb_parts.append(f" {st.session_state.selected_school}")
if st.session_state.selected_grade:
    breadcrumb_parts.append(f" Grade {st.session_state.selected_grade}")
if st.session_state.selected_section:
    breadcrumb_parts.append(f" Section {st.session_state.selected_section}")

st.markdown(f"**Navigation:** {' → '.join(breadcrumb_parts)}")

# Reset button
if st.button("Reset to School View"):
    reset_to_school()
    st.rerun()

# Only proceed if data is loaded
if not df.empty:
    # Main visualization based on current level
    if st.session_state.current_level == 'school':
        st.header(" School-Level Analysis")
        st.markdown("**Click on any school in the table below to drill down to grade-level analysis**")
        
        # School-level aggregation with dynamic column detection
        available_columns = df.columns.tolist()
        
        # Define column mappings for different subject types
        if st.session_state.subject_type == "Communication":
            metric_cols = ['AbilityToSpeak', 'AbilityToEngage']
            display_names = ['AbilityToSpeak', 'AbilityToEngage']
        else:  # STEM
            metric_cols = ['Logical Reasoning  %', 'Critical Thinking %'] 
            display_names = ['Logical Reasoning', 'Critical Thinking']
        
        # Check which columns actually exist
        existing_metric_cols = [col for col in metric_cols if col in available_columns]
        
        if not existing_metric_cols:
            st.error(f"No metric columns found for {st.session_state.subject_type}. Available columns: {available_columns}")
            st.write("**Debug Info:**")
            st.write(f"Looking for columns: {metric_cols}")
            st.write(f"Available columns: {list(available_columns)}")
            st.write(f"Data shape: {df.shape}")
            st.write("**Sample data:**")
            st.dataframe(df.head())
            st.stop()
        
        # Build aggregation dictionary dynamically
        agg_dict = {}
        for col in existing_metric_cols:
            agg_dict[col] = 'mean'
        agg_dict['StudentName'] = 'count'
        
        school_summary = df.groupby(['SchoolName', 'SchoolType', 'City']).agg(agg_dict).round(1).reset_index()
        
        # Rename columns dynamically
        new_column_names = ['SchoolName', 'SchoolType', 'City'] + existing_metric_cols + ['StudentCount']
        school_summary.columns = new_column_names
        
        # Sort school_summary to ensure consistent ordering for click mapping
        school_summary = school_summary.sort_values('SchoolName').reset_index(drop=True)
        
        # Debug: Show school summary data
        st.write("🔍 **DEBUG: School Summary Data**")
        st.write(f"Number of schools: {len(school_summary)}")
        st.write(f"Columns: {list(school_summary.columns)}")
        st.write(f"Existing metric cols: {existing_metric_cols}")
        if len(school_summary) > 0:
            st.dataframe(school_summary.head())
            st.write(f"Sample data - X values: {school_summary[existing_metric_cols[0]].values[:5]}")
            st.write(f"Sample data - Y values: {school_summary[existing_metric_cols[1]].values[:5]}")
        else:
            st.error("❌ School summary is empty!")
        
        # Create interactive scatter plot with click functionality
        fig = px.scatter(school_summary, 
                        x=existing_metric_cols[0], 
                        y=existing_metric_cols[1],
                        size='StudentCount',
                        hover_name='SchoolName',
                        hover_data={'SchoolType': True, 'City': True, 'StudentCount': True},
                        title=f"School Performance: {display_names[0]} vs {display_names[1]}",
                        labels={
                            existing_metric_cols[0]: display_names[0],
                            existing_metric_cols[1]: display_names[1]
                        })
        
        # Force axis ranges and update layout
        fig.update_layout(
            xaxis=dict(range=[0, 100], title=display_names[0]),
            yaxis=dict(range=[0, 100], title=display_names[1]),
            width=800,
            height=600,
            showlegend=False
        )
        
        # Force marker properties with much larger base size
        fig.update_traces(
            marker=dict(
                size=50,  # Very large base size
                sizemin=50,  # Minimum size
                color='#1f4e79',
                opacity=1.0,
                line=dict(width=5, color='white'),
                sizemode='area'  # Use area mode
            ),
            textfont=dict(color='#2c3e50', size=12),
            hovertemplate='<b>%{hovertext}</b><br>' +
                         f'{display_names[0]}: %{{x}}%<br>' +
                         f'{display_names[1]}: %{{y}}%<br>' +
                         'Students: %{marker.size}<br>' +
                         '<extra></extra>'
        )
        
        # Use streamlit-plotly-events with stable implementation
        try:
            from streamlit_plotly_events import plotly_events
            
            # Display plot with click events (no state management needed)
            selected_points = plotly_events(
                fig,
                click_event=True,
                hover_event=False,
                select_event=False,
                override_height=600,
                key="school_plot_stable"
            )
            
            # Handle click events only when points are actually selected
            if selected_points and len(selected_points) > 0:
                point = selected_points[0]
                selected_school_name = None
                
                # Use pointIndex first as it's more reliable (from backup_2.py)
                if 'pointIndex' in point:
                    point_index = point['pointIndex']
                    if 0 <= point_index < len(school_summary):
                        selected_school_name = school_summary.iloc[point_index]['SchoolName']
                elif 'customdata' in point and point['customdata']:
                    school_name = point['customdata'][0]
                    if school_name in school_summary['SchoolName'].values:
                        selected_school_name = school_name
                
                if selected_school_name:
                    go_to_grade(selected_school_name)
                    st.rerun()
                            
        except ImportError:
            st.info(" For better click functionality, install: `pip install streamlit-plotly-events`")
            st.plotly_chart(fig, use_container_width=True, key="school_plot_fallback")
        
        # Add clickable school selection table for navigation
        st.subheader(" Click to Navigate to School")
        
        # Create a simplified table for school selection
        school_nav_data = school_summary[['SchoolName', 'SchoolType', 'City', existing_metric_cols[0], existing_metric_cols[1], 'StudentCount']].copy()
        school_nav_data.columns = ['School Name', 'Type', 'City', f'{existing_metric_cols[0]} %', f'{existing_metric_cols[1]} %', 'Students']
        
        # Use custom HTML table function
        st.components.v1.html(create_custom_table(school_nav_data), height=300, scrolling=True)
        
        # Handle school selection from table
        if st.button("Select School"):
            selected_idx = 0  # Replace with actual selection logic
            selected_school_name = school_summary.iloc[selected_idx]['SchoolName']
            go_to_grade(selected_school_name)
            st.rerun()
        
        # School selection dropdown as alternative to clicking
        st.subheader("Or Select School Manually:")
        selected_school_dropdown = st.selectbox(
            "Choose a school to analyze:",
            options=[''] + sorted(df['SchoolName'].unique().tolist()),
            key="school_dropdown"
        )
        
        if selected_school_dropdown:
            go_to_grade(selected_school_dropdown)
            st.rerun()

    elif st.session_state.current_level == 'grade':
        st.header(" Grade-Level Analysis")
        st.markdown("**Click on any grade in the table below to drill down to section-level analysis**")
        
        # Filter data for selected school
        school_data = df[df['SchoolName'] == st.session_state.selected_school]
        
        # Grade-level aggregation with dynamic column detection
        available_columns = school_data.columns.tolist()
        
        # Define column mappings for different subject types
        if st.session_state.subject_type == "Communication":
            metric_cols = ['AbilityToSpeak', 'AbilityToEngage']
            display_names = ['AbilityToSpeak', 'AbilityToEngage']
        else:  # STEM
            metric_cols = ['Logical Reasoning  %', 'Critical Thinking %'] 
            display_names = ['Logical Reasoning', 'Critical Thinking']
        
        # Check which columns actually exist
        existing_metric_cols = [col for col in metric_cols if col in available_columns]
        
        if not existing_metric_cols:
            st.error(f"No metric columns found for {st.session_state.subject_type}. Available columns: {available_columns}")
            st.write("**Debug Info:**")
            st.write(f"Looking for columns: {metric_cols}")
            st.write(f"Available columns: {list(available_columns)}")
            st.write(f"Data shape: {df.shape}")
            st.write("**Sample data:**")
            st.dataframe(df.head())
            st.stop()
        
        # Build aggregation dictionary dynamically
        agg_dict = {}
        for col in existing_metric_cols:
            agg_dict[col] = 'mean'
        agg_dict['StudentName'] = 'count'
        
        grade_summary = school_data.groupby('Grade').agg(agg_dict).round(1).reset_index()
        
        # Rename columns dynamically
        new_column_names = ['Grade'] + existing_metric_cols + ['StudentCount']
        grade_summary.columns = new_column_names
        
        # Debug: Show grade summary data
        st.write("🔍 **DEBUG: Grade Summary Data**")
        st.write(f"Number of grades: {len(grade_summary)}")
        st.write(f"Columns: {list(grade_summary.columns)}")
        st.write(f"Existing metric cols: {existing_metric_cols}")
        if len(grade_summary) > 0:
            st.dataframe(grade_summary.head())
            st.write(f"Sample data - X values: {grade_summary[existing_metric_cols[0]].values[:5]}")
            st.write(f"Sample data - Y values: {grade_summary[existing_metric_cols[1]].values[:5]}")
        else:
            st.error("❌ Grade summary is empty!")
        
        # Create interactive scatter plot with click functionality
        fig = px.scatter(grade_summary, 
                        x=existing_metric_cols[0], 
                        y=existing_metric_cols[1],
                        size='StudentCount',
                        text='Grade',
                        title=f"Grade Performance in {st.session_state.selected_school}",
                        labels={existing_metric_cols[0]: f'Average {display_names[0]} (%)', 
                               existing_metric_cols[1]: f'Average {display_names[1]} (%)'},
                        size_max=50)  # Increased from 20
        
        fig.update_traces(textposition="middle center")
        fig.update_layout(height=600)
        
        # Professional marker styling for grade plot - force no borders and consistent color
        fig.update_traces(
            marker=dict(
                size=50,  # Very large base size
                sizemin=50,  # Minimum size
                color='#1f4e79',
                opacity=1.0,  # Full opacity
                line=dict(width=5, color='white'),  # Thicker white border
                sizemode='area'  # Ensure size is interpreted as diameter
            ),
            textfont=dict(color='#2c3e50', size=12),
            hovertemplate=f'<b>%{{text}}</b><br>' +
                         f'{display_names[0]}: %{{x}}%<br>' +
                         f'{display_names[1]}: %{{y}}%<br>' +
                         'Students: %{marker.size}<br>' +
                         '<extra></extra>'
        )
        
        # Enable click selection
        fig.update_layout(
            clickmode='event+select',
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(color='#2c3e50', size=12),
            xaxis=dict(
                gridcolor='#e0e0e0',
                title_font=dict(color='#2c3e50', size=14),
                tickfont=dict(color='#2c3e50'),
                showgrid=True,
                range=[0, 100]
            ),
            yaxis=dict(
                gridcolor='#e0e0e0',
                title_font=dict(color='#2c3e50', size=14),
                tickfont=dict(color='#2c3e50'),
                showgrid=True,
                range=[0, 100]
            ),
            title=dict(
                font=dict(color='#2c3e50', size=16),
                x=0.5
            ),
            legend=dict(
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#e0e0e0',
                borderwidth=1
            )
        )
        
        # Use streamlit-plotly-events for grade plot click functionality
        try:
            from streamlit_plotly_events import plotly_events
            
            # Display plot with click events
            selected_points = plotly_events(
                fig,
                click_event=True,
                hover_event=False,
                select_event=False,
                override_height=600,
                key="grade_plot_events"
            )
            
            # Handle click events
            if selected_points and len(selected_points) > 0:
                point = selected_points[0]
                selected_grade = None
                
                if 'pointIndex' in point:
                    point_index = point['pointIndex']
                    if 0 <= point_index < len(grade_summary):
                        selected_grade = grade_summary.iloc[point_index]['Grade']
                elif 'customdata' in point and point['customdata']:
                    grade = point['customdata'][0]
                    if grade in grade_summary['Grade'].values:
                        selected_grade = grade
                
                if selected_grade:
                    go_to_section(selected_grade)
                    st.rerun()
                            
        except ImportError:
            st.info("For better click functionality, install: `pip install streamlit-plotly-events`")
            st.plotly_chart(fig, use_container_width=True, key="grade_plot_fallback")
        
        # Alternative: Use session state to track clicks
        if 'grade_clicked' not in st.session_state:
            st.session_state.grade_clicked = None
            
        # Check if there's a clicked grade in session state
        if st.session_state.grade_clicked:
            go_to_section(st.session_state.grade_clicked)
            st.session_state.grade_clicked = None  # Clear after use
            st.rerun()
        
        # Add clickable grade selection table
        st.subheader(" Click to Navigate to Grade")
        
        grade_nav_data = grade_summary.copy()
        grade_nav_data.columns = ['Grade', 'Speak %', 'Engage %', 'Students']
        
        # Use custom HTML table function
        st.components.v1.html(create_custom_table(grade_nav_data), height=300, scrolling=True)
        
        # Handle grade selection from table
        if st.button("Select Grade"):
            selected_idx = 0  # Replace with actual selection logic
            selected_grade = grade_summary.iloc[selected_idx]['Grade']
            go_to_section(selected_grade)
            st.rerun()
        
        # Grade selection dropdown
        st.subheader("Or Select Grade Manually:")
        available_grades = sorted(school_data['Grade'].unique())
        selected_grade_dropdown = st.selectbox(
            "Choose a grade to analyze:",
            options=[''] + available_grades,
            key="grade_dropdown"
        )
        
        if selected_grade_dropdown:
            go_to_section(selected_grade_dropdown)
            st.rerun()

    elif st.session_state.current_level == 'section':
        st.header(" Section-Level Analysis")
        st.markdown("**Click on any section in the table below to drill down to student-level analysis**")
        
        # Filter data for selected school and grade
        grade_data = df[(df['SchoolName'] == st.session_state.selected_school) & 
                       (df['Grade'] == st.session_state.selected_grade)]
        
        # Section-level aggregation with dynamic column detection
        available_columns = grade_data.columns.tolist()
        
        # Define column mappings for different subject types
        if st.session_state.subject_type == "Communication":
            metric_cols = ['AbilityToSpeak', 'AbilityToEngage']
            display_names = ['AbilityToSpeak', 'AbilityToEngage']
        else:  # STEM
            metric_cols = ['Logical Reasoning  %', 'Critical Thinking %'] 
            display_names = ['Logical Reasoning', 'Critical Thinking']
        
        # Check which columns actually exist
        existing_metric_cols = [col for col in metric_cols if col in available_columns]
        
        if not existing_metric_cols:
            st.error(f"No metric columns found for {st.session_state.subject_type}. Available columns: {available_columns}")
            st.write("**Debug Info:**")
            st.write(f"Looking for columns: {metric_cols}")
            st.write(f"Available columns: {list(available_columns)}")
            st.write(f"Data shape: {df.shape}")
            st.write("**Sample data:**")
            st.dataframe(df.head())
            st.stop()
        
        # Build aggregation dictionary dynamically
        agg_dict = {}
        for col in existing_metric_cols:
            agg_dict[col] = 'mean'
        agg_dict['StudentName'] = 'count'
        
        section_summary = grade_data.groupby('Section').agg(agg_dict).round(1).reset_index()
        
        # Rename columns dynamically
        new_column_names = ['Section'] + existing_metric_cols + ['StudentCount']
        section_summary.columns = new_column_names
        
        # Debug: Show section summary data
        st.write("🔍 **DEBUG: Section Summary Data**")
        st.write(f"Number of sections: {len(section_summary)}")
        st.write(f"Columns: {list(section_summary.columns)}")
        st.write(f"Existing metric cols: {existing_metric_cols}")
        if len(section_summary) > 0:
            st.dataframe(section_summary.head())
            st.write(f"Sample data - X values: {section_summary[existing_metric_cols[0]].values[:5]}")
            st.write(f"Sample data - Y values: {section_summary[existing_metric_cols[1]].values[:5]}")
        else:
            st.error("❌ Section summary is empty!")
        
        # Create interactive scatter plot with click functionality
        fig = px.scatter(section_summary, 
                        x=existing_metric_cols[0], 
                        y=existing_metric_cols[1],
                        size='StudentCount',
                        text='Section',
                        title=f"Section Performance in Grade {st.session_state.selected_grade}",
                        labels={existing_metric_cols[0]: f'Average {display_names[0]} (%)', 
                               existing_metric_cols[1]: f'Average {display_names[1]} (%)'},
                        size_max=70)  # Increased from 20
        
        fig.update_traces(textposition="middle center")
        fig.update_layout(height=600)
        
        # Professional marker styling for section plot - force no borders
        fig.update_traces(
            marker=dict(
                size=60,  # Much larger base size
                sizemin=60,  # Minimum size
                color='#1f4e79',
                opacity=1.0,  # Full opacity
                line=dict(width=6, color='white'),  # Thicker white border
                sizemode='area'  # Ensure size is interpreted as diameter
            ),
            textfont=dict(color='#2c3e50', size=12),
            hovertemplate='<b>%{text}</b><br>' +
                         f'{display_names[0]}: %{{x}}%<br>' +
                         f'{display_names[1]}: %{{y}}%<br>' +
                         'Students: %{marker.size}<br>' +
                         '<extra></extra>'
        )
        
        # Enable click selection
        fig.update_layout(
            clickmode='event+select',
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(color='#2c3e50', size=12),
            xaxis=dict(
                gridcolor='#e0e0e0',
                title_font=dict(color='#2c3e50', size=14),
                tickfont=dict(color='#2c3e50'),
                showgrid=True,
                range=[0, 100]
            ),
            yaxis=dict(
                gridcolor='#e0e0e0',
                title_font=dict(color='#2c3e50', size=14),
                tickfont=dict(color='#2c3e50'),
                showgrid=True,
                range=[0, 100]
            ),
            title=dict(
                font=dict(color='#2c3e50', size=16),
                x=0.5
            )
        )
        
        # Display the plot with event handling
        try:
            from streamlit_plotly_events import plotly_events
            
            # Display plot with click events
            selected_points = plotly_events(
                fig,
                click_event=True,
                hover_event=False,
                select_event=False,
                override_height=600,
                override_width="100%",
                key="section_plot"
            )
            
            # Handle click events for navigation
            if selected_points:
                try:
                    if hasattr(selected_points, 'get') and selected_points.get('points'):
                        point_data = selected_points['points'][0]
                        point_index = point_data.get('pointIndex')
                        
                        if point_index is not None and 0 <= point_index < len(section_summary):
                            selected_section = section_summary.iloc[point_index]['Section']
                            go_to_student(selected_section)
                            st.rerun()
                    elif isinstance(selected_points, list) and len(selected_points) > 0:
                        # Handle different return format
                        point_data = selected_points[0]
                        if 'pointIndex' in point_data:
                            point_index = point_data['pointIndex']
                            if point_index is not None and 0 <= point_index < len(section_summary):
                                selected_section = section_summary.iloc[point_index]['Section']
                                go_to_student(selected_section)
                                st.rerun()
                except (AttributeError, KeyError, IndexError, TypeError):
                    # Silently handle any errors in click processing
                    pass
                            
        except ImportError:
            # Fallback to regular plotly chart
            st.plotly_chart(fig, use_container_width=True, key="section_plot")
        
        # Alternative: Use session state to track clicks
        if 'section_clicked' not in st.session_state:
            st.session_state.section_clicked = None
            
        # Check if there's a clicked section in session state
        if st.session_state.section_clicked:
            go_to_student(st.session_state.section_clicked)
            st.session_state.section_clicked = None  # Clear after use
            st.rerun()
        
        # Add clickable section selection table
        st.subheader(" Click to Navigate to Section")
        
        section_nav_data = section_summary.copy()
        section_nav_data.columns = ['Section', 'Speak %', 'Engage %', 'Students']
        
        # Use custom HTML table function
        st.components.v1.html(create_custom_table(section_nav_data), height=300, scrolling=True)
        
        # Handle section selection from table
        if st.button("Select Section"):
            selected_idx = 0  # Replace with actual selection logic
            selected_section = section_summary.iloc[selected_idx]['Section']
            go_to_student(selected_section)
            st.rerun()
        
        # Section selection dropdown
        st.subheader("Or Select Section Manually:")
        available_sections = sorted(grade_data['Section'].unique())
        selected_section_dropdown = st.selectbox(
            "Choose a section to analyze:",
            options=[''] + available_sections,
            key="section_dropdown"
        )
        
        if selected_section_dropdown:
            go_to_student(selected_section_dropdown)
            st.rerun()

    elif st.session_state.current_level == 'student':
        st.header(f" Student-Level Analysis - {st.session_state.selected_school}, Grade {st.session_state.selected_grade}, Section {st.session_state.selected_section}")
        
        # Filter data for selected school, grade, and section
        section_data = df[(df['SchoolName'] == st.session_state.selected_school) & 
                         (df['Grade'] == st.session_state.selected_grade) &
                         (df['Section'] == st.session_state.selected_section)]
        
        # Dynamic column detection for student details display
        if st.session_state.subject_type == "Communication":
            # Communication columns
            display_cols = ['StudentName', 'Articulation', 'StructuredThinking', 'BodyLanguage', 
                           'AudienceEngagement', 'AbilityToSpeak', 'AbilityToEngage', 'Weakness']
            sort_col = 'AbilityToSpeak'
            radar_metrics = ['Articulation', 'StructuredThinking', 'BodyLanguage', 'AudienceEngagement', 
                           'AbilityToSpeak', 'AbilityToEngage']
            radar_labels = ['Articulation', 'Structured Thinking', 'Body Language', 
                           'Audience Engagement', 'Ability to Speak', 'Ability to Engage']
        else:  # STEM
            # STEM columns
            display_cols = ['StudentName', 'Logical Reasoning  %', 'Critical Thinking %', 
                           'Creative Thinking %', 'Real Life Application %', 'Computational Thinking %', 
                           'Creative Thinking Skills %', 'Weakness']
            sort_col = 'Logical Reasoning  %'
            radar_metrics = ['Logical Reasoning  %', 'Critical Thinking %', 'Creative Thinking %', 
                           'Real Life Application %', 'Computational Thinking %', 'Creative Thinking Skills %']
            radar_labels = ['Logical Reasoning', 'Critical Thinking', 'Creative Thinking', 
                           'Real Life Application', 'Computational Thinking', 'Creative Thinking Skills']
        
        # Filter display columns to only include those that exist
        available_display_cols = [col for col in display_cols if col in section_data.columns]
        
        # Create student scatter plot with dynamic columns
        if st.session_state.subject_type == "Communication":
            scatter_x = 'AbilityToSpeak'
            scatter_y = 'AbilityToEngage'
            hover_cols = ['StudentName', 'Articulation', 'StructuredThinking', 'BodyLanguage', 'AudienceEngagement']
            x_label = 'Ability to Speak (%)'
            y_label = 'Ability to Engage (%)'
        else:  # STEM
            scatter_x = 'Logical Reasoning  %'
            scatter_y = 'Critical Thinking %'
            hover_cols = ['StudentName', 'Logical Reasoning  %', 'Critical Thinking %', 'Creative Thinking %']
            x_label = 'Logical Reasoning (%)'
            y_label = 'Critical Thinking (%)'
        
        # Check if required columns exist for scatter plot
        if scatter_x in section_data.columns and scatter_y in section_data.columns:
            # Filter hover columns to only include existing ones
            available_hover_cols = [col for col in hover_cols if col in section_data.columns]
            
            fig = px.scatter(section_data, 
                            x=scatter_x, 
                            y=scatter_y,
                            hover_data=available_hover_cols,
                            title=f"Individual Student Performance in Section {st.session_state.selected_section}",
                            labels={scatter_x: x_label, scatter_y: y_label})

            fig.update_layout(height=600)
            
            # Professional marker styling for student plot
            fig.update_traces(
                marker=dict(
                    size=15,
                    color='#1f4e79',
                    opacity=0.8,
                    line=dict(width=0, color='rgba(0,0,0,0)')
                ),
                hovertemplate='<b>%{hovertext}</b><br>' +
                             f'{x_label}: %{{x}}%<br>' +
                             f'{y_label}: %{{y}}%<br>' +
                             '<extra></extra>'
            )
            
            # Configure for consistent professional theme
            fig.update_layout(
                plot_bgcolor='#ffffff',
                paper_bgcolor='#ffffff',
                font=dict(color='#2c3e50', size=12),
                xaxis=dict(
                    gridcolor='#e0e0e0',
                    title_font=dict(color='#2c3e50', size=14),
                    tickfont=dict(color='#2c3e50'),
                    showgrid=True,
                    range=[0, 100]
                ),
                yaxis=dict(
                    gridcolor='#e0e0e0',
                    title_font=dict(color='#2c3e50', size=14),
                    tickfont=dict(color='#2c3e50'),
                    showgrid=True,
                    range=[0, 100]
                ),
                title=dict(
                    font=dict(color='#2c3e50', size=16),
                    x=0.5
                )
            )
            
            # Display the plot
            st.plotly_chart(fig, use_container_width=True, key="student_plot")
        
        # Student details table
        st.subheader(" Detailed Student Performance")
        
        # Calculate weakness for each student
        skill_cols = ['Articulation', 'StructuredThinking', 'BodyLanguage', 'AudienceEngagement']
        section_data_copy = section_data.copy()
        
        # Find weakest skill for each student
        def find_weakness(row):
            skills = {}
            for col in skill_cols:
                if col in row and pd.notna(row[col]):
                    skills[col] = row[col]
            
            if skills:
                weakest_skill = min(skills, key=skills.get)
                weakest_score = skills[weakest_skill]
                
                # Format skill name for display
                skill_display_names = {
                    'Articulation': 'Articulation',
                    'StructuredThinking': 'Structured Thinking',
                    'BodyLanguage': 'Body Language',
                    'AudienceEngagement': 'Audience Engagement'
                }
                
                return f"{skill_display_names.get(weakest_skill, weakest_skill)} ({weakest_score}%)"
            return "N/A"
        
        section_data_copy['Weakness'] = section_data_copy.apply(find_weakness, axis=1)
        
        # Use custom HTML table function
        st.components.v1.html(create_custom_table(section_data_copy[available_display_cols].sort_values(sort_col, ascending=False)), height=300, scrolling=True)
        
        # Individual student analysis
        st.subheader(" Individual Student Radar Chart")
        selected_student = st.selectbox(
            "Select a student for detailed analysis:",
            section_data['StudentName'].unique()
        )
        
        if selected_student:
            student_data = section_data[section_data['StudentName'] == selected_student].iloc[0]
            
            # Radar chart for individual student
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=[student_data[col] for col in radar_metrics],
                theta=radar_labels,
                fill='toself',
                name=selected_student
            ))
            
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                title=f"Performance Profile - {selected_student}",
                plot_bgcolor='#f5f4f0',
                paper_bgcolor='#f5f4f0',
                font=dict(color='#000000', size=12),
                title_font=dict(color='#000000', size=16),
                polar_bgcolor='#f5f4f0',
                polar_radialaxis=dict(
                    gridcolor='#e0e0e0',
                    linecolor='#e0e0e0',
                    tickfont=dict(color='#000000')
                ),
                polar_angularaxis=dict(
                    gridcolor='#e0e0e0',
                    linecolor='#e0e0e0',
                    tickfont=dict(color='#000000')
                )
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)

    # Summary statistics sidebar
    st.sidebar.header(" Current View Statistics")

    if st.session_state.current_level == 'school':
        current_data = df
        st.sidebar.metric("Total Schools", df['SchoolName'].nunique())
        st.sidebar.metric("Total Students", len(df))
        
        # Dynamic column selection for performance calculation
        if st.session_state.subject_type == "Communication":
            perf_cols = ['AbilityToSpeak', 'AbilityToEngage']
        else:  # STEM
            perf_cols = ['Logical Reasoning  %', 'Critical Thinking %']
        
        # Check which columns exist and calculate average
        existing_perf_cols = [col for col in perf_cols if col in df.columns]
        if existing_perf_cols:
            avg_performance = df[existing_perf_cols].mean().mean()
            st.sidebar.metric("Overall Avg Performance", f"{avg_performance:.1f}%")

    elif st.session_state.current_level == 'grade':
        current_data = df[df['SchoolName'] == st.session_state.selected_school]
        st.sidebar.metric("Grades in School", current_data['Grade'].nunique())
        st.sidebar.metric("Students in School", len(current_data))
        
        # Dynamic column selection for performance calculation
        if st.session_state.subject_type == "Communication":
            perf_cols = ['AbilityToSpeak', 'AbilityToEngage']
        else:  # STEM
            perf_cols = ['Logical Reasoning  %', 'Critical Thinking %']
        
        existing_perf_cols = [col for col in perf_cols if col in current_data.columns]
        if existing_perf_cols:
            avg_performance = current_data[existing_perf_cols].mean().mean()
            st.sidebar.metric("School Avg Performance", f"{avg_performance:.1f}%")

    elif st.session_state.current_level == 'section':
        current_data = df[(df['SchoolName'] == st.session_state.selected_school) & 
                         (df['Grade'] == st.session_state.selected_grade)]
        st.sidebar.metric("Sections in Grade", current_data['Section'].nunique())
        st.sidebar.metric("Students in Grade", len(current_data))
        
        # Dynamic column selection for performance calculation
        if st.session_state.subject_type == "Communication":
            perf_cols = ['AbilityToSpeak', 'AbilityToEngage']
        else:  # STEM
            perf_cols = ['Logical Reasoning  %', 'Critical Thinking %']
        
        existing_perf_cols = [col for col in perf_cols if col in current_data.columns]
        if existing_perf_cols:
            avg_performance = current_data[existing_perf_cols].mean().mean()
            st.sidebar.metric("Grade Avg Performance", f"{avg_performance:.1f}%")

    elif st.session_state.current_level == 'student':
        current_data = df[(df['SchoolName'] == st.session_state.selected_school) & 
                         (df['Grade'] == st.session_state.selected_grade) &
                         (df['Section'] == st.session_state.selected_section)]
        st.sidebar.metric("Students in Section", len(current_data))
        
        # Dynamic column selection for performance calculation
        if st.session_state.subject_type == "Communication":
            perf_cols = ['AbilityToSpeak', 'AbilityToEngage']
        else:  # STEM
            perf_cols = ['Logical Reasoning  %', 'Critical Thinking %']
        
        existing_perf_cols = [col for col in perf_cols if col in current_data.columns]
        if existing_perf_cols:
            avg_performance = current_data[existing_perf_cols].mean().mean()
            st.sidebar.metric("Section Avg Performance", f"{avg_performance:.1f}%")

else:
    st.error("Please ensure your CSV files are in the 'data/' directory and try refreshing the page.")
