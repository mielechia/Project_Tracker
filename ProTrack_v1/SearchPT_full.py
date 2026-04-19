# Search Projects
def search_projects():
    st.header("🔍 Project Directory")
    st.markdown("Browse all projects or refine the list using search criteria below.")

    if "selected_project" not in st.session_state:
        st.session_state["selected_project"] = None
    if "project_search_results" not in st.session_state:
        st.session_state["project_search_results"] = None
    if "project_search_success" not in st.session_state:
        st.session_state["project_search_success"] = False
    if "project_search_label" not in st.session_state:
        st.session_state["project_search_label"] = None
    if "project_search_value" not in st.session_state:
        st.session_state["project_search_value"] = None

    search_config = {
        "All Projects": {
            "type": "special",
            "runner": lambda _: get_all_projects(),
            "value_label": "Showing all projects",
        },
        "Project Name Keyword": {
            "type": "text",
            "label": "Project Name Keyword",
            "key": "keyword",
            "placeholder": "Enter keyword to search in project names",
            "runner": get_projects_by_name_keyword,
        },
        "Project SID": {
            "type": "text",
            "label": "Project SID",
            "key": "sid",
            "placeholder": "Enter project SID",
            "runner": get_projects_by_sid,
        },
        "Project Segment": {
            "type": "select",
            "label": "Project Segment",
            "key": "segment",
            "options": [
                "Full Service",
                "Sample Only",
                "Sample Only (External)",
                "Coverage",
                "Other",
            ],
            "runner": get_projects_by_segment,
        },
        "Project Type": {
            "type": "select",
            "label": "Project Type",
            "key": "p_type",
            "options": ["Tracker", "Ad Hoc", "Other"],
            "runner": get_projects_by_type,
        },
        "Project TA ID": {
            "type": "text",
            "label": "Project TA ID",
            "key": "ta_id",
            "placeholder": "Enter project TA ID",
            "runner": get_projects_by_ta_id,
        },
        "Project Job ID": {
            "type": "text",
            "label": "Project Job ID",
            "key": "job_id",
            "placeholder": "Enter project Job ID",
            "runner": get_projects_by_job_id,
        },
        "Project Job OL ID": {
            "type": "text",
            "label": "Project Job OL ID",
            "key": "job_ol_id",
            "placeholder": "Enter project Job OL ID",
            "runner": get_projects_by_job_ol_id,
        },
        "Project Job RA ID": {
            "type": "text",
            "label": "Project Job RA ID",
            "key": "job_ra_id",
            "placeholder": "Enter project Job RA ID",
            "runner": get_projects_by_job_ra_id,
        },
        "Project Status": {
            "type": "select",
            "label": "Project Status",
            "key": "status",
            "options": ["Field", "Completed", "Other"],
            "runner": get_projects_by_status,
        },
        "Project Manager": {
            "type": "text",
            "label": "Project Manager",
            "key": "manager",
            "placeholder": "Enter project manager name",
            "runner": get_projects_by_manager,
        },
        "Project Business Unit": {
            "type": "text",
            "label": "Business Unit",
            "key": "b_unit",
            "placeholder": "Enter business unit",
            "runner": get_projects_by_business_unit,
        },
        "Project Business Country": {
            "type": "text",
            "label": "Business Country",
            "key": "b_country",
            "placeholder": "Enter business country",
            "runner": get_projects_by_business_country,
        },
        "Project Business Name": {
            "type": "text",
            "label": "Business Name",
            "key": "b_name",
            "placeholder": "Enter business name",
            "runner": get_projects_by_business_name,
        },
        "Project Margin Band": {
            "type": "select",
            "label": "Margin Band",
            "key": "f_margin_band",
            "options": ["0%", "1-19%", "20-49%", "50-79%", "80-100%"],
            "runner": get_projects_by_margin_band,
        },
        "Project Date Filter": {
            "type": "date_filter",
            "runner": get_projects_by_date,
        },
    }

    with st.container(border=True):
        st.markdown("### Filter Projects")

        search_criteria = st.selectbox(
            "Search Type",
            list(search_config.keys()),
            key="project_search_type",
        )

        config = search_config[search_criteria]
        input_value = None

        if config["type"] == "text":
            input_value = st.text_input(
                config["label"],
                max_chars=100,
                placeholder=config["placeholder"],
                key=f"search_input_{config['key']}",
            )

        elif config["type"] == "select":
            input_value = st.selectbox(
                config["label"],
                config["options"],
                key=f"search_input_{config['key']}",
            )

        elif config["type"] == "date_filter":
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
                    key="search_input_month",
                )
            with col2:
                year = st.text_input(
                    "Year",
                    max_chars=4,
                    placeholder="E.g. 2026",
                    key="search_input_year",
                )

        col_btn1, col_btn2 = st.columns([1, 5])

        with col_btn1:
            if st.button("Apply Filter", key="project_search_apply"):
                if config["type"] == "special":
                    response_data, success = config["runner"](None)
                    search_value = config["value_label"]

                elif config["type"] == "date_filter":
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
                    response_data, success = config["runner"](
                        month=month_number,
                        year=year_number,
                    )
                    search_value = f"Month: {month or '-'} | Year: {year or '-'}"

                else:
                    response_data, success = config["runner"](input_value)
                    search_value = input_value

                st.session_state["project_search_results"] = response_data
                st.session_state["project_search_success"] = success
                st.session_state["project_search_label"] = search_criteria
                st.session_state["project_search_value"] = search_value
                st.session_state["selected_project"] = None
                st.session_state["search_project_page"] = 1
                st.rerun()

        with col_btn2:
            if st.button("Clear Search", key="project_search_clear"):
                st.session_state["project_search_results"] = None
                st.session_state["project_search_success"] = False
                st.session_state["project_search_label"] = None
                st.session_state["project_search_value"] = None
                st.session_state["selected_project"] = None
                st.rerun()

    st.markdown("")

    if (
        st.session_state["project_search_results"] is None
        and search_criteria == "All Projects"
    ):
        response_data, success = get_all_projects()
        if success:
            display_search_results(
                response_data,
                mode="all",
                active_search_label="All Projects",
                active_search_value="Showing all projects",
            )
        else:
            st.error("Failed to retrieve projects. Please try again later.")
        return

    if st.session_state["project_search_results"] is not None:
        if st.session_state["project_search_success"]:
            display_search_results(
                st.session_state["project_search_results"],
                mode="search",
                active_search_label=st.session_state["project_search_label"],
                active_search_value=st.session_state["project_search_value"],
            )
        else:
            st.error(
                f"No projects found for {st.session_state['project_search_label']}: "
                f"{st.session_state['project_search_value']}"
            )
    else:
        st.info(
            "Select a search type, enter a value if needed, and click 'Apply Filter'."
        )


# Display project with full details
def render_project_full_details(project):
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("#### 📋 Project")
        st.markdown(f"**DB ID:** {project.get('db_id', '-')}")
        st.markdown(f"**Name:** {project.get('p_name', '-')}")
        st.markdown(f"**Manager:** {project.get('p_manager', '-')}")
        st.markdown(f"**Team:** {project.get('p_team', '-')}")
        st.markdown(f"**Segment:** {project.get('p_segment', '-')}")
        st.markdown(f"**Type:** {project.get('p_type', '-')}")
        st.markdown(f"**Status:** {project.get('p_status', '-')}")
        st.markdown(f"**IR:** {project.get('ir', '-')}")
        st.markdown(f"**LOI:** {project.get('loi', '-')}")

    with col2:
        st.markdown("#### 🆔 Operational")
        st.markdown(f"**Start:** {project.get('p_s_date', '-')}")
        st.markdown(f"**End:** {project.get('p_e_date', '-')}")
        st.markdown(f"**Job ID:** {project.get('job_id', '-')}")
        st.markdown(f"**OL ID:** {project.get('job_ol_id', '-')}")
        st.markdown(f"**RA ID:** {project.get('job_ra_id', '-')}")
        st.markdown(f"**SID:** {project.get('s_id', '-')}")
        st.markdown(f"**TA ID:** {project.get('ta_id', '-')}")
        st.markdown(f"**Folder:** {project.get('pf_link', '-')}")

    with col3:
        st.markdown("#### 🏢 Business")
        st.markdown(f"**Unit:** {project.get('b_unit', '-')}")
        st.markdown(f"**Country:** {project.get('b_country', '-')}")
        st.markdown(f"**Name:** {project.get('b_name', '-')}")
        st.markdown(f"**Name ID:** {project.get('b_name_id', '-')}")
        st.markdown(f"**Market:** {project.get('market', '-')}")

    with col4:
        st.markdown("#### 💰 Financial")
        st.markdown(f"**Deliverables:** {project.get('f_deliverables', '-')}")
        st.markdown(f"**Currency:** {project.get('f_currency', '-')}")
        st.markdown(f"**Revenue:** {project.get('f_revenue', '-')}")
        st.markdown(f"**Cost:** {project.get('f_cost', '-')}")
        st.markdown(f"**Profit:** {project.get('f_nprofit', '-')}")
        st.markdown(f"**Margin:** {project.get('f_margin', '-')}")
        st.markdown(f"**Remarks:** {project.get('f_remarks', '-')}")

    st.markdown("---")

    col_close, _ = st.columns([1, 5])
    with col_close:
        if st.button("Close", key="close_project_details"):
            st.session_state["selected_project"] = None
            st.rerun()


# Display Search Results
def display_search_results(
    response_data,
    mode="search",
    active_search_label=None,
    active_search_value=None,
):
    if not response_data:
        st.info("No results found matching the search criteria.")
        return

    projects = response_data.get("projects", [])

    if not projects:
        st.info("No projects found matching the search criteria.")
        return

    table_rows = []
    for project in projects:
        table_rows.append(
            {
                "DB ID": project.get("db_id"),
                "Project Name": project.get("p_name", "Unnamed Project"),
                "SID": project.get("s_id", "Unknown"),
                "Manager": project.get("p_manager", "Unknown"),
                "Status": project.get("p_status", "Unknown"),
            }
        )

    df = pd.DataFrame(table_rows)

    title = "All Projects" if mode == "all" else "Search Results"
    st.markdown(f"### {title} ({len(df)} projects)")

    if active_search_label and active_search_value:
        st.caption(f"Active Criteria: {active_search_label} → {active_search_value}")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        keyword = st.text_input(
            "Filter current results",
            placeholder="Search by project name, DB ID, SID, manager, or status",
            key=f"{mode}_project_keyword",
        ).strip()

    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["DB ID", "Project Name", "SID", "Manager", "Status"],
            key=f"{mode}_project_sort_by",
        )

    with col3:
        page_size = st.selectbox(
            "Projects per page",
            [10, 20, 30, 50],
            index=1,
            key=f"{mode}_project_page_size",
        )

    if keyword:
        keyword_lower = keyword.lower()
        df = df[
            df["Project Name"]
            .astype(str)
            .str.lower()
            .str.contains(keyword_lower, na=False)
            | df["SID"].astype(str).str.lower().str.contains(keyword_lower, na=False)
            | df["DB ID"].astype(str).str.lower().str.contains(keyword_lower, na=False)
            | df["Manager"]
            .astype(str)
            .str.lower()
            .str.contains(keyword_lower, na=False)
            | df["Status"].astype(str).str.lower().str.contains(keyword_lower, na=False)
        ]

    if df.empty:
        st.info("No projects found for the current filter.")
        return

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
            "◀ Prev",
            key=f"{mode}_prev_page",
            disabled=st.session_state[page_key] <= 1,
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

    st.dataframe(
        page_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### View Full Details")

    visible_db_ids = page_df["DB ID"].tolist()
    visible_projects = []

    for db_id in visible_db_ids:
        matched_project = next(
            (p for p in projects if str(p.get("db_id")) == str(db_id)),
            None,
        )
        if matched_project:
            visible_projects.append(matched_project)

    for project in visible_projects:
        col_a, col_b = st.columns([4, 1])

        with col_a:
            st.markdown(
                f"**{project.get('p_name', 'Unnamed Project')}**  \n"
                f"DB ID: {project.get('db_id')} | "
                f"SID: {project.get('s_id', 'Unknown')} | "
                f"Manager: {project.get('p_manager', 'Unknown')} | "
                f"Status: {project.get('p_status', 'Unknown')}"
            )

        with col_b:
            if st.button("View Details", key=f"{mode}_view_{project.get('db_id')}"):
                st.session_state["selected_project"] = project
                st.rerun()

    selected_project = st.session_state.get("selected_project")
    if selected_project:
        render_project_full_details(selected_project)
