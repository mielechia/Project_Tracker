#Project Tracker Main Application Logic (Streamlit)

from re import search
from unittest import result
import requests
import streamlit as st
from datetime import datetime

#Configuration of page
st.set_page_config(
    page_title="Project Tracker", 
    page_icon=":clipboard:", 
    layout="wide",
    initial_sidebar_state="expanded"
)

#API base URL
API_BASE_URL = "http://localhost:8000"

#Check if API is running
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

#Create Project    
def create_project_api(project):
    try:
        response = requests.post(f"{API_BASE_URL}/projects/", json=project)
        if response.status_code == 201:
            return response.json(), True
        else:
            st.error(f"Failed to create project: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False

#Retrieve all projects
def get_all_projects():
    try:
        response = requests.get(f"{API_BASE_URL}/projects/")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False

#Retrieve Project by Database ID
def get_project_by_db_id(db_id):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/id/{db_id}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve project: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False
    
#Retrieve Projects by Project Name Keyword (Case-Insensitive)
def get_projects_by_name_keyword(keyword):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/search/{keyword}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False

#Retrieve Projects by Project SID
def get_projects_by_sid(sid):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/sid/{sid}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False
    
#Retrieve Projects by Project Segment
def get_projects_by_segment(segment):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/segment/{segment}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False  

#Retrieve Projects by Project Type
def get_projects_by_type(p_type): 
    try:
        response = requests.get(f"{API_BASE_URL}/projects/type/{p_type}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False

#Retrieve Projects by Project TA ID
def get_projects_by_ta_id(ta_id):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/ta_id/{ta_id}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False

#Retrieve Projects by Project Job ID
def get_projects_by_job_id(job_id):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/job_id/{job_id}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False

#Retrieve Projects by Project Job OL ID
def get_projects_by_job_ol_id(job_ol_id):   
    try:
        response = requests.get(f"{API_BASE_URL}/projects/job_ol_id/{job_ol_id}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False

#Retrieve Projects by Project Job RA ID
def get_projects_by_job_ra_id(job_ra_id):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/job_ra_id/{job_ra_id}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False
    
#Retrieve Projects by Project Status
def get_projects_by_status(status):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/status/{status}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False
    
#Retrieve Projects by Project Manager
def get_projects_by_manager(manager):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/manager/{manager}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False
    
#Retrieve Projects by Project Business Unit
def get_projects_by_business_unit(b_unit):  
    try:
        response = requests.get(f"{API_BASE_URL}/projects/business_unit/{b_unit}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False
    
#Retrieve Projects by Project Business Country   
def get_projects_by_business_country(b_country):    
    try:
        response = requests.get(f"{API_BASE_URL}/projects/business_country/{b_country}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False
    
#Retrieve Projects by Project Business Name
def get_projects_by_business_name(b_name):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/business_name/{b_name}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False
    
#Retrieve Projects by Project Margin Band
def get_projects_by_margin_band(f_margin_band):
    try:
        response = requests.get(f"{API_BASE_URL}/projects/margin_band/{f_margin_band}")
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False
    
#Retrieve Projects by Project Date Filter
def get_projects_by_date(month=None, year=None, since=None, until=None, date_type="start"):
    try:
        params = {}
        if month:
            params['month'] = month
        if year:
            params['year'] = year
        if since:
            params['since'] = since
        if until:
            params['until'] = until
        if date_type:
            params['date_type'] = date_type
        
        response = requests.get(f"{API_BASE_URL}/projects/filter/date", params=params)
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to retrieve projects: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False
    
#Update Project by Database ID
def update_project_by_db_id(db_id, updates):
    try:
        response = requests.put(f"{API_BASE_URL}/projects/{db_id}", json=updates)
        if response.status_code == 200:
            return response.json(), True
        else:
            st.error(f"Failed to update project: {response.text}")
            return None, False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None, False

#Delete Project by Database ID
def delete_project_by_db_id(db_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/projects/{db_id}")
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to delete project: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return False

#Main function to run the Streamlit app
def main():
    st.title("Project Tracker Dashboard")
    st.markdown("Welcome to the Project Tracker! Please use the sidebar to navigate through different sections.")
    
    if not check_api_connection():
        st.error("API connection failed. Please start the API server and refresh the page.")
        st.info("To start the API server, run ` uvicorn EP_Project_Tracker:app --reload ` in your terminal.")
        return
    
    st.success("You are connected to Project Tracker API successfully!")

    #Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Dashboard", "Create Project", "Search Projects"])
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Create Project":
        create_project_ui()
    elif page == "Search Projects":
        search_projects()

#Dashboard
def show_dashboard():
    st.header("Project Dashboard")
    st.markdown("This section will display key metrics and visualizations about your projects.")

    response_data, success = get_all_projects()

    if success:
        projects = response_data["projects"]
        st.metric("Total Projects", len(projects))
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.subheader("Total Projects")
            status_counts = {}
            for project in projects:
                status = project.get("p_status", "Unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            st.bar_chart(status_counts)
        with col2:
            st.subheader("Projects by Status")
            status_counts = {}
            for project in projects:
                status = project.get("p_status", "Unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            st.bar_chart(status_counts)
        with col3:
            st.subheader("Projects by Business Unit")
            business_unit_counts = {}
            for project in projects:
                business_unit = project.get("b_unit", "Unknown")
                business_unit_counts[business_unit] = business_unit_counts.get(business_unit, 0) + 1
            st.bar_chart(business_unit_counts)
        with col4:
            st.subheader("Projects by Start Date")
            start_date_counts = {}
            for project in projects:
                start_date = project.get("p_s_date", "Unknown")
                start_date_counts[start_date] = start_date_counts.get(start_date, 0) + 1
            st.bar_chart(start_date_counts)
        with col5:
            st.subheader("Projects by Margin Band")
            margin_band_counts = {}
            for project in projects:
                margin_band = project.get("margin_band") or project.get("f_margin_band", "Unknown")
                margin_band_counts[margin_band] = margin_band_counts.get(margin_band, 0) + 1
            st.bar_chart(margin_band_counts)
        with col6:
            st.subheader("Projects by Project Manager")
            p_manager_counts = {}
            for project in projects:
                project_manager = project.get("p_manager", "Unknown")
                p_manager_counts[project_manager] = p_manager_counts.get(project_manager, 0) + 1
            st.bar_chart(p_manager_counts)
        
        st.markdown("### Recent Projects")
        recent_projects = sorted(
            projects, 
            key=lambda x: x.get("created_at") or "", 
            reverse=True
        )

        for project in recent_projects:
            st.markdown(f"**{project.get('p_name', 'Unnamed Project')}**, "
                        f"sid: {project.get('s_id', 'Unknown')},"
                        f"Status: {project.get('p_status', 'Unknown')}, "
                        f"Segment: {project.get('p_segment', 'Unknown')}, "
                        f"Type: {project.get('p_type', 'Unknown')}")

    else:
        st.error("Failed to load projects for dashboard.")

#Create Project
def create_project_ui():
    st.header("Create New Project")
    st.markdown("Fill out the form below to create a new project.")

    with st.form("create_project_form"):
        p_name = st.text_input("Project Name", max_chars=100)
        p_manager = st.text_input("Project Manager", max_chars=100)
        p_team = st.text_input("Project Team", max_chars=100)
        p_segment = st.selectbox("Project Segment", ["Sample Only (External)", "Sample Only", "Full Service", "Coverage", "Other"])
        p_type = st.selectbox("Project Type", ["Ad Hoc", "Tracker", "Other"])
        p_status = st.selectbox("Project Status", ["Field", "Completed", "Other"])
        p_s_date = st.date_input("Project Start Date")
        p_e_date = st.date_input("Project End Date")
        job_id = st.text_input("Job ID", max_chars=20)
        job_ol_id = st.text_input("Job OL ID", max_chars=20)
        job_ra_id = st.text_input("Job RA ID", max_chars=20)
        s_id = st.text_input("SID", max_chars=20)
        ta_id = st.text_input("TA ID", max_chars=10)
        pf_link = st.text_input("Path Folder Link", max_chars=200)
        b_unit = st.text_input("Business Unit", max_chars=100)
        b_country = st.text_input("Business Country", max_chars=100)
        b_name = st.text_input("Business Name", max_chars=100)
        b_name_id = st.text_input("Business Name ID", max_chars=100) 
        market = st.text_input("Market", max_chars=100)
        ir = st.text_input("IR (%)", max_chars=2)
        loi = st.text_input("LOI (Minutes)", max_chars=2)
        f_deliverables = st.number_input("Final Deliverables", min_value=0, step=1, max_value=99999)
        f_currency = st.text_input("Final Currency (e.g. AUD / USD)", max_chars=3)
        f_revenue = st.text_input("Fieldwork Revenue", max_chars=20)
        f_cost = st.text_input("Fieldwork Cost", max_chars=20)
        f_nprofit = st.text_input("Fieldwork Net Profit", max_chars=20)
        margin_band = st.selectbox("Margin Band", ["0%", "1-19%", "20-49%", "50-79%", "80-100%"])
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
        if not ta_id or not ta_id.strip():
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
        if not b_name_id or not b_name_id.strip():
            st.error("Business Name ID is required.")
            return
        if not market or not market.strip():
            st.error("Market is required.")
            return
        if not ir or not ir.strip():
            st.error("IR is required.")
            return
        if not loi or not loi.strip():
            st.error("LOI is required.")
            return

        try:
            ta_id_val = int(ta_id) if ta_id.strip() else None
        except ValueError:
            st.error("TA ID must be a number.")
            return
        try:
            b_name_id_val = int(b_name_id) if b_name_id.strip() else None
        except ValueError:
            st.error("Business Name ID must be a number.")
            return
        try:
            ir_val = float(ir) if ir.strip() else None 
        except ValueError:
            st.error("IR must be a number.")
            return
        try:
            loi_val = float(loi) if loi.strip() else None
        except ValueError:
            st.error("LOI must be a number.")
            return

        margin_map = {
            "0%": 0,
            "1-19%": 10,
            "20-49%": 30,
            "50-79%": 60,
            "80-100%": 90
        }   

        new_project = {
            "p_name": p_name,
            "p_manager": p_manager,
            "p_team": p_team,
            "p_segment": p_segment,
            "p_type": p_type,
            "p_status": p_status,       
            "p_s_date": p_s_date.strftime("%d-%m-%Y"),
            "p_e_date": p_e_date.strftime("%d-%m-%Y"),
            "job_id": job_id,
            "job_ol_id": job_ol_id,
            "job_ra_id": job_ra_id,
            "s_id": s_id,
            "ta_id": ta_id_val,
            "pf_link": pf_link,
            "b_unit": b_unit,
            "b_country": b_country,
            "b_name": b_name,
            "b_name_id": b_name_id_val,
            "market": market,
            "ir": ir_val,
            "loi": loi_val,
            "f_deliverables": int(f_deliverables) if f_deliverables else 0,
            "f_currency": f_currency,
            "f_revenue": float(f_revenue) if f_revenue else 0,
            "f_cost": float(f_cost) if f_cost else 0,
            "f_nprofit": float(f_nprofit) if f_nprofit else 0,
            "f_margin": margin_map.get(margin_band, 0),
            "margin_band": margin_band,
            "f_remarks": f_remarks,
        }   

        response, success = create_project_api(new_project)

        if success:
            st.success(f"Project'{p_name} created successfully! DB ID: {response['db_id']}")
            st.rerun()
        else:
            st.error("Failed to create project. Please try again.")
    else:
        st.info("Fill out the form and click 'Create Project' to add a new project to the tracker.")

#Search Projects
def search_projects():
    st.header("Search Projects")

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
        search_criteria = st.selectbox("Search by", [
            "Project Name Keyword", "Project SID", "Project Segment", "Project Type", 
            "Project TA ID", "Project Job ID", "Project Job OL ID", "Project Job RA ID", 
            "Project Status", "Project Manager", "Project Business Unit", 
            "Project Business Country", "Project Business Name", "Project Margin Band",
            "Project Date Filter"
        ])

        if search_criteria == "Project Name Keyword":
            keyword = st.text_input("Enter keyword to search in project names", max_chars=100)
            if st.button("Search", key="search_name_keyword"):
                response_data, success = get_projects_by_name_keyword(keyword)
                if success:
                    display_search_results(response_data)
                else: 
                    st.error("No projects found matching the search criteria. Please try a different keyword.")
    
        elif search_criteria == "Project SID":
            sid = st.text_input("Enter Project SID", max_chars=20)
            if st.button("Search", key="search_sid"):
                response_data, success = get_projects_by_sid(sid)
                if success:
                    display_search_results(response_data)
                else:
                    st.error("No projects found matching the search criteria. Please try a different SID.")
    
        elif search_criteria == "Project Segment":
            segment = st.selectbox("Select Project Segment", ["Full Service", "Sample Only", "Sample Only (External)", "Coverage", "Other"])
            if st.button("Search", key="search_segment"):
                response_data, success = get_projects_by_segment(segment)
                if success:
                    display_search_results(response_data)
                else:
                    st.error("No projects found matching the search criteria. Please try a different segment.")
    
        elif search_criteria == "Project Type":
            p_type = st.selectbox("Select Project Type", ["Tracker", "Ad Hoc", "Other"])
            if st.button("Search", key="search_type"):
                response_data, success = get_projects_by_type(p_type)
                if success:
                    display_search_results(response_data)
                else:
                    st.error("No projects found matching the search criteria. Please try a different type.")
    
        elif search_criteria == "Project TA ID":
            ta_id = st.text_input("Enter Project TA ID", max_chars=10)
            if st.button("Search", key="search_ta_id"):
                response_data, success = get_projects_by_ta_id(ta_id)
                if success:
                    display_search_results(response_data)
                else:
                    st.error("No projects found matching the search criteria. Please try a different TA ID.")

        elif search_criteria == "Project Job ID":   
            job_id = st.text_input("Enter Project Job ID", max_chars=20)
            if st.button("Search", key="search_job_id"):
                response_data, success = get_projects_by_job_id(job_id)
                if success:
                    display_search_results(response_data)
                else:
                    st.error("No projects found matching the search criteria. Please try a different Job ID.")
    
        elif search_criteria == "Project Job OL ID":
            job_ol_id = st.text_input("Enter Project Job OL ID", max_chars=20)
            if st.button("Search", key="search_job_ol_id"):
                response_data, success = get_projects_by_job_ol_id(job_ol_id)
                if success:
                    display_search_results(response_data)
            else:
                st.error("No projects found matching the search criteria. Please try a different Job OL ID.")

        elif search_criteria == "Project Job RA ID":        
            job_ra_id = st.text_input("Enter Project Job RA ID", max_chars=20)
            if st.button("Search", key="search_job_ra_id"):
                response_data, success = get_projects_by_job_ra_id(job_ra_id)
                if success:
                    display_search_results(response_data)
            else:
                st.error("No projects found matching the search criteria. Please try a different Job RA ID.")

        elif search_criteria == "Project Status":   
            status = st.selectbox("Select Project Status", ["Field", "Completed", "Other"])
            if st.button("Search", key="search_status"):
                response_data, success = get_projects_by_status(status)
                if success:
                    display_search_results(response_data)
                else:
                    st.error("No projects found matching the search criteria. Please try a different status.")

        elif search_criteria == "Project Manager":
            manager = st.text_input("Enter Project Manager Name", max_chars=100)
            if st.button("Search", key="search_manager"):
                response_data, success = get_projects_by_manager(manager)
                if success:
                    display_search_results(response_data)
            else:
                st.error("No projects found matching the search criteria. Please try a different project manager name.")

        elif search_criteria == "Project Business Unit":    
            b_unit = st.text_input("Enter Business Unit", max_chars=100)
            if st.button("Search", key="search_business_unit"):
                response_data, success = get_projects_by_business_unit(b_unit)
                if success:
                    display_search_results(response_data)
            else:
                st.error("No projects found matching the search criteria. Please try a different business unit.")

        elif search_criteria == "Project Business Country":
            b_country = st.text_input("Enter Business Country", max_chars=100)
            if st.button("Search", key="search_business_country"):
                response_data, success = get_projects_by_business_country(b_country)
                if success:
                    display_search_results(response_data)
            else:
                st.error("No projects found matching the search criteria. Please try a different business country.")

        elif search_criteria == "Project Business Name":    
            b_name = st.text_input("Enter Business Name", max_chars=100)
            if st.button("Search", key="search_business_name"):
                response_data, success = get_projects_by_business_name(b_name)
                if success:
                    display_search_results(response_data)
            else:
                st.error("No projects found matching the search criteria. Please try a different business name.")

        elif search_criteria == "Project Margin Band":
            f_margin_band = st.selectbox("Select Margin Band", ["0%", "1-19%", "20-49%", "50-79%", "80-100%"])
            if st.button("Search", key="search_margin_band"):
                response_data, success = get_projects_by_margin_band(f_margin_band)
                if success:
                    display_search_results(response_data)
            else:
                st.error("No projects found matching the search criteria. Please try a different margin band.")

        elif search_criteria == "Project Date Filter":
            col1, col2 = st.columns(2)
            with col1:
                month = st.selectbox("Select Month", ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
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
                    "December": 12
                }
                month_number = month_map.get(month)
                year_number = int(year) if year else None
                response_data, success = get_projects_by_date(month=month_number, year=year_number)
                if success:
                    display_search_results(response_data)
                else:
                    st.error("No projects found matching the search criteria. Please try different date filters.")

#Display Function
def display_search_results(response_data):
    if not response_data:
        st.info("No results found matching the search criteria.")
        return
        
    projects = response_data.get("projects", [])

    if not projects:
        st.info("No projects found matching the search criteria.")
        return
        
    st.markdown(f"### Search Results ({len(projects)} projects found)")

    for project in projects:
        created_at = project.get("created_at")
        if created_at:
            try:
                dt =datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                created_at = dt.strftime("%d-%m-%Y, %I:%M:%p")
            except Exception:
                created_at = created_at

        st.markdown(f"""
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