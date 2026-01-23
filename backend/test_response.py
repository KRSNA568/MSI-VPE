import sys
sys.path.insert(0, '.')
from app.services.analysis_service import AnalysisService
import json

test_script = """
INT. COFFEE SHOP - DAY

SARAH sits alone, staring at her phone. Her hands tremble.

SARAH
I can't believe you did this.

JOHN enters, hesitant.

JOHN
I'm sorry. I didn't mean to hurt you.
"""

service = AnalysisService()
results = service.analyze_script(test_script, "test-123")
if results:
    print(json.dumps(results[0].model_dump(), indent=2, default=str))
