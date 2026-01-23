from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import logging
import json

from app.schemas.sis_schema import ScriptInput, AnalysisResponse, SceneIntentSchema
from app.services.analysis_service import AnalysisService
from app.core.database import get_db
from app.models.job import AnalysisJob, JobStatus

router = APIRouter()
logger = logging.getLogger(__name__)

# Singleton wrapper or dependency
_service_instance = None

def get_analysis_service():
    global _service_instance
    if _service_instance is None:
        _service_instance = AnalysisService()
    return _service_instance

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_script(
    input_data: ScriptInput,
    background_tasks: BackgroundTasks,
    service: AnalysisService = Depends(get_analysis_service),
    db: Session = Depends(get_db)
):
    """
    Submit a screenplay scene for analysis.
    Returns immediately with a job ID (Pending status), unless configured to wait.
    For this MVP, we execute synchronously but store result in DB.
    """
    job_id = str(uuid.uuid4())
    logger.info(f"Received analysis request: {job_id}")
    
    # Create Job Record
    job = AnalysisJob(
        id=job_id,
        script_title=input_data.title,
        status=JobStatus.PROCESSING # We are starting immediately
    )
    db.add(job)
    db.commit()
    
    try:
        # Parse and Analyze
        # Note: This is synchronous blocking code. 
        # For production large scripts, this should be offloaded to Celery/FastAPI BackgroundTasks
        results = service.analyze_script(input_data.script_text, job_id)
        
        if not results:
            job.status = JobStatus.FAILED
            job.error_message = "No valid scenes found in input text"
            db.commit()
            
            return AnalysisResponse(
                job_id=job_id,
                status="failed",
                error="No valid scenes found in input text"
            )
            
        # Success
        result_schema = results[0]
        
        # Serialize result for DB
        # SceneIntentSchema.model_dump_json() if pydantic v2
        job.result_json = result_schema.model_dump_json()
        job.status = JobStatus.COMPLETED
        db.commit()
        
        return AnalysisResponse(
            job_id=job_id,
            status="completed",
            result=result_schema,
            progress=100
        )
        
    except Exception as e:
        logger.error(f"Analysis failed for {job_id}: {e}", exc_info=True)
        job.status = JobStatus.FAILED
        job.error_message = str(e)
        db.commit()
        
        return AnalysisResponse(
            job_id=job_id,
            status="failed",
            error=str(e)
        )

@router.get("/jobs/{job_id}", response_model=AnalysisResponse)
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve status and result of an analysis job.
    """
    job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    result_data = None
    if job.result_json:
        result_data = SceneIntentSchema.model_validate_json(job.result_json)
        
    return AnalysisResponse(
        job_id=job.id,
        status=job.status.value,
        result=result_data,
        error=job.error_message,
        progress=100 if job.status == JobStatus.COMPLETED else 0
    )
