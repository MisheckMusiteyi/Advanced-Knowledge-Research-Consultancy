import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
from datetime import datetime, date

# ============================================
# GOOGLE SHEETS SETUP
# ============================================
@st.cache_resource
def connect_to_sheets():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    
    # For Streamlit Cloud — read from secrets at top level
    try:
        creds_dict = dict(st.secrets)
        # Remove non-credential keys from secrets
        creds_dict.pop("admin_password", None)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    except Exception as e:
        # Fallback for local development
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
# SESSION STATE
# ============================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'researcher_name' not in st.session_state:
    st.session_state.researcher_name = None

# ============================================
# LOGIN PAGE
# ============================================
def login_page():
    st.title("Advanced Knowledge Research Consultancy")
    st.subheader("Portal Login")

    login_type = st.radio("Login as:", ["Researcher", "Admin"])

    if login_type == "Researcher":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            logins_df = load_data("Researcher Logins")

            match = logins_df[(logins_df['Email'] == email) &
                            (logins_df['Password'] == password) &
                            (logins_df['Active'] == 'Yes')]

            if len(match) > 0:
                st.session_state.logged_in = True
                st.session_state.user_type = "Researcher"
                st.session_state.researcher_name = match.iloc[0]['Researcher Name']
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials or account inactive.")

    else:
        admin_password = st.text_input("Admin Password", type="password")

        if st.button("Login"):
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
    st.title(f"Welcome, {st.session_state.researcher_name}")
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
            with st.expander(f"{task['Project Name']} - {task['Task Description']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Deadline:** {task['Deadline'].strftime('%Y-%m-%d')}")
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

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.researcher_name = None
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

    tab1, tab2, tab3 = st.tabs(["Projects Overview", "Financial Overview", "All Data"])

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
            overdue = len(projects_df[(pd.to_datetime(projects_df['Deadline']) < pd.Timestamp(date.today())) &
                                    (projects_df['Status'] != 'Completed')])
            st.metric("Overdue", overdue)

        st.subheader("Completion by Project")
        project_progress = projects_df.groupby('Project Name').agg(
            Total_Tasks=('Task Description', 'count'),
            Completed_Tasks=('Status', lambda x: (x == 'Completed').sum())
        )
        project_progress['Completion %'] = (project_progress['Completed_Tasks'] / project_progress['Total_Tasks'] * 100).round(1)
        st.dataframe(project_progress, use_container_width=True)
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
        
        st.dataframe(project_finance, use_container_width=True)

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

        st.dataframe(filtered_df, use_container_width=True)

        csv = filtered_df.to_csv(index=False)
        st.download_button("Download as CSV", csv, "projects_export.csv", "text/csv")

    if st.sidebar.button("Logout"):
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
