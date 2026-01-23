import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.models.job import AnalysisJob, JobStatus

class TestDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        # Use in-memory SQLite for testing
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(bind=self.engine)
        
        self.db = self.SessionLocal()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)

    def test_create_and_retrieve_job(self):
        """Test creating and retrieving a job record"""
        job_id = "test_job_1"
        job = AnalysisJob(
            id=job_id,
            script_title="Test Script",
            status=JobStatus.PENDING
        )
        self.db.add(job)
        self.db.commit()
        
        # Retrieve
        retrieved_job = self.db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
        self.assertIsNotNone(retrieved_job)
        self.assertEqual(retrieved_job.script_title, "Test Script")
        self.assertEqual(retrieved_job.status, JobStatus.PENDING)

    def test_update_job_status(self):
        """Test updating job status and result"""
        job_id = "test_job_2"
        job = AnalysisJob(
            id=job_id,
            status=JobStatus.PROCESSING
        )
        self.db.add(job)
        self.db.commit()
        
        # Update
        job.status = JobStatus.COMPLETED
        job.result_json = '{"test": "data"}'
        self.db.commit()
        
        # Verify
        updated_job = self.db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
        self.assertEqual(updated_job.status, JobStatus.COMPLETED)
        self.assertEqual(updated_job.result_json, '{"test": "data"}')

if __name__ == "__main__":
    unittest.main()
