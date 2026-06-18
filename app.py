st.markdown("""
<style>
    /* Global font and background */
    * {
        font-family: 'Georgia', 'Times New Roman', serif !important;
    }
    
    .stApp {
        background-color: #fef9f5;
    }
    
    /* Faint orange watermark/background pattern */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(ellipse at 20% 50%, rgba(242, 101, 10, 0.04) 0%, transparent 50%),
                    radial-gradient(ellipse at 80% 20%, rgba(242, 101, 10, 0.04) 0%, transparent 50%),
                    radial-gradient(ellipse at 50% 80%, rgba(242, 101, 10, 0.04) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        position: relative;
        z-index: 1;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5 {
        color: #f2650a !important;
        font-weight: 700 !important;
        font-family: 'Georgia', 'Times New Roman', serif !important;
    }
    
    h1 {
        font-size: 2.2rem !important;
        letter-spacing: 0.5px;
    }
    
    h2 {
        font-size: 1.6rem !important;
    }
    
    /* Subheader divider */
    hr {
        border-color: #f2650a;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #f2650a !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-family: 'Georgia', 'Times New Roman', serif !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #d45508 !important;
        box-shadow: 0 4px 12px rgba(242, 101, 10, 0.3) !important;
        transform: translateY(-1px);
    }
    
    /* Scorecard/metrics */
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-family: 'Georgia', 'Times New Roman', serif !important;
    }
    [data-testid="stMetricLabel"] {
        color: #666666 !important;
        font-family: 'Georgia', 'Times New Roman', serif !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2 {
        color: #f2650a !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background-color: #f2650a !important;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: #333 !important;
        font-family: 'Georgia', 'Times New Roman', serif !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f0f0;
        border-radius: 6px 6px 0 0;
        padding: 10px 20px;
        color: #333;
        font-family: 'Georgia', 'Times New Roman', serif !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #f2650a !important;
        color: white !important;
    }
    
    /* Dataframes */
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    
    /* Expanders - FIXED */
    .streamlit-expanderHeader {
        background-color: #fef9f5 !important;
        border-left: 3px solid #f2650a !important;
        border-radius: 4px !important;
        font-family: 'Georgia', 'Times New Roman', serif !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    /* Hide the default expander arrow text overlap */
    .streamlit-expanderHeader p {
        font-weight: 600 !important;
        color: #1a1a1a !important;
        margin: 0 !important;
    }
    
    /* Fix expander content area */
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #f0f0f0 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 16px !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #e8f5e9 !important;
        border-left: 4px solid #4caf50 !important;
    }
    .stError {
        background-color: #fef0f0 !important;
        border-left: 4px solid #f44336 !important;
    }
    
    /* Text inputs */
    .stTextInput input, .stDateInput input {
        border: 1px solid #ccc !important;
        border-radius: 6px !important;
        font-family: 'Georgia', 'Times New Roman', serif !important;
    }
    .stTextInput input:focus, .stDateInput input:focus {
        border-color: #f2650a !important;
        box-shadow: 0 0 0 2px rgba(242, 101, 10, 0.2) !important;
    }
    
    /* Select boxes and multiselect */
    .stSelectbox select, .stMultiSelect {
        font-family: 'Georgia', 'Times New Roman', serif !important;
    }
    
    /* Fix paragraph spacing in expanders */
    .stMarkdown p {
        margin-bottom: 8px !important;
    }
</style>
""", unsafe_allow_html=True)
