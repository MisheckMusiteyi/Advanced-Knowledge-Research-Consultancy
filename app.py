import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import base64
from io import BytesIO
from datetime import datetime, date
from PIL import Image

# ============================================
# PAGE CONFIGURATION - MUST BE FIRST
# ============================================
st.set_page_config(
    page_title="AKRC Portal",
    page_icon="🔬",
    layout="wide"
)

# ============================================
# LOGO URL
# ============================================
LOGO_URL = "https://raw.githubusercontent.com/MisheckMusiteyi/Advanced-Knowledge-Research-Consultancy/285f1bab55b659e07c37687ca5f5c1b8a2e9bae8/Advanced%20Knowledge%20Research%20Consultancy.png"

# ============================================
# CUSTOM CSS STYLING
# ============================================
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
    
    /* ============================================
       EXPANDER FIX
       ============================================ */
    [data-testid="stExpander"] {
        border: 1px solid #f0f0f0 !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
        overflow: hidden;
    }

    [data-testid="stExpander"] summary {
        background-color: #fef9f5 !important;
        border-left: 3px solid #f2650a !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        padding: 12px 16px !important;
        list-style: none !important;
        position: relative !important;
    }

    [data-testid="stExpander"] summary::marker,
    [data-testid="stExpander"] summary::-webkit-details-marker {
        display: none !important;
        content: none !important;
    }

    [data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"],
    [data-testid="stExpander"] summary [data-testid="stIconMaterial"],
    [data-testid="stExpander"] summary svg,
    [data-testid="stExpander"] summary .material-icons,
    [data-testid="stExpander"] summary span[class*="icon"] {
        font-size: 0 !important;
        line-height: 0 !important;
        width: 8px !important;
        height: 8px !important;
        color: transparent !important;
        flex-shrink: 0 !important;
        position: relative !important;
        order: -1 !important;
    }

    [data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"]::before,
    [data-testid="stExpander"] summary [data-testid="stIconMaterial"]::before {
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 50% !important;
        width: 0 !important;
        height: 0 !important;
        border-left: 5px solid #f2650a !important;
        border-top: 4px solid transparent !important;
        border-bottom: 4px solid transparent !important;
        transform: translateY(-50%) !important;
        transition: transform 0.15s ease !important;
    }

    [data-testid="stExpander"] details[open] summary [data-testid="stExpanderToggleIcon"]::before,
    [data-testid="stExpander"] details[open] summary [data-testid="stIconMaterial"]::before {
        transform: translateY(-50%) rotate(90deg) !important;
    }

    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p {
        font-family: 'Georgia', 'Times New Roman', serif !important;
        font-size: 16px !important;
        color: #1a1a1a !important;
        font-weight: 600 !important;
        margin: 0 !important;
        line-height: 1.4 !important;
    }

    [data-testid="stExpanderDetails"] {
        background-color: #ffffff !important;
        border-top: 1px solid #f0f0f0 !important;
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
    
    /* Fix paragraph spacing */
    [data-testid="stExpanderDetails"] .stMarkdown p {
        margin-bottom: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# GOOGLE SHEETS SETUP
# ============================================
@st.cache_resource
def connect_to_sheets():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    
    try:
        creds_dict = dict(st.secrets)
        creds_dict.pop("admin_password", None)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    except Exception as e:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    
    client = gspread.authorize(creds)
    return client

def load_data(sheet_name):
    client = connect_to_sheets()
    sheet = client.open("Advanced Knowledge Research Consultancy").worksheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def update_cell(sheet_name, row, col, value):
    client = connect_to_sheets()
    sheet = client.open("Advanced Knowledge Research Consultancy").worksheet(sheet_name)
    sheet.update_cell(row, col, value)

# ============================================
# PROFILE MANAGEMENT FUNCTIONS
# ============================================
def get_profile_data(username):
    """Retrieve saved profile information from Google Sheets."""
    try:
        df = load_data("Researcher Profiles")
        user = df[df["Username"] == username]
        if len(user) > 0:
            return user.iloc[0].to_dict()
    except:
        pass
    
    return {
        "Username": username,
        "Display Name": "",
        "Profile Photo": "",
        "Image Type": "image/png"
    }

def save_profile(username, display_name, photo_b64="", image_type="image/png"):
    """Update or create profile records in Google Sheets."""
    client = connect_to_sheets()
    sheet = client.open("Advanced Knowledge Research Consultancy").worksheet("Researcher Profiles")
    records = sheet.get_all_records()
    
    # If photo is too large, skip storing it
    if len(photo_b64) > 45000:
        st.warning("⚠️ Image too large. Please use a smaller image (under 100KB).")
        photo_b64 = ""
    
    for idx, row in enumerate(records, start=2):
        if row["Username"] == username:
            sheet.update(f"B{idx}", display_name)
            sheet.update(f"C{idx}", photo_b64)
            sheet.update(f"D{idx}", image_type)
            return
    
    sheet.append_row([username, display_name, photo_b64, image_type])

def resize_image_for_storage(image_bytes):
    """Resize image to fit within Google Sheets cell limits."""
    img = Image.open(BytesIO(image_bytes))
    
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    img.thumbnail((300, 300), Image.LANCZOS)
    
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=60, optimize=True)
    buffer.seek(0)
    
    return buffer.getvalue()

def display_profile_image(photo_b64=None, image_type="image/png"):
    """Display the profile image in a circular format."""
    if photo_b64:
        st.markdown(
            f"""
            <img src="data:{image_type};base64,{photo_b64}"
            style="
                width:120px;
                height:120px;
                border-radius:50%;
                object-fit:cover;
                border:4px solid #f2650a;
            ">
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="
                width:120px;
                height:120px;
                border-radius:50%;
                background:#f2650a;
                display:flex;
                align-items:center;
                justify-content:center;
                color:white;
                font-size:50px;
                font-weight:bold;
            ">
            👤
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================
# DIALOG: Profile Settings
# ============================================
@st.dialog("⚙️ Profile Settings")
def profile_settings_dialog(display_name, profile):
    """Profile settings popup dialog."""
    new_name = st.text_input("Display Name", value=display_name)
    new_photo = st.file_uploader("Profile Photo", type=["png", "jpg", "jpeg"])
    
    # Image preview before saving
    if new_photo:
        st.image(new_photo, width=150, caption="Profile Preview")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Profile", use_container_width=True):
            photo_b64 = profile["Profile Photo"]
            image_type = profile.get("Image Type", "image/png")
            
            if new_photo:
                compressed_bytes = resize_image_for_storage(new_photo.getvalue())
                image_type = "image/jpeg"
                photo_b64 = base64.b64encode(compressed_bytes).decode()
            
            save_profile(st.session_state.username, new_name, photo_b64, image_type)
            st.success("Profile updated successfully!")
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

# ============================================
# SESSION STATE
# ============================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'researcher_name' not in st.session_state:
    st.session_state.researcher_name = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'profile_image' not in st.session_state:
    st.session_state.profile_image = None

# ============================================
# LOGIN PAGE
# ============================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(LOGO_URL, width=350)
    
    st.markdown("<h1 style='text-align: center; margin-top: -10px;'>Advanced Knowledge Research Consultancy</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 16px;'>Research Consultancy Portal</p>", unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_type = st.radio("Login as:", ["Researcher", "Admin"], horizontal=True)

        if login_type == "Researcher":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login", use_container_width=True):
                logins_df = load_data("Researcher Logins")

                match = logins_df[(logins_df['Username'] == username) &
                                (logins_df['Password'] == password) &
                                (logins_df['Status'] == 'Active')]

                if len(match) > 0:
                    st.session_state.logged_in = True
                    st.session_state.user_type = "Researcher"
                    st.session_state.username = username
                    st.session_state.researcher_name = match.iloc[0]['Researcher Name']
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials or account inactive.")

        else:
            admin_password = st.text_input("Admin Password", type="password")

            if st.button("Login", use_container_width=True):
                try:
                    correct_password = st.secrets["admin_password"]
                except:
                    correct_password = "admin123"
                
                if admin_password == correct_password:
                    st.session_state.logged_in = True
                    st.session_state.user_type = "Admin"
                    st.success("Admin login successful!")
                    st.rerun()
                else:
                    st.error("Invalid admin password.")

# ============================================
# RESEARCHER DASHBOARD
# ============================================
def researcher_dashboard():
    # Load profile data
    profile = get_profile_data(st.session_state.username)
    display_name = profile["Display Name"] if profile["Display Name"] else st.session_state.researcher_name
    image_type = profile.get("Image Type", "image/png")
    
    # Profile section at top
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        display_profile_image(profile["Profile Photo"], image_type)
    
    with col2:
        st.title(f"Welcome, {display_name}")
    
    with col3:
        # Display name
        st.markdown(f"""
        <div style="text-align: center; margin-top: 10px;">
            <p style="color: #f2650a; font-weight: 700; font-size: 14px; margin: 5px 0 0 0;">{display_name}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("Your Active Tasks")

    projects_df = load_data("Projects")

    my_tasks = projects_df[projects_df['Researcher Assigned'] == st.session_state.researcher_name]

    if len(my_tasks) == 0:
        st.info("No tasks assigned yet.")
    else:
        today = date.today()
        my_tasks = my_tasks.copy()
        my_tasks['Project Deadline'] = pd.to_datetime(my_tasks['Project Deadline'])
        my_tasks['Days Remaining'] = (my_tasks['Project Deadline'] - pd.Timestamp(today)).dt.days

        def status_color(row):
            if row['Status'] == 'Completed':
                return '✅ Completed'
            elif row['Days Remaining'] < 0:
                return '🔴 Overdue'
            elif row['Days Remaining'] <= 3:
                return '🟡 Due Soon'
            else:
                return '🟢 In Progress'

        my_tasks['Status Display'] = my_tasks.apply(status_color, axis=1)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", len(my_tasks))
        with col2:
            completed_count = len(my_tasks[my_tasks['Status'] == 'Completed'])
            st.metric("Completed", completed_count)
        with col3:
            overdue_count = len(my_tasks[(my_tasks['Days Remaining'] < 0) & (my_tasks['Status'] != 'Completed')])
            st.metric("Overdue", overdue_count)

        st.divider()

        for idx, task in my_tasks.iterrows():
            with st.expander(f"{task['Project Name']} - {task['Task Name/Description']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Deadline:** {task['Project Deadline'].strftime('%Y-%m-%d')}")
                    st.write(f"**Days Remaining:** {task['Days Remaining']}")
                    st.write(f"**Status:** {task['Status Display']}")
                with col2:
                    st.write(f"**Comments:** {task.get('Comments', 'None')}")
                    st.write(f"**Decision:** {task.get('Decision', 'Pending')}")

                if task['Status'] != 'Completed':
                    if st.button("✅ Mark as Completed", key=f"complete_{idx}"):
                        sheet_row = idx + 2
                        update_cell("Projects", sheet_row, 7, "Completed")
                        st.success("Task marked as completed!")
                        st.rerun()

    # Sidebar - Clean with only navigation
    with st.sidebar:
        st.markdown("## AKRC Portal")
        st.markdown("---")
        
        # Profile Settings button
        if st.button("⚙️ Profile Settings", use_container_width=True):
            profile_settings_dialog(display_name, profile)
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.researcher_name = None
            st.session_state.username = None
            st.session_state.profile_image = None
            st.rerun()

# ============================================
# ADMIN DASHBOARD
# ============================================
def admin_dashboard():
    st.title("Admin Dashboard - Advanced Knowledge Research Consultancy")

    projects_df = load_data("Projects")
    revenue_df = load_data("Projects Revenue")
    payments_df = load_data("Project Payments Received")
    payouts_df = load_data("Researcher Payouts")

    tab1, tab2, tab3 = st.tabs(["📊 Projects Overview", "💰 Financial Overview", "📋 All Data"])

    with tab1:
        st.subheader("Project Progress")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_projects = projects_df['Project Name'].nunique()
            st.metric("Total Projects", total_projects)
        with col2:
            total_tasks = len(projects_df)
            st.metric("Total Tasks", total_tasks)
        with col3:
            completed = len(projects_df[projects_df['Status'] == 'Completed'])
            st.metric("Completed", completed)
        with col4:
            overdue = len(projects_df[(pd.to_datetime(projects_df['Project Deadline']) < pd.Timestamp(date.today())) &
                                    (projects_df['Status'] != 'Completed')])
            st.metric("Overdue", overdue)

        st.subheader("Completion by Project")
        project_progress = projects_df.groupby('Project Name').agg(
            Total_Tasks=('Task Name/Description', 'count'),
            Completed_Tasks=('Status', lambda x: (x == 'Completed').sum())
        )
        project_progress['Completion %'] = (project_progress['Completed_Tasks'] / project_progress['Total_Tasks'] * 100).round(1)
        st.dataframe(project_progress, width='stretch')
        st.bar_chart(project_progress['Completion %'])

    with tab2:
        st.subheader("Financial Overview")

        total_invoiced = revenue_df['Total Amount Billed'].sum()
        total_received = payments_df['Amount Received'].sum()
        total_payouts = payouts_df['Payout Amount'].sum()
        total_retained = revenue_df['Amount Retained (Company)'].sum()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Invoiced", f"${total_invoiced:,.0f}")
        with col2:
            st.metric("Total Received", f"${total_received:,.0f}")
        with col3:
            st.metric("Balance Owing", f"${total_invoiced - total_received:,.0f}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Company Retained", f"${total_retained:,.0f}")
        with col2:
            st.metric("Researcher Payouts", f"${total_payouts:,.0f}")

        st.subheader("Per-Project Financials")
        project_finance = revenue_df.groupby('Project Name').agg(
            Invoiced=('Total Amount Billed', 'sum'),
            Retained=('Amount Retained (Company)', 'sum')
        ).reset_index()
        
        payments_by_project = payments_df.groupby('Project Name').agg(
            Received=('Amount Received', 'sum')
        ).reset_index()
        
        project_finance = project_finance.merge(payments_by_project, on='Project Name', how='left')
        project_finance['Received'] = project_finance['Received'].fillna(0)
        project_finance['Balance'] = project_finance['Invoiced'] - project_finance['Received']
        
        st.dataframe(project_finance, width='stretch')

    with tab3:
        st.subheader("All Projects & Tasks")

        col1, col2, col3 = st.columns(3)
        with col1:
            project_filter = st.multiselect("Filter by Project", projects_df['Project Name'].unique())
        with col2:
            researcher_filter = st.multiselect("Filter by Researcher", projects_df['Researcher Assigned'].unique())
        with col3:
            status_filter = st.multiselect("Filter by Status", projects_df['Status'].unique())

        filtered_df = projects_df.copy()
        if project_filter:
            filtered_df = filtered_df[filtered_df['Project Name'].isin(project_filter)]
        if researcher_filter:
            filtered_df = filtered_df[filtered_df['Researcher Assigned'].isin(researcher_filter)]
        if status_filter:
            filtered_df = filtered_df[filtered_df['Status'].isin(status_filter)]

        st.dataframe(filtered_df, width='stretch')

        csv = filtered_df.to_csv(index=False)
        st.download_button("📥 Download as CSV", csv, "projects_export.csv", "text/csv")

    with st.sidebar:
        st.markdown("## AKRC Portal")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.rerun()

# ============================================
# MAIN
# ============================================
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.user_type == "Researcher":
        researcher_dashboard()
    else:
        admin_dashboard()
