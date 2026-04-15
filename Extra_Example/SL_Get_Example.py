# ---------- REUSABLE SEARCH FUNCTION ----------
def run_search(label, key, func, *args):
    if st.button(label, key=key):
        response_data, success = func(*args)
        if success:
            display_search_results(response_data)
        else:
            st.error("No projects found matching the criteria.")


# ---------- MAIN SEARCH PAGE ----------
def search_projects():
    st.header("Search Projects")

    tab1, tab2 = st.tabs(["Show all projects", "Search by criteria"])

    # ---------- TAB 1 ----------
    with tab1:
        st.markdown("### All Projects")
        response_data, success = get_all_projects()

        if success:
            display_search_results(response_data)
        else:
            st.error("Failed to retrieve projects.")

    # ---------- TAB 2 ----------
    with tab2:
        st.markdown("Click on the criteria below to search for projects.")

        search_criteria = st.selectbox("Search by", [
            "Project Name Keyword", "Project SID", "Project Segment", "Project Type",
            "Project TA ID", "Project Job ID", "Project Job OL ID", "Project Job RA ID",
            "Project Status", "Project Manager", "Project Business Unit",
            "Project Business Country", "Project Business Name", "Project Margin Band",
            "Project Date Filter"
        ])

        # ---------- NAME ----------
        if search_criteria == "Project Name Keyword":
            keyword = st.text_input("Enter keyword", max_chars=100)

            run_search("Search", "search_name", get_projects_by_name_keyword, keyword)

        # ---------- SID ----------
        elif search_criteria == "Project SID":
            sid = st.text_input("Enter SID")

            run_search("Search", "search_sid", get_projects_by_sid, sid)

        # ---------- SEGMENT ----------
        elif search_criteria == "Project Segment":
            segment = st.selectbox("Segment", ["Full Service", "Sample Only", "Coverage", "Other"])

            run_search("Search", "search_segment", get_projects_by_segment, segment)

        # ---------- TYPE ----------
        elif search_criteria == "Project Type":
            p_type = st.selectbox("Type", ["Tracker", "Ad Hoc", "Other"])

            run_search("Search", "search_type", get_projects_by_type, p_type)

        # ---------- TA ID ----------
        elif search_criteria == "Project TA ID":
            ta_id = st.text_input("Enter TA ID")

            run_search("Search", "search_ta", get_projects_by_ta_id, ta_id)

        # ---------- JOB ID ----------
        elif search_criteria == "Project Job ID":
            job_id = st.text_input("Enter Job ID")

            run_search("Search", "search_job", get_projects_by_job_id, job_id)

        # ---------- JOB OL ----------
        elif search_criteria == "Project Job OL ID":
            job_ol_id = st.text_input("Enter Job OL ID")

            run_search("Search", "search_job_ol", get_projects_by_job_ol_id, job_ol_id)

        # ---------- JOB RA ----------
        elif search_criteria == "Project Job RA ID":
            job_ra_id = st.text_input("Enter Job RA ID")

            run_search("Search", "search_job_ra", get_projects_by_job_ra_id, job_ra_id)

        # ---------- STATUS ----------
        elif search_criteria == "Project Status":
            status = st.selectbox("Status", ["Field", "Completed", "Other"])

            run_search("Search", "search_status", get_projects_by_status, status)

        # ---------- MANAGER ----------
        elif search_criteria == "Project Manager":
            manager = st.text_input("Enter Manager Name")

            run_search("Search", "search_manager", get_projects_by_manager, manager)

        # ---------- BUSINESS UNIT ----------
        elif search_criteria == "Project Business Unit":
            b_unit = st.text_input("Enter Business Unit")

            run_search("Search", "search_bunit", get_projects_by_business_unit, b_unit)

        # ---------- BUSINESS COUNTRY ----------
        elif search_criteria == "Project Business Country":
            b_country = st.text_input("Enter Country")

            run_search("Search", "search_bcountry", get_projects_by_business_country, b_country)

        # ---------- BUSINESS NAME ----------
        elif search_criteria == "Project Business Name":
            b_name = st.text_input("Enter Business Name")

            run_search("Search", "search_bname", get_projects_by_business_name, b_name)

        # ---------- MARGIN ----------
        elif search_criteria == "Project Margin Band":
            margin = st.selectbox("Margin Band", ["<19%", "20-49%", "50-79%", ">80%"])

            run_search("Search", "search_margin", get_projects_by_margin_band, margin)

        # ---------- DATE FILTER ----------
        elif search_criteria == "Project Date Filter":
            col1, col2 = st.columns(2)

            with col1:
                month = st.selectbox("Month", [
                    "", "January", "February", "March", "April", "May",
                    "June", "July", "August", "September", "October",
                    "November", "December"
                ])

            with col2:
                year = st.text_input("Year (e.g. 2026)", max_chars=4)

            run_search("Search", "search_date", get_projects_by_date, month, year)