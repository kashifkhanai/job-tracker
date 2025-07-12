from fastapi import APIRouter, Depends
from core.role_check import require_role
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.db_getter import get_db
from schemas.models import JobPostModel,JobPostResponse,JobResponseModel

router = APIRouter(prefix="/jobs")

#EMPLOYER: Post a Job

@router.post("/post", status_code=201,response_model=JobPostResponse)
async def post_job(
    job: JobPostModel,
    db: AsyncIOMotorDatabase = Depends(get_db),
    employer = Depends(require_role("employer"))
):
    job_data = job.model_dump()
    job_data["employer_id"] = str(employer["_id"])
    job_data["employer_name"] = employer["firstname"] + " " + employer.get("lastname", "")
    job_data["employer_email"] = employer["email"]
    result = await db["jobs"].insert_one(job_data)
    return {"message": "Job posted successfully", "job_id": str(result.inserted_id)}


# JOB SEEKER: View all jobs

@router.get("/all",response_model=JobResponseModel)
async def get_all_jobs(
    db: AsyncIOMotorDatabase = Depends(get_db),
    seeker = Depends(require_role("job_seeker"))
):
    jobs = await db["jobs"].find({}, {"_id": 0}).to_list(length=100)
    return jobs

#Get Unique Job Titles
@router.get("/titles", response_model=list[str])
async def get_unique_job_titles(
    db: AsyncIOMotorDatabase = Depends(get_db),
    seeker=Depends(require_role("job_seeker"))
):
    titles = await db["jobs"].distinct("title")  # MongoDB distinct titles
    return titles


