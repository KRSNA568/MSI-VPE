from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import logging
import json
import io
import io

from app.schemas.sis_schema import ScriptInput, AnalysisResponse, SceneIntentSchema
from app.services.analysis_service import AnalysisService
from app.services.pdf_export import get_pdf_exporter
from app.core.database import get_db
from app.core.security import require_api_key
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

@router.post("/analyze", response_model=AnalysisResponse, dependencies=[Depends(require_api_key)])
async def analyze_script(
    input_data: ScriptInput,
    background_tasks: BackgroundTasks,
    service: AnalysisService = Depends(get_analysis_service),
    db: Session = Depends(get_db)
):
    """
    Submit a screenplay scene for analysis (JSON format).
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


@router.post("/upload", response_model=AnalysisResponse, dependencies=[Depends(require_api_key)])
async def upload_script_file(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = None,
    service: AnalysisService = Depends(get_analysis_service),
    db: Session = Depends(get_db)
):
    """
    Upload a screenplay file (PDF, Fountain, or TXT) for analysis.
    Supports PDF text extraction.
    """
    job_id = str(uuid.uuid4())
    logger.info(f"Received file upload: {file.filename}, job_id: {job_id}")
    
    # Extract text from file
    try:
        content = await file.read()
        
        # Determine file type and extract text
        if file.filename.lower().endswith('.pdf'):
            # Extract text from PDF
            from PyPDF2 import PdfReader
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            script_text = ""
            for page in reader.pages:
                script_text += page.extract_text() + "\n"
            logger.info(f"Extracted {len(script_text)} characters from PDF")
        else:
            # Plain text file (.fountain, .txt)
            script_text = content.decode('utf-8')
    except Exception as e:
        logger.error(f"File extraction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract text from file: {str(e)}"
        )
    
    if not script_text or len(script_text) < 10:
        raise HTTPException(
            status_code=400,
            detail="Extracted text is too short or empty"
        )
    
    # Use filename as title if not provided
    if not title:
        title = file.filename.rsplit('.', 1)[0]
    
    # Create Job Record
    job = AnalysisJob(
        id=job_id,
        script_title=title,
        status=JobStatus.PROCESSING
    )
    db.add(job)
    db.commit()
    
    try:
        # Parse and Analyze
        # Note: This is synchronous blocking code. 
        # For production large scripts, this should be offloaded to Celery/FastAPI BackgroundTasks
        results = service.analyze_script(script_text, job_id)
        
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

@router.get("/jobs/{job_id}", response_model=AnalysisResponse, dependencies=[Depends(require_api_key)])
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

@router.get("/export/{job_id}/pdf", dependencies=[Depends(require_api_key)])
async def export_pdf(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Export analysis results as a PDF report for filmmakers.
    Professional format with visual recommendations.
    """
    job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Analysis not completed yet")
    
    if not job.result_json:
        raise HTTPException(status_code=404, detail="No analysis results found")
    
    # Parse the result
    result_data = json.loads(job.result_json)
    
    # Generate PDF
    pdf_exporter = get_pdf_exporter()
    
    analysis_data = {
        'status': job.status.value,
        'analysis_result': result_data
    }
    
    script_filename = job.script_title or "Screenplay"
    pdf_buffer = pdf_exporter.generate_pdf(analysis_data, script_filename)
    
    # Return as downloadable file
    filename = f"{script_filename.replace(' ', '_')}_analysis.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )