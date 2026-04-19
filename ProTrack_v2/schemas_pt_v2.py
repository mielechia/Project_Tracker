# Project Tracker API using FastAPI (endpoint implementations)

from fastapi import FastAPI, HTTPException, status, APIRouter, Query, Depends
from pydantic import BaseModel, Field, field_validator, model_validator, validator
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import List, Optional
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from db_pt_v2 import DatabaseManager
from collections import defaultdict
from google import genai
import os
import requests

ai_router = APIRouter()
app = FastAPI(title="Project Tracker API", version="1.0.0")

SECRET_KEY = "abc123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SUPERUSER_REGISTER_CODE = "super123"
ADMIN_REGISTER_CODE = "admin123"


# --- Pydantic Models for Data Validation ---
class ProjectBase(BaseModel):
    p_name: str = Field(..., min_length=1, max_length=100)
    p_manager: str = Field(..., min_length=1, max_length=100)
    p_team: str = Field(..., min_length=1, max_length=100)
    p_segment: str = Field(..., min_length=1, max_length=100)
    p_type: str = Field(..., min_length=1, max_length=100)
    p_status: str = Field(..., min_length=1, max_length=100)
    p_s_date: date = Field(..., description="Project start date in DD-MM-YYYY format")
    p_e_date: Optional[date] = Field(
        None, description="Project end date in DD-MM-YYYY format"
    )
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
    ir: float = Field(ge=0, le=100.0)
    loi: float = Field(ge=0)
    f_deliverables: Optional[int] = Field(None, ge=0)
    f_currency: Optional[str] = Field(None, max_length=3)
    f_revenue: Optional[float] = Field(None, ge=0)
    f_cost: Optional[float] = Field(None, ge=0)
    f_nprofit: Optional[float] = Field(None)
    f_margin: Optional[float] = Field(None)
    f_remarks: Optional[str] = None

    # To change date format
    # @field_validator("p_s_date", "p_e_date", mode="before")
    # @classmethod
    # def parse_ddmmyyyy(cls, v):
    #     if v is None:
    #         return v
    #     if isinstance(v, date):
    #         return v
    #     try:
    #         return datetime.strptime(v, "%d-%m-%Y").date()
    #     except ValueError:
    #         raise ValueError("Date must be in DD-MM-YYYY format")

    # @validator("p_s_date", "p_e_date")
    # def parse_dates(cls, v):
    #     if isinstance(v, str):
    #         try:
    #             return datetime.strptime(v, "%d-%m-%Y").date()
    #         except ValueError:
    #             raise ValueError("Date must be in DD-MM-YYYY format")

    #     if isinstance(v, date):
    #         return v

    #     raise ValueError("Invalid date format")


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
    ir: Optional[float] = Field(None, ge=0, le=100)
    loi: Optional[float] = Field(None, ge=0)
    f_deliverables: Optional[int] = Field(None, ge=0)
    f_currency: Optional[str] = Field(None, max_length=3)
    f_revenue: Optional[float] = Field(None, ge=0)
    f_cost: Optional[float] = Field(None, ge=0)
    f_nprofit: Optional[float] = None
    f_margin: Optional[float] = None
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


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    role: str
    role_code: Optional[str] = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        value = value.lower()
        if value not in {"user", "superuser", "admin"}:
            raise ValueError("Role must be user, superuser, or admin")
        return value


class UpdateUserRoleRequest(BaseModel):
    role: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        value = value.lower()
        if value not in {"user", "superuser", "admin"}:
            raise ValueError("Invalid role")
        return value


def require_roles(allowed_roles: list[str]):
    allowed_roles = [r.lower() for r in allowed_roles]

    def checker(current_user=Depends(get_current_user)):
        current_role = str(current_user[3]).lower()
        if current_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user

    return checker


class ChangeOwnPasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6, max_length=128)


class UserResponse(BaseModel):
    user_id: int
    username: str
    role: str
    is_active: bool
    created_at: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str


class ResetPasswordRequest(BaseModel):
    new_password: str = Field(..., min_length=6, max_length=128)


class UpdateUserStatusRequest(BaseModel):
    is_active: bool


class AIInsightSchema(BaseModel):
    id: int
    manager: str
    period: str
    summary: str
    created_at: datetime

    class Config:
        from_attributes = True


def get_start_date(period: str):
    now = datetime.now()

    mapping = {"daily": 1, "weekly": 7, "monthly": 30, "yearly": 365}

    days = mapping.get(period, 30)
    return now - timedelta(days=days)


def get_genai_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set")
    return genai.Client(api_key=api_key)


def get_kl_time_string():
    kl_now = datetime.now(ZoneInfo("Asia/Kuala_Lumpur"))
    return kl_now.strftime("%A, %d %B %Y, %H:%M")


def is_weather_question(text: str) -> bool:
    if not text:
        return False

    lower_text = text.lower()
    weather_keywords = [
        "weather",
        "temperature",
        "forecast",
        "rain",
        "raining",
        "humid",
        "humidity",
        "wind",
        "sunny",
        "cloudy",
        "storm",
        "thunderstorm",
        "hot today",
        "cold today",
    ]
    return any(keyword in lower_text for keyword in weather_keywords)


def fetch_live_weather(location: str = "Kuala Lumpur"):
    api_key = os.getenv("WEATHERAPI_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="WEATHERAPI_KEY is not set")

    response = requests.get(
        "https://api.weatherapi.com/v1/current.json",
        params={"key": api_key, "q": location, "aqi": "no"},
        timeout=15,
    )

    if response.status_code != 200:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text

        raise HTTPException(
            status_code=500, detail=f"Weather API request failed: {error_detail}"
        )

    data = response.json()

    location_data = data.get("location", {})
    current_data = data.get("current", {})

    return {
        "name": location_data.get("name", location),
        "region": location_data.get("region", ""),
        "country": location_data.get("country", ""),
        "localtime": location_data.get("localtime", ""),
        "condition": current_data.get("condition", {}).get("text", "Unknown"),
        "temp_c": current_data.get("temp_c"),
        "feelslike_c": current_data.get("feelslike_c"),
        "humidity": current_data.get("humidity"),
        "wind_kph": current_data.get("wind_kph"),
        "wind_dir": current_data.get("wind_dir"),
        "precip_mm": current_data.get("precip_mm"),
        "cloud": current_data.get("cloud"),
        "last_updated": current_data.get("last_updated"),
    }


# --- Database Initialization ---
db = DatabaseManager()


def project_field(project):
    return ProjectResponse(
        db_id=project[0],
        p_name=project[1],
        p_manager=project[2],
        p_team=project[3],
        p_segment=project[4],
        p_type=project[5],
        p_status=project[6],
        p_s_date=project[7],
        p_e_date=project[8],
        job_id=project[9],
        job_ol_id=project[10],
        job_ra_id=project[11],
        s_id=project[12],
        ta_id=project[13],
        pf_link=project[14],
        b_unit=project[15],
        b_country=project[16],
        b_name=project[17],
        b_name_id=project[18],
        market=project[19],
        ir=project[20],
        loi=project[21],
        f_deliverables=project[22],
        f_currency=project[23],
        f_revenue=project[24],
        f_cost=project[25],
        f_nprofit=project[26],
        f_margin=project[27],
        f_remarks=project[28],
        created_at=parse_datetime(project[29]),
    )


def row_to_user_response(user):
    if hasattr(user, "keys"):
        return {
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"],
            "is_active": bool(user["is_active"]),
            "created_at": user["created_at"],
        }

    if len(user) >= 6:
        # e.g. user_id, username, password_hash, role, is_active, created_at
        return {
            "user_id": user[0],
            "username": user[1],
            "role": user[3],
            "is_active": bool(user[4]),
            "created_at": user[5],
        }

    return {
        "user_id": user[0],
        "username": user[1],
        "role": user[2],
        "is_active": bool(user[3]),
        "created_at": user[4],
    }


def hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > 128:
        raise HTTPException(
            status_code=400, detail="Password too long. Max 128 characters."
        )
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str):
    user = db.get_user_by_username(username)
    if not user:
        return None
    if not bool(user[4]):
        return None
    if not verify_password(password, user[2]):
        return None
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.get_user_by_username(username)
    if not user or not bool(user[4]):
        raise credentials_exception
    return user


def require_roles(allowed_roles: list[str]):
    def checker(current_user=Depends(get_current_user)):
        if current_user[3] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user

    return checker


def get_visible_projects_for_user(current_user):
    role = current_user["role"] if hasattr(current_user, "keys") else current_user[3]
    username = (
        current_user["username"] if hasattr(current_user, "keys") else current_user[1]
    )

    if role in ["superuser", "admin"]:
        return db.get_all_projects()

    return db.get_projects_by_p_manager(username)


def get_role_and_username(current_user):
    if hasattr(current_user, "keys"):
        return current_user["role"], current_user["username"]
    return current_user[3], current_user[1]


def enforce_project_access(project, current_user, action: str):
    role, username = get_role_and_username(current_user)

    if role in ["superuser", "admin"]:
        return

    project_manager = project["p_manager"] if hasattr(project, "keys") else project[2]

    if project_manager != username:
        raise HTTPException(
            status_code=403,
            detail=f"You can only {action} your own projects",
        )


# --- API Endpoints ---
@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Project Tracker API!", "version": "1.0.0"}


@app.post("/register")
async def register_user(user: UserRegister):
    existing_user = db.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    requested_role = user.role

    SUPERUSER_REGISTER_CODE = "super123"
    ADMIN_REGISTER_CODE = "admin123"

    if requested_role == "superuser":
        if user.role_code != SUPERUSER_REGISTER_CODE:
            raise HTTPException(
                status_code=403,
                detail="Invalid superuser registration code",
            )

    if requested_role == "admin":
        if user.role_code != ADMIN_REGISTER_CODE:
            raise HTTPException(
                status_code=403,
                detail="Invalid admin registration code",
            )

    user_id = db.create_user(
        user.username,
        hash_password(user.password),
        requested_role,
    )

    if not user_id:
        raise HTTPException(status_code=400, detail="Failed to create user")

    created_user = db.get_user_by_id(user_id)
    return {
        "message": "User created successfully",
        "user": row_to_user_response(created_user),
    }


@app.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token({"sub": user[1], "role": user[3]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user[1],
        "role": user[3],
    }


@app.get("/me")
async def read_me(current_user=Depends(get_current_user)):
    return row_to_user_response(current_user)


@app.get(
    "/users",
    response_model=List[UserResponse],
)
async def get_all_users(
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    users = db.get_all_users()
    role = current_user[3]
    username = current_user[1]

    if role == "admin":
        visible_users = users
    elif role == "superuser":
        visible_users = [
            u for u in users if row_to_user_response(u)["role"] in ["user", "superuser"]
        ]
    else:
        visible_users = [
            u for u in users if row_to_user_response(u)["username"] == username
        ]

    return [row_to_user_response(user) for user in visible_users]


@app.put(
    "/users/{user_id}/password",
    dependencies=[Depends(require_roles(["admin", "superuser"]))],
)
async def reset_user_password(
    user_id: int,
    payload: ResetPasswordRequest,
    current_user=Depends(get_current_user),
):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    target_user_id = user[0]
    target_role = str(
        user[2]
    ).lower()  # get_user_by_id -> user_id, username, role, is_active, created_at
    current_user_id = current_user[0]
    current_role = str(current_user[3]).lower()

    if current_role == "superuser":
        if target_user_id == current_user_id:
            raise HTTPException(
                status_code=400,
                detail="Use /me/password to change your own password",
            )
        if target_role != "user":
            raise HTTPException(
                status_code=403,
                detail="Superuser can only reset passwords for users with role 'user'",
            )

    ok = db.update_user_password(user_id, hash_password(payload.new_password))
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to reset password")

    return {"message": "Password reset successfully"}


@app.post(
    "/users",
    response_model=UserResponse,
)
async def create_user_admin(
    payload: UserRegister,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    existing_user = db.get_user_by_username(payload.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    creator_role = current_user[3]
    target_role = payload.role

    if creator_role in ["user", "superuser"] and target_role != "user":
        raise HTTPException(status_code=403, detail="You can only create user accounts")

    user_id = db.create_user(
        payload.username, hash_password(payload.password), target_role
    )
    if not user_id:
        raise HTTPException(status_code=400, detail="Failed to create user")
    return row_to_user_response(db.get_user_by_id(user_id))


@app.put(
    "/users/{user_id}/role",
    response_model=UserResponse,
    dependencies=[Depends(require_roles(["admin"]))],
)
async def update_user_role(user_id: int, payload: UpdateUserRoleRequest):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user[3] == "admin" and payload.role != "admin" and db.count_active_admins() <= 1:
        raise HTTPException(
            status_code=400, detail="At least one active admin must remain"
        )
    if not db.update_user_role(user_id, payload.role):
        raise HTTPException(status_code=400, detail="Failed to update role")
    return row_to_user_response(db.get_user_by_id(user_id))


@app.put("/users/{user_id}/password")
async def reset_user_password(
    user_id: int,
    payload: ResetPasswordRequest,
    current_user=Depends(require_roles(["superuser", "admin"])),
):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    actor_role = current_user[3]
    target_role = row_to_user_response(user)["role"]

    if actor_role == "superuser" and target_role != "user":
        raise HTTPException(status_code=403, detail="You can only reset user passwords")

    ok = db.update_user_password(user_id, hash_password(payload.new_password))
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to reset password")
    return {"message": "Password reset successfully"}


@app.put("/me/password")
async def change_own_password(
    payload: ChangeOwnPasswordRequest,
    current_user=Depends(get_current_user),
):
    if not verify_password(payload.current_password, current_user[2]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    if payload.current_password == payload.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from current password",
        )

    ok = db.update_user_password(current_user[0], hash_password(payload.new_password))
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to update password")

    return {"message": "Password updated successfully"}


@app.put(
    "/users/{user_id}/status",
    response_model=UserResponse,
    dependencies=[Depends(require_roles(["admin", "superuser"]))],
)
async def update_user_status(
    user_id: int,
    payload: UpdateUserStatusRequest,
    current_user=Depends(get_current_user),
):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    target_user_id = user[0]
    target_role = str(user[2]).lower()
    current_user_id = current_user[0]
    current_role = str(current_user[3]).lower()

    if target_user_id == current_user_id and payload.is_active is False:
        raise HTTPException(
            status_code=400,
            detail="You cannot deactivate your own current account",
        )

    if current_role == "superuser":
        if target_user_id == current_user_id:
            raise HTTPException(
                status_code=403,
                detail="Superuser cannot change their own status here",
            )
        if target_role != "user":
            raise HTTPException(
                status_code=403,
                detail="Superuser can only activate/deactivate users with role 'user'",
            )

    if (
        target_role == "admin"
        and payload.is_active is False
        and db.count_active_admins() <= 1
    ):
        raise HTTPException(
            status_code=400,
            detail="At least one active admin must remain",
        )

    ok = db.update_user_status(user_id, payload.is_active)
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to update status")

    return row_to_user_response(db.get_user_by_id(user_id))


# --- Create Project ---
@app.post(
    "/projects/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED
)
async def create_project(
    project: ProjectCreate,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        project_data = project.model_dump()

        revenue = project_data.get("f_revenue")
        cost = project_data.get("f_cost")

        if revenue is not None and cost is not None:
            net_profit = revenue - cost
            project_data["f_nprofit"] = net_profit

            if revenue != 0:
                project_data["f_margin"] = round((net_profit / revenue) * 100, 2)
            else:
                project_data["f_margin"] = 0

        if hasattr(current_user, "keys"):
            role = current_user["role"]
            username = current_user["username"]
        else:
            role = current_user[3]
            username = current_user[1]

        if role == "user":
            project_data["p_manager"] = username

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
            detail="Failed to create project (Integrity or Database Error)",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the project: {e}",
        )


# --- Retrieve All Projects ---
@app.get(
    "/projects/",
    response_model=ProjectListResponse,
)
async def get_all_projects(
    current_user=Depends(require_roles(["user", "superuser", "admin"]))
):
    try:
        if hasattr(current_user, "keys"):
            role = current_user["role"]
            username = current_user["username"]
        else:
            role = current_user[3]
            username = current_user[1]

        if role == "user":
            projects = db.get_projects_by_p_manager(username)
        else:
            projects = get_visible_projects_for_user(current_user)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": "Projects retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# --- Filter Projects with Optional Parameters ---
@app.get(
    "/projects/filter/",
    response_model=ProjectListResponse,
)
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
    margin_band: Optional[str] = None,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):

    try:
        projects = db.filter_projects(
            name=p_name,
            sid=s_id,
            segment=p_segment,
            type=p_type,
            ta_id=ta_id,
            job_id=job_id,
            job_ol_id=job_ol_id,
            job_ra_id=job_ra_id,
            status=p_status,
            manager=p_manager,
            business_unit=b_unit,
            business_country=b_country,
            business_name=b_name,
            business_status=b_status,
            margin_band=margin_band,
        )

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": "Projects retrieved successfully with applied filters!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while filtering projects: {e}",
        )


# Retrieve Project by Database ID
@app.get(
    "/projects/id/{db_id}",
)
async def get_project_by_db_id(
    db_id: int,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        project = db.get_project_by_db_id(db_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )
        enforce_project_access(project, current_user, "view")

        formatted_project = project_field(project)

        return {
            "message": f"Project with ID '{db_id}' retrieved successfully!",
            "count": len([formatted_project]),
            "projects": [formatted_project],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the project: {e}",
        )


# Retrieve Projects by Project Name Keyword (Case-Insensitive)
@app.get(
    "/projects/search/{keyword}",
    response_model=ProjectListResponse,
)
async def get_projects_by_name_keyword(
    keyword: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_name_keyword(keyword)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects matching '{keyword}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while searching for projects: {e}",
        )


# Retrieve Projects by Project SID
@app.get(
    "/projects/sid/{sid}",
    response_model=ProjectListResponse,
)
async def get_projects_by_s_id(
    sid: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_s_id(sid)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with SID '{sid}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Segment
@app.get(
    "/projects/segment/{segment}",
    response_model=ProjectListResponse,
)
async def get_projects_by_p_segment(
    segment: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_p_segment(segment)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects in segment '{segment}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Type
@app.get(
    "/projects/type/{type}",
    response_model=ProjectListResponse,
)
async def get_projects_by_p_type(
    p_type: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_p_type(p_type)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with type '{p_type}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project TA ID
@app.get(
    "/projects/ta_id/{ta_id}",
    response_model=ProjectListResponse,
)
async def get_projects_by_ta_id(
    ta_id: int,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_ta_id(ta_id)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with TA ID '{ta_id}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Job ID
@app.get(
    "/projects/job_id/{job_id}",
    response_model=ProjectListResponse,
)
async def get_projects_by_job_id(
    job_id: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_job_id(job_id)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with Job ID '{job_id}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Job OL ID
@app.get(
    "/projects/job_ol_id/{job_ol_id}",
    response_model=ProjectListResponse,
)
async def get_projects_by_job_ol_id(
    job_ol_id: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_job_ol_id(job_ol_id)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with Job OL ID '{job_ol_id}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Job RA ID
@app.get(
    "/projects/job_ra_id/{job_ra_id}",
    response_model=ProjectListResponse,
)
async def get_projects_by_job_ra_id(
    job_ra_id: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_job_ra_id(job_ra_id)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with Job RA ID '{job_ra_id}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Status
@app.get(
    "/projects/status/{p_status}",
    response_model=ProjectListResponse,
)
async def get_projects_by_p_status(
    p_status: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_p_status(p_status)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with status '{p_status}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Manager
@app.get(
    "/projects/manager/{manager}",
    response_model=ProjectListResponse,
)
async def get_projects_by_p_manager(
    p_manager: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_p_manager(p_manager)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with manager '{p_manager}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Business Unit
@app.get(
    "/projects/business_unit/{b_unit}",
    response_model=ProjectListResponse,
)
async def get_projects_by_b_unit(
    b_unit: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_b_unit(b_unit)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects in business unit '{b_unit}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Business Country
@app.get(
    "/projects/business_country/{b_country}",
    response_model=ProjectListResponse,
)
async def get_projects_by_b_country(
    b_country: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_b_country(b_country)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects in business country '{b_country}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Business Name
@app.get(
    "/projects/business_name/{b_name}",
    response_model=ProjectListResponse,
)
async def get_projects_by_b_name(
    b_name: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_b_name(b_name)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with business name '{b_name}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Business Status
@app.get(
    "/projects/business_status/{b_status}",
    response_model=ProjectListResponse,
)
async def get_projects_by_b_status(
    b_status: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_b_status(b_status)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with business status '{b_status}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Margin Band
@app.get(
    "/projects/margin_band/{f_margin_band}",
    response_model=ProjectListResponse,
)
async def get_projects_by_f_margin_band(
    f_margin_band: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = db.get_projects_by_f_margin_band(f_margin_band)

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects with margin band '{f_margin_band}' retrieved successfully!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects: {e}",
        )


# Retrieve Projects by Project Date Filter
@app.get(
    "/projects/filter/date",
    response_model=ProjectListResponse,
)
async def get_projects_by_date(
    month: Optional[int] = None,
    year: Optional[int] = None,
    since: bool = False,
    date_type: str = "start",
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    if date_type not in ["start", "end"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="date_type must be 'start' or 'end'",
        )
    try:
        projects = db.get_projects_by_date_filter(
            month=month, year=year, since=since, date_type=date_type
        )

        formatted_projects = [project_field(project) for project in projects]

        return {
            "message": f"Projects retrieved successfully using '{date_type}' date filter!",
            "count": len(formatted_projects),
            "projects": formatted_projects,
        }

    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving projects by date: {e}",
        )


# --- Update Project by Database ID ---
@app.put(
    "/projects/{db_id}",
    response_model=ProjectResponse,
)
async def update_project_by_db_id(
    db_id: int,
    updates: ProjectUpdate,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        update_data = updates.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )

        existing_project = db.get_project_by_db_id(db_id)

        if not existing_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID '{db_id}' not found",
            )

        if hasattr(current_user, "keys"):
            role = current_user["role"]
            username = current_user["username"]
        else:
            role = current_user[3]
            username = current_user[1]

        project_manager = (
            existing_project["p_manager"]
            if hasattr(existing_project, "keys")
            else existing_project[2]
        )

        if role == "user" and project_manager != username:
            raise HTTPException(
                status_code=403,
                detail="You can only update your own projects",
            )

        if "p_s_date" in update_data and update_data["p_s_date"]:
            update_data["p_s_date"] = update_data["p_s_date"].isoformat()

        if "p_e_date" in update_data and update_data["p_e_date"]:
            update_data["p_e_date"] = update_data["p_e_date"].isoformat()

        # validate dates using updated values if provided, otherwise existing values
        start_date = update_data.get("p_s_date", existing_project[7])
        end_date = update_data.get("p_e_date", existing_project[8])

        if start_date and end_date and end_date < start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project end date cannot be before project start date",
            )

        # auto recalculate net profit + margin
        current_revenue = existing_project[24]
        current_cost = existing_project[25]

        revenue = update_data.get("f_revenue", current_revenue)
        cost = update_data.get("f_cost", current_cost)

        if revenue is not None and cost is not None:
            net_profit = float(revenue) - float(cost)
            update_data["f_nprofit"] = round(net_profit, 2)

            if float(revenue) != 0:
                update_data["f_margin"] = round((net_profit / float(revenue)) * 100, 2)
            else:
                update_data["f_margin"] = 0.0

        success = db.update_project(db_id, **update_data)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID '{db_id}' not found",
            )

        updated_project = db.get_project_by_db_id(db_id)

        if not updated_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Updated project with ID '{db_id}' could not be retrieved",
            )

        return project_field(updated_project)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the project: {e}",
        )


# --- Delete Project by Database ID ---
@app.delete("/projects/{db_id}")
async def delete_project_by_db_id(
    db_id: int, current_user=Depends(require_roles(["user", "superuser", "admin"]))
):
    try:
        project = db.get_project_by_db_id(db_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID '{db_id}' not found",
            )

        if hasattr(current_user, "keys"):
            role = current_user["role"]
            username = current_user["username"]
        else:
            role = current_user[3]
            username = current_user[1]

        project_manager = (
            project["p_manager"] if hasattr(project, "keys") else project[2]
        )

        if role == "user" and project_manager != username:
            raise HTTPException(
                status_code=403,
                detail="You can only delete your own projects",
            )

        success = db.delete_project(db_id)
        if success:
            return {
                "message": f"Project with ID '{db_id}' deleted successfully!",
                "count": 0,
                "projects": [],
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID '{db_id}' not found",
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the project: {e}",
        )


# --- AI Insights ---
@ai_router.get(
    "/ai/manager-summary/",
)
def manager_summary(
    period: str = "monthly",
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = get_visible_projects_for_user(current_user)

        summary = defaultdict(lambda: {"total": 0, "completed": 0, "active": 0})

        for p in projects:
            manager = p[2] or "Unknown"
            status = p[6] or "Unknown"

            summary[manager]["total"] += 1

            if str(status).lower() == "completed":
                summary[manager]["completed"] += 1
            else:
                summary[manager]["active"] += 1

        return {"period": period, "summary": dict(summary)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate manager summary: {str(e)}"
        )


@ai_router.get(
    "/ai/llm-summary/",
)
def llm_summary(
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        client = get_genai_client()
        projects = get_visible_projects_for_user(current_user)

        project_data = "\n".join(f"- {p[1]} | {p[6]} | {p[2]}" for p in projects)

        system_prompt = """
        You are a professional business/data analyst.

        Use the provided project data to analyse and summarize:
        1. Overall project performance
        2. Manager productivity
        3. Completion trends
        4. Risks or bottlenecks

        Be concise, structured, and actionable.
        """

        prompt = f"""{system_prompt}

        Project Data:
        {project_data}

        Provide a structured summary.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", contents=prompt
        )

        return {"ai_summary": response.text}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate LLM summary: {str(e)}"
        )


@ai_router.get("/ai/report/")
async def generate_report(
    period: str = Query("weekly"),
    manager: Optional[str] = None,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):

    try:
        projects = get_visible_projects_for_user(current_user)
        start_date = get_start_date(period)

        filtered = []
        for p in projects:
            created_at_raw = p[29] if len(p) > 29 else None
            if not created_at_raw:
                continue

            try:
                created_at = datetime.fromisoformat(created_at_raw)
            except Exception:
                continue

            if created_at >= start_date:
                filtered.append(p)

        if manager and manager != "All":
            filtered = [p for p in filtered if p[2] == manager]

        total = len(filtered)
        completed = sum(1 for p in filtered if str(p[6] or "").lower() == "completed")
        active = total - completed
        completion_rate = round((completed / total) * 100, 2) if total else 0

        workload = "high" if active > completed else "balanced"
        performance = "strong" if completion_rate >= 70 else "needs improvement"
        trend = "positive" if completed >= active else "warning"

        manager_label = manager if manager and manager != "All" else "All Managers"

        report = f"""📊 {period.upper()} PROJECT REPORT

        📌 Scope:
        - Manager: {manager_label}

        📌 Summary:
        - Total Projects: {total}
        - Completed: {completed}
        - Active: {active}
        - Completion Rate: {completion_rate}%

        📈 Insights:
        - Workload: {workload}
        - Performance: {performance}
        - Trend: {trend}
        """.strip()

        return {
            "period": period,
            "manager": manager_label,
            "start_date": start_date.isoformat(),
            "total_projects": total,
            "completed": completed,
            "active": active,
            "completion_rate": completion_rate,
            "insights": {
                "workload": workload,
                "performance": performance,
                "trend": trend,
            },
            "report": report,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate AI report: {str(e)}"
        )


@ai_router.post("/ai/chat/")
async def ai_chat(
    query: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        user_query = (query or "").strip()
        lower_query = user_query.lower()
        kl_time_str = get_kl_time_string()

        if not user_query:
            return {"response": "Please enter a question first."}

        # -----------------------------------
        # Live weather path
        # -----------------------------------
        if is_weather_question(user_query):
            weather = fetch_live_weather("Kuala Lumpur")

            # If Gemini is available, let it present the weather more naturally
            if os.getenv("GEMINI_API_KEY"):
                client = get_genai_client()

                weather_prompt = f"""
                    You are a helpful AI assistant.

                    Current context:
                    - Location: Kuala Lumpur, Malaysia
                    - Kuala Lumpur time now: {kl_time_str}

                    The user asked:
                    "{user_query}"

                    Live weather data:
                    - Location: {weather['name']}, {weather['country']}
                    - Local time: {weather['localtime']}
                    - Condition: {weather['condition']}
                    - Temperature: {weather['temp_c']}°C
                    - Feels like: {weather['feelslike_c']}°C
                    - Humidity: {weather['humidity']}%
                    - Wind: {weather['wind_kph']} kph ({weather['wind_dir']})
                    - Precipitation: {weather['precip_mm']} mm
                    - Cloud cover: {weather['cloud']}%
                    - Last updated: {weather['last_updated']}

                    Instructions:
                    - Answer naturally and clearly.
                    - Use the live weather data above.
                    - Keep it concise and helpful.
                    - Mention that the weather shown is for Kuala Lumpur unless the user asked otherwise.
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite", contents=weather_prompt
                )

                reply_text = getattr(response, "text", None)
                if reply_text:
                    return {"response": reply_text.strip()}

            # Fallback: return weather directly without Gemini
            return {
                "response": (
                    f"Current weather for {weather['name']}, {weather['country']}:\n\n"
                    f"- Condition: {weather['condition']}\n"
                    f"- Temperature: {weather['temp_c']}°C\n"
                    f"- Feels like: {weather['feelslike_c']}°C\n"
                    f"- Humidity: {weather['humidity']}%\n"
                    f"- Wind: {weather['wind_kph']} kph ({weather['wind_dir']})\n"
                    f"- Precipitation: {weather['precip_mm']} mm\n"
                    f"- Cloud cover: {weather['cloud']}%\n"
                    f"- Local time: {weather['localtime']}\n"
                    f"- Last updated: {weather['last_updated']}"
                )
            }

        # -----------------------------------
        # Fallback mode when Gemini is not configured
        # -----------------------------------
        if not os.getenv("GEMINI_API_KEY"):
            projects = db.get_all_projects()
            total_projects = len(projects)
            completed = sum(
                1 for p in projects if str(p[6] or "").lower() == "completed"
            )
            active = total_projects - completed

            if lower_query in ["hi", "hello", "hey", "helo", "heelo"]:
                return {
                    "response": (
                        f"Hello! 👋\n\n"
                        f"Current time in Kuala Lumpur: {kl_time_str}\n\n"
                        f"I can help with project insights right now. "
                        f"Enable GEMINI_API_KEY to unlock full general AI features."
                    )
                }

            return {
                "response": (
                    f"Gemini AI is not enabled yet.\n\n"
                    f"Quick local summary:\n"
                    f"- Total Projects: {total_projects}\n"
                    f"- Completed: {completed}\n"
                    f"- Active: {active}"
                )
            }

        # -----------------------------------
        # Gemini mode for project/general chat
        # -----------------------------------
        client = get_genai_client()
        projects = get_visible_projects_for_user(current_user)

        lower_q = query.lower()

        if "low margin" in lower_q or "low margins" in lower_q:
            low_projects = []

            for p in projects:
                margin = p[27]

                if margin is not None and float(margin) < 20:
                    low_projects.append(
                        f"- {p[1]} | Margin: {margin}% | Profit: {p[26]}"
                    )

            if low_projects:
                return {
                    "response": "Projects with low margins (<20%):\n\n"
                    + "\n".join(low_projects)
                }
            else:
                return {"response": "No projects with low margins found."}

        project_data = "\n".join(
            [
                f"""
            Project Name: {p[1]}
            Manager: {p[2]}
            Status: {p[6]}
            Revenue: {p[24]}
            Cost: {p[25]}
            Net Profit: {p[26]}
            Margin: {p[27]}
            """.strip()
                for p in projects
            ]
        )

        prompt = f"""
            You are a smart AI assistant within a project tracking system.

            ===================================
            CONTEXT
            ===================================
            Location: Kuala Lumpur, Malaysia
            Local Time: {kl_time_str}

            ===================================
            MODE 1: PROJECT ANALYST
            ===================================
            Use the available project data when the question relates to:
            - projects
            - managers
            - performance
            - trends
            - workload
            - profit or margin
            - operations

            Analysis Guidelines:
            - Make reasonable assumptions based on available data
            - Identify patterns (e.g. many active vs completed projects)
            - Compare managers where possible
            - Highlight potential concerns (e.g. backlog, low completion)
            - Provide practical, actionable insights
            
            If user asks about:
            - low margins → use Margin field
            - profit → use Net Profit field
            Always list project names and values when possible.

            Important:
            - Do NOT say "insufficient data" unless absolutely necessary
            - Use what is available to generate meaningful insights

            Response Style:
            - Be concise and structured
            - Use bullet points where helpful
            - Keep it professional and clear

            ===================================
            MODE 2: GENERAL ASSISTANT
            ===================================
            If the question is NOT related to project data:
            - Answer naturally like a normal AI assistant
            - Do NOT force project context into the answer
            - Only mention limitations if real-time or external data is required

            ===================================
            USER QUESTION
            ===================================
            {user_query}

            ===================================
            PROJECT DATA
            ===================================
            {project_data}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", contents=prompt
        )

        reply_text = getattr(response, "text", None)

        if not reply_text:
            return {"response": "I couldn’t generate a response. Please try again."}

        return {"response": reply_text.strip()}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI chat failed: {str(e)}")


# Admin Settings
@app.get("/reports/projects")
async def project_report(
    period: str,
    manager: Optional[str] = None,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    try:
        projects = get_visible_projects_for_user(current_user)
        now = datetime.now()

        def parse_created_at(p):
            created_at_raw = p[29] if len(p) > 29 else None
            if not created_at_raw:
                return None
            try:
                return datetime.fromisoformat(created_at_raw)
            except Exception:
                return None

        def filter_by_period(created_at):
            if not created_at:
                return False

            if period == "daily":
                return created_at.date() == now.date()
            elif period == "weekly":
                return created_at >= now - timedelta(days=7)
            elif period == "monthly":
                return created_at.month == now.month and created_at.year == now.year
            elif period == "yearly":
                return created_at.year == now.year
            return False

        filtered = []
        for p in projects:
            created_at = parse_created_at(p)
            if filter_by_period(created_at):
                filtered.append(p)

        if manager and manager != "All":
            filtered = [p for p in filtered if p[2] == manager]

        if len(filtered) == 0:
            return {
                "period": period,
                "manager": manager,
                "count": 0,
                "total_profit": 0,
                "avg_margin": 0,
                "projects": [],
                "message": "No data in selected time range",
            }

        total_profit = sum((p[26] or 0) for p in filtered)

        margins = [p[27] for p in filtered if p[27] is not None]
        avg_margin = round(sum(margins) / len(margins), 2) if margins else 0

        project_list = [
            {
                "db_id": p[0],
                "p_name": p[1],
                "p_manager": p[2],
                "p_status": p[6],
                "p_s_date": p[7],
                "created_at": p[29],
            }
            for p in filtered
        ]

        return {
            "period": period,
            "manager": manager,
            "count": len(filtered),
            "total_profit": round(total_profit, 2),
            "avg_margin": avg_margin,
            "projects": project_list,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate project report: {str(e)}"
        )


@app.put("/me/password")
async def change_own_password(
    payload: ChangeOwnPasswordRequest,
    current_user=Depends(get_current_user),
):
    if not verify_password(payload.current_password, current_user[2]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    if payload.current_password == payload.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from current password",
        )

    ok = db.update_user_password(current_user[0], hash_password(payload.new_password))
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to update password")

    return {"message": "Password updated successfully"}


@app.delete("/users/{user_id}")
async def delete_user_admin(
    user_id: int,
    current_user=Depends(require_roles(["admin", "superuser"])),
):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    target_user_id = user[0]
    target_role = str(user[2]).lower()
    current_user_id = current_user[0]
    current_role = str(current_user[3]).lower()

    if target_user_id == current_user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own current account",
        )

    if current_role == "superuser" and target_role != "user":
        raise HTTPException(
            status_code=403,
            detail="Superuser can only delete users with role 'user'",
        )

    if target_role == "admin" and db.count_active_admins() <= 1:
        raise HTTPException(
            status_code=400,
            detail="At least one active admin must remain",
        )

    ok = db.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Failed to delete user")

    return {"message": "User deleted successfully"}


app.include_router(ai_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
