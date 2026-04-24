# Project Tracker API using FastAPI (endpoint implementations)

from fastapi import FastAPI, HTTPException, status, APIRouter, Query, Depends
from pydantic import BaseModel, Field, field_validator, model_validator, validator
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import List, Optional
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from db_pt_v3 import DatabaseManager
from collections import defaultdict
from google import genai
import os
import requests
from io import BytesIO

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
    f_revenue_usd: Optional[float] = Field(None)
    f_cost_usd: Optional[float] = Field(None)
    f_nprofit_usd: Optional[float] = Field(None)
    exchange_rate: Optional[float] = Field(None)
    exchange_rate_source: Optional[str] = None
    exchange_rate_date: Optional[str] = None
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
    f_revenue_usd: Optional[float] = None
    f_cost_usd: Optional[float] = None
    f_nprofit_usd: Optional[float] = None
    exchange_rate: Optional[float] = None
    exchange_rate_source: Optional[str] = None
    exchange_rate_date: Optional[str] = None
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
    f_revenue_usd: Optional[float] = None
    f_cost_usd: Optional[float] = None
    f_nprofit_usd: Optional[float] = None
    exchange_rate: Optional[float] = None
    exchange_rate_source: Optional[str] = None
    exchange_rate_date: Optional[str] = None
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


def get_usd_exchange_rate(from_currency: Optional[str]):
    """Return rate to convert one unit of from_currency into USD using ExchangeRate-API."""
    currency = (from_currency or "USD").strip().upper()
    if currency == "USD":
        return 1.0, "ExchangeRate-API", datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).isoformat()

    api_key = os.getenv("EXCHANGERATE_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="EXCHANGERATE_API_KEY is not set. Add your free ExchangeRate-API key before creating non-USD projects.",
        )

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{currency}/USD"
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Exchange rate API request failed: {response.text}")

    data = response.json()
    if data.get("result") != "success" or data.get("conversion_rate") is None:
        raise HTTPException(status_code=500, detail=f"Exchange rate API returned an invalid response: {data}")

    rate_date = data.get("time_last_update_utc") or datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).isoformat()
    return float(data["conversion_rate"]), "ExchangeRate-API", rate_date


def apply_usd_financials(project_data: dict):
    """Calculate and store USD values using the project currency at creation/update time."""
    currency = (project_data.get("f_currency") or "USD").strip().upper()
    project_data["f_currency"] = currency

    revenue = project_data.get("f_revenue")
    cost = project_data.get("f_cost")
    net_profit = project_data.get("f_nprofit")

    if revenue is None and cost is None and net_profit is None:
        return project_data

    rate, source, rate_date = get_usd_exchange_rate(currency)

    if revenue is not None:
        project_data["f_revenue_usd"] = round(float(revenue) * rate, 2)
    if cost is not None:
        project_data["f_cost_usd"] = round(float(cost) * rate, 2)
    if net_profit is not None:
        project_data["f_nprofit_usd"] = round(float(net_profit) * rate, 2)

    project_data["exchange_rate"] = rate
    project_data["exchange_rate_source"] = source
    project_data["exchange_rate_date"] = rate_date
    return project_data


def usd_profit_from_row(project):
    if len(project) > 32 and project[32] is not None:
        return float(project[32])
    return float(project[26] or 0)


def fmt_usd(value):
    return f"USD {float(value or 0):,.2f}"


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
        f_revenue_usd=project[30] if len(project) > 30 else None,
        f_cost_usd=project[31] if len(project) > 31 else None,
        f_nprofit_usd=project[32] if len(project) > 32 else None,
        exchange_rate=project[33] if len(project) > 33 else None,
        exchange_rate_source=project[34] if len(project) > 34 else None,
        exchange_rate_date=project[35] if len(project) > 35 else None,
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
    db.auto_complete_overdue_projects()
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


@app.get("/reports/projects/pdf")
async def project_report_pdf(
    period: str,
    manager: Optional[str] = None,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    """Generate a nicely formatted PDF report using USD analysis values."""
    try:
        report_data = await project_report(period=period, manager=manager, current_user=current_user)

        buffer = BytesIO()
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"ReportLab is required for PDF export: {exc}")

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="TitleBlue", parent=styles["Title"], textColor=colors.HexColor("#1F4E79"), fontSize=22, leading=26))
        styles.add(ParagraphStyle(name="SmallGrey", parent=styles["Normal"], textColor=colors.HexColor("#666666"), fontSize=9))
        styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], textColor=colors.HexColor("#1F4E79"), fontSize=14, spaceBefore=14))

        story = []
        title = f"Project Performance Report - {period.capitalize()}"
        story.append(Paragraph(title, styles["TitleBlue"]))
        story.append(Paragraph(f"Manager: {manager or 'All'} | Generated: {get_kl_time_string()} | Currency Basis: USD", styles["SmallGrey"]))
        story.append(Spacer(1, 0.2 * inch))

        kpi_data = [
            ["Total Projects", "Total Net Profit (USD)", "Average Margin"],
            [str(report_data.get("count", 0)), fmt_usd(report_data.get("total_profit", 0)), f"{report_data.get('avg_margin', 0)}%"],
        ]
        kpi_table = Table(kpi_data, colWidths=[2.1 * inch, 2.3 * inch, 2.1 * inch])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF2F8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D6DBDF")),
            ("BACKGROUND", (0, 1), (-1, 1), colors.white),
            ("FONTSIZE", (0, 1), (-1, 1), 13),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 0.25 * inch))

        story.append(Paragraph("Matching Projects", styles["Section"]))
        rows = [["DB ID", "Project", "Manager", "Status", "USD Net Profit"]]
        for project in report_data.get("projects", []):
            rows.append([
                str(project.get("db_id", "-")),
                Paragraph(str(project.get("p_name", "Unnamed Project")), styles["Normal"]),
                Paragraph(str(project.get("p_manager", "-")), styles["Normal"]),
                str(project.get("p_status", "-")),
                fmt_usd(project.get("f_nprofit_usd", 0)),
            ])
        if len(rows) == 1:
            rows.append(["-", "No projects found", "-", "-", "-"])

        table = Table(rows, colWidths=[0.6 * inch, 2.1 * inch, 1.4 * inch, 1.0 * inch, 1.4 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D6DBDF")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9F9")]),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("Note: Financial analysis is converted and stored in USD at project creation/update using the configured exchange-rate API.", styles["SmallGrey"]))

        doc.build(story)
        buffer.seek(0)
        filename = f"project_report_{period}_{(manager or 'all').replace(' ', '_')}.pdf"
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF report: {str(e)}")


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

        project_data = apply_usd_financials(project_data)

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
        db.auto_complete_overdue_projects()
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
        current_currency = existing_project[23]

        revenue = update_data.get("f_revenue", current_revenue)
        cost = update_data.get("f_cost", current_cost)
        currency = update_data.get("f_currency", current_currency)

        if revenue is not None and cost is not None:
            net_profit = float(revenue) - float(cost)
            update_data["f_nprofit"] = round(net_profit, 2)

            if float(revenue) != 0:
                update_data["f_margin"] = round((net_profit / float(revenue)) * 100, 2)
            else:
                update_data["f_margin"] = 0.0

        if any(field in update_data for field in ["f_currency", "f_revenue", "f_cost", "f_nprofit"]):
            conversion_payload = {
                "f_currency": currency,
                "f_revenue": revenue,
                "f_cost": cost,
                "f_nprofit": update_data.get("f_nprofit", existing_project[26]),
            }
            conversion_payload = apply_usd_financials(conversion_payload)
            update_data.update({
                "f_revenue_usd": conversion_payload.get("f_revenue_usd"),
                "f_cost_usd": conversion_payload.get("f_cost_usd"),
                "f_nprofit_usd": conversion_payload.get("f_nprofit_usd"),
                "exchange_rate": conversion_payload.get("exchange_rate"),
                "exchange_rate_source": conversion_payload.get("exchange_rate_source"),
                "exchange_rate_date": conversion_payload.get("exchange_rate_date"),
            })

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

        project_data = "\n".join(f"- {p[1]} | {p[6]} | {p[2]} | Profit: {fmt_usd(usd_profit_from_row(p))}" for p in projects)

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


def _safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default


def _project_created_date(project):
    raw = project[29] if len(project) > 29 else None
    if not raw:
        return None
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).date()
    except Exception:
        try:
            return datetime.strptime(str(raw)[:10], "%Y-%m-%d").date()
        except Exception:
            return None


def _filter_projects_for_query(query: str, projects: list):
    q = (query or "").lower()
    today = datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).date()

    if "today" in q or "daily" in q:
        return [p for p in projects if _project_created_date(p) == today], "today"

    if "this week" in q or "weekly" in q or "week" in q:
        start = today - timedelta(days=7)
        return [p for p in projects if (_project_created_date(p) and _project_created_date(p) >= start)], "last 7 days"

    if "this month" in q or "monthly" in q or "month" in q:
        return [p for p in projects if (_project_created_date(p) and _project_created_date(p).year == today.year and _project_created_date(p).month == today.month)], "this month"

    if "this year" in q or "yearly" in q or "year" in q:
        return [p for p in projects if (_project_created_date(p) and _project_created_date(p).year == today.year)], "this year"

    return projects, "all available projects"


def _manager_performance_rows(projects: list):
    managers = defaultdict(lambda: {
        "projects": 0,
        "completed": 0,
        "active": 0,
        "low_margin": 0,
        "profit": 0.0,
        "margin_total": 0.0,
        "margin_count": 0,
    })

    for p in projects:
        manager = p[2] or "Unknown"
        status = str(p[6] or "").lower()
        margin = _safe_float(p[27], 0)
        profit = usd_profit_from_row(p)

        managers[manager]["projects"] += 1
        managers[manager]["profit"] += profit
        managers[manager]["margin_total"] += margin
        managers[manager]["margin_count"] += 1

        if status == "completed":
            managers[manager]["completed"] += 1
        elif status == "field":
            managers[manager]["active"] += 1

        if margin < 20:
            managers[manager]["low_margin"] += 1

    rows = []
    for manager, data in managers.items():
        total = data["projects"]
        completion = round((data["completed"] / total) * 100, 2) if total else 0
        avg_margin = round(data["margin_total"] / data["margin_count"], 2) if data["margin_count"] else 0
        score = (data["profit"] / max(total, 1)) + (completion * 100) + (avg_margin * 50) - (data["low_margin"] * 500)
        rows.append({
            "manager": manager,
            "projects": total,
            "completed": data["completed"],
            "active": data["active"],
            "completion_rate": completion,
            "avg_margin": avg_margin,
            "low_margin": data["low_margin"],
            "profit": round(data["profit"], 2),
            "score": score,
        })
    return rows


def generate_local_project_analysis(query: str, projects: list):
    q = (query or "").lower()
    filtered, scope = _filter_projects_for_query(q, projects)

    if not filtered:
        return f"No matching project records found for {scope}. Try a wider period such as monthly, yearly, or all projects."

    total = len(filtered)
    completed = sum(1 for p in filtered if str(p[6] or "").lower() == "completed")
    active = sum(1 for p in filtered if str(p[6] or "").lower() == "field")
    completion_rate = round((completed / total) * 100, 2) if total else 0
    total_profit = round(sum(usd_profit_from_row(p) for p in filtered), 2)
    margins = [_safe_float(p[27], 0) for p in filtered if p[27] is not None]
    avg_margin = round(sum(margins) / len(margins), 2) if margins else 0
    low_margin_projects = [p for p in filtered if _safe_float(p[27], 0) < 20]

    manager_rows = _manager_performance_rows(filtered)
    top_manager = max(manager_rows, key=lambda r: r["profit"], default=None)
    underperformers = sorted(manager_rows, key=lambda r: r["score"])[:3]

    if any(word in q for word in ["underperform", "weak", "poor", "bottom", "needs review", "manager"]):
        lines = [
            "📉 Underperforming Manager Review (USD)",
            f"Scope: {scope} | Projects reviewed: {total}",
            "",
            "Managers requiring closer review:",
        ]
        for idx, row in enumerate(underperformers, start=1):
            lines.append(
                f"{idx}. {row['manager']} — {row['projects']} project(s), "
                f"completion {row['completion_rate']}%, avg margin {row['avg_margin']}%, "
                f"low-margin projects {row['low_margin']}, total USD profit {fmt_usd(row['profit'])}"
            )
        lines += [
            "",
            "Recommended actions:",
            "- Review low-margin projects first and check whether cost or pricing is causing the gap.",
            "- Follow up on active projects that have not moved to completed status.",
            "- Compare each manager by USD profit, completion rate, and margin rather than project count only.",
        ]
        return "\n".join(lines)

    if "low margin" in q or "low margins" in q or "margin" in q:
        top_low = sorted(low_margin_projects, key=lambda p: _safe_float(p[27], 0))[:10]
        lines = [
            "⚠️ Low-Margin Project Review",
            f"Scope: {scope} | Low-margin projects: {len(low_margin_projects)}",
            "",
        ]
        if top_low:
            lines.append("Projects to review first:")
            for p in top_low:
                lines.append(
                    f"- {p[1]} | Manager: {p[2]} | Margin: {_safe_float(p[27], 0)}% | USD Profit: {fmt_usd(usd_profit_from_row(p))}"
                )
        else:
            lines.append("No low-margin projects found under the selected scope.")
        return "\n".join(lines)

    if any(word in q for word in ["risk", "risks", "overdue", "attention", "watchout", "watchouts"]):
        today = datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).date()
        overdue = []
        for p in filtered:
            status = str(p[6] or "").lower()
            end_raw = p[8] if len(p) > 8 else None
            try:
                end_date = datetime.fromisoformat(str(end_raw)).date() if end_raw else None
            except Exception:
                end_date = None
            if status == "field" and end_date and end_date < today:
                overdue.append(p)
        lines = [
            "🚨 Project Risk Review",
            f"Scope: {scope} | Projects reviewed: {total}",
            f"- Overdue active projects: {len(overdue)}",
            f"- Low-margin projects: {len(low_margin_projects)}",
            f"- Active / in-field projects: {active}",
            "",
            "Recommended focus:",
            "- Clear overdue active projects first.",
            "- Review low-margin projects before they affect overall profitability.",
            "- Check managers with many active projects but low completion rate.",
        ]
        return "\n".join(lines)

    return "\n".join([
        "📊 Project Performance Summary (USD)",
        f"Scope: {scope}",
        "",
        f"📦 Total Projects: {total}",
        f"✅ Completed: {completed}",
        f"🚧 Active / Field: {active}",
        f"📊 Completion Rate: {completion_rate}%",
        f"💰 Total Net Profit: {fmt_usd(total_profit)}",
        f"💹 Average Margin: {avg_margin}%",
        "",
        "📈 Highlights:",
        f"- Top manager by USD profit: {top_manager['manager'] if top_manager else 'N/A'} ({fmt_usd(top_manager['profit']) if top_manager else 'USD 0.00'}).",
        f"- {completed} project(s) are completed under this scope.",
        "",
        "⚠️ Watchouts:",
        f"- {len(low_margin_projects)} low-margin project(s) below 20% margin.",
        f"- {active} active/in-field project(s) may need follow-up depending on timeline.",
        "",
        "📌 Takeout:",
        "Overall performance is positive." if total_profit > 0 else "Overall performance needs review because total USD net profit is not positive.",
    ])


def is_project_analysis_question(query: str):
    q = (query or "").lower()
    keywords = [
        "project", "projects", "manager", "managers", "performance", "summary", "summarise", "summarize",
        "overview", "report", "reports", "profit", "net profit", "usd", "margin", "low margin",
        "monthly", "weekly", "daily", "yearly", "trend", "trends", "risk", "risks", "overdue",
        "active", "completed", "underperform", "underperforming", "workload", "delivery", "field"
    ]
    return any(word in q for word in keywords)


@ai_router.post("/ai/chat/")
async def ai_chat(
    query: str,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    user_query = (query or "").strip()
    lower_query = user_query.lower()
    kl_time_str = get_kl_time_string()

    if not user_query:
        return {"response": "Please enter a question first."}

    if lower_query in ["hi", "hello", "hey", "helo", "heelo"]:
        return {"response": "Hi! 👋 You can ask me about project performance, manager trends, low margins, risks, reports, or general questions."}

    if is_weather_question(user_query):
        try:
            weather = fetch_live_weather("Kuala Lumpur")
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
        except Exception as e:
            return {"response": f"Live weather is not available right now. Please check WEATHERAPI_KEY or connection. Details: {str(e)}"}

    projects = get_visible_projects_for_user(current_user)

    if is_project_analysis_question(user_query):
        local_analysis = generate_local_project_analysis(user_query, projects)

        if os.getenv("GEMINI_API_KEY"):
            try:
                client = get_genai_client()
                prompt = f"""
                You are a project performance analyst for a project tracking system.
                Rewrite the analysis below into a concise management-ready answer.
                Keep all numbers exactly as provided. Do not invent figures.

                User question: {user_query}
                Local analysis:
                {local_analysis}
                """
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite", contents=prompt
                )
                reply_text = getattr(response, "text", None)
                if reply_text:
                    return {"response": reply_text.strip()}
            except Exception:
                pass

        return {"response": local_analysis}

    if os.getenv("GEMINI_API_KEY"):
        try:
            client = get_genai_client()
            prompt = f"""
            You are a helpful AI assistant inside a project tracker app.
            Current Kuala Lumpur time: {kl_time_str}
            Answer the user's general question naturally and concisely.

            User question: {user_query}
            """
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite", contents=prompt
            )
            reply_text = getattr(response, "text", None)
            if reply_text:
                return {"response": reply_text.strip()}
        except Exception:
            pass

    return {
        "response": (
            "I can help with that. For project-related questions, I can analyse USD profit, margins, managers, risks, and monthly/weekly performance. "
            "For general questions, please make sure the Gemini API key has available quota."
        )
    }


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

        total_profit = sum(usd_profit_from_row(p) for p in filtered)

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
                "f_currency": p[23],
                "f_nprofit": p[26],
                "f_nprofit_usd": p[32] if len(p) > 32 else p[26],
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


@app.get("/reports/projects/pdf")
async def project_report_pdf(
    period: str,
    manager: Optional[str] = None,
    current_user=Depends(require_roles(["user", "superuser", "admin"])),
):
    """Generate a nicely formatted PDF report using USD analysis values."""
    try:
        report_data = await project_report(period=period, manager=manager, current_user=current_user)

        buffer = BytesIO()
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"ReportLab is required for PDF export: {exc}")

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="TitleBlue", parent=styles["Title"], textColor=colors.HexColor("#1F4E79"), fontSize=22, leading=26))
        styles.add(ParagraphStyle(name="SmallGrey", parent=styles["Normal"], textColor=colors.HexColor("#666666"), fontSize=9))
        styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], textColor=colors.HexColor("#1F4E79"), fontSize=14, spaceBefore=14))

        story = []
        title = f"Project Performance Report - {period.capitalize()}"
        story.append(Paragraph(title, styles["TitleBlue"]))
        story.append(Paragraph(f"Manager: {manager or 'All'} | Generated: {get_kl_time_string()} | Currency Basis: USD", styles["SmallGrey"]))
        story.append(Spacer(1, 0.2 * inch))

        kpi_data = [
            ["Total Projects", "Total Net Profit (USD)", "Average Margin"],
            [str(report_data.get("count", 0)), fmt_usd(report_data.get("total_profit", 0)), f"{report_data.get('avg_margin', 0)}%"],
        ]
        kpi_table = Table(kpi_data, colWidths=[2.1 * inch, 2.3 * inch, 2.1 * inch])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF2F8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D6DBDF")),
            ("BACKGROUND", (0, 1), (-1, 1), colors.white),
            ("FONTSIZE", (0, 1), (-1, 1), 13),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 0.25 * inch))

        story.append(Paragraph("Matching Projects", styles["Section"]))
        rows = [["DB ID", "Project", "Manager", "Status", "USD Net Profit"]]
        for project in report_data.get("projects", []):
            rows.append([
                str(project.get("db_id", "-")),
                Paragraph(str(project.get("p_name", "Unnamed Project")), styles["Normal"]),
                Paragraph(str(project.get("p_manager", "-")), styles["Normal"]),
                str(project.get("p_status", "-")),
                fmt_usd(project.get("f_nprofit_usd", 0)),
            ])
        if len(rows) == 1:
            rows.append(["-", "No projects found", "-", "-", "-"])

        table = Table(rows, colWidths=[0.6 * inch, 2.1 * inch, 1.4 * inch, 1.0 * inch, 1.4 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D6DBDF")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9F9")]),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("Note: Financial analysis is converted and stored in USD at project creation/update using the configured exchange-rate API.", styles["SmallGrey"]))

        doc.build(story)
        buffer.seek(0)
        filename = f"project_report_{period}_{(manager or 'all').replace(' ', '_')}.pdf"
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF report: {str(e)}")


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
