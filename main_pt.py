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
        response = requests.delete(f"{API_BASE_URL}/projects/{db_id}", timeout=30)

        if response.status_code == 200:
            return response.json(), True
        elif response.status_code == 404:
            return None, False
        else:
            return None, False

    except requests.exceptions.RequestException:
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
        st.toast("✅ Connected to ProTrack successfully!")
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
    st.header("💼 Project Dashboard")
    st.markdown(
        "A quick overview of project activity, delivery status, and performance trends."
    )

    response_data, success = get_all_projects()

    if not success:
        st.error("Failed to load projects for dashboard.")
        return

    projects = response_data.get("projects", [])

    if not projects:
        st.info("No projects available.")
        return

    # -----------------------------
    # KPI calculations
    # -----------------------------
    total_projects = len(projects)
    completed_projects = sum(
        1 for p in projects if str(p.get("p_status", "")).lower() == "completed"
    )
    active_projects = sum(
        1 for p in projects if str(p.get("p_status", "")).lower() == "field"
    )
    completion_rate = (
        round((completed_projects / total_projects) * 100, 2) if total_projects else 0
    )

    margins = [
        float(p.get("f_margin")) for p in projects if p.get("f_margin") is not None
    ]
    avg_margin = round(sum(margins) / len(margins), 2) if margins else 0

    profits = [
        float(p.get("f_nprofit")) for p in projects if p.get("f_nprofit") is not None
    ]
    total_net_profit = round(sum(profits), 2) if profits else 0

    # -----------------------------
    # KPI Section
    # -----------------------------
    st.subheader("📈 Performance KPIs")

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi4, kpi5, kpi6 = st.columns(3)

    kpi1.metric("📦 Total Projects", total_projects)
    kpi2.metric("✅ Completed", completed_projects)
    kpi3.metric("🚧 Active", active_projects)

    kpi4.metric("📊 Completion Rate", f"{completion_rate}%")
    kpi5.metric("💹 Avg Margin", f"{avg_margin}%")
    kpi6.metric("💰 Total Net Profit", f"{total_net_profit}")

    st.markdown("---")

    # -----------------------------
    # Aggregate data for charts
    # -----------------------------
    status_counts = {}
    manager_counts = {}
    segment_counts = {}
    business_unit_counts = {}
    start_month_counts = {}

    for project in projects:
        status = project.get("p_status", "Unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

        manager = project.get("p_manager", "Unknown")
        manager_counts[manager] = manager_counts.get(manager, 0) + 1

        segment = project.get("p_segment", "Unknown")
        segment_counts[segment] = segment_counts.get(segment, 0) + 1

        business_unit = project.get("b_unit", "Unknown")
        business_unit_counts[business_unit] = (
            business_unit_counts.get(business_unit, 0) + 1
        )

        if project.get("p_s_date"):
            month = str(project.get("p_s_date"))[:7]
            start_month_counts[month] = start_month_counts.get(month, 0) + 1

    status_df = pd.DataFrame(
        [{"Status": k, "Projects": v} for k, v in status_counts.items()]
    ).sort_values("Projects", ascending=False)

    manager_df = pd.DataFrame(
        [{"Manager": k, "Projects": v} for k, v in manager_counts.items()]
    ).sort_values("Projects", ascending=False)

    segment_df = pd.DataFrame(
        [{"Segment": k, "Projects": v} for k, v in segment_counts.items()]
    ).sort_values("Projects", ascending=False)

    business_unit_df = pd.DataFrame(
        [{"Business Unit": k, "Projects": v} for k, v in business_unit_counts.items()]
    ).sort_values("Projects", ascending=False)

    start_month_df = pd.DataFrame(
        [{"Start Month": k, "Projects": v} for k, v in start_month_counts.items()]
    ).sort_values("Start Month", ascending=True)

    # -----------------------------
    # Charts
    # -----------------------------
    st.subheader("📊 Project Distribution")

    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

    with row1_col1:
        st.markdown("#### Projects by Status")
        st.bar_chart(status_df.set_index("Status"), use_container_width=True)

    with row1_col2:
        st.markdown("#### Projects by Manager")
        st.bar_chart(manager_df.set_index("Manager"), use_container_width=True)

    with row1_col3:
        st.markdown("#### Projects by Segment")
        st.bar_chart(segment_df.set_index("Segment"), use_container_width=True)

    with row1_col4:
        st.markdown("#### Projects by Business Unit")
        st.bar_chart(
            business_unit_df.set_index("Business Unit"), use_container_width=True
        )

    st.markdown("#### Projects by Start Month")
    st.line_chart(start_month_df.set_index("Start Month"), use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Latest Projects + Attention Summary
    # -----------------------------
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("🕒 Latest Projects Added")

        recent_projects = sorted(
            projects, key=lambda x: x.get("created_at") or "", reverse=True
        )

        recent_rows = []
        for project in recent_projects[:8]:
            recent_rows.append(
                {
                    "DB ID": project.get("db_id"),
                    "Project Name": project.get("p_name", "Unnamed Project"),
                    "SID": project.get("s_id", "Unknown"),
                    "Manager": project.get("p_manager", "Unknown"),
                    "Status": project.get("p_status", "Unknown"),
                }
            )

        recent_df = pd.DataFrame(recent_rows)

        st.dataframe(
            recent_df,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Tip: Use the DB ID in the Update, Delete, or Search tabs for quick reference."
        )

    with col_right:
        st.subheader("⚠️ Attention Summary")

        active_attention = [
            p for p in projects if str(p.get("p_status", "")).lower() == "field"
        ]

        no_end_date_projects = [p for p in projects if not p.get("p_e_date")]

        low_margin_projects = [
            p
            for p in projects
            if p.get("f_margin") is not None and float(p.get("f_margin", 0)) < 20
        ]

        s1, s2 = st.columns(2)
        s1.metric("Active", len(active_attention))
        s2.metric("No End Date", len(no_end_date_projects))
        st.metric("Low Margin", len(low_margin_projects))

        attention_rows = []
        for project in active_attention[:4]:
            attention_rows.append(
                {
                    "DB ID": project.get("db_id"),
                    "Project Name": project.get("p_name", "Unnamed Project"),
                    "Status": project.get("p_status", "Unknown"),
                }
            )

        if attention_rows:
            attention_df = pd.DataFrame(attention_rows)

            st.markdown("##### Review First")
            st.dataframe(
                attention_df,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No projects currently require attention.")


# Create Project
def create_project_ui():
    st.header("➕ Create New Project")
    st.markdown(
        "Add a new project record with project, operational, business, and financial details."
    )

    with st.form("create_project_form"):
        st.markdown("### 📋 Project Information")
        col1, col2 = st.columns(2)

        with col1:
            p_name = st.text_input(
                "Project Name", max_chars=100, placeholder="Enter project name"
            )
            p_manager = st.text_input(
                "Project Manager", max_chars=100, placeholder="Enter project manager"
            )
            p_team = st.text_input(
                "Project Team", max_chars=100, placeholder="Enter project team"
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

            ir = st.number_input(
                "IR (%)",
                min_value=0.0,
                max_value=100.0,
                value=None,
                placeholder="Enter IR (%)",
            )

        with col2:
            p_type = st.selectbox("Project Type", ["Ad Hoc", "Tracker", "Other"])
            p_status = st.selectbox("Project Status", ["Field", "Completed", "Other"])
            p_s_date = st.date_input("Project Start Date")
            p_e_date = st.date_input("Project End Date")

            loi = st.number_input(
                "LOI (Minutes)",
                min_value=0,
                max_value=999,
                value=None,
                placeholder="Enter LOI",
            )

        st.markdown("---")
        st.markdown("### 🆔 Operational Information")
        col3, col4 = st.columns(2)

        with col3:
            job_id = st.text_input("Job ID", max_chars=12, placeholder="Enter Job ID")
            job_ol_id = st.text_input(
                "Job OL ID", max_chars=15, placeholder="Enter Job OL ID"
            )
            job_ra_id = st.text_input(
                "Job RA ID", max_chars=15, placeholder="Enter Job RA ID"
            )

        with col4:
            s_id = st.text_input("SID", value="S", max_chars=9, placeholder="Enter SID")
            ta_id = st.number_input(
                "TA ID",
                min_value=0,
                max_value=999999,
                value=None,
                placeholder="Enter TA ID",
            )
            pf_link = st.text_input(
                "Folder / Path Link",
                max_chars=200,
                placeholder="Enter folder or path link",
            )

        st.markdown("---")
        st.markdown("### 🏢 Business Information")
        col5, col6 = st.columns(2)

        with col5:
            b_unit = st.text_input(
                "Business Unit",
                max_chars=100,
                placeholder="Enter client company / business unit",
            )
            b_country = st.text_input(
                "Business Country", max_chars=100, placeholder="Enter business country"
            )

        with col6:
            b_name = st.text_input(
                "Business Name",
                max_chars=100,
                placeholder="Enter client / business name",
            )
            b_name_id = st.number_input(
                "Business Name ID",
                min_value=0,
                max_value=999999,
                value=None,
                placeholder="Enter Symphony / client ID",
            )

        st.markdown("---")
        st.markdown("### 💰 Financial Information")
        col7, col8 = st.columns(2)

        with col7:
            f_deliverables = st.number_input(
                "Final Deliverables",
                min_value=0,
                max_value=99999,
                value=None,
                placeholder="Enter final deliverables",
            )
            f_currency = (
                st.text_input(
                    "Final Currency", max_chars=3, placeholder="E.g. AUD / USD / MYR"
                )
                .strip()
                .upper()
            )
            f_revenue = st.number_input(
                "Fieldwork Revenue",
                min_value=0.0,
                max_value=999999999.0,
                value=None,
                placeholder="Enter revenue",
            )

        with col8:
            f_cost = st.number_input(
                "Fieldwork Cost",
                min_value=0.0,
                max_value=999999999.0,
                value=None,
                placeholder="Enter cost / incentive",
            )

            auto_nprofit = None
            if f_revenue is not None and f_cost is not None:
                auto_nprofit = round(float(f_revenue) - float(f_cost), 2)

            f_nprofit = st.number_input(
                "Fieldwork Net Profit",
                min_value=0.0,
                max_value=999999999.0,
                value=auto_nprofit if auto_nprofit is not None else None,
                placeholder="Auto-calculated if revenue and cost are filled",
            )

            margin_band = st.selectbox(
                "Margin Band", ["0%", "1-19%", "20-49%", "50-79%", "80-100%"]
            )
        f_remarks = st.text_area(
            "Fieldwork Remarks", max_chars=500, placeholder="Enter remarks or notes"
        )

        st.markdown("---")
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
            st.error("Job ID is required.")
            return
        if not job_ol_id or not job_ol_id.strip():
            st.error("Job OL ID is required.")
            return
        if not job_ra_id or not job_ra_id.strip():
            st.error("Job RA ID is required.")
            return
        if not s_id or not s_id.strip():
            st.error("SID is required.")
            return
        if ta_id is None:
            st.error("TA ID is required.")
            return
        if not pf_link or not pf_link.strip():
            st.error("Folder / Path Link is required.")
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
            ir_val = float(ir) if str(ir).strip() else None
        except ValueError:
            st.error("IR must be a number.")
            return

        try:
            loi_val = float(loi) if str(loi).strip() else None
        except ValueError:
            st.error("LOI must be a number.")
            return

        margin_map = {"0%": 0, "1-19%": 10, "20-49%": 30, "50-79%": 60, "80-100%": 90}

        final_nprofit = auto_nprofit if auto_nprofit is not None else f_nprofit

        new_project = {
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
            "ta_id": int(ta_id_val),
            "pf_link": pf_link.strip(),
            "b_unit": b_unit.strip(),
            "b_country": b_country.strip(),
            "b_name": b_name.strip(),
            "b_name_id": int(b_name_id_val),
            "market": market.strip(),
            "ir": float(ir_val),
            "loi": float(loi_val),
            "f_deliverables": f_deliverables,
            "f_currency": f_currency,
            "f_revenue": f_revenue,
            "f_cost": f_cost,
            "f_nprofit": final_nprofit,
            "f_margin": margin_map.get(margin_band, 0.0),
            "f_remarks": f_remarks.strip(),
        }

        response, success, error_msg = create_project_api(new_project)

        if success:
            st.session_state["success_msg"] = (
                f"Project '{p_name}' created successfully! "
                f"DB ID: {response['db_id']} | SID: {s_id} | Manager: {p_manager}"
            )
            st.rerun()
        else:
            st.error(f"Failed to create project: {error_msg}")

    if "success_msg" in st.session_state:
        st.markdown("---")
        st.success(st.session_state["success_msg"])
        del st.session_state["success_msg"]

    st.caption(
        "Tip: Revenue and Cost will automatically suggest Net Profit where possible."
    )


# Search Projects
def search_projects():
    st.header("🔍 Project Directory")
    st.markdown("Browse all projects or refine the list using search criteria below.")

    with st.container(border=True):
        st.markdown("### Filter Projects")

        search_criteria = st.selectbox(
            "Search Type",
            [
                "All Projects",
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

        response_data = None
        success = False
        search_clicked = False

        # Default: show all projects
        if search_criteria == "All Projects":
            response_data, success = get_all_projects()

        elif search_criteria == "Project Name Keyword":
            keyword = st.text_input(
                "Project Name Keyword",
                max_chars=100,
                placeholder="Enter keyword to search in project names",
            )
            search_clicked = st.button("Apply Filter", key="search_name_keyword")
            if search_clicked:
                response_data, success = get_projects_by_name_keyword(keyword)

        elif search_criteria == "Project SID":
            sid = st.text_input(
                "Project SID",
                max_chars=20,
                placeholder="Enter project SID",
            )
            search_clicked = st.button("Apply Filter", key="search_sid")
            if search_clicked:
                response_data, success = get_projects_by_sid(sid)

        elif search_criteria == "Project Segment":
            segment = st.selectbox(
                "Project Segment",
                [
                    "Full Service",
                    "Sample Only",
                    "Sample Only (External)",
                    "Coverage",
                    "Other",
                ],
            )
            search_clicked = st.button("Apply Filter", key="search_segment")
            if search_clicked:
                response_data, success = get_projects_by_segment(segment)

        elif search_criteria == "Project Type":
            p_type = st.selectbox(
                "Project Type",
                ["Tracker", "Ad Hoc", "Other"],
            )
            search_clicked = st.button("Apply Filter", key="search_type")
            if search_clicked:
                response_data, success = get_projects_by_type(p_type)

        elif search_criteria == "Project TA ID":
            ta_id = st.text_input(
                "Project TA ID",
                max_chars=10,
                placeholder="Enter project TA ID",
            )
            search_clicked = st.button("Apply Filter", key="search_ta_id")
            if search_clicked:
                response_data, success = get_projects_by_ta_id(ta_id)

        elif search_criteria == "Project Job ID":
            job_id = st.text_input(
                "Project Job ID",
                max_chars=20,
                placeholder="Enter project Job ID",
            )
            search_clicked = st.button("Apply Filter", key="search_job_id")
            if search_clicked:
                response_data, success = get_projects_by_job_id(job_id)

        elif search_criteria == "Project Job OL ID":
            job_ol_id = st.text_input(
                "Project Job OL ID",
                max_chars=20,
                placeholder="Enter project Job OL ID",
            )
            search_clicked = st.button("Apply Filter", key="search_job_ol_id")
            if search_clicked:
                response_data, success = get_projects_by_job_ol_id(job_ol_id)

        elif search_criteria == "Project Job RA ID":
            job_ra_id = st.text_input(
                "Project Job RA ID",
                max_chars=20,
                placeholder="Enter project Job RA ID",
            )
            search_clicked = st.button("Apply Filter", key="search_job_ra_id")
            if search_clicked:
                response_data, success = get_projects_by_job_ra_id(job_ra_id)

        elif search_criteria == "Project Status":
            status = st.selectbox(
                "Project Status",
                ["Field", "Completed", "Other"],
            )
            search_clicked = st.button("Apply Filter", key="search_status")
            if search_clicked:
                response_data, success = get_projects_by_status(status)

        elif search_criteria == "Project Manager":
            manager = st.text_input(
                "Project Manager",
                max_chars=100,
                placeholder="Enter project manager name",
            )
            search_clicked = st.button("Apply Filter", key="search_manager")
            if search_clicked:
                response_data, success = get_projects_by_manager(manager)

        elif search_criteria == "Project Business Unit":
            b_unit = st.text_input(
                "Business Unit",
                max_chars=100,
                placeholder="Enter business unit",
            )
            search_clicked = st.button("Apply Filter", key="search_business_unit")
            if search_clicked:
                response_data, success = get_projects_by_business_unit(b_unit)

        elif search_criteria == "Project Business Country":
            b_country = st.text_input(
                "Business Country",
                max_chars=100,
                placeholder="Enter business country",
            )
            search_clicked = st.button("Apply Filter", key="search_business_country")
            if search_clicked:
                response_data, success = get_projects_by_business_country(b_country)

        elif search_criteria == "Project Business Name":
            b_name = st.text_input(
                "Business Name",
                max_chars=100,
                placeholder="Enter business name",
            )
            search_clicked = st.button("Apply Filter", key="search_business_name")
            if search_clicked:
                response_data, success = get_projects_by_business_name(b_name)

        elif search_criteria == "Project Margin Band":
            f_margin_band = st.selectbox(
                "Margin Band",
                ["0%", "1-19%", "20-49%", "50-79%", "80-100%"],
            )
            search_clicked = st.button("Apply Filter", key="search_margin_band")
            if search_clicked:
                response_data, success = get_projects_by_margin_band(f_margin_band)

        elif search_criteria == "Project Date Filter":
            col1, col2 = st.columns(2)
            with col1:
                month = st.selectbox(
                    "Month",
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
                year = st.text_input(
                    "Year",
                    max_chars=4,
                    placeholder="E.g. 2026",
                )

            search_clicked = st.button("Apply Filter", key="search_date")

            if search_clicked:
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
                    month=month_number,
                    year=year_number,
                )

    st.markdown("")

    # Show all projects by default
    if search_criteria == "All Projects":
        if success:
            display_search_results(response_data, mode="all")
        else:
            st.error("Failed to retrieve projects. Please try again later.")

    # Show filtered results only after button click
    else:
        if search_clicked:
            if success:
                display_search_results(response_data, mode="search")
            else:
                st.error(
                    "No projects found matching the selected criteria. Please try a different value."
                )
        else:
            st.info(
                "Select a search type, enter a value if needed, and click 'Apply Filter'."
            )


# Display Search Results
def display_search_results(response_data, mode="search"):
    if not response_data:
        st.info("No results found matching the search criteria.")
        return

    projects = response_data.get("projects", [])

    if not projects:
        st.info("No projects found matching the search criteria.")
        return

    # -----------------------------
    # Build compact table data
    # -----------------------------
    table_rows = []
    for project in projects:
        table_rows.append(
            {
                "DB ID": project.get("db_id"),
                "Project Name": project.get("p_name", "Unnamed Project"),
                "SID": project.get("s_id", "Unknown"),
            }
        )

    df = pd.DataFrame(table_rows)

    # -----------------------------
    # Header
    # -----------------------------
    title = "All Projects" if mode == "all" else "Search Results"
    st.markdown(f"### {title} ({len(df)} projects)")

    # -----------------------------
    # Toolbar: keyword filter + sort + page size
    # -----------------------------
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        keyword = st.text_input(
            "Filter by keyword",
            placeholder="Search by project name, DB ID, or SID",
            key=f"{mode}_project_keyword",
        ).strip()

    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["DB ID", "Project Name", "SID"],
            key=f"{mode}_project_sort_by",
        )

    with col3:
        page_size = st.selectbox(
            "Projects per page",
            [10, 20, 30, 50],
            index=1,
            key=f"{mode}_project_page_size",
        )

    # -----------------------------
    # Apply filter
    # -----------------------------
    if keyword:
        keyword_lower = keyword.lower()
        df = df[
            df["Project Name"]
            .astype(str)
            .str.lower()
            .str.contains(keyword_lower, na=False)
            | df["SID"].astype(str).str.lower().str.contains(keyword_lower, na=False)
            | df["DB ID"].astype(str).str.lower().str.contains(keyword_lower, na=False)
        ]

    if df.empty:
        st.info("No projects found for the current filter.")
        return

    # -----------------------------
    # Sort controls
    # -----------------------------
    col4, col5 = st.columns([1, 3])

    with col4:
        sort_order = st.radio(
            "Order",
            ["Ascending", "Descending"],
            horizontal=True,
            key=f"{mode}_project_sort_order",
        )

    ascending = sort_order == "Ascending"
    df = df.sort_values(by=sort_by, ascending=ascending).reset_index(drop=True)

    # -----------------------------
    # Pagination
    # -----------------------------
    total_rows = len(df)
    total_pages = max(1, (total_rows + page_size - 1) // page_size)

    page_key = f"{mode}_project_page"
    if page_key not in st.session_state:
        st.session_state[page_key] = 1

    if st.session_state[page_key] > total_pages:
        st.session_state[page_key] = total_pages

    nav1, nav2, nav3, nav4 = st.columns([1, 1, 1, 2])

    with nav1:
        if st.button(
            "◀ Prev", key=f"{mode}_prev_page", disabled=st.session_state[page_key] <= 1
        ):
            st.session_state[page_key] -= 1
            st.rerun()

    with nav2:
        if st.button(
            "Next ▶",
            key=f"{mode}_next_page",
            disabled=st.session_state[page_key] >= total_pages,
        ):
            st.session_state[page_key] += 1
            st.rerun()

    with nav3:
        page_number = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=st.session_state[page_key],
            step=1,
            key=f"{mode}_page_number_input",
        )
        if page_number != st.session_state[page_key]:
            st.session_state[page_key] = page_number
            st.rerun()

    with nav4:
        start_item = (st.session_state[page_key] - 1) * page_size + 1
        end_item = min(st.session_state[page_key] * page_size, total_rows)
        st.caption(f"Showing {start_item}–{end_item} of {total_rows} projects")

    start_idx = (st.session_state[page_key] - 1) * page_size
    end_idx = start_idx + page_size
    page_df = df.iloc[start_idx:end_idx].copy()

    # -----------------------------
    # Display compact table
    # -----------------------------
    st.dataframe(
        page_df,
        use_container_width=True,
        hide_index=True,
    )

    # -----------------------------
    # Optional quick help
    # -----------------------------
    with st.expander("Tips", expanded=False):
        st.markdown(
            """
            - Use the keyword filter to search by **Project Name**, **DB ID**, or **SID**  
            - Sort by **DB ID** to quickly find newest or oldest records  
            - Adjust **Projects per page** (20–30 recommended) for easier browsing  
            - Combine filters and sorting to narrow down results efficiently  
            """
        )


# Update Project
def update_project():
    st.header("✏️ Update Project")
    st.markdown(
        "Enter the Database ID to load a project, then choose which section you would like to update."
    )

    db_id_input = st.text_input(
        "Enter Database ID of the project to update",
        max_chars=10,
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
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("### 📋 Project Information")
            st.markdown(f"**DB ID:** {project.get('db_id')}")
            st.markdown(f"**Project Name:** {project.get('p_name')}")
            st.markdown(f"**Project Manager:** {project.get('p_manager')}")
            st.markdown(f"**Project Team:** {project.get('p_team')}")
            st.markdown(f"**Segment:** {project.get('p_segment')}")
            st.markdown(f"**Type:** {project.get('p_type')}")
            st.markdown(f"**Status:** {project.get('p_status')}")
            st.markdown(f"**IR:** {project.get('ir')}")
            st.markdown(f"**LOI:** {project.get('loi')}")

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
            st.markdown("### 🏢 Business Details")
            st.markdown(f"**Business Unit:** {project.get('b_unit')}")
            st.markdown(f"**Business Country:** {project.get('b_country')}")
            st.markdown(f"**Business Name:** {project.get('b_name')}")
            st.markdown(f"**Business Name ID:** {project.get('b_name_id')}")
            st.markdown(f"**Market:** {project.get('market')}")

        with col4:
            st.markdown("### 💰 Financial Details")
            st.markdown(f"**Final Deliverables:** {project.get('f_deliverables')}")
            st.markdown(f"**Final Currency:** {project.get('f_currency')}")
            st.markdown(f"**Revenue:** {project.get('f_revenue')}")
            st.markdown(f"**Cost:** {project.get('f_cost')}")
            st.markdown(f"**Net Profit:** {project.get('f_nprofit')}")
            st.markdown(f"**Margin:** {project.get('f_margin')}")
            st.markdown(f"**Remarks:** {project.get('f_remarks')}")

    st.markdown("---")
    st.subheader("Choose Section to Update")

    section_to_update = st.selectbox(
        "Update Section",
        [
            "Project Information",
            "Operational Details",
            "Business Details",
            "Financial Details",
        ],
    )

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
        updates = {}

        if section_to_update == "Project Information":
            st.markdown("### 📋 Edit Project Information")

            p_name = st.text_input(
                "Project Name",
                value=project.get("p_name", ""),
                key=f"update_p_name_{db_id}",
            )
            p_manager = st.text_input(
                "Project Manager",
                value=project.get("p_manager", ""),
                key=f"update_p_manager_{db_id}",
            )
            p_team = st.text_input(
                "Project Team",
                value=project.get("p_team", ""),
                key=f"update_p_team_{db_id}",
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
                key=f"update_p_segment_{db_id}",
            )
            p_type = st.selectbox(
                "Project Type",
                ["Ad Hoc", "Tracker", "Other"],
                index=(
                    ["Ad Hoc", "Tracker", "Other"].index(project.get("p_type", "Other"))
                    if project.get("p_type", "Other") in ["Ad Hoc", "Tracker", "Other"]
                    else 2
                ),
                key=f"update_p_type_{db_id}",
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
                key=f"update_p_status_{db_id}",
            )
            ir = st.number_input(
                "IR (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(project.get("ir") or 0.0),
                step=0.1,
                key=f"update_ir_{db_id}",
            )
            loi = st.number_input(
                "LOI (Minutes)",
                min_value=0.0,
                value=float(project.get("loi") or 0.0),
                step=0.1,
                key=f"update_loi_{db_id}",
            )

            updates = {
                "p_name": p_name.strip(),
                "p_manager": p_manager.strip(),
                "p_team": p_team.strip(),
                "p_segment": p_segment,
                "p_type": p_type,
                "p_status": p_status,
                "ir": float(ir),
                "loi": float(loi),
            }

        elif section_to_update == "Operational Details":
            st.markdown("### 🆔 Edit Operational Details")

            p_s_date = st.date_input(
                "Project Start Date",
                value=original_start_date,
                key=f"update_p_s_date_{db_id}",
            )
            p_e_date = st.date_input(
                "Project End Date",
                value=original_end_date,
                key=f"update_p_e_date_{db_id}",
            )
            job_id = st.text_input(
                "Job ID",
                value=str(project.get("job_id") or ""),
                key=f"update_job_id_{db_id}",
            )
            job_ol_id = st.text_input(
                "Job OL ID",
                value=str(project.get("job_ol_id") or ""),
                key=f"update_job_ol_id_{db_id}",
            )
            job_ra_id = st.text_input(
                "Job RA ID",
                value=str(project.get("job_ra_id") or ""),
                key=f"update_job_ra_id_{db_id}",
            )
            s_id = st.text_input(
                "SID",
                value=str(project.get("s_id") or ""),
                key=f"update_s_id_{db_id}",
            )
            ta_id = st.number_input(
                "TA ID",
                min_value=0,
                value=int(project.get("ta_id") or 0),
                step=1,
                key=f"update_ta_id_{db_id}",
            )
            pf_link = st.text_input(
                "Path Folder Link",
                value=str(project.get("pf_link") or ""),
                key=f"update_pf_link_{db_id}",
            )

            updates = {
                "p_s_date": p_s_date.isoformat() if p_s_date else None,
                "p_e_date": p_e_date.isoformat() if p_e_date else None,
                "job_id": job_id.strip(),
                "job_ol_id": job_ol_id.strip(),
                "job_ra_id": job_ra_id.strip(),
                "s_id": s_id.strip(),
                "ta_id": int(ta_id),
                "pf_link": pf_link.strip(),
            }

        elif section_to_update == "Business Details":
            st.markdown("### 🏢 Edit Business Details")

            b_unit = st.text_input(
                "Business Unit",
                value=str(project.get("b_unit") or ""),
                key=f"update_b_unit_{db_id}",
            )
            b_country = st.text_input(
                "Business Country",
                value=str(project.get("b_country") or ""),
                key=f"update_b_country_{db_id}",
            )
            b_name = st.text_input(
                "Business Name",
                value=str(project.get("b_name") or ""),
                key=f"update_b_name_{db_id}",
            )
            b_name_id = st.number_input(
                "Business Name ID",
                min_value=0,
                value=int(project.get("b_name_id") or 0),
                step=1,
                key=f"update_b_name_id_{db_id}",
            )
            market = st.text_input(
                "Market",
                value=str(project.get("market") or ""),
                key=f"update_market_{db_id}",
            )

            updates = {
                "b_unit": b_unit.strip(),
                "b_country": b_country.strip(),
                "b_name": b_name.strip(),
                "b_name_id": int(b_name_id),
                "market": market.strip(),
            }

        elif section_to_update == "Financial Details":
            st.markdown("### 💰 Edit Financial Details")

            f_deliverables = st.number_input(
                "Final Deliverables",
                min_value=0,
                value=int(project.get("f_deliverables") or 0),
                step=1,
                key=f"update_f_deliverables_{db_id}",
            )
            f_currency = (
                st.text_input(
                    "Final Currency",
                    value=str(project.get("f_currency") or ""),
                    key=f"update_f_currency_{db_id}",
                )
                .strip()
                .upper()
            )
            f_revenue = st.number_input(
                "Fieldwork Revenue",
                min_value=0.0,
                value=float(project.get("f_revenue") or 0.0),
                step=0.01,
                key=f"update_f_revenue_{db_id}",
            )
            f_cost = st.number_input(
                "Fieldwork Cost",
                min_value=0.0,
                value=float(project.get("f_cost") or 0.0),
                step=0.01,
                key=f"update_f_cost_{db_id}",
            )
            f_nprofit = st.number_input(
                "Fieldwork Net Profit",
                min_value=0.0,
                value=float(project.get("f_nprofit") or 0.0),
                step=0.01,
                key=f"update_f_nprofit_{db_id}",
            )
            f_margin = st.number_input(
                "Final Margin (%)",
                min_value=0.0,
                value=float(project.get("f_margin") or 0.0),
                step=0.1,
                key=f"update_f_margin_{db_id}",
            )
            f_remarks = st.text_area(
                "Fieldwork Remarks",
                value=str(project.get("f_remarks") or ""),
                key=f"update_f_remarks_{db_id}",
            )

            updates = {
                "f_deliverables": int(f_deliverables),
                "f_currency": f_currency,
                "f_revenue": float(f_revenue),
                "f_cost": float(f_cost),
                "f_nprofit": float(f_nprofit),
                "f_margin": float(f_margin),
                "f_remarks": f_remarks.strip(),
            }

        submit_update = st.form_submit_button("Update Project", type="primary")

    if submit_update:
        if (
            section_to_update == "Operational Details"
            and updates.get("p_e_date")
            and updates.get("p_s_date")
            and updates["p_e_date"] < updates["p_s_date"]
        ):
            st.error("Project End Date cannot be before Start Date.")
            return

        original_data = {
            "p_name": str(project.get("p_name") or "").strip(),
            "p_manager": str(project.get("p_manager") or "").strip(),
            "p_team": str(project.get("p_team") or "").strip(),
            "p_segment": str(project.get("p_segment") or "").strip(),
            "p_type": str(project.get("p_type") or "").strip(),
            "p_status": str(project.get("p_status") or "").strip(),
            "ir": float(project.get("ir") or 0.0),
            "loi": float(project.get("loi") or 0.0),
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
            "f_deliverables": int(project.get("f_deliverables") or 0),
            "f_currency": str(project.get("f_currency") or "").strip(),
            "f_revenue": float(project.get("f_revenue") or 0.0),
            "f_cost": float(project.get("f_cost") or 0.0),
            "f_nprofit": float(project.get("f_nprofit") or 0.0),
            "f_margin": float(project.get("f_margin") or 0.0),
            "f_remarks": str(project.get("f_remarks") or "").strip(),
        }

        changed_updates = {}
        changes = {}

        for key, new_value in updates.items():
            old_value = original_data.get(key)

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
            success_msg = f"{project.get('p_name', 'Project')} updated successfully! DB ID: {db_id}"
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
                    "ir": "IR",
                    "loi": "LOI",
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

            st.session_state["update_success"] = True
            st.session_state["success_msg"] = success_msg
            st.session_state["updated_changes"] = changes

        else:
            st.error(f"Project update failed: {error_msg}")


# Delete Project
def delete_project():
    st.header("🗑️ Delete Project")
    st.markdown("Enter the Database ID to review a project before deletion.")

    if "delete_review_mode" not in st.session_state:
        st.session_state["delete_review_mode"] = False
    if "delete_target_id" not in st.session_state:
        st.session_state["delete_target_id"] = None
    if "delete_success" not in st.session_state:
        st.session_state["delete_success"] = False
    if "delete_msg" not in st.session_state:
        st.session_state["delete_msg"] = ""

    db_id_input = st.text_input(
        "Database ID",
        max_chars=10,
        placeholder="Enter project DB ID",
    )

    if st.session_state.get("delete_success"):
        st.success(st.session_state.get("delete_msg", "Project deleted successfully!"))
        st.session_state["delete_success"] = False
        st.session_state["delete_msg"] = ""

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

    st.markdown("### Project Preview")

    with st.container(border=True):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"#### {project.get('p_name', 'Unnamed Project')}")
            st.markdown(f"**Project Manager:** {project.get('p_manager', '-')}")
            st.markdown(f"**Status:** {project.get('p_status', '-')}")
            st.markdown(f"**Segment:** {project.get('p_segment', '-')}")
            st.markdown(f"**Business Name:** {project.get('b_name', '-')}")
            st.markdown(f"**Market:** {project.get('market', '-')}")

        with col2:
            st.markdown(f"**DB ID:** {project.get("db_id", "-")}")
            st.markdown(f"**SID:** {project.get('s_id', '-')}")
            st.markdown(f"**Start Date:** {project.get('p_s_date', '-')}")
            st.markdown(f"**End Date:** {project.get('p_e_date', '-')}")

    st.markdown("")

    if (
        not st.session_state["delete_review_mode"]
        or st.session_state["delete_target_id"] != db_id
    ):
        col1, col2 = st.columns([1, 3])

        with col1:
            if st.button("Review Deletion", type="primary"):
                st.session_state["delete_review_mode"] = True
                st.session_state["delete_target_id"] = db_id
                st.rerun()

    if (
        st.session_state.get("delete_review_mode")
        and st.session_state.get("delete_target_id") == db_id
    ):
        st.warning(
            f"You are about to permanently delete **{project.get('p_name', 'this project')}** "
            f"(DB ID: **{project.get('db_id')}**). This action cannot be undone."
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Confirm Delete", type="primary"):
                response_delete, delete_success = delete_project_by_db_id(db_id)

                if delete_success:
                    st.session_state["delete_success"] = True
                    st.session_state["delete_msg"] = (
                        f"Project '{project.get('p_name', db_id)}' deleted successfully."
                    )
                    st.session_state["delete_review_mode"] = False
                    st.session_state["delete_target_id"] = None
                    st.rerun()
                else:
                    st.error("Failed to delete project.")

        with col2:
            if st.button("Cancel"):
                st.session_state["delete_review_mode"] = False
                st.session_state["delete_target_id"] = None
                st.rerun()


# AI Insights
# def ai_insights():
#     st.header("🤖 AI Insights")
#     st.markdown(
#         "Explore project performance, manager-level trends, and AI-generated summaries."
#     )

#     # -----------------------------
#     # Session State Initialisation
#     # -----------------------------
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     if "ai_prefill" not in st.session_state:
#         st.session_state["ai_prefill"] = ""

#     projects_data, success = get_all_projects()

#     if not success:
#         st.error("Failed to load data")
#         return

#     projects = projects_data.get("projects", [])

#     # -----------------------------
#     # AI Snapshot
#     # -----------------------------
#     st.subheader("🧠 AI Snapshot")

#     total_projects = len(projects)
#     completed_projects = sum(
#         1 for p in projects if str(p.get("p_status", "")).lower() == "completed"
#     )
#     active_projects = sum(
#         1 for p in projects if str(p.get("p_status", "")).lower() == "field"
#     )
#     completion_rate = (
#         round((completed_projects / total_projects) * 100, 2) if total_projects else 0
#     )

#     margins = [
#         float(p.get("f_margin")) for p in projects if p.get("f_margin") is not None
#     ]
#     avg_margin = round(sum(margins) / len(margins), 2) if margins else 0

#     manager_counts_snapshot = Counter(p.get("p_manager", "Unknown") for p in projects)
#     top_manager = (
#         max(manager_counts_snapshot, key=manager_counts_snapshot.get)
#         if manager_counts_snapshot
#         else "N/A"
#     )

#     snap1, snap2, snap3, snap4 = st.columns(4)
#     snap1.metric("📦 Total Projects", total_projects)
#     snap2.metric("✅ Completed", completed_projects)
#     snap3.metric("🚧 Active", active_projects)
#     snap4.metric("📊 Completion Rate", f"{completion_rate}%")

#     insight_col1, insight_col2 = st.columns(2)

#     with insight_col1:
#         if active_projects > completed_projects:
#             st.warning(
#                 "⚠️ Active projects currently exceed completed projects, which may indicate delivery backlog."
#             )
#         else:
#             st.success("✅ Completed projects are keeping pace with active workload.")

#     with insight_col2:
#         if avg_margin < 20:
#             st.warning(
#                 f"⚠️ Average margin is {avg_margin}%, which may require profitability review."
#             )
#         else:
#             st.success(f"💹 Average margin is {avg_margin}%, which looks healthy.")

#     st.caption(f"Top workload currently sits with: {top_manager}")

#     st.markdown("---")

#     # -----------------------------
#     # Smart Actions
#     # -----------------------------
#     st.subheader("💡 Smart Actions")
#     st.caption("Quick prompts to explore common project insights.")

#     suggestions = [
#         "Summarise monthly project performance",
#         "Analyse performance trends by manager",
#         "Identify underperforming managers",
#         "Show projects with low profit margins",
#         "Highlight potential project risks",
#         "Projects initiated this week",
#     ]

#     # Left-aligned layout (2 columns + empty space)
#     col_left, col_right, _ = st.columns([1, 1, 2])

#     for i, suggestion in enumerate(suggestions):
#         target_col = col_left if i % 2 == 0 else col_right

#         with target_col:
#             if st.button(suggestion, key=f"suggestion_{i}"):

#                 # Save user message
#                 st.session_state.chat_history.append(
#                     {"role": "user", "message": suggestion}
#                 )

#                 # Call AI backend
#                 try:
#                     response = requests.post(
#                         f"{API_BASE_URL}/ai/chat/",
#                         params={"query": suggestion},
#                         timeout=30,
#                     )

#                     if response.status_code == 200:
#                         ai_reply = response.json().get(
#                             "response", "No response from AI"
#                         )
#                     else:
#                         try:
#                             error_detail = response.json().get("detail", response.text)
#                         except Exception:
#                             error_detail = response.text

#                         ai_reply = f"⚠️ AI request failed: {error_detail}"

#                 except requests.exceptions.RequestException as e:
#                     ai_reply = f"⚠️ AI request failed: {str(e)}"

#                 # Save AI reply
#                 st.session_state.chat_history.append(
#                     {"role": "ai", "message": ai_reply}
#                 )

#                 st.rerun()

#     st.markdown("---")

#     # -----------------------------
#     # Chat UI
#     # -----------------------------
#     st.subheader("💬 AI Chat Assistant")

#     chat_container = st.container()

#     with chat_container:
#         for chat in st.session_state.chat_history:
#             if chat["role"] == "user":
#                 st.markdown(f"🧑 **You:** {chat['message']}")
#             else:
#                 st.markdown(f"🤖 **AI:** {chat['message']}")

#     user_input = st.text_input(
#         "Ask about projects, managers, performance insights, or general queries.",
#         value=st.session_state.get("ai_prefill", ""),
#         placeholder="E.g. Summarise current project performance",
#         key="ai_chat_input",
#     )

#     st.session_state["ai_prefill"] = ""

#     col1, col2 = st.columns([1, 1])

#     with col1:
#         if st.button("Send 💬"):
#             if user_input:
#                 # Save user message
#                 st.session_state.chat_history.append(
#                     {"role": "user", "message": user_input}
#                 )

#                 # Call AI backend
#                 try:
#                     response = requests.post(
#                         f"{API_BASE_URL}/ai/chat/",
#                         params={"query": user_input},
#                         timeout=30,
#                     )

#                     if response.status_code == 200:
#                         ai_reply = response.json().get(
#                             "response", "No response from AI"
#                         )
#                     else:
#                         try:
#                             error_detail = response.json().get("detail", response.text)
#                         except Exception:
#                             error_detail = response.text

#                         if "GEMINI_API_KEY is not set" in str(error_detail):
#                             ai_reply = (
#                                 "⚠️ AI assistant is not available yet because GEMINI_API_KEY is not set. "
#                                 "Please add your Gemini API key to enable general AI questions like weather."
#                             )
#                         elif "WEATHERAPI_KEY is not set" in str(error_detail):
#                             ai_reply = (
#                                 "⚠️ Live weather is not available yet because WEATHERAPI_KEY is not set. "
#                                 "Please add your weather API key to enable weather queries."
#                             )
#                         else:
#                             ai_reply = f"⚠️ AI request failed: {error_detail}"

#                 except requests.exceptions.RequestException as e:
#                     ai_reply = f"⚠️ AI request failed: {str(e)}"

#                 # Save AI reply
#                 st.session_state.chat_history.append(
#                     {"role": "ai", "message": ai_reply}
#                 )

#                 st.rerun()

#     with col2:
#         if st.button("Clear Chat 🗑️"):
#             st.session_state.chat_history = []
#             st.rerun()

#     st.markdown("---")

#     # -----------------------------
#     # Manager Performance Report
#     # -----------------------------
#     st.subheader("📊 Manager Performance Report")

#     manager_list = sorted(list(set(p.get("p_manager", "Unknown") for p in projects)))
#     manager_counts = Counter(p.get("p_manager") for p in projects)
#     manager_options = ["All"] + [f"{m} ({manager_counts[m]})" for m in manager_list]

#     col1, col2 = st.columns(2)

#     with col1:
#         period = st.selectbox("Select Period", ["daily", "weekly", "monthly", "yearly"])

#     with col2:
#         selected_manager_display = st.selectbox("Select Manager", manager_options)
#         selected_manager = selected_manager_display.split(" (")[0]

#     if st.button("Generate Report 📄"):
#         try:
#             params = {"period": period}

#             if selected_manager != "All":
#                 params["manager"] = selected_manager

#             res = requests.get(
#                 f"{API_BASE_URL}/reports/projects", params=params, timeout=30
#             )

#             if res.status_code == 200:
#                 data = res.json()

#                 st.success(f"📅 {period.capitalize()} Report")

#                 col1, col2, col3 = st.columns(3)
#                 col1.metric("📦 Total Projects", data.get("count", 0))
#                 col2.metric("💰 Total Net Profit", f"{data.get('total_profit', 0)}")
#                 col3.metric("📊 Avg Margin (%)", f"{data.get('avg_margin', 0)}%")

#                 st.markdown(f"**Manager Filter:** {selected_manager}")
#                 st.caption(f"Period: {period.capitalize()}")

#                 if data.get("count", 0) == 0:
#                     st.info("No projects found for this selection.")
#                 else:
#                     if data.get("avg_margin", 0) < 20:
#                         st.warning(
#                             "⚠️ Low margin detected — potential profitability issue"
#                         )

#                     st.markdown("### Matching Projects")
#                     for project in data.get("projects", []):
#                         with st.container(border=True):
#                             st.markdown(
#                                 f"**{project.get('p_name', 'Unnamed Project')}**"
#                             )
#                             st.caption(
#                                 f"DB ID: {project.get('db_id')} | "
#                                 f"Manager: {project.get('p_manager')} | "
#                                 f"Status: {project.get('p_status')}"
#                             )
#                             st.markdown(
#                                 f"Start Date: {project.get('p_s_date')}  \n"
#                                 f"Created At: {project.get('created_at')}"
#                             )

#             else:
#                 try:
#                     error_detail = res.json().get("detail", res.text)
#                 except Exception:
#                     error_detail = res.text

#                 st.error(f"Failed to generate report: {error_detail}")

#         except requests.exceptions.RequestException as e:
#             st.error(f"Failed to generate report: {str(e)}")

#     st.markdown("---")

#     # -----------------------------
#     # AI Manager Summary
#     # -----------------------------
#     st.subheader("🧠 AI Manager Summary")

#     col1, col2 = st.columns(2)

#     with col1:
#         ai_summary_period = st.selectbox(
#             "Summary Period",
#             ["daily", "weekly", "monthly", "yearly"],
#             index=2,
#             key="ai_summary_period",
#         )

#     with col2:
#         ai_summary_manager_display = st.selectbox(
#             "Summary Manager", manager_options, key="ai_summary_manager"
#         )
#         ai_summary_manager = ai_summary_manager_display.split(" (")[0]

#     if st.button("Generate AI Summary", key="generate_ai_summary"):
#         try:
#             params = {"period": ai_summary_period}

#             if ai_summary_manager != "All":
#                 params["manager"] = ai_summary_manager

#             res = requests.get(f"{API_BASE_URL}/ai/report", params=params, timeout=30)

#             if res.status_code == 200:
#                 data = res.json()
#                 st.success("AI summary generated successfully")
#                 st.text(data.get("report", "No summary available"))
#             else:
#                 try:
#                     error_detail = res.json().get("detail", res.text)
#                 except Exception:
#                     error_detail = res.text

#                 st.error(f"Failed to generate AI summary: {error_detail}")

#         except requests.exceptions.RequestException as e:
#             st.error(f"Failed to generate AI summary: {str(e)}")


def ai_insights():
    st.header("🤖 AI Insights")
    st.markdown(
        "Explore project performance, manager-level trends, and AI-generated summaries."
    )

    # -----------------------------
    # Session State Initialisation
    # -----------------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "ai_prefill" not in st.session_state:
        st.session_state["ai_prefill"] = ""

    projects_data, success = get_all_projects()

    if not success:
        st.error("Failed to load data")
        return

    projects = projects_data.get("projects", [])

    if not projects:
        st.info("No projects available for AI insights yet.")
        return

    # -----------------------------
    # Shared Calculations
    # -----------------------------
    total_projects = len(projects)
    completed_projects = sum(
        1 for p in projects if str(p.get("p_status", "")).lower() == "completed"
    )
    active_projects = sum(
        1 for p in projects if str(p.get("p_status", "")).lower() == "field"
    )
    completion_rate = (
        round((completed_projects / total_projects) * 100, 2) if total_projects else 0
    )

    margins = [
        float(p.get("f_margin")) for p in projects if p.get("f_margin") is not None
    ]
    avg_margin = round(sum(margins) / len(margins), 2) if margins else 0

    profits = [
        float(p.get("f_nprofit")) for p in projects if p.get("f_nprofit") is not None
    ]
    total_net_profit = round(sum(profits), 2) if profits else 0

    manager_counts_snapshot = Counter(p.get("p_manager", "Unknown") for p in projects)
    top_manager = (
        max(manager_counts_snapshot, key=manager_counts_snapshot.get)
        if manager_counts_snapshot
        else "N/A"
    )

    status_counts_snapshot = Counter(p.get("p_status", "Unknown") for p in projects)
    top_status = (
        max(status_counts_snapshot, key=status_counts_snapshot.get)
        if status_counts_snapshot
        else "N/A"
    )

    # Manager dropdown options
    manager_list = sorted(list(set(p.get("p_manager", "Unknown") for p in projects)))
    manager_counts = Counter(p.get("p_manager", "Unknown") for p in projects)
    manager_options = ["All"] + [f"{m} ({manager_counts[m]})" for m in manager_list]

    # -----------------------------
    # Sub Tabs
    # -----------------------------
    subtab1, subtab2, subtab3 = st.tabs(
        ["📊 Overview", "📄 Reports", "💬 AI Assistant"]
    )

    # =====================================================
    # TAB 1: OVERVIEW
    # =====================================================
    with subtab1:
        st.subheader("🧠 AI Snapshot")

        snap1, snap2, snap3, snap4 = st.columns(4)
        snap1.metric("📦 Total Projects", total_projects)
        snap2.metric("✅ Completed", completed_projects)
        snap3.metric("🚧 Active", active_projects)
        snap4.metric("📊 Completion Rate", f"{completion_rate}%")

        snap5, snap6, snap7 = st.columns(3)
        snap5.metric("💹 Avg Margin", f"{avg_margin}%")
        snap6.metric("💰 Total Net Profit", f"{total_net_profit}")
        snap7.metric("👤 Top Manager", top_manager)

        insight_col1, insight_col2 = st.columns(2)

        with insight_col1:
            if active_projects > completed_projects:
                st.warning(
                    "⚠️ Active projects currently exceed completed projects, which may indicate delivery backlog."
                )
            else:
                st.success(
                    "✅ Completed projects are keeping pace with active workload."
                )

        with insight_col2:
            if avg_margin < 20:
                st.warning(
                    f"⚠️ Average margin is {avg_margin}%, which may require profitability review."
                )
            else:
                st.success(f"💹 Average margin is {avg_margin}%, which looks healthy.")

        st.caption(f"Most common status: {top_status}")
        st.markdown("---")

        st.subheader("📌 Quick Project Snapshot")

        recent_projects = sorted(
            projects, key=lambda x: x.get("created_at") or "", reverse=True
        )[:6]

        if recent_projects:
            recent_rows = []
            for project in recent_projects:
                recent_rows.append(
                    {
                        "DB ID": project.get("db_id"),
                        "Project Name": project.get("p_name", "Unnamed Project"),
                        "Manager": project.get("p_manager", "Unknown"),
                        "Status": project.get("p_status", "Unknown"),
                        "Created At": project.get("created_at", "-"),
                    }
                )

            recent_df = pd.DataFrame(recent_rows)
            st.dataframe(recent_df, use_container_width=True, hide_index=True)
        else:
            st.info("No recent projects available.")

    # =====================================================
    # TAB 2: REPORTS
    # =====================================================
    with subtab2:
        report_tab1, report_tab2 = st.tabs(
            ["📁 Project Performance Report", "🧠 AI Manager Summary"]
        )

        # -----------------------------
        # Project Performance Report
        # -----------------------------
        with report_tab1:
            st.subheader("📊 Project Performance Report")

            col1, col2 = st.columns(2)

            with col1:
                period = st.selectbox(
                    "Select Period",
                    ["daily", "weekly", "monthly", "yearly"],
                    key="project_report_period",
                )

            with col2:
                selected_manager_display = st.selectbox(
                    "Select Manager",
                    manager_options,
                    key="project_report_manager",
                )
                selected_manager = selected_manager_display.split(" (")[0]

            if st.button("Generate Report 📄", key="generate_project_report"):
                try:
                    params = {"period": period}

                    if selected_manager != "All":
                        params["manager"] = selected_manager

                    res = requests.get(
                        f"{API_BASE_URL}/reports/projects", params=params, timeout=30
                    )

                    if res.status_code == 200:
                        data = res.json()

                        st.success(f"📅 {period.capitalize()} Report")

                        metric1, metric2, metric3 = st.columns(3)
                        metric1.metric("📦 Total Projects", data.get("count", 0))
                        metric2.metric(
                            "💰 Total Net Profit", f"{data.get('total_profit', 0)}"
                        )
                        metric3.metric(
                            "📊 Avg Margin (%)", f"{data.get('avg_margin', 0)}%"
                        )

                        st.markdown(f"**Manager Filter:** {selected_manager}")
                        st.caption(f"Period: {period.capitalize()}")

                        if data.get("count", 0) == 0:
                            st.info("No projects found for this selection.")
                        else:
                            if data.get("avg_margin", 0) < 20:
                                st.warning(
                                    "⚠️ Low margin detected — potential profitability issue"
                                )

                            st.markdown("### Matching Projects")
                            for project in data.get("projects", []):
                                with st.container(border=True):
                                    st.markdown(
                                        f"**{project.get('p_name', 'Unnamed Project')}**"
                                    )
                                    st.caption(
                                        f"DB ID: {project.get('db_id')} | "
                                        f"Manager: {project.get('p_manager')} | "
                                        f"Status: {project.get('p_status')}"
                                    )
                                    st.markdown(
                                        f"Start Date: {project.get('p_s_date')}  \n"
                                        f"Created At: {project.get('created_at')}"
                                    )

                    else:
                        try:
                            error_detail = res.json().get("detail", res.text)
                        except Exception:
                            error_detail = res.text

                        st.error(f"Failed to generate report: {error_detail}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to generate report: {str(e)}")

        # -----------------------------
        # AI Manager Summary
        # -----------------------------
        with report_tab2:
            st.subheader("🧠 AI Manager Summary")

            col1, col2 = st.columns(2)

            with col1:
                ai_summary_period = st.selectbox(
                    "Summary Period",
                    ["daily", "weekly", "monthly", "yearly"],
                    index=2,
                    key="ai_summary_period",
                )

            with col2:
                ai_summary_manager_display = st.selectbox(
                    "Summary Manager",
                    manager_options,
                    key="ai_summary_manager",
                )
                ai_summary_manager = ai_summary_manager_display.split(" (")[0]

            if st.button("Generate AI Summary", key="generate_ai_summary"):
                try:
                    params = {"period": ai_summary_period}

                    if ai_summary_manager != "All":
                        params["manager"] = ai_summary_manager

                    res = requests.get(
                        f"{API_BASE_URL}/ai/report", params=params, timeout=30
                    )

                    if res.status_code == 200:
                        data = res.json()

                        st.success("AI summary generated successfully")

                        info1, info2, info3, info4 = st.columns(4)
                        info1.metric("📦 Total", data.get("total_projects", 0))
                        info2.metric("✅ Completed", data.get("completed", 0))
                        info3.metric("🚧 Active", data.get("active", 0))
                        info4.metric(
                            "📊 Completion Rate",
                            f"{data.get('completion_rate', 0)}%",
                        )

                        insights = data.get("insights", {})
                        box1, box2, box3 = st.columns(3)
                        box1.info(f"**Workload:** {insights.get('workload', '-')}")
                        box2.info(
                            f"**Performance:** {insights.get('performance', '-')}"
                        )
                        box3.info(f"**Trend:** {insights.get('trend', '-')}")

                        st.markdown("### Summary Output")
                        st.text(data.get("report", "No summary available"))

                    else:
                        try:
                            error_detail = res.json().get("detail", res.text)
                        except Exception:
                            error_detail = res.text

                        st.error(f"Failed to generate AI summary: {error_detail}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to generate AI summary: {str(e)}")

    # =====================================================
    # TAB 3: AI ASSISTANT
    # =====================================================
    with subtab3:
        st.subheader("💬 AI Chat Assistant")

        current_prefill = st.session_state.get("ai_prefill", "")

        user_input = st.text_input(
            "Ask about projects, managers, performance insights, or general queries.",
            value=current_prefill,
            key="ai_chat_input",
        )

        chat_action_col1, chat_action_col2 = st.columns([1, 1])

        with chat_action_col1:
            send_clicked = st.button("Send 💬", key="send_ai_chat")

        with chat_action_col2:
            if st.button("Clear Chat 🗑️", key="clear_ai_chat"):
                st.session_state.chat_history = []
                st.session_state["ai_prefill"] = ""
                st.rerun()

        if send_clicked:
            if user_input.strip():
                st.session_state.chat_history.append(
                    {"role": "user", "message": user_input.strip()}
                )

                try:
                    response = requests.post(
                        f"{API_BASE_URL}/ai/chat/",
                        params={"query": user_input.strip()},
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

                        if "GEMINI_API_KEY is not set" in str(error_detail):
                            ai_reply = (
                                "⚠️ AI assistant is not available yet because GEMINI_API_KEY is not set. "
                                "Please add your Gemini API key to enable general AI questions like weather."
                            )
                        elif "WEATHERAPI_KEY is not set" in str(error_detail):
                            ai_reply = (
                                "⚠️ Live weather is not available yet because WEATHERAPI_KEY is not set. "
                                "Please add your weather API key to enable weather queries."
                            )
                        else:
                            ai_reply = f"⚠️ AI request failed: {error_detail}"

                except requests.exceptions.RequestException as e:
                    ai_reply = f"⚠️ AI request failed: {str(e)}"

                st.session_state.chat_history.append(
                    {"role": "ai", "message": ai_reply}
                )
                st.session_state["ai_prefill"] = ""
                st.rerun()

        st.markdown("---")

        st.subheader("📝 Conversation")

        if st.session_state.chat_history:
            for chat in st.session_state.chat_history:
                with st.container(border=True):
                    if chat["role"] == "user":
                        st.markdown(f"🧑 **You**")
                    else:
                        st.markdown(f"🤖 **AI**")
                    st.write(chat["message"])
        else:
            st.info(
                "No chat history yet. Start with a question or use one of the quick prompts."
            )

        st.markdown("---")

        st.subheader("💡 Smart Actions")
        st.caption("Quick prompts to explore common project insights.")

        suggestions = [
            "Summarise monthly project performance",
            "Analyse performance trends by manager",
            "Identify underperforming managers",
            "Show projects with low profit margins",
            "Highlight potential project risks",
            "Projects initiated this week",
        ]

        # Left-aligned layout (2 columns + empty space)
        col_left, col_right, _ = st.columns([1, 1, 2])

        for i, suggestion in enumerate(suggestions):
            target_col = col_left if i % 2 == 0 else col_right

            with target_col:
                if st.button(suggestion, key=f"suggestion_{i}"):

                    # Save user message
                    st.session_state.chat_history.append(
                        {"role": "user", "message": suggestion}
                    )

                    # Call AI backend
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/ai/chat/",
                            params={"query": suggestion},
                            timeout=30,
                        )

                        if response.status_code == 200:
                            ai_reply = response.json().get(
                                "response", "No response from AI"
                            )
                        else:
                            try:
                                error_detail = response.json().get(
                                    "detail", response.text
                                )
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

    st.markdown("---")


if __name__ == "__main__":
    main()
