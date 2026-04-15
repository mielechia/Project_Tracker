#Project Tracker API using FastAPI (endpoint implementations)

import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator, model_validator, validator
from typing import List, Optional
from datetime import date, datetime
from zoneinfo import ZoneInfo
from DB_Project_Tracker import DatabaseManager

app = FastAPI(title="Project Tracker API", version="1.0.0")

# --- Pydantic Models for Data Validation ---
class ProjectBase(BaseModel):
    p_name: str = Field(..., min_length=1, max_length=100)
    p_manager: str = Field(..., min_length=1, max_length=100)
    p_team: str = Field(..., min_length=1, max_length=100)
    p_segment: str = Field(..., min_length=1, max_length=100)
    p_type: str = Field(..., min_length=1, max_length=100)
    p_status: str = Field(..., min_length=1, max_length=100)
    p_s_date: date = Field(..., description="Project start date in DD-MM-YYYY format")
    p_e_date: Optional[date] = Field(None, description="Project end date in DD-MM-YYYY format")
    job_id: str = Field(..., max_length=12)
    job_ol_id: str = Field(..., max_length=15)
    job_ra_id: str = Field(..., max_length=15)
    s_id: str = Field(..., max_length=10)
    ta_id: int
    pf_link: str
    b_unit: str
    b_country: str
    b_name: str
    b_name_id: int
    market: str
    ir: float = Field(None, ge=0)
    loi: float = Field(None, ge=0)
    f_deliverables: Optional[int] = Field(None, ge=0)
    f_currency: Optional[str] = Field(None, max_length=3)
    f_revenue: Optional[float] = Field(None, ge=0)
    f_cost: Optional[float] = Field(None, ge=0)
    f_nprofit: Optional[float] = Field(None, ge=0)
    f_margin: Optional[float] = Field(None, ge=0)
    f_remarks: Optional[str] = None

    @field_validator("p_s_date", "p_e_date", mode="before")
    @classmethod
    def parse_ddmmyyyy(cls, v):
        if v is None:
            return v
        if isinstance(v, date):
            return v
        try:
            return datetime.strptime(v, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Date must be in DD-MM-YYYY format")
        
    @validator("p_s_date", "p_e_date")
    def parse_dates(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%d-%m-%Y").date()
            except ValueError:
                raise ValueError("Date must be in DD-MM-YYYY format")

        if isinstance(v, date):
            return v

        raise ValueError("Invalid date format")

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    p_name: Optional[str] = Field(None, min_length=1, max_length=100)
    p_manager: Optional[str] = Field(None, min_length=1, max_length=100)
    p_team: Optional[str] = Field(None, min_length=1, max_length=100)
    p_segment: Optional[str] = Field(None, min_length=1, max_length=100)
    p_type: Optional[str] = Field(None, min_length=1, max_length=100)
    p_status: Optional[str] = Field(None, min_length=1, max_length=100)
    p_s_date: Optional[date] = None 
    p_e_date: Optional[date] = None 
    job_id: Optional[str] = Field(None, max_length=12)
    job_ol_id: Optional[str] = Field(None, max_length=15)
    job_ra_id: Optional[str] = Field(None, max_length=15)
    s_id: Optional[str] = Field(None, max_length=10)
    ta_id: Optional[int] = None
    pf_link: Optional[str] = None
    b_unit: Optional[str] = None
    b_country: Optional[str] = None
    b_name: Optional[str] = None
    b_name_id: Optional[int] = None
    market: Optional[str] = None
    ir: Optional[float] = Field(None, max_length=2)
    loi: Optional[float] = Field(None, max_length=2)
    f_deliverables: Optional[int] = Field(None, ge=0)
    f_currency: Optional[str] = Field(None, max_length=3)
    f_revenue: Optional[float] = Field(None, ge=0)
    f_cost: Optional[float] = Field(None, ge=0)
    f_nprofit: Optional[float] = Field(None, ge=0)
    f_margin: Optional[float] = Field(None, ge=0)
    f_remarks: Optional[str] = None

    @validator("p_s_date", "p_e_date")
    def parse_dates(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%d-%m-%Y").date()
            except ValueError:
                raise ValueError("Date must be in DD-MM-YYYY format")

        if isinstance(v, date):
            return v

        raise ValueError("Invalid date format")
        
class ProjectResponse(BaseModel):
    db_id: int
    p_name: str
    p_manager: str
    p_team: str
    p_segment: str
    p_type: str
    p_status: str
    p_s_date: date
    p_e_date: Optional[date]
    job_id: str
    job_ol_id: str
    job_ra_id: str
    s_id: str
    ta_id: int
    pf_link: str
    b_unit: str
    b_country: str
    b_name: str
    b_name_id: int
    market: str
    ir: float
    loi: float
    f_deliverables: Optional[int]
    f_currency: Optional[str]
    f_revenue: Optional[float]
    f_cost: Optional[float]
    f_nprofit: Optional[float]
    f_margin: Optional[float]
    f_remarks: Optional[str]
    created_at: Optional[datetime] = None

def parse_datetime(value):
    if value:
        try:
            return datetime.fromisoformat(value)
        except:
            return None
    return None

class ProjectListResponse(BaseModel):
    message: str
    count: int
    projects: List[ProjectResponse]

# --- Database Initialization ---
db = DatabaseManager()

def project_field(project):
    return ProjectResponse(
        db_id=project[0], p_name=project[1], p_manager=project[2], p_team=project[3], p_segment=project[4],
        p_type=project[5], p_status=project[6], p_s_date=project[7], p_e_date=project[8], job_id=project[9],
        job_ol_id=project[10], job_ra_id=project[11], s_id=project[12], ta_id=project[13], pf_link=project[14],
        b_unit=project[15], b_country=project[16], b_name=project[17], b_name_id=project[18], market=project[19],
        ir=project[20], loi=project[21], f_deliverables=project[22], f_currency=project[23], f_revenue=project[24], 
        f_cost=project[25],f_nprofit=project[26], f_margin=project[27], f_remarks=project[28], created_at=parse_datetime(project[29])
    )

# --- API Endpoints ---
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Project Tracker API!", "version": "1.0.0"}

# --- Create Project ---
@app.post("/projects/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    try:
        project_data = project.model_dump()

        project_data["p_s_date"] = project_data["p_s_date"].isoformat()
        if project_data.get("p_e_date"):
            project_data["p_e_date"] = project_data["p_e_date"].isoformat()

        created_at = datetime.now().isoformat()
        project_data["created_at"] = created_at

        db_id = db.create_project(project_data)

        if db_id:
            return ProjectResponse(db_id=db_id, **project_data)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Failed to create project (Integrity or Database Error)")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while creating the project: {e}")

# --- Retrieve All Projects ---
@app.get("/projects/", response_model=ProjectListResponse)
async def get_all_projects():
    try:
        projects = db.get_all_projects()
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": "Projects retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")

#--- Filter Projects with Optional Parameters ---
@app.get("/projects/filter/", response_model=ProjectListResponse)
async def filter_projects(
    p_name: Optional[str] = None, 
    s_id: Optional[str] = None, 
    p_segment: Optional[str] = None, 
    p_type: Optional[str] = None, 
    ta_id: Optional[int] = None, 
    job_id: Optional[int] = None, 
    job_ol_id: Optional[int] = None, 
    job_ra_id: Optional[int] = None, 
    p_status: Optional[str] = None, 
    p_manager: Optional[str] = None, 
    b_unit: Optional[str] = None, 
    b_country: Optional[str] = None, 
    b_name: Optional[str] = None, 
    b_status: Optional[str] = None, 
    margin_band: Optional[str] = None):
    
    try:
        projects = db.filter_projects(name=p_name, sid=s_id, segment=p_segment, type=p_type, ta_id=ta_id,
                                      job_id=job_id, job_ol_id=job_ol_id, job_ra_id=job_ra_id,
                                      status=p_status, manager=p_manager, business_unit=b_unit,
                                      business_country=b_country, business_name=b_name,
                                      business_status=b_status, margin_band=margin_band)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": "Projects retrieved successfully with applied filters!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while filtering projects: {e}")

#Retrieve Project by Database ID
@app.get("/projects/id/{db_id}")
async def get_project_by_db_id(db_id: int):
    try:
        project = db.get_project_by_db_id(db_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        formatted_project = project_field(project)
        
        return {
            "message": f"Project with ID '{db_id}' retrieved successfully!",
            "count": len([formatted_project]),
            "projects": [formatted_project] 
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving the project: {e}")

#Retrieve Projects by Project Name Keyword (Case-Insensitive)
@app.get("/projects/search/{keyword}", response_model=ProjectListResponse)
async def get_projects_by_name_keyword(keyword: str):
    try:
        projects = db.get_projects_by_name_keyword(keyword)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects matching '{keyword}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while searching for projects: {e}")

#Retrieve Projects by Project SID
@app.get("/projects/sid/{sid}", response_model=ProjectListResponse)
async def get_projects_by_s_id(sid: str):
    try:
        projects = db.get_projects_by_s_id(sid)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with SID '{sid}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")

#Retrieve Projects by Project Segment
@app.get("/projects/segment/{segment}", response_model=ProjectListResponse)
async def get_projects_by_p_segment(segment: str):
    try:
        projects = db.get_projects_by_p_segment(segment)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects in segment '{segment}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")

#Retrieve Projects by Project Type
@app.get("/projects/type/{type}", response_model=ProjectListResponse)
async def get_projects_by_p_type(p_type: str):
    try:
        projects = db.get_projects_by_p_type(p_type)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with type '{p_type}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")
    
#Retrieve Projects by Project TA ID
@app.get("/projects/ta_id/{ta_id}", response_model=ProjectListResponse)
async def get_projects_by_ta_id(ta_id: int):
    try:
        projects = db.get_projects_by_ta_id(ta_id)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with TA ID '{ta_id}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}") 

#Retrieve Projects by Project Job ID
@app.get("/projects/job_id/{job_id}", response_model=ProjectListResponse)
async def get_projects_by_job_id(job_id: str):
    try:
        projects = db.get_projects_by_job_id(job_id)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with Job ID '{job_id}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")

#Retrieve Projects by Project Job OL ID
@app.get("/projects/job_ol_id/{job_ol_id}", response_model=ProjectListResponse)
async def get_projects_by_job_ol_id(job_ol_id: str):
    try:
        projects = db.get_projects_by_job_ol_id(job_ol_id)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with Job OL ID '{job_ol_id}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")

#Retrieve Projects by Project Job RA ID
@app.get("/projects/job_ra_id/{job_ra_id}", response_model=ProjectListResponse)
async def get_projects_by_job_ra_id(job_ra_id: str):   
    try:
        projects = db.get_projects_by_job_ra_id(job_ra_id)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with Job RA ID '{job_ra_id}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}") 

#Retrieve Projects by Project Status
@app.get("/projects/status/{p_status}", response_model=ProjectListResponse)
async def get_projects_by_p_status(p_status: str):
    try:
        projects = db.get_projects_by_p_status(p_status)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with status '{p_status}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")
    
#Retrieve Projects by Project Manager
@app.get("/projects/manager/{manager}", response_model=ProjectListResponse)
async def get_projects_by_p_manager(p_manager: str):
    try:
        projects = db.get_projects_by_p_manager(p_manager)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with manager '{p_manager}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}") 

#Retrieve Projects by Project Business Unit
@app.get("/projects/business_unit/{b_unit}", response_model=ProjectListResponse)
async def get_projects_by_b_unit(b_unit: str):
    try:
        projects = db.get_projects_by_b_unit(b_unit)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects in business unit '{b_unit}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}") 

#Retrieve Projects by Project Business Country   
@app.get("/projects/business_country/{b_country}", response_model=ProjectListResponse)
async def get_projects_by_b_country(b_country: str):
    try:
        projects = db.get_projects_by_b_country(b_country)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects in business country '{b_country}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")
    
#Retrieve Projects by Project Business Name
@app.get("/projects/business_name/{b_name}", response_model=ProjectListResponse)
async def get_projects_by_b_name(b_name: str):
    try:
        projects = db.get_projects_by_b_name(b_name)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with business name '{b_name}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")
    
#Retrieve Projects by Project Business Status
@app.get("/projects/business_status/{b_status}", response_model=ProjectListResponse)
async def get_projects_by_b_status(b_status: str):
    try:
        projects = db.get_projects_by_b_status(b_status)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with business status '{b_status}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")
    
#Retrieve Projects by Project Margin Band
@app.get("/projects/margin_band/{f_margin_band}", response_model=ProjectListResponse)
async def get_projects_by_f_margin_band(f_margin_band: str):
    try:
        projects = db.get_projects_by_f_margin_band(f_margin_band)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with margin band '{f_margin_band}' retrieved successfully!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects: {e}")
    
#Retrieve Projects by Project Date Filter
@app.get("/projects/filter/date", response_model=ProjectListResponse)
async def get_projects_by_date(
    month: Optional[int] = None, 
    year: Optional[int] = None, 
    since: bool = False, 
    date_type: str = "start"):
    if date_type not in ["start", "end"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="date_type must be 'start' or 'end'")
    try:
        projects = db.get_projects_by_date_filter(month=month, year=year, since=since, date_type=date_type)
        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects retrieved successfully using '{date_type}' date filter!", 
            "count": len(formatted_projects),
            "projects": formatted_projects
        }

    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while retrieving projects by date: {e}") 

#--- Update Project by Database ID ---
@app.put("/projects/{db_id}")
async def update_project_by_db_id(db_id: int, updates: ProjectUpdate):
    try:
        update_data = updates.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

        success = db.update_project(db_id, **update_data)
        if success:
            updated_project = db.get_project_by_db_id(db_id)
            formatted = project_field(updated_project)
            return {
                "message": f"Project with ID '{db_id}' updated successfully!",
                "count": 1,
                "projects": [formatted]
            }
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Project with ID '{db_id}' not found")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while updating the project: {e}")

#--- Delete Project by Database ID ---
@app.delete("/projects/{db_id}")
async def delete_project_by_db_id(db_id: int):
    try:
        project = db.get_project_by_db_id(db_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Project with ID '{db_id}' not found")
        
        success = db.delete_project(db_id)
        if success:
            return {"message": f"Project with ID '{db_id}' deleted successfully!",
                    "count": 0, 
                    "projects": []}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Project with ID '{db_id}' not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred while deleting the project: {e}")

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

