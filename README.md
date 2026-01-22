# MSI-VPE: Multimodal Scene Intent & Visual Planning Engine
## Screenplay Emotion-to-Visual Mapper

**🎓 College Capstone Project**  
**📅 Academic Year:** 2025-2026  
**🔬 Research Domain:** AI/ML + Film Cinematography  
**⚡ Status:** In Development

---

## 🎯 Project Overview

MSI-VPE is an AI-driven proof-of-concept system that analyzes screenplay text and generates comprehensive visual recommendations (lighting, color palettes, camera angles, movements, and shot compositions) based on detected emotional content. The system bridges the gap between narrative intent and cinematographic execution, serving as an intelligent creative assistant for filmmakers.

### Core Innovation
- **Input:** Fountain-format screenplay scenes
- **Processing:** Multi-model emotion detection (20+ emotions) + cinematography knowledge graph
- **Output:** Structured visual planning recommendations with professional parameters

---

## 🎬 Key Features

### Emotion Detection System
- **20+ comprehensive emotions** across primary, secondary, and tertiary categories
- **Ensemble ML approach** using multiple Hugging Face transformer models
- **Mixed emotion support** with confidence scoring
- Scene-level and dialogue-level analysis

### Visual Recommendation Engine

#### 1. Color Science Mapping
- Rich color palettes (primary, secondary, accent colors)
- Emotion-specific hex codes with saturation/brightness parameters
- Color harmony principles (complementary, analogous, triadic)

#### 2. Comprehensive Lighting System
- **Quality:** Soft to hard (0-100 scale)
- **Direction:** 8+ positions (front, side, back, under, overhead, etc.)
- **Temperature:** Full Kelvin spectrum (2700K-9000K+)
- **Intensity:** Low, medium, high with lux values
- **Contrast ratio:** 2:1 to 18:1
- **Techniques:** Rembrandt, butterfly, split, loop, chiaroscuro, and more

#### 3. Camera Angle System
- **15+ angles:** Extreme low, low, eye-level, high, extreme high, overhead, Dutch, POV, etc.
- **Power dynamics mapping:** Authority vs vulnerability
- **Psychological effects documented

#### 4. Camera Movement Recommendations
- **12+ movements:** Static, pan, tilt, dolly, track, handheld, Steadicam, crane, zoom, whip pan
- Intensity and pacing matched to emotion

#### 5. Shot Composition
- **10+ shot sizes:** ECU, CU, MCU, MS, MLS, LS, ELS
- **Multi-character shots:** 2-shot, 3-shot, OTS
- **Focal length psychology:** 14mm-200mm+ with emotional mapping

---

## 🏗️ Technical Architecture

### Backend (Python)
```
backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── parsers/
│   │   └── fountain_parser.py  # Screenplay parsing
│   ├── services/
│   │   ├── emotion_detector.py # Ensemble emotion detection
│   │   └── visual_mapper.py    # Emotion → visual translation
│   ├── schemas/
│   │   └── sis_schema.py       # Scene Intent Schema (Pydantic)
│   └── core/
│       └── config.py           # Configuration
└── tests/                      # Unit & integration tests
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/
│   │   ├── ScriptUploader.jsx
│   │   ├── EmotionGraph.jsx
│   │   ├── ColorPalette.jsx
│   │   ├── LightingCard.jsx
│   │   ├── CameraCard.jsx
│   │   └── ResultsVisualization.jsx
│   └── App.jsx
└── package.json
```

### Knowledge Base
```
knowledge-base/
├── emotion_color_map.json           # 20+ emotions → color palettes
├── cinematography_rules.json        # 50+ professional principles
├── lighting_techniques.json         # Rembrandt, butterfly, etc.
├── camera_angle_psychology.json     # Angle → emotional effect
└── sources.md                       # Academic citations
```

---

## 🛠️ Technology Stack

### AI/ML
- **Hugging Face Transformers** (emotion detection)
  - Primary: `SamLowe/roberta-base-go_emotions` (27 emotions)
  - Secondary: `j-hartmann/emotion-english-distilroberta-base` (7 emotions)
  - Tertiary: `bhadresh-savani/distilbert-base-uncased-emotion` (6 emotions)
- **Ensemble approach** for robust emotion detection

### Backend
- **FastAPI** - High-performance Python web framework
- **Pydantic** - Data validation and serialization
- **SQLite** - Lightweight database for analysis storage
- **Python 3.11+** - Modern type hints and performance

### Frontend
- **React 18+** - Component-based UI
- **Vite** - Fast development and building
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization (emotion graphs)
- **Axios** - API communication

### Development & Deployment
- **Git/GitHub** - Version control
- **Pytest** - Python testing
- **Render/Railway** - Backend hosting (free tier)
- **Vercel/Netlify** - Frontend hosting (free tier)

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- Git

### Backend Setup
```bash
# Clone repository
git clone <repository-url>
cd MSI-VPE/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download AI models (first run - ~500MB)
python -c "from transformers import pipeline; pipeline('text-classification', model='SamLowe/roberta-base-go_emotions')"

# Run backend server
uvicorn app.main:app --reload

# Backend runs at http://localhost:8000
```

### Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Frontend runs at http://localhost:5173
```

### Run Tests
```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm run test
```

---

## 🚀 Usage

### 1. Upload Screenplay
- Navigate to `http://localhost:5173`
- Drag and drop a `.fountain` screenplay file
- Or paste screenplay text directly

### 2. Analyze Scene
- System automatically parses screenplay into scenes
- Detects emotions using ensemble ML models
- Generates comprehensive visual recommendations

### 3. Explore Results
- **Emotion Timeline:** Visual graph of emotions across scenes
- **Color Palette:** Rich color schemes with hex codes
- **Lighting Setup:** Complete lighting parameters and diagrams
- **Camera Package:** Angles, movements, shot sizes, focal lengths
- **Export:** Download complete JSON report

### Example Output
```json
{
  "scene_id": "scene_001",
  "emotions": [
    {"emotion": "betrayal", "confidence": 0.89, "intensity": 85},
    {"emotion": "sadness", "confidence": 0.62, "intensity": 65}
  ],
  "visual_recommendations": {
    "colors": {
      "primary": ["#991B1B", "#6B21A8"],
      "secondary": ["#7C2D12", "#581C87"],
      "accent": ["#65A30D"]
    },
    "lighting": {
      "quality": 90,
      "temperature": "6500K",
      "direction": "harsh_side_split",
      "contrast_ratio": "12:1",
      "technique": "split_lighting"
    },
    "camera": {
      "angle": "high_angle",
      "movement": "slow_dolly_out",
      "shot_size": "extreme_closeup",
      "focal_length": "85mm"
    }
  }
}
```

---

## 📚 Documentation

- [**CAPSTONE_PROJECT_PLAN.md**](CAPSTONE_PROJECT_PLAN.md) - Complete project overview and strategy
- [**CAPSTONE_TODO_16WEEKS.md**](CAPSTONE_TODO_16WEEKS.md) - Week-by-week implementation plan
- [**EMOTION_VISUAL_MAPPING_REFERENCE.md**](EMOTION_VISUAL_MAPPING_REFERENCE.md) - Authoritative emotion-visual mappings
- [**DEEP_ANALYSIS.md**](DEEP_ANALYSIS.md) - Technical architecture and gap analysis
- [**docs/api.md**](docs/api.md) - API endpoint documentation
- [**docs/architecture.md**](docs/architecture.md) - System architecture
- [**knowledge-base/sources.md**](knowledge-base/sources.md) - Academic citations

---

## 🎓 Academic Components

### Research Question
"Can automated NLP systems accurately infer appropriate cinematographic parameters from screenplay text to match human expert recommendations?"

### Evaluation Methodology
1. **Quantitative:** Emotion detection accuracy, precision, recall
2. **Qualitative:** User study with film students and professionals
3. **Comparative:** System output vs. baseline random recommendations
4. **Case Study:** Analysis of 3 famous screenplay scenes

### Learning Outcomes
- Full-stack web development (React + Python)
- AI/ML integration with transformer models
- Domain-specific knowledge synthesis (film + CS)
- Research methodology and academic writing
- Software testing and validation

---

## 🧪 Testing Strategy

### Unit Tests (80%+ coverage target)
- Parser validation with diverse screenplay formats
- Emotion detection accuracy on known samples
- Visual mapping rule verification
- API endpoint response validation

### Integration Tests
- End-to-end workflow (upload → analyze → export)
- Database operations and state management
- Frontend-backend communication
- Error handling and edge cases

### Validation Testing
- Blind test with film professionals (10+ participants)
- Compare recommendations to actual film choices
- Measure creative alignment score (target: >4/5)
- Document accuracy metrics and feedback

---

## 📊 Success Metrics

### Technical Metrics
- ✅ Emotion detection accuracy: **>70%**
- ✅ API response time: **<2 seconds per scene**
- ✅ Code coverage: **>80%**
- ✅ System uptime: **>99%** during demo period

### Academic Metrics
- ✅ Creative alignment score: **>4/5** from film professionals
- ✅ User satisfaction: **>4.5/5**
- ✅ Novel research contribution documented
- ✅ Publication-ready results

---

## 🗓️ Project Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| **Week 1-2** | Setup & Schema | Project structure, SIS schema, knowledge base |
| **Week 3-4** | Backend Foundation | Parser, emotion detection, data models |
| **Week 5-7** | Visual Mapping | Comprehensive mapping logic, all parameters |
| **Week 8-10** | API Development | FastAPI endpoints, database, testing |
| **Week 11-13** | Frontend | React UI, visualizations, export |
| **Week 14-15** | Testing & Validation | User study, accuracy testing, refinement |
| **Week 16** | Deployment & Delivery | Deploy, documentation, presentation |

**Total Duration:** 16 weeks (1 semester)

---

## 🎯 Current Status

**Week:** 1 of 16  
**Phase:** Foundation & Setup  
**Completed:**
- ✅ Project structure created
- ✅ Documentation framework established
- ✅ Comprehensive emotion-visual mapping defined
- ⏳ Core schema implementation (in progress)

**Next Steps:**
- Define complete Scene Intent Schema (SIS)
- Create knowledge base JSON files
- Implement Fountain parser
- Setup FastAPI backend skeleton

---

## 👥 Team

- **[Your Name]** - Full-Stack Development, AI/ML Integration, Research
- **Advisor:** [Advisor Name] - Academic Guidance
- **Film Consultant:** [Name] - Cinematography Validation (if applicable)

---

## 🤝 Contributing

This is an academic capstone project. Contributions are welcome for:
- Additional emotion-visual mappings from film theory
- Cinematography rule validation
- Code improvements and bug fixes
- Testing and validation feedback

Please open an issue or submit a pull request with detailed description.

---

## 📄 License

MIT License - See LICENSE file for details.

This is an academic research project. If you use this work, please cite:
```
[Your Name]. (2026). MSI-VPE: Multimodal Scene Intent & Visual Planning Engine. 
Capstone Project, [Your University]. GitHub: [repository-url]
```

---

## 🙏 Acknowledgments

### Academic Sources
- Blain Brown - "Cinematography: Theory and Practice"
- Joseph V. Mascelli - "The Five C's of Cinematography"
- American Society of Cinematographers (ASC) articles
- Film theory papers on visual storytelling

### Technical Foundations
- Hugging Face for transformer models
- FastAPI and React communities
- Open-source cinematography knowledge

### Inspiration
- Professional pre-visualization artists
- Student filmmakers seeking creative tools
- The intersection of AI and creative arts

---

## 📞 Contact

- **Email:** [your-email@university.edu]
- **GitHub:** [your-github-username]
- **Project Demo:** [demo-url-when-deployed]
- **Video Walkthrough:** [youtube-link-when-available]

---

## 🌟 Project Goals

This capstone aims to:
1. **Demonstrate** the feasibility of AI-assisted cinematographic planning
2. **Bridge** the gap between narrative text and visual parameters
3. **Provide** a practical tool for student and indie filmmakers
4. **Contribute** novel research to the intersection of NLP and film studies
5. **Showcase** full-stack development and AI integration skills

**Built with passion for film and technology. 🎬🤖**

---

*Last Updated: January 23, 2026*  
*Version: 1.0.0*  
*Status: Active Development*
