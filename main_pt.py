# Project Tracker Main Application Logic (Streamlit)

from re import search
from unittest import result
from pandas import col
import requests
import streamlit as st
from datetime import datetime
import pandas as pd
from collections import Counter


# Configuration of page
st.set_page_config(
    page_title="Project Tracker",
    page_icon=":clipboard:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API base URL
API_BASE_URL = "http://localhost:8000"


# Check if API is running
def check_api_connection():
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        st.error("Unable to connect to the API. Please ensure the API is running.")
        return False


# Create Project
def create_project_api(project):
    try:
        response = requests.post(f"{API_BASE_URL}/projects/", json=project, timeout=30)

        if response.status_code in (200, 201):
            return response.json(), True, None

        try:
            error_detail = response.json().get("detail", response.text)
        except Exception:
            error_detail = response.text

        return None, False, error_detail

    except requests.exceptions.RequestException as e:
        return None, False, str(e)


# Retrieve all projects
def get_all_projects():
    try:
        response = requests.get(f"{API_BASE_URL}/projects/")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Project by Database ID
def get_project_by_db_id(db_id):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/id/{db_id}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Name Keyword (Case-Insensitive)
def get_projects_by_name_keyword(keyword):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/search/{keyword}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project SID
def get_projects_by_sid(sid):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/sid/{sid}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Segment
def get_projects_by_segment(segment):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/segment/{segment}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Type
def get_projects_by_type(p_type):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/type/{p_type}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project TA ID
def get_projects_by_ta_id(ta_id):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/ta_id/{ta_id}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Job ID
def get_projects_by_job_id(job_id):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/job_id/{job_id}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Job OL ID
def get_projects_by_job_ol_id(job_ol_id):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/job_ol_id/{job_ol_id}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Job RA ID
def get_projects_by_job_ra_id(job_ra_id):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/job_ra_id/{job_ra_id}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Status
def get_projects_by_status(status):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/status/{status}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Manager
def get_projects_by_manager(manager):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/manager/{manager}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Business Unit
def get_projects_by_business_unit(b_unit):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/business_unit/{b_unit}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Business Country
def get_projects_by_business_country(b_country):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/business_country/{b_country}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Business Name
def get_projects_by_business_name(b_name):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/business_name/{b_name}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Margin Band
def get_projects_by_margin_band(f_margin_band):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/margin_band/{f_margin_band}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Retrieve Projects by Project Date Filter
def get_projects_by_date(
    month=None, year=None, since=None, until=None, date_type="start"
):
    try:
        params = {}
        if month:
            params["month"] = month
        if year:
            params["year"] = year
        if since:
            params["since"] = since
        if until:
            params["until"] = until
        if date_type:
            params["date_type"] = date_type

        response = requests.get(f"{API_BASE_URL}/projects/filter/date", params=params)
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# Update Project by Database ID
def update_project_by_db_id(db_id, updates):
    try:
        response = requests.put(
            f"{API_BASE_URL}/projects/{db_id}", json=updates, timeout=30
        )

        if response.status_code == 200:
            return response.json(), True, None

        try:
            error_detail = response.json().get("detail", response.text)
        except Exception:
            error_detail = response.text

        return None, False, error_detail

    except requests.exceptions.RequestException as e:
        return None, False, str(e)


# Delete Project by Database ID
def delete_project_by_db_id(db_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/projects/{db_id}")
        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False
    except requests.exceptions.RequestException as e:
        return None, False


# AI Insights Input
def generate_ai_response(user_query, projects):
    total_projects = len(projects)

    managers = {}
    statuses = {}

    for p in projects:
        managers[p.get("p_manager", "Unknown")] = (
            managers.get(p.get("p_manager", "Unknown"), 0) + 1
        )
        statuses[p.get("p_status", "Unknown")] = (
            statuses.get(p.get("p_status", "Unknown"), 0) + 1
        )

    top_manager = max(managers, key=managers.get) if managers else "N/A"
    top_status = max(statuses, key=statuses.get) if statuses else "N/A"

    return f"""
    🧠 AI Insight

    User Question: {user_query}

    📊 Summary:
    - Total Projects: {total_projects}
    - Top Manager (by volume): {top_manager}
    - Most Common Status: {top_status}

    📌 Sample Projects:
    {[p.get('p_name') for p in projects[:5]]}
    """


# Main function to run the Streamlit app
def main():
    st.title("ProTrack")
    st.markdown(
        "<h4 style='color: #6c757d; font-weight: 400;'>A Centralised Platform for Project Management and Performance Insights</h4>",
        unsafe_allow_html=True,
    )

    if not check_api_connection():
        st.error(
            "API connection failed. Please start the API server and refresh the page."
        )
        st.info(
            "To start the API server, run ` uvicorn EP_Project_Tracker:app --reload ` in your terminal."
        )
        return

    if "connected_toast" not in st.session_state:
        st.toast("✅ Connected to Project Tracker successfully!")
        st.session_state.connected_toast = True

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📊 Dashboard",
            "➕ Create Project",
            "🔍 Search Project",
            "✏️ Update Project",
            "🗑️ Delete Project",
            "🤖 AI Insights",
        ]
    )

    with tab1:
        show_dashboard()
    with tab2:
        create_project_ui()
    with tab3:
        search_projects()
    with tab4:
        update_project()
    with tab5:
        delete_project()
    with tab6:
        ai_insights()


# Dashboard
def show_dashboard():
    st.header("💼 Project Tracker Dashboard")
    st.markdown("Visual insights into project performance, trends, and distribution.")

    response_data, success = get_all_projects()

    if not success:
        st.error("Failed to load projects for dashboard.")
        return

    projects = response_data.get("projects", [])

    # def extract_projects(response_data):
    #     if isinstance(response_data, list):
    #         return response_data
    #     if isinstance(response_data, dict):
    #         return response_data.get("projects") or response_data.get("data") or []
    #     return []

    if not projects:
        st.info("No projects available.")
        return

    # KPI Section
    st.subheader("📈 Performance KPIs")
    total = len(projects)
    completed = sum(1 for p in projects if p.get("p_status") == "Completed")
    active = sum(1 for p in projects if p.get("p_status") == "Field")
    # active_statuses = {"Field", "Ongoing", "Active"}
    # active = sum(1 for p in projects if p.get("p_status") in active_statuses)

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Projects", total)
    col2.metric("✅ Completed", completed)
    col3.metric("🚧 Active", active)

    st.markdown("---")

    # Data
    status_counts = {}
    business_unit_counts = {}
    manager_counts = {}
    segment_counts = {}
    start_date_counts = {}

    for project in projects:
        status = project.get("p_status", "Unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

        b_unit = project.get("b_unit", "Unknown")
        business_unit_counts[b_unit] = business_unit_counts.get(b_unit, 0) + 1

        manager = project.get("p_manager", "Unknown")
        manager_counts[manager] = manager_counts.get(manager, 0) + 1

        segment = project.get("p_segment", "Unknown")
        segment_counts[segment] = segment_counts.get(segment, 0) + 1

        if project.get("p_s_date"):
            month = project["p_s_date"][:7]
            start_date_counts[month] = start_date_counts.get(month, 0) + 1

    # Chart
    st.subheader("📊 Distributions")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("📌 Projects by Status")
        st.bar_chart(status_counts)

    with col2:
        st.markdown("🏢 Projects by Business Unit")
        st.bar_chart(business_unit_counts)

    with col3:
        st.markdown("🧩 Projects by Segment")
        st.bar_chart(segment_counts)

    with col4:
        st.markdown("📅 Projects by Start Month")
        st.bar_chart(start_date_counts)

    with col5:
        st.markdown("👤 Projects by Manager")
        st.bar_chart(manager_counts)

    st.markdown("---")

    # Recent Project
    st.subheader("📌 Recent Projects")

    recent_projects = sorted(
        projects, key=lambda x: x.get("created_at") or "", reverse=True
    )

    for project in recent_projects[:5]:
        st.markdown(
            f"""
            **{project.get('p_name', 'Unnamed Project')}**  
            🆔 SID: {project.get('s_id', 'Unknown')}  
            📊 Status: {project.get('p_status', 'Unknown')}  
            🧩 Segment: {project.get('p_segment', 'Unknown')}  
            👤 Manager: {project.get('p_manager', 'Unknown')}  
            📅 Start: {project.get('p_s_date', 'Unknown')}  
            """
        )

    # if success:
    #     projects = response_data["projects"]
    #     st.metric("Total Projects", len(projects))
    #     col1, col2, col3, col4, col5, col6 = st.columns(6)
    #     with col1:
    #         st.subheader("Total Projects")
    #         status_counts = {}
    #         for project in projects:
    #             status = project.get("p_status", "Unknown")
    #             status_counts[status] = status_counts.get(status, 0) + 1
    #         st.bar_chart(status_counts)
    #     with col2:
    #         st.subheader("Projects by Status")
    #         status_counts = {}
    #         for project in projects:
    #             status = project.get("p_status", "Unknown")
    #             status_counts[status] = status_counts.get(status, 0) + 1
    #         st.bar_chart(status_counts)
    #     with col3:
    #         st.subheader("Projects by Business Unit")
    #         business_unit_counts = {}
    #         for project in projects:
    #             business_unit = project.get("b_unit", "Unknown")
    #             business_unit_counts[business_unit] = business_unit_counts.get(business_unit, 0) + 1
    #         st.bar_chart(business_unit_counts)
    #     with col4:
    #         st.subheader("Projects by Start Date")
    #         start_date_counts = {}
    #         for project in projects:
    #             start_date = project.get("p_s_date", "Unknown")
    #             start_date_counts[start_date] = start_date_counts.get(start_date, 0) + 1
    #         st.bar_chart(start_date_counts)
    #     with col5:
    #         st.subheader("Projects by Margin Band")
    #         margin_band_counts = {}
    #         for project in projects:
    #             margin_band = project.get("margin_band") or project.get("f_margin_band", "Unknown")
    #             margin_band_counts[margin_band] = margin_band_counts.get(margin_band, 0) + 1
    #         st.bar_chart(margin_band_counts)
    #     with col6:
    #         st.subheader("Projects by Project Manager")
    #         p_manager_counts = {}
    #         for project in projects:
    #             project_manager = project.get("p_manager", "Unknown")
    #             p_manager_counts[project_manager] = p_manager_counts.get(project_manager, 0) + 1
    #         st.bar_chart(p_manager_counts)

    # st.markdown("### Recent Projects")
    # recent_projects = sorted(
    #     projects,
    #     key=lambda x: x.get("created_at") or "",
    #     reverse=True
    # )

    # for project in recent_projects:
    #     st.markdown(f"**{project.get('p_name', 'Unnamed Project')}**, "
    #                 f"sid: {project.get('s_id', 'Unknown')},"
    #                 f"Status: {project.get('p_status', 'Unknown')}, "
    #                 f"Segment: {project.get('p_segment', 'Unknown')}, "
    #                 f"Type: {project.get('p_type', 'Unknown')}")

    else:
        st.markdown("The end of Project Tracker Dashboard")


# Create Project
def create_project_ui():
    st.header("➕ Create New Project")
    st.markdown("Fill out the form below to create a new project.")

    with st.form("create_project_form"):
        p_name = st.text_input(
            "Project Name", max_chars=100, placeholder="Enter Project Name"
        )
        p_manager = st.text_input(
            "Project Manager", max_chars=100, placeholder="Enter Project Manager"
        )
        p_team = st.text_input(
            "Project Team", max_chars=100, placeholder="Enter Project Team"
        )
        p_segment = st.selectbox(
            "Project Segment",
            [
                "Sample Only (External)",
                "Sample Only",
                "Full Service",
                "Coverage",
                "Other",
            ],
        )
        p_type = st.selectbox("Project Type", ["Ad Hoc", "Tracker", "Other"])
        p_status = st.selectbox("Project Status", ["Field", "Completed", "Other"])
        p_s_date = st.date_input("Project Start Date")
        p_e_date = st.date_input("Project End Date")
        job_id = st.text_input(
            "Job ID", max_chars=12, placeholder="Enter 10 Digit Job ID"
        )
        job_ol_id = st.text_input(
            "Job OL ID", max_chars=15, placeholder="Enter 12 Digit Job OL ID"
        )
        job_ra_id = st.text_input(
            "Job RA ID", max_chars=15, placeholder="Enter 12 Digit Job RA ID"
        )
        s_id = st.text_input("SID", value="S", max_chars=9, placeholder="Enter SID")
        ta_id = st.number_input(
            "TA ID",
            min_value=0,
            max_value=999999,
            value=None,
            placeholder="Enter TA ID",
        )
        pf_link = st.text_input(
            "Path Folder Link", max_chars=200, placeholder="Enter Path Folder Link"
        )
        b_unit = st.text_input(
            "Business Unit", max_chars=100, placeholder="Enter Client Company"
        )
        b_country = st.text_input(
            "Business Country", max_chars=100, placeholder="Enter Client Country"
        )
        b_name = st.text_input(
            "Business Name", max_chars=100, placeholder="Enter Client Name"
        )
        b_name_id = st.number_input(
            "Business Name ID",
            min_value=0,
            max_value=99,
            value=None,
            placeholder="Enter Client ID (Symphony)",
        )
        market = st.text_input(
            "Market", max_chars=100, placeholder="Enter Fieldwork Market"
        )
        ir = st.number_input(
            "IR (%)",
            min_value=0.0,
            max_value=100.0,
            value=None,
            placeholder="Enter IR (%)",
        )
        loi = st.number_input(
            "LOI (Minutes)",
            min_value=0,
            max_value=999,
            value=None,
            placeholder="Enter LOI (Minutes)",
        )
        f_deliverables = st.number_input(
            "Final Deliverables",
            min_value=0,
            max_value=99999,
            value=None,
            placeholder="Enter Final Deliverables",
        )
        f_currency = (
            st.text_input(
                "Final Currency (e.g. AUD / USD)",
                max_chars=3,
                placeholder="Enter Final Currency",
            )
            .strip()
            .upper()
        )
        f_revenue = st.number_input(
            "Fieldwork Revenue",
            min_value=0.0,
            max_value=9999999.0,
            value=None,
            placeholder="Enter Fieldwork Revenue",
        )
        f_cost = st.number_input(
            "Fieldwork Cost",
            min_value=0.0,
            max_value=9999999.0,
            value=None,
            placeholder="Enter Fieldwork Cost/Incentive",
        )
        f_nprofit = st.number_input(
            "Fieldwork Net Profit",
            min_value=0.0,
            max_value=9999999.0,
            value=None,
            placeholder="Enter Fieldwork Net Profit",
        )
        margin_band = st.selectbox(
            "Margin Band", ["0%", "1-19%", "20-49%", "50-79%", "80-100%"]
        )
        f_remarks = st.text_area("Fieldwork Remarks", max_chars=500)

        submit_button = st.form_submit_button(label="Create Project", type="primary")

    if submit_button:

        if not p_name or not p_name.strip():
            st.error("Project Name is required.")
            return
        if not p_manager or not p_manager.strip():
            st.error("Project Manager is required.")
            return
        if not p_team or not p_team.strip():
            st.error("Project Team is required.")
            return
        if not p_segment or not p_segment.strip():
            st.error("Project Segment is required.")
            return
        if not p_type or not p_type.strip():
            st.error("Project Type is required.")
            return
        if not p_status or not p_status.strip():
            st.error("Project Status is required.")
            return
        if p_e_date < p_s_date:
            st.error("Project End Date cannot be before Start Date.")
            return
        if not p_s_date:
            st.error("Project Start Date is required.")
            return
        if not job_id or not job_id.strip():
            st.error("Project Job ID is required.")
            return
        if not job_ol_id or not job_ol_id.strip():
            st.error("Project Job OL ID is required.")
            return
        if not job_ra_id or not job_ra_id.strip():
            st.error("Project Job RA ID is required.")
            return
        if not s_id or not s_id.strip():
            st.error("Project SID is required.")
            return
        if ta_id is None:
            st.error("Project TA ID is required.")
            return
        if not pf_link or not pf_link.strip():
            st.error("Path Folder Link is required.")
            return
        if not b_unit or not b_unit.strip():
            st.error("Business Unit is required.")
            return
        if not b_country or not b_country.strip():
            st.error("Business Country is required.")
            return
        if not b_name or not b_name.strip():
            st.error("Business Name is required.")
            return
        if b_name_id is None:
            st.error("Business Name ID is required.")
            return
        if not market or not market.strip():
            st.error("Market is required.")
            return
        if ir is None:
            st.error("IR is required.")
            return
        if loi is None:
            st.error("LOI is required.")
            return

        try:
            ta_id_val = int(ta_id) if str(ta_id).strip() else None
        except ValueError:
            st.error("TA ID must be a number.")
            return
        try:
            b_name_id_val = int(b_name_id) if str(b_name_id).strip() else None
        except ValueError:
            st.error("Business Name ID must be a number.")
            return
        try:
            ir_val = int(ir) if str(ir).strip() else None
        except ValueError:
            st.error("IR must be a number.")
            return
        try:
            loi_val = int(loi) if str(loi).strip() else None
        except ValueError:
            st.error("LOI must be a number.")
            return

        margin_map = {"0%": 0, "1-19%": 10, "20-49%": 30, "50-79%": 60, "80-100%": 90}

        new_project = {
            "p_name": p_name,
            "p_manager": p_manager,
            "p_team": p_team,
            "p_segment": p_segment,
            "p_type": p_type,
            "p_status": p_status,
            "p_s_date": p_s_date.isoformat() if p_s_date else None,
            "p_e_date": p_e_date.isoformat() if p_e_date else None,
            "job_id": job_id,
            "job_ol_id": job_ol_id,
            "job_ra_id": job_ra_id,
            "s_id": s_id,
            "ta_id": int(ta_id_val),
            "pf_link": pf_link,
            "b_unit": b_unit,
            "b_country": b_country,
            "b_name": (b_name),
            "b_name_id": int(b_name_id_val),
            "market": market,
            "ir": int(ir_val),
            "loi": int(loi_val),
            "f_deliverables": f_deliverables,
            "f_currency": f_currency,
            "f_revenue": f_revenue,
            "f_cost": f_cost,
            "f_nprofit": f_nprofit,
            "f_margin": margin_map.get(margin_band, 0.0),
            "f_remarks": f_remarks,
        }

        response, success, error_msg = create_project_api(new_project)

        if success:
            st.session_state["success_msg"] = (
                f"Project: {p_name} created successfully! DB ID: {response['db_id']}"
            )
            st.rerun()
        else:
            st.error(f"Failed to create project: {error_msg}")

    if "success_msg" in st.session_state:
        st.markdown("---")
        st.success(st.session_state["success_msg"])
        del st.session_state["success_msg"]

    st.info(
        "Fill out the form and click 'Create Project' to add a new project to the tracker."
    )


# Search Projects
def search_projects():
    st.header("🔍 Search Projects")

    tab1, tab2 = st.tabs(["Show all projects", "Search by criteria"])

    with tab1:
        st.markdown("### All Projects")
        response_data, success = get_all_projects()
        if success:
            projects = response_data["projects"]
            display_search_results(response_data)
        else:
            st.error("Failed to retrieve projects. Please try again later.")

    with tab2:
        st.markdown("Click on the criteria below to search for projects.")
        search_criteria = st.selectbox(
            "Search by",
            [
                "Project Name Keyword",
                "Project SID",
                "Project Segment",
                "Project Type",
                "Project TA ID",
                "Project Job ID",
                "Project Job OL ID",
                "Project Job RA ID",
                "Project Status",
                "Project Manager",
                "Project Business Unit",
                "Project Business Country",
                "Project Business Name",
                "Project Margin Band",
                "Project Date Filter",
            ],
        )

        if search_criteria == "Project Name Keyword":
            keyword = st.text_input(
                "Enter keyword to search in project names", max_chars=100
            )
            if st.button("Search", key="search_name_keyword"):
                response_data, success = get_projects_by_name_keyword(keyword)
                if success:
                    display_search_results(response_data)
                else:
                    st.error(
                        "No projects found matching the search criteria. Please try a different keyword."
                    )

        elif search_criteria == "Project SID":
            sid = st.text_input("Enter Project SID", max_chars=20)
            if st.button("Search", key="search_sid"):
                response_data, success = get_projects_by_sid(sid)
                if success:
                    display_search_results(response_data)
                else:
                    st.error(
                        "No projects found matching the search criteria. Please try a different SID."
                    )

        elif search_criteria == "Project Segment":
            segment = st.selectbox(
                "Select Project Segment",
                [
                    "Full Service",
                    "Sample Only",
                    "Sample Only (External)",
                    "Coverage",
                    "Other",
                ],
            )
            if st.button("Search", key="search_segment"):
                response_data, success = get_projects_by_segment(segment)
                if success:
                    display_search_results(response_data)
                else:
                    st.error(
                        "No projects found matching the search criteria. Please try a different segment."
                    )

        elif search_criteria == "Project Type":
            p_type = st.selectbox("Select Project Type", ["Tracker", "Ad Hoc", "Other"])
            if st.button("Search", key="search_type"):
                response_data, success = get_projects_by_type(p_type)
                if success:
                    display_search_results(response_data)
                else:
                    st.error(
                        "No projects found matching the search criteria. Please try a different type."
                    )

        elif search_criteria == "Project TA ID":
            ta_id = st.text_input("Enter Project TA ID", max_chars=10)
            if st.button("Search", key="search_ta_id"):
                response_data, success = get_projects_by_ta_id(ta_id)
                if success:
                    display_search_results(response_data)
                else:
                    st.error(
                        "No projects found matching the search criteria. Please try a different TA ID."
                    )

        elif search_criteria == "Project Job ID":
            job_id = st.text_input("Enter Project Job ID", max_chars=20)
            if st.button("Search", key="search_job_id"):
                response_data, success = get_projects_by_job_id(job_id)
                if success:
                    display_search_results(response_data)
                else:
                    st.error(
                        "No projects found matching the search criteria. Please try a different Job ID."
                    )

        elif search_criteria == "Project Job OL ID":
            job_ol_id = st.text_input("Enter Project Job OL ID", max_chars=20)
            if st.button("Search", key="search_job_ol_id"):
                response_data, success = get_projects_by_job_ol_id(job_ol_id)
                if success:
                    display_search_results(response_data)
            else:
                st.error(
                    "No projects found matching the search criteria. Please try a different Job OL ID."
                )

        elif search_criteria == "Project Job RA ID":
            job_ra_id = st.text_input("Enter Project Job RA ID", max_chars=20)
            if st.button("Search", key="search_job_ra_id"):
                response_data, success = get_projects_by_job_ra_id(job_ra_id)
                if success:
                    display_search_results(response_data)
            else:
                st.error(
                    "No projects found matching the search criteria. Please try a different Job RA ID."
                )

        elif search_criteria == "Project Status":
            status = st.selectbox(
                "Select Project Status", ["Field", "Completed", "Other"]
            )
            if st.button("Search", key="search_status"):
                response_data, success = get_projects_by_status(status)
                if success:
                    display_search_results(response_data)
                else:
                    st.error(
                        "No projects found matching the search criteria. Please try a different status."
                    )

        elif search_criteria == "Project Manager":
            manager = st.text_input("Enter Project Manager Name", max_chars=100)
            if st.button("Search", key="search_manager"):
                response_data, success = get_projects_by_manager(manager)
                if success:
                    display_search_results(response_data)
            else:
                st.error(
                    "No projects found matching the search criteria. Please try a different project manager name."
                )

        elif search_criteria == "Project Business Unit":
            b_unit = st.text_input("Enter Business Unit", max_chars=100)
            if st.button("Search", key="search_business_unit"):
                response_data, success = get_projects_by_business_unit(b_unit)
                if success:
                    display_search_results(response_data)
            else:
                st.error(
                    "No projects found matching the search criteria. Please try a different business unit."
                )

        elif search_criteria == "Project Business Country":
            b_country = st.text_input("Enter Business Country", max_chars=100)
            if st.button("Search", key="search_business_country"):
                response_data, success = get_projects_by_business_country(b_country)
                if success:
                    display_search_results(response_data)
            else:
                st.error(
                    "No projects found matching the search criteria. Please try a different business country."
                )

        elif search_criteria == "Project Business Name":
            b_name = st.text_input("Enter Business Name", max_chars=100)
            if st.button("Search", key="search_business_name"):
                response_data, success = get_projects_by_business_name(b_name)
                if success:
                    display_search_results(response_data)
            else:
                st.error(
                    "No projects found matching the search criteria. Please try a different business name."
                )

        elif search_criteria == "Project Margin Band":
            f_margin_band = st.selectbox(
                "Select Margin Band", ["0%", "1-19%", "20-49%", "50-79%", "80-100%"]
            )
            if st.button("Search", key="search_margin_band"):
                response_data, success = get_projects_by_margin_band(f_margin_band)
                if success:
                    display_search_results(response_data)
            else:
                st.error(
                    "No projects found matching the search criteria. Please try a different margin band."
                )

        elif search_criteria == "Project Date Filter":
            col1, col2 = st.columns(2)
            with col1:
                month = st.selectbox(
                    "Select Month",
                    [
                        "",
                        "January",
                        "February",
                        "March",
                        "April",
                        "May",
                        "June",
                        "July",
                        "August",
                        "September",
                        "October",
                        "November",
                        "December",
                    ],
                )
            with col2:
                year = st.text_input("Enter Year (e.g. 2026)", max_chars=4)
            if st.button("Search", key="search_date"):
                month_map = {
                    "": None,
                    "January": 1,
                    "February": 2,
                    "March": 3,
                    "April": 4,
                    "May": 5,
                    "June": 6,
                    "July": 7,
                    "August": 8,
                    "September": 9,
                    "October": 10,
                    "November": 11,
                    "December": 12,
                }
                month_number = month_map.get(month)
                year_number = int(year) if year else None
                response_data, success = get_projects_by_date(
                    month=month_number, year=year_number
                )
                if success:
                    display_search_results(response_data)
                else:
                    st.error(
                        "No projects found matching the search criteria. Please try different date filters."
                    )


# Update Project
def update_project():
    st.header("✏️ Update Project")
    st.markdown(
        "Enter the Database ID to load a project, then edit only the fields you want to change."
    )

    db_id_input = st.text_input(
        "Enter Database ID of the project to update", max_chars=10
    )

    if not db_id_input:
        return

    if not db_id_input.isdigit():
        st.error("Database ID must be a number.")
        return

    db_id = int(db_id_input)

    response_data, success = get_project_by_db_id(db_id)

    project = None
    if isinstance(response_data, dict):
        if "project" in response_data:
            project = response_data["project"]
        elif "projects" in response_data and response_data["projects"]:
            project = response_data["projects"][0]
        elif "data" in response_data:
            project = response_data["data"]

    if not success or not project:
        st.error(f"No project found with Database ID {db_id}.")
        return

    st.markdown(
        f"### Current Details for Project: {project.get('p_name', 'Unnamed Project')}"
    )

    with st.expander("View current project details", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 📋 Project Information")
            st.markdown(f"**DB ID:** {project.get('db_id')}")
            st.markdown(f"**Project Name:** {project.get('p_name')}")
            st.markdown(f"**Project Manager:** {project.get('p_manager')}")
            st.markdown(f"**Project Team:** {project.get('p_team')}")
            st.markdown(f"**Segment:** {project.get('p_segment')}")
            st.markdown(f"**Type:** {project.get('p_type')}")
            st.markdown(f"**Status:** {project.get('p_status')}")

        with col2:
            st.markdown("### 🆔 Operational Details")
            st.markdown(f"**Start Date:** {project.get('p_s_date')}")
            st.markdown(f"**End Date:** {project.get('p_e_date')}")
            st.markdown(f"**Job ID:** {project.get('job_id')}")
            st.markdown(f"**Job OL ID:** {project.get('job_ol_id')}")
            st.markdown(f"**Job RA ID:** {project.get('job_ra_id')}")
            st.markdown(f"**SID:** {project.get('s_id')}")
            st.markdown(f"**TA ID:** {project.get('ta_id')}")
            st.markdown(f"**Path Folder Link:** {project.get('pf_link')}")

        with col3:
            st.markdown("### 💰 Business / Financial Details")
            st.markdown(f"**Business Unit:** {project.get('b_unit')}")
            st.markdown(f"**Business Country:** {project.get('b_country')}")
            st.markdown(f"**Business Name:** {project.get('b_name')}")
            st.markdown(f"**Business Name ID:** {project.get('b_name_id')}")
            st.markdown(f"**Market:** {project.get('market')}")
            st.markdown(f"**IR:** {project.get('ir')}")
            st.markdown(f"**LOI:** {project.get('loi')}")
            st.markdown(f"**Final Deliverables:** {project.get('f_deliverables')}")
            st.markdown(f"**Final Currency:** {project.get('f_currency')}")
            st.markdown(f"**Revenue:** {project.get('f_revenue')}")
            st.markdown(f"**Cost:** {project.get('f_cost')}")
            st.markdown(f"**Net Profit:** {project.get('f_nprofit')}")
            st.markdown(f"**Margin:** {project.get('f_margin')}")
            st.markdown(f"**Remarks:** {project.get('f_remarks')}")

    st.markdown("---")
    st.subheader("Edit Project Fields")

    def parse_date(value):
        if not value:
            return None
        try:
            return datetime.fromisoformat(str(value)).date()
        except Exception:
            return None

    original_start_date = parse_date(project.get("p_s_date"))
    original_end_date = parse_date(project.get("p_e_date"))

    with st.form(f"update_project_form_{db_id}"):
        col1, col2 = st.columns(2)

        with col1:
            p_name = st.text_input("Project Name", value=project.get("p_name", ""))
            p_manager = st.text_input(
                "Project Manager", value=project.get("p_manager", "")
            )
            p_team = st.text_input("Project Team", value=project.get("p_team", ""))
            p_segment = st.selectbox(
                "Project Segment",
                [
                    "Sample Only (External)",
                    "Sample Only",
                    "Full Service",
                    "Coverage",
                    "Other",
                ],
                index=(
                    [
                        "Sample Only (External)",
                        "Sample Only",
                        "Full Service",
                        "Coverage",
                        "Other",
                    ].index(project.get("p_segment", "Other"))
                    if project.get("p_segment", "Other")
                    in [
                        "Sample Only (External)",
                        "Sample Only",
                        "Full Service",
                        "Coverage",
                        "Other",
                    ]
                    else 4
                ),
            )
            p_type = st.selectbox(
                "Project Type",
                ["Ad Hoc", "Tracker", "Other"],
                index=(
                    ["Ad Hoc", "Tracker", "Other"].index(project.get("p_type", "Other"))
                    if project.get("p_type", "Other") in ["Ad Hoc", "Tracker", "Other"]
                    else 2
                ),
            )
            p_status = st.selectbox(
                "Project Status",
                ["Field", "Completed", "Other"],
                index=(
                    ["Field", "Completed", "Other"].index(
                        project.get("p_status", "Other")
                    )
                    if project.get("p_status", "Other")
                    in ["Field", "Completed", "Other"]
                    else 2
                ),
            )
            p_s_date = st.date_input("Project Start Date", value=original_start_date)
            p_e_date = st.date_input("Project End Date", value=original_end_date)

            job_id = st.text_input("Job ID", value=str(project.get("job_id") or ""))
            job_ol_id = st.text_input(
                "Job OL ID", value=str(project.get("job_ol_id") or "")
            )
            job_ra_id = st.text_input(
                "Job RA ID", value=str(project.get("job_ra_id") or "")
            )
            s_id = st.text_input("SID", value=str(project.get("s_id") or ""))
            ta_id = st.number_input(
                "TA ID", min_value=0, value=int(project.get("ta_id") or 0), step=1
            )
            pf_link = st.text_input(
                "Path Folder Link", value=str(project.get("pf_link") or "")
            )

        with col2:
            b_unit = st.text_input(
                "Business Unit", value=str(project.get("b_unit") or "")
            )
            b_country = st.text_input(
                "Business Country", value=str(project.get("b_country") or "")
            )
            b_name = st.text_input(
                "Business Name", value=str(project.get("b_name") or "")
            )
            b_name_id = st.number_input(
                "Business Name ID",
                min_value=0,
                value=int(project.get("b_name_id") or 0),
                step=1,
            )
            market = st.text_input("Market", value=str(project.get("market") or ""))
            ir = st.number_input(
                "IR (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(project.get("ir") or 0.0),
                step=0.1,
            )
            loi = st.number_input(
                "LOI (Minutes)",
                min_value=0.0,
                value=float(project.get("loi") or 0.0),
                step=0.1,
            )
            f_deliverables = st.number_input(
                "Final Deliverables",
                min_value=0,
                value=int(project.get("f_deliverables") or 0),
                step=1,
            )
            f_currency = (
                st.text_input(
                    "Final Currency", value=str(project.get("f_currency") or "")
                )
                .strip()
                .upper()
            )
            f_revenue = st.number_input(
                "Fieldwork Revenue",
                min_value=0.0,
                value=float(project.get("f_revenue") or 0.0),
                step=0.01,
            )
            f_cost = st.number_input(
                "Fieldwork Cost",
                min_value=0.0,
                value=float(project.get("f_cost") or 0.0),
                step=0.01,
            )
            f_nprofit = st.number_input(
                "Fieldwork Net Profit",
                min_value=0.0,
                value=float(project.get("f_nprofit") or 0.0),
                step=0.01,
            )
            f_margin = st.number_input(
                "Final Margin (%)",
                min_value=0.0,
                value=float(project.get("f_margin") or 0.0),
                step=0.1,
            )
            f_remarks = st.text_area(
                "Fieldwork Remarks", value=str(project.get("f_remarks") or "")
            )

        submit_update = st.form_submit_button("Update Project", type="primary")

    if submit_update:
        if p_e_date and p_s_date and p_e_date < p_s_date:
            st.error("Project End Date cannot be before Start Date.")
            return

        form_data = {
            "p_name": p_name.strip(),
            "p_manager": p_manager.strip(),
            "p_team": p_team.strip(),
            "p_segment": p_segment,
            "p_type": p_type,
            "p_status": p_status,
            "p_s_date": p_s_date.isoformat() if p_s_date else None,
            "p_e_date": p_e_date.isoformat() if p_e_date else None,
            "job_id": job_id.strip(),
            "job_ol_id": job_ol_id.strip(),
            "job_ra_id": job_ra_id.strip(),
            "s_id": s_id.strip(),
            "ta_id": int(ta_id),
            "pf_link": pf_link.strip(),
            "b_unit": b_unit.strip(),
            "b_country": b_country.strip(),
            "b_name": b_name.strip(),
            "b_name_id": int(b_name_id),
            "market": market.strip(),
            "ir": float(ir),
            "loi": float(loi),
            "f_deliverables": int(f_deliverables),
            "f_currency": f_currency,
            "f_revenue": float(f_revenue),
            "f_cost": float(f_cost),
            "f_nprofit": float(f_nprofit),
            "f_margin": float(f_margin),
            "f_remarks": f_remarks.strip(),
        }

        original_data = {
            "p_name": str(project.get("p_name") or "").strip(),
            "p_manager": str(project.get("p_manager") or "").strip(),
            "p_team": str(project.get("p_team") or "").strip(),
            "p_segment": str(project.get("p_segment") or "").strip(),
            "p_type": str(project.get("p_type") or "").strip(),
            "p_status": str(project.get("p_status") or "").strip(),
            "p_s_date": str(project.get("p_s_date") or ""),
            "p_e_date": (
                str(project.get("p_e_date") or "") if project.get("p_e_date") else None
            ),
            "job_id": str(project.get("job_id") or "").strip(),
            "job_ol_id": str(project.get("job_ol_id") or "").strip(),
            "job_ra_id": str(project.get("job_ra_id") or "").strip(),
            "s_id": str(project.get("s_id") or "").strip(),
            "ta_id": int(project.get("ta_id") or 0),
            "pf_link": str(project.get("pf_link") or "").strip(),
            "b_unit": str(project.get("b_unit") or "").strip(),
            "b_country": str(project.get("b_country") or "").strip(),
            "b_name": str(project.get("b_name") or "").strip(),
            "b_name_id": int(project.get("b_name_id") or 0),
            "market": str(project.get("market") or "").strip(),
            "ir": float(project.get("ir") or 0.0),
            "loi": float(project.get("loi") or 0.0),
            "f_deliverables": int(project.get("f_deliverables") or 0),
            "f_currency": str(project.get("f_currency") or "").strip(),
            "f_revenue": float(project.get("f_revenue") or 0.0),
            "f_cost": float(project.get("f_cost") or 0.0),
            "f_nprofit": float(project.get("f_nprofit") or 0.0),
            "f_margin": float(project.get("f_margin") or 0.0),
            "f_remarks": str(project.get("f_remarks") or "").strip(),
        }

        updates = {}
        for key, new_value in form_data.items():
            old_value = original_data.get(key)
            if old_value != new_value:
                updates[key] = new_value

        if not updates:
            st.info("No changes detected.")
            return

        # only keep changed fields
        changed_updates = {}
        changes = {}

        for key, new_value in updates.items():
            old_value = project.get(key)

            # normalize both sides for comparison
            old_str = "" if old_value is None else str(old_value).strip()
            new_str = "" if new_value is None else str(new_value).strip()

            if old_str != new_str:
                changed_updates[key] = new_value
                changes[key] = {"old": old_value, "new": new_value}

        if not changed_updates:
            st.info("No changes detected.")
            return

        response, success, error_msg = update_project_by_db_id(db_id, changed_updates)

        if success:
            success_msg = f"{p_name} updated successfully! DB ID: {db_id}"

            st.success(success_msg)

            if changes:
                st.markdown("### 🔍 Updated Fields:")
                field_labels = {
                    "p_name": "Project Name",
                    "p_manager": "Project Manager",
                    "p_team": "Project Team",
                    "p_segment": "Project Segment",
                    "p_type": "Project Type",
                    "p_status": "Project Status",
                    "p_s_date": "Start Date",
                    "p_e_date": "End Date",
                    "job_id": "Job ID",
                    "job_ol_id": "Job OL ID",
                    "job_ra_id": "Job RA ID",
                    "s_id": "SID",
                    "ta_id": "TA ID",
                    "pf_link": "Path Folder Link",
                    "b_unit": "Business Unit",
                    "b_country": "Business Country",
                    "b_name": "Business Name",
                    "b_name_id": "Business Name ID",
                    "market": "Market",
                    "ir": "IR",
                    "loi": "LOI",
                    "f_deliverables": "Deliverables",
                    "f_currency": "Currency",
                    "f_revenue": "Revenue",
                    "f_cost": "Cost",
                    "f_nprofit": "Net Profit",
                    "f_margin": "Margin",
                    "f_remarks": "Remarks",
                }

                for field, change in changes.items():
                    label = field_labels.get(field, field)
                    old_val = "None" if change["old"] is None else change["old"]
                    new_val = "None" if change["new"] is None else change["new"]
                    st.markdown(f"- **{label}**: `{old_val}` → `{new_val}`")

            # optional: also save in session state if you still want it after rerun
            st.session_state["update_success"] = True
            st.session_state["success_msg"] = success_msg
            st.session_state["updated_changes"] = changes

        else:
            st.error(f"Project update failed: {error_msg}")


# Delete Project
def delete_project():
    st.header("🗑️ Delete Project")

    db_id = st.text_input("Enter Project DB ID")

    if db_id:
        if not db_id.isdigit():
            st.error("DB ID must be numeric")
            return

        db_id = int(db_id)

        response_data, success = get_project_by_db_id(db_id)

        project = None
        if success and isinstance(response_data, dict):
            project = (
                response_data.get("project")
                or (response_data.get("projects") or [None])[0]
                or response_data.get("data")
            )

        if project:
            st.subheader("📌 Project Details")

            st.write(f"**Name:** {project.get('p_name')}")
            st.write(f"**Manager:** {project.get('p_manager')}")
            st.write(f"**Status:** {project.get('p_status')}")
            st.write(f"**SID:** {project.get('s_id')}")

            st.warning("⚠️ This action cannot be undone.")

            confirm = st.checkbox("Confirm to delete this project")

            if st.button("Delete Project", type="primary"):
                if not confirm:
                    st.error("Please confirm deletion first.")
                    return

            response_data, success = delete_project_by_db_id(db_id)

            if success:
                st.session_state["delete_success"] = True
                st.session_state["delete_msg"] = (
                    f"Project {db_id} deleted successfully!"
                )
                st.rerun()
            else:
                st.error("Failed to delete project")

        else:
            st.info("Project not found")

    if st.session_state.get("delete_success"):
        st.markdown("---")
        st.success(st.session_state.get("delete_msg"))
        st.session_state["delete_success"] = False
        st.session_state["delete_msg"] = ""


# AI Insights
def ai_insights():
    st.header("🤖 AI Project Insights")

    # -----------------------------
    # 🧠 SESSION STATE (Chat Memory)
    # -----------------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # -----------------------------
    # 💬 CHAT UI
    # -----------------------------
    st.subheader("💬 AI Chat Assistant")

    chat_container = st.container()

    with chat_container:
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f"🧑 **You:** {chat['message']}")
            else:
                st.markdown(f"🤖 **AI:** {chat['message']}")

    # Input box (bottom style)
    user_input = st.text_input(
        "Ask anything (projects, managers, or even general questions like weather)"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Send 💬"):
            if user_input:
                # Save user message
                st.session_state.chat_history.append(
                    {"role": "user", "message": user_input}
                )

                # Call AI backend
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/ai/chat/",
                        params={"query": user_input},
                        timeout=30,
                    )

                    if response.status_code == 200:
                        ai_reply = response.json().get(
                            "response", "No response from AI"
                        )
                    else:
                        try:
                            error_detail = response.json().get("detail", response.text)
                        except Exception:
                            error_detail = response.text

                        ai_reply = f"⚠️ AI request failed: {error_detail}"

                except requests.exceptions.RequestException as e:
                    ai_reply = f"⚠️ AI request failed: {str(e)}"

                # Save AI reply
                st.session_state.chat_history.append(
                    {"role": "ai", "message": ai_reply}
                )

                st.rerun()

    with col2:
        if st.button("Clear Chat 🗑️"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")

    # -----------------------------
    # 💡 SUGGESTED PROMPTS
    # -----------------------------
    st.subheader("💡 Try asking:")

    suggestions = [
        "Which manager is underperforming?",
        "Summarize this month's project performance",
        "How many projects started this week?",
        "Show trends by manager",
        "What are potential risks in current projects?",
    ]

    for s in suggestions:
        st.markdown(f"- {s}")

    st.markdown("---")

    # -----------------------------
    # 📊 REPORT GENERATOR
    # -----------------------------
    st.subheader("📊 Manager Performance Report")

    # Load projects (for dropdown)
    projects_data, success = get_all_projects()

    if not success:
        st.error("Failed to load data")
        return

    projects = projects_data.get("projects", [])

    # Extract managers
    manager_list = sorted(list(set(p.get("p_manager", "Unknown") for p in projects)))

    # Show project count beside name
    manager_counts = Counter(p.get("p_manager") for p in projects)

    manager_options = ["All"] + [f"{m} ({manager_counts[m]})" for m in manager_list]

    # Filter UI
    col1, col2 = st.columns(2)

    with col1:
        period = st.selectbox("Select Period", ["daily", "weekly", "monthly", "yearly"])

    with col2:
        selected_manager_display = st.selectbox("Select Manager", manager_options)
        selected_manager = selected_manager_display.split(" (")[0]

    # Generate Report
    if st.button("Generate Report 📄"):
        params = {"period": period}

        if selected_manager != "All":
            params["manager"] = selected_manager

        res = requests.get(f"{API_BASE_URL}/reports/projects", params=params)

        if res.status_code == 200:
            data = res.json()

            st.success(f"📅 {period.capitalize()} Report")

            # Metrics Display
            col1, col2, col3 = st.columns(3)

            col1.metric("📦 Total Projects", data["count"])
            col2.metric("💰 Total Net Profit", f"{data['total_profit']}")
            col3.metric("📊 Avg Margin (%)", f"{data['avg_margin']}%")

            st.markdown(
                f"""**Manager Filter:** {selected_manager if selected_manager else 'All'}"""
            )

            # Extra Info
            st.caption(f"Manager: {selected_manager}")

            # Simple Insight (Nice touch)
            if data["avg_margin"] < 20:
                st.warning("⚠️ Low margin detected — potential profitability issue")

            if data["count"] == 0:
                st.info("No projects found for this selection")

    # -----------------------------
    # 🧠 QUICK AI SUMMARY
    # -----------------------------
    st.subheader("🧠 AI Manager Summary")

    if st.button("Generate AI Summary"):
        try:
            res = requests.get(
                f"{API_BASE_URL}/ai/report", params={"period": "monthly"}, timeout=30
            )

            if res.status_code == 200:
                data = res.json()
                st.success("AI summary generated successfully")
                st.text(data.get("report", "No summary available"))
            else:
                try:
                    error_detail = res.json().get("detail", res.text)
                except Exception:
                    error_detail = res.text

                st.error(f"Failed to generate AI summary: {error_detail}")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to generate AI summary: {str(e)}")


# Display Function
def display_search_results(response_data):
    if not response_data:
        st.info("No results found matching the search criteria.")
        return

    projects = response_data.get("projects", [])

    # def extract_projects(response_data):
    #     if isinstance(response_data, list):
    #         return response_data
    #     if isinstance(response_data, dict):
    #         return response_data.get("projects") or response_data.get("data") or []
    #     return []

    if not projects:
        st.info("No projects found matching the search criteria.")
        return

    st.markdown(f"### Search Results ({len(projects)} projects found)")

    for project in projects:
        created_at = project.get("created_at")
        if created_at:
            try:
                dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                created_at = dt.strftime("%d-%m-%Y, %I:%M:%p")
            except Exception:
                created_at = created_at

        st.markdown(
            f"""
            **{project.get('p_name', 'Unnamed Project')}**
            - SID: {project.get('s_id', 'Unknown')}
            - Status: {project.get('p_status', 'Unknown')}
            - Segment: {project.get('p_segment', 'Unknown')}
            - Type: {project.get('p_type', 'Unknown')}
            - Manager: {project.get('p_manager', 'Unknown')}
            - Start Date: {project.get('p_s_date', 'Unknown')}
            - End Date: {project.get('p_e_date', 'Unknown')}
            - Created At: {created_at or 'Unknown'}
            ---
        """
        )
    else:
        st.info("No projects found matching the search criteria.")


if __name__ == "__main__":
    main()
