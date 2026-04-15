#Project Tracker Database Management

#Crete a database folder
import sqlite3
from typing import Optional
from datetime import date, datetime
from zoneinfo import ZoneInfo

from numpy import rint

class DatabaseManager:
    def __init__(self, db_name="Project_Tracker.db"):
        self.db_name = db_name
        self.init_database()

#Initialise database 
    def init_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    db_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    p_name TEXT NOT NULL,
                    p_manager TEXT NOT NULL,
                    p_team TEXT,
                    p_segment TEXT NOT NULL,
                    p_type TEXT NOT NULL,
                    p_status TEXT NOT NULL,
                    p_s_date TEXT NOT NULL,
                    p_e_date TEXT,
                    job_id TEXT NOT NULL,
                    job_ol_id TEXT NOT NULL,
                    job_ra_id TEXT NOT NULL,
                    s_id TEXT NOT NULL,
                    ta_id INTEGER NOT NULL,
                    pf_link TEXT NOT NULL,
                    b_unit TEXT NOT NULL,
                    b_country TEXT NOT NULL,
                    b_name TEXT NOT NULL,
                    b_name_id INTEGER NOT NULL,
                    market TEXT NOT NULL,
                    ir FLOAT NOT NULL,
                    loi FLOAT NOT NULL,
                    f_deliverables INTEGER,
                    f_currency TEXT,
                    f_revenue FLOAT,
                    f_cost FLOAT,
                    f_nprofit FLOAT,
                    f_margin FLOAT,
                    f_remarks TEXT,
                    created_at TEXT
                )           
            ''')
            conn.commit()

    def to_sql_date(self, date_str):
        """Convert date from DD-MM-YYYY to YYYY-MM-DD format."""
        try:
            return datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid date format. Please use DD-MM-YYYY.")

#Project creation
    def create_project(self, project_data): 
        query = """
            INSERT INTO projects (
                p_name, p_manager, p_team, p_segment, p_type, p_s_date, 
                p_e_date, job_id, job_ol_id, job_ra_id,s_id, ta_id, pf_link, 
                p_status, b_unit, b_country, b_name, b_name_id,market, ir, loi, 
                f_deliverables, f_currency, f_revenue, f_cost,f_nprofit, f_margin, 
                f_remarks
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        values = (
            project_data.get("p_name"),
            project_data.get("p_manager"),
            project_data.get("p_team"),
            project_data.get("p_segment"),                
            project_data.get("p_type"),
            project_data.get("p_s_date"),
            project_data.get("p_e_date"),
            project_data.get("job_id"),
            project_data.get("job_ol_id"),
            project_data.get("job_ra_id"),
            project_data.get("s_id"),
            project_data.get("ta_id"),
            project_data.get("pf_link"),
            project_data.get("p_status"),
            project_data.get("b_unit"),
            project_data.get("b_country"),
            project_data.get("b_name"),
            project_data.get("b_name_id"),
            project_data.get("market"),
            project_data.get("ir"),
            project_data.get("loi"),
            project_data.get("f_deliverables"),
            project_data.get("f_currency"),
            project_data.get("f_revenue"),
            project_data.get("f_cost"),
            project_data.get("f_nprofit"),
            project_data.get("f_margin"),
            project_data.get("f_remarks")
        )

        created_at = datetime.now(ZoneInfo("Asia/Kuala_Lumpur"))

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
                print(f"Project '{project_data.get('p_name')}' created successfully with DB ID: {cursor.lastrowid}")
                return cursor.lastrowid
            
        except sqlite3.IntegrityError as e:
            print(f"An error occurred: {e}")
            return None

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

#Project count
    def fetch_all_projects_count(self, query, params=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            print(f"Total projects count: {len(results)}")  
            return results

    def fetch_one_with_count(self, query, params=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            count = self.fetch_all_projects_count(query, params)
            print(f"Project count: {len(count)}")
            return result

#Project retrieval
    def get_all_projects(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects')
            return self.fetch_all_projects_count('SELECT * FROM projects')  
        
    def get_project_by_db_id(self, db_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE db_id = ?', (db_id,))
            return self.fetch_one_with_count('SELECT * FROM projects WHERE db_id = ?', (db_id,))  
    
    def get_projects_by_name_keyword(self, keyword):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE p_name LIKE ? COLLATE NOCASE ORDER BY p_name', (f'%{keyword}%',))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE p_name LIKE ? COLLATE NOCASE ORDER BY p_name', (f'%{keyword}%',))
    
    def get_projects_by_s_id(self, s_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE s_id = ?', (s_id,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE s_id = ?', (s_id,))
    
    def get_projects_by_p_segment(self, p_segment):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE p_segment = ?', (p_segment,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE p_segment = ?', (p_segment,))
    
    def get_projects_by_p_type(self, p_type):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE p_type = ?', (p_type,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE p_type = ?', (p_type,))  

    def get_projects_by_ta_id(self, ta_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE ta_id = ?', (ta_id,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE ta_id = ?', (ta_id,))    
    
    def get_projects_by_job_id(self, job_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE job_id = ?', (job_id,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE job_id = ?', (job_id,))  
        
    def get_projects_by_job_ol_id(self, job_ol_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE job_ol_id = ?', (job_ol_id,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE job_ol_id = ?', (job_ol_id,))      
    
    def get_projects_by_job_ra_id(self, job_ra_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE job_ra_id = ?', (job_ra_id,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE job_ra_id = ?', (job_ra_id,))  
    
    def get_projects_by_p_status(self, p_status):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE p_status = ?', (p_status,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE p_status = ?', (p_status,))
        
    def get_projects_by_p_manager(self, p_manager):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE p_manager = ?', (p_manager,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE p_manager = ?', (p_manager,))
        
    def get_projects_by_b_unit(self, b_unit):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE b_unit = ?', (b_unit,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE b_unit = ?', (b_unit,))
    
    def get_projects_by_b_country(self, b_country):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE b_country = ?', (b_country,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE b_country = ?', (b_country,))
    
    def get_projects_by_b_name(self, b_name):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE b_name = ?', (b_name,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE b_name = ?', (b_name,))
    
    def get_projects_by_b_status(self, b_status):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE b_status = ?', (b_status,))
            return self.fetch_all_projects_count('SELECT * FROM projects WHERE b_status = ?', (b_status,))

    def get_projects_by_f_margin_band(self, f_margin_band):
        """Filter projects by margin range."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            if f_margin_band == "0":
                cursor.execute('SELECT * FROM projects WHERE f_margin = 0')
                return self.fetch_all_projects_count('SELECT * FROM projects WHERE f_margin = 0')
            elif f_margin_band == "1%_to_19%":
                cursor.execute('SELECT * FROM projects WHERE f_margin BETWEEN 1 AND 19')
                return self.fetch_all_projects_count('SELECT * FROM projects WHERE f_margin BETWEEN 1 AND 19')
            elif f_margin_band == "20%_to_49%":
                cursor.execute('SELECT * FROM projects WHERE f_margin BETWEEN 20 AND 49')
                return self.fetch_all_projects_count('SELECT * FROM projects WHERE f_margin BETWEEN 20 AND 49')
            elif f_margin_band == "50%_to_79%":
                cursor.execute('SELECT * FROM projects WHERE f_margin BETWEEN 50 AND 79')
                return self.fetch_all_projects_count('SELECT * FROM projects WHERE f_margin BETWEEN 50 AND 79')
            elif f_margin_band == "80%_to_100%":
                cursor.execute('SELECT * FROM projects WHERE f_margin BETWEEN 80 AND 100')
                return self.fetch_all_projects_count('SELECT * FROM projects WHERE f_margin BETWEEN 80 AND 100')
            else: 
                return self.fetch_all_projects_count('SELECT * FROM projects')
            
    def get_projects_by_date_filter(self, month=None, year=None, since=False, date_type="start"):
        """Filter by month/year or since month/year for start or end date."""
        current_year = datetime.now().year

        col = "p_s_date" if date_type == "start" else "p_e_date"

        if month is not None:
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError("month must be between 1 and 12")

        if year is not None:
            year = int(year)

        if since:
            if month is not None and year is None:
                start_date = f"{current_year}-{month:02d}-01"
            elif month is not None and year is not None:
                start_date = f"{year}-{month:02d}-01"
            elif month is None and year is not None:
                start_date = f"{year}-01-01"
            else:
                return self.fetch_all_projects_count(f'SELECT * FROM projects ORDER BY "{col}"')

            return self.fetch_all_projects_count(
                f'SELECT * FROM projects WHERE "{col}" >= ? ORDER BY "{col}"',
                (start_date,)
            )

        if month is not None and year is None:
            return self.fetch_all_projects_count(
                f'''
                SELECT * FROM projects
                WHERE CAST(strftime('%m', "{col}") AS INTEGER) = ?
                  AND CAST(strftime('%Y', "{col}") AS INTEGER) = ?
                ORDER BY "{col}"
                ''',
                (month, current_year)
            )

        if month is not None and year is not None:
            return self.fetch_all_projects_count(
                f'''
                SELECT * FROM projects
                WHERE CAST(strftime('%m', "{col}") AS INTEGER) = ?
                AND CAST(strftime('%Y', "{col}") AS INTEGER) = ?
                ORDER BY "{col}"
                ''',
                (month, year)
            )

        if year is not None:
            return self.fetch_all_projects_count(
                f'''
                SELECT * FROM projects
                WHERE CAST(strftime('%Y', "{col}") AS INTEGER) = ?
                ORDER BY "{col}"
                ''',
                (year,)
            )

        return self.fetch_all_projects_count(f'SELECT * FROM projects ORDER BY "{col}"')
    
#Project update
    def update_project(self, db_id, **kwargs):
        if not kwargs:
            print("No fields provided for update.")
            return False

        allowed_fields = {
            "p_name", "p_manager", "p_team", "p_segment", "p_type",
            "p_status", "p_s_date", "p_e_date", "job_id", "job_ol_id",
            "job_ra_id", "s_id", "ta_id", "pf_link", "b_unit",
            "b_country", "b_name", "b_name_id", "market",
            "ir", "loi", "f_deliverables", "f_revenue", "f_cost",
            "f_nprofit", "f_margin", "f_remarks"
        }

        fields = []
        values = []

        for key, value in kwargs.items():
            if key not in allowed_fields:
                continue
            fields.append(f"{key} = ?")
            values.append(value)

        if not fields:
            print("No valid fields provided for update.")
            return False

        values.append(db_id)

        sql = f"UPDATE projects SET {', '.join(fields)} WHERE db_id = ?"

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()

            if cursor.rowcount > 0:
                print(f"Project {db_id} updated successfully.")
                return True
            else:
                print(f"No project found with db_id {db_id}.")
                return False

#Project deletion
    def delete_project(self, db_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM projects WHERE db_id = ?', (db_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"Project {db_id} deleted successfully.")
                return True
            else:
                print(f"No project found with db_id {db_id}.")
                return False
            
#Project display menu
    def display_menu(self):
        print("\n" + "="*30)
        print("Project Tracker Menu:")
        print("="*30)
        print("1. Project Creation")
        print("2. Project Retrieval")
        print("3. Project Update")
        print("4. Project Deletion")
        print("5. Exit")
        print("="*30)

    def main(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                print("\nProject Creation:")
                p_name = input("Project Name: ")
                p_manager = input("Project Manager: ")
                p_team = input("Project Team: ")
                p_segment = input("Project Segment: ")
                p_type = input("Project Type: ")
                p_s_date = self.to_sql_date(input("Start Date (DD-MM-YYYY): "))
                p_e_date_input = input("End Date (DD-MM-YYYY, optional): ")
                p_e_date = self.to_sql_date(p_e_date_input) if p_e_date_input else None
                job_id = str(input("Job ID: "))
                job_ol_id = str(input("Job OL ID: "))
                job_ra_id = str(input("Job RAES ID: "))
                s_id = str(input("SID: "))
                ta_id = int(input("TA ID: "))
                pf_link = input("Path Folder Link: ")
                p_status = input("Project Status: ")
                b_unit = input("Business Unit: ")
                b_country = input("Business Country: ")
                b_name = input("Business Name: ")
                b_name_id = int(input("Business Name ID: "))
                market = input("Market: ")
                ir = float(input("IR (%): "))
                loi = float(input("LOI (minutes): "))
                f_deliverables_input = input("Final Deliverables (optional): ")
                f_deliverables = int(f_deliverables_input) if f_deliverables_input else None
                f_currency_input = input("Final Currency (optional): ")
                f_currency = f_currency_input if f_currency_input else None
                f_revenue_input = input("Final Revenue (optional): ")
                f_revenue = float(f_revenue_input) if f_revenue_input else None
                f_cost_input = input("Final Cost (optional): ")
                f_cost = float(f_cost_input) if f_cost_input else None
                f_nprofit_input = input("Final Net Profit ($) (optional): ")
                f_nprofit = float(f_nprofit_input) if f_nprofit_input else None
                f_margin_input = input("Final Margin (%)(optional): ")
                f_margin = float(f_margin_input) if f_margin_input else None
                f_remarks_input = input("Final Remarks (optional): ")
                f_remarks = f_remarks_input if f_remarks_input else None
                
                project_data = {
                    "p_name": p_name,
                    "p_manager": p_manager,
                    "p_team": p_team,
                    "p_segment": p_segment,
                    "p_type": p_type,
                    "p_s_date": p_s_date,
                    "p_e_date": p_e_date,
                    "job_id": job_id,
                    "job_ol_id": job_ol_id,
                    "job_ra_id": job_ra_id,
                    "s_id": s_id,
                    "ta_id": ta_id,
                    "pf_link": pf_link,
                    "p_status": p_status,
                    "b_unit": b_unit,
                    "b_country": b_country,
                    "b_name": b_name,
                    "b_name_id": b_name_id,
                    "market": market,
                    "ir": ir,
                    "loi": loi,
                    "f_deliverables": f_deliverables,
                    "f_currency": f_currency,
                    "f_revenue": f_revenue,
                    "f_cost": f_cost,
                    "f_nprofit": f_nprofit,
                    "f_margin": f_margin,
                    "f_remarks": f_remarks
                }

                try:
                    db_id = self.create_project(project_data)                
                    if db_id: 
                        print(f"Project created successfully with ID: {db_id}")
                    else:
                        print("Failed to create project.")
                except ValueError as e:
                    print(f"Error creating project: {e}")
                
            elif choice == '2':
                print("\n" + "="*30)
                print("\nProject Retrieval:")
                print("="*30)
                print("1. Retrieve total project count")
                print("2. Retrieve all projects")
                print("3. Retrieve project by Database ID")
                print("4. Retrieve projects by Project Name")
                print("5. Retrieve projects by SID")
                print("6. Retrieve projects by Project Segment")
                print("7. Retrieve projects by Project Type")
                print("8. Retrieve projects by TA ID")
                print("9. Retrieve projects by Job ID")
                print("10. Retrieve projects by Job OL ID")
                print("11. Retrieve projects by Job RAES ID")
                print("12. Retrieve projects by Project Status")
                print("13. Retrieve projects by Project Manager")
                print("14. Retrieve projects by Business Unit")
                print("15. Retrieve projects by Business Country")
                print("16. Retrieve projects by Business Name")
                print("17. Retrieve projects by Final Margin Band")
                print("18. Retrieve projects by Date Filter")
                print("19. Back to Main Menu")
                sub_choice = input("Enter your choice (1-19): ")

                if sub_choice == '1':
                    projects = self.fetch_all_projects_count()
                    print(f"Total projects count: {len(projects)}")
                
                if sub_choice == '2':
                    projects = self.get_all_projects()
                    print(f"Total projects count: {len(projects)}")
                    for project in projects:
                        print(project)
                
                if sub_choice == '3':
                    try:
                        db_id = int(input("Enter Database ID: "))
                        project = self.get_project_by_db_id(db_id)
                        if project:
                            print(project)
                        else:
                            print(f"No project found with Database ID: {db_id}")
                    except ValueError as e:
                        print(f"Invalid input: {e}")

                if sub_choice == '4':
                    keyword = input("Enter project name keyword: ")
                    projects = self.get_projects_by_name_keyword(keyword)
                    if projects:
                        print(f"Projects matching '{keyword}':")
                        for i, project in enumerate(projects, start=1):
                            print(f"{i}. DB ID: {project[0]}, SID: {project[11]}, Project Name: {project[1]}, Project Manager: {project[2]}")
                        
                        selected_db_id = int(input("Enter the DB ID to view full project details: "))
                        project = self.get_project_by_db_id(selected_db_id)
                        print(project)
                    else:
                        print(f"No projects found matching '{keyword}'.")
                
                if sub_choice == '5':
                    try:
                        s_id = int(input("Enter SID: "))
                        projects = self.get_projects_by_s_id(s_id)
                        if projects:
                            print(f"Projects with SID {s_id}:")
                            for project in projects:
                                print(project)
                        else:
                            print(f"No projects found with SID: {s_id}")
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                
                if sub_choice == '6':
                    p_segment = input("Enter Project Segment: ")
                    projects = self.get_projects_by_p_segment(p_segment)
                    if projects:
                        print(f"Projects in Segment '{p_segment}':")
                        for project in projects:
                            print(project)
                    else:
                        print(f"No projects found in Segment: {p_segment}")
                
                if sub_choice == '7':
                    p_type = input("Enter Project Type: ")
                    projects = self.get_projects_by_p_type(p_type)
                    if projects:
                        print(f"Projects of Type '{p_type}':")
                        for project in projects:
                            print(project)
                    else:
                        print(f"No projects found of Type: {p_type}")

                if sub_choice == '8':
                    try:
                        ta_id = int(input("Enter TA ID: "))
                        projects = self.get_projects_by_ta_id(ta_id)
                        if projects:
                            print(f"Projects with TA ID {ta_id}:")
                            for project in projects:
                                print(project)
                        else:
                            print(f"No projects found with TA ID: {ta_id}")
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                
                if sub_choice == '9':
                    try:
                        job_id = int(input("Enter Job ID: "))
                        projects = self.get_projects_by_job_id(job_id)
                        if projects:
                            print(f"Projects with Job ID {job_id}:")
                            for project in projects:
                                print(project)
                        else:
                            print(f"No projects found with Job ID: {job_id}")
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                
                if sub_choice == '10':
                    try:
                        job_ol_id = int(input("Enter Job OL ID: "))
                        projects = self.get_projects_by_job_ol_id(job_ol_id)
                        if projects:
                            print(f"Projects with Job OL ID {job_ol_id}:")
                            for project in projects:
                                print(project)
                        else:
                            print(f"No projects found with Job OL ID: {job_ol_id}")
                    except ValueError as e:
                        print(f"Invalid input: {e}")

                if sub_choice == '11':
                    try:
                        job_ra_id = int(input("Enter Job RAES ID: "))
                        projects = self.get_projects_by_job_ra_id(job_ra_id)
                        if projects:
                            print(f"Projects with Job RAES ID {job_ra_id}:")
                            for project in projects:
                                print(project)
                        else:
                            print(f"No projects found with Job RAES ID: {job_ra_id}")
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                
                if sub_choice == '12':
                    p_status = input("Enter Project Status: ")
                    projects = self.get_projects_by_p_status(p_status)
                    if projects:
                        print(f"Projects with Status '{p_status}':")
                        for project in projects:
                            print(project)
                    else:
                        print(f"No projects found with Status: {p_status}")

                if sub_choice == '13':
                    p_manager = input("Enter Project Manager: ")
                    projects = self.get_projects_by_p_manager(p_manager)
                    if projects:
                        print(f"Projects managed by '{p_manager}':")
                        for project in projects:
                            print(project)
                    else:
                        print(f"No projects found managed by: {p_manager}")
                
                if sub_choice == '14':
                    b_unit = input("Enter Business Unit: ")
                    projects = self.get_projects_by_b_unit(b_unit)
                    if projects:
                        print(f"Projects in Business Unit '{b_unit}':")
                        for project in projects:
                            print(project)
                    else:
                        print(f"No projects found in Business Unit: {b_unit}")

                if sub_choice == '15':
                    b_country = input("Enter Business Country: ")
                    projects = self.get_projects_by_b_country(b_country)
                    if projects:
                        print(f"Projects in Business Country '{b_country}':")
                        for project in projects:
                            print(project)
                    else:
                        print(f"No projects found in Business Country: {b_country}")
                
                if sub_choice == '16':
                    b_name = input("Enter Business Name: ")
                    projects = self.get_projects_by_b_name(b_name)
                    if projects:
                        print(f"Projects for Business Name '{b_name}':")
                        for project in projects:
                            print(project)
                    else:
                        print(f"No projects found for Business Name: {b_name}")

                if sub_choice == '17':
                    print("Margin Bands:")
                    print("1. 0%")
                    print("2. 1% to 19%")
                    print("3. 20% to 49%")
                    print("4. 50% to 79%")
                    print("5. 80% to 100%")
                    margin_choice = input("Select a margin band (1-5): ")
                    margin_bands = {
                        '1': "0",
                        '2': "1%_to_19%",
                        '3': "20%_to_49%",
                        '4': "50%_to_79%",
                        '5': "80%_to_100%"
                    }
                    selected_band = margin_bands.get(margin_choice)
                    if selected_band:
                        projects = self.get_projects_by_f_margin_band(selected_band)
                        if projects:
                            print(f"Projects with Final Margin in '{selected_band}':")
                            for project in projects:
                                print(project)
                        else:
                            print(f"No projects found with Final Margin in: {selected_band}")
                    else:
                        print("Invalid margin band choice.")

                if sub_choice == '18':
                    date_type = input("Filter by Start Date or End Date? (enter 'start' or 'end'): ").strip().lower()
                    if date_type not in ['start', 'end']:
                        print("Invalid date type choice.")
                        continue

                    month_input = input("Enter month (1-12) for filtering (optional): ")
                    year_input = input("Enter year (e.g., 2024) for filtering (optional): ")
                    since_input = input("Filter projects since the specified month/year? (yes/no): ").strip().lower()

                    month = int(month_input) if month_input else None
                    year = int(year_input) if year_input else None
                    since = since_input == 'yes'

                    try:
                        projects = self.get_projects_by_date_filter(month=month, year=year, since=since, date_type=date_type)
                        if projects:
                            print(f"Projects filtered by {date_type} date:")
                            for project in projects:
                                print(project)
                        else:
                            print(f"No projects found for the specified date filter.")
                    except ValueError as e:
                        print(f"Invalid input: {e}")

                if sub_choice == '19':
                    print("Returning to Main Menu...")
                    continue
            
            elif choice == '3':
                print("\nProject Update:")
                db_id = int(input("Enter the Database ID of the project to update: "))
                print("\n" + "="*30)
                print("\nProject update:")
                print("="*30)
                print("1. Update Project Name")
                print("2. Update Project Manager")
                print("3. Update Project Team")
                print("4. Update Project Segment")
                print("5. Update Project Type")
                print("6. Update Start Date")
                print("7. Update End Date")
                print("8. Update Job ID")
                print("9. Update Job OL ID")
                print("10. Update Job RAES ID")
                print("11. Update SID")
                print("12. Update TAID")
                print("13. Update Path Folder Link")
                print("14. Update Project Status")
                print("15. Update Business Unit")
                print("16. Update Business Country")
                print("17. Update Business Name")
                print("18. Update Business Name ID")
                print("19. Update Market")
                print("20. Update IR")
                print("21. Update LOI")
                print("22. Update Final Deliverables")
                print("23. Update Final Currency")
                print("24. Update Final Revenue")
                print("25. Update Final Cost")
                print("26. Update Final Net Profit")
                print("27. Update Final Margin")
                print("28. Update Final Remarks")
                print("29. Back to Main Menu")
                update_choice = input("Enter your choice (1-29): ")

                field_mapping = {
                    '1': 'p_name',
                    '2': 'p_manager',
                    '3': 'p_team',
                    '4': 'p_segment',
                    '5': 'p_type',
                    '6': 'p_s_date',
                    '7': 'p_e_date',
                    '8': 'job_id',
                    '9': 'job_ol_id',
                    '10': 'job_ra_id',
                    '11': 's_id',
                    '12': 'ta_id',
                    '13': 'pf_link',
                    '14': 'p_status',
                    '15': 'b_unit',
                    '16': 'b_country',
                    '17': 'b_name',
                    '18': 'b_name_id',
                    '19': 'market',
                    '20': 'ir',
                    '21': 'loi',
                    '22': 'f_deliverables',
                    '23': 'f_currency',
                    '24': 'f_revenue',
                    '25': 'f_cost',
                    '26': 'f_nprofit',
                    '27': 'f_margin',
                    '28': 'f_remarks',
                    '29': None  
                }
                field_name = field_mapping.get(update_choice)
                if field_name:
                    new_value = input(f"Enter new value for {field_name}: ")
                    try:
                        if field_name in ['job_id', 'job_ol_id', 'job_ra_id', 's_id', 'ta_id', 'b_name_id', 'f_currency']:
                            new_value = int(new_value)
                        elif field_name in ['ir', 'f_revenue', 'f_cost', 'f_nprofit', 'f_margin']:
                            new_value = float(new_value)
                        elif field_name in ['p_s_date', 'p_e_date']:
                            new_value = self.to_sql_date(new_value)
                        
                        self.update_project(db_id, **{field_name: new_value})
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                else:
                    print("Invalid choice for update field.")
                
            elif choice == '4':
                print("\nProject Deletion:")
                try:
                    db_id = int(input("Enter the Database ID of the project to delete: "))
                    confirm = input(f"Please confirm to delete project (yes/no): \n"
                                    f"Database ID: {db_id} \n"
                                    f"Project Name: {p_name} \n")
                    if confirm.lower() == 'yes':
                        self.delete_project(db_id)
                        print(f"Project {db_id} {p_name} deleted successfully.")
                    else:
                        print("Project deletion canceled.")
                except ValueError as e:
                    print(f"Invalid input: {e}")

            elif choice == '5':
                print("Exiting Project Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
            
        input("\n Press Enter to continue...")

if __name__ == "__main__":
    db = DatabaseManager()
    db.main()
