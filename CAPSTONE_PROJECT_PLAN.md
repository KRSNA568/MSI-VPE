# MSI-VPE: College Capstone Project Adaptation
## Screenplay Emotion-to-Visual Mapper

**Academic Level:** Undergraduate/Graduate Capstone  
**Duration:** 1-2 Semesters (16-32 weeks)  
**Team Size:** 3-4 students OR Solo project (scope adjusted)  
**Date:** January 23, 2026

---

## PROJECT OVERVIEW

### Scaled-Down Vision
Build a **proof-of-concept AI system** that analyzes screenplay text and generates visual recommendations (lighting, color, camera) based on emotional content. Focus on **demonstrating the core innovation** rather than building a production-ready system.

### Academic Value
- **Research Component:** Novel application of NLP to cinematography
- **Technical Challenge:** Multimodal AI (text → visual parameters)
- **Practical Impact:** Tool for student filmmakers and indie creators
- **Learning Outcomes:** Full-stack development, AI/ML integration, domain knowledge synthesis

### Key Simplifications from Professional Version
1. ❌ No expensive LLM APIs (Claude Opus $75/1M tokens)
2. ❌ No complex infrastructure (Kubernetes, cloud deployment)
3. ❌ No USD/Unreal Engine integration (too specialized)
4. ✅ Use free/open-source AI models
5. ✅ Simple local deployment
6. ✅ Focus on 3-5 emotions instead of comprehensive taxonomy
7. ✅ Web demo instead of production API

---

## CAPSTONE PROJECT SCOPE

### What You WILL Build (MVP)

#### Core Features (Must-Have)
1. **Simple Script Parser**
   - Support Fountain format only (simplest, plaintext)
   - Extract scenes, dialogue, and action descriptions
   - Identify character names

2. **Emotion Detection System**
   - Comprehensive emotion taxonomy: 20+ emotions across 6 categories
   - Primary: Joy, Sadness, Anger, Fear, Surprise, Disgust
   - Secondary: Tension, Melancholy, Euphoria, Anxiety, Nostalgia, Loneliness
   - Tertiary: Hope, Despair, Triumph, Betrayal, Confusion, Serenity, Dread, Passion
   - Use open-source NLP (RoBERTa emotion models)
   - Scene-level + dialogue-level emotion classification
   - Support for mixed/layered emotions

3. **Visual Recommendation Engine**
   - Map emotions to 5 comprehensive visual dimensions:
     - **Color palette** (20+ emotions → distinct color schemes with primaries, secondaries, accents)
     - **Lighting** (10+ parameters: quality, hardness, direction, temperature, intensity, contrast ratio, shadows)
     - **Camera angles** (15+ angles: extreme low, low, eye-level, high, extreme high, Dutch angle, overhead, POV)
     - **Camera movement** (Static, pan, tilt, dolly, track, handheld, Steadicam, crane, zoom)
     - **Shot composition** (ECU, CU, MCU, MS, MLS, LS, ELS, 2-shot, 3-shot, OTS)
   - Advanced rule-based mapping with cinematography knowledge graph
   - ML confidence scores for all recommendations
   - Context-aware adjustments (genre, character dynamics, narrative arc)

4. **Web Interface**
   - Upload .fountain script
   - Display scene-by-scene analysis
   - Show visual recommendations with explanations
   - Export as JSON report

5. **Knowledge Base (Minimal)**
   - 20-30 cinematography rules from film textbooks
   - Emotion-to-visual mapping database (JSON/CSV)
   - Cite sources for academic rigor

### What You WON'T Build (Out of Scope)
- ❌ Multiple script formats (.fdx, .pdf) - Too complex for parsing
- ❌ Real-time 3D integration - Requires specialized skills
- ❌ Advanced AI reasoning - Too expensive/complex
- ❌ Production infrastructure - Not needed for proof-of-concept
- ❌ User authentication - Not core to research question
- ❌ Multiple style profiles - Keep it simple with one validated approach

---

## SIMPLIFIED TECHNICAL STACK

### Frontend (Simple Web App)
- **Framework:** React with Vite (faster than Next.js for capstone)
- **Styling:** Tailwind CSS (quick, modern)
- **Visualization:** Chart.js or Recharts (emotion graphs)
- **Deployment:** Vercel or Netlify (free tier)

### Backend (Lightweight API)
- **Framework:** FastAPI (Python) OR Flask (simpler)
- **AI/ML:** 
  - Hugging Face Transformers (free, local)
  - Primary Model: `SamLowe/roberta-base-go_emotions` (27 emotions)
  - Secondary: `j-hartmann/emotion-english-distilroberta-base` (7 emotions)
  - Ensemble approach for better accuracy across emotion spectrum
  - Custom emotion aggregation and layering logic
- **Parser:** Pure Python with regex (no SpaCy needed for Fountain)
- **Database:** SQLite (no setup required) OR JSON files

### Deployment
- **Development:** Local (Python backend + React frontend)
- **Demo:** Backend on Render/Railway (free), Frontend on Vercel
- **Total Cost:** $0-10/month (vs $675/month professional version)

### No Infrastructure Needed
- ❌ No Docker/Kubernetes
- ❌ No Neo4j/Weaviate/Pinecone
- ❌ No cloud services beyond hosting
- ✅ Everything runs on laptop during development

---

## REALISTIC TIMELINE

### Option A: One Semester (16 Weeks) - Solo/Pair Project

#### Weeks 1-2: Research & Planning
- [ ] Literature review: NLP + cinematography papers
- [ ] Study 5 film theory sources (textbooks, articles)
- [ ] Create emotion-to-visual mapping database (20 rules)
- [ ] Write project proposal with research question
- [ ] Setup GitHub repo with README

#### Weeks 3-4: Backend Foundation
- [ ] Implement Fountain parser (regex-based)
- [ ] Integrate Hugging Face emotion detection model
- [ ] Test emotion detection on 10 sample scenes
- [ ] Create JSON schema for output

#### Week 5-7: Visual Mapping Logic (EXPANDED)
- [ ] Create comprehensive emotion-to-color mapping (20+ emotions → palettes)
  - Define primary, secondary, and accent colors for each emotion
  - Create color harmony rules (complementary, analogous, triadic)
  - Map color saturation and brightness to intensity
- [ ] Implement advanced lighting recommendations
  - Quality: soft/medium/hard (0-100 scale)
  - Direction: front/side/back/under/overhead (with angles)
  - Temperature: 2700K-8000K spectrum
  - Intensity: low/medium/high with lux values
  - Contrast ratio: low/medium/high
  - Shadow characteristics: diffused/defined/harsh
  - Special techniques: Rembrandt, butterfly, split, loop, chiaroscuro
- [ ] Implement comprehensive camera angle system
  - Vertical angles: extreme low, low, eye-level, high, extreme high, overhead, worm's-eye, bird's-eye
  - Horizontal angles: frontal, 3/4, profile, OTS (over-the-shoulder)
  - Dutch angles for disorientation
  - POV shots for subjectivity
- [ ] Implement camera movement recommendations
  - Static, pan, tilt, dolly-in/out, track, handheld, Steadicam, crane, zoom, whip pan
- [ ] Implement shot composition system
  - Shot sizes: ECU, CU, MCU, MS, MLS, LS, ELS
  - Multi-character: 2-shot, 3-shot, group shots
  - Depth staging recommendations
- [ ] Write comprehensive unit tests for all mapping logic

#### Weeks 8-10: Backend API
- [ ] Create FastAPI endpoints (upload, analyze, results)
- [ ] Add error handling
- [ ] Test with sample scripts
- [ ] Document API with examples

#### Weeks 11-13: Frontend Development
- [ ] Build React UI with script upload
- [ ] Display analysis results with visualizations
- [ ] Show color palettes and recommendations
- [ ] Make it visually appealing for demo

#### Weeks 14-15: Testing & Validation
- [ ] Test with 10+ different screenplay scenes
- [ ] Validate recommendations with film students/professors
- [ ] Compare AI output to human expert judgments
- [ ] Document accuracy metrics

#### Week 16: Final Deliverables
- [ ] Deploy demo online
- [ ] Create demo video (5 minutes)
- [ ] Write final report (15-20 pages)
- [ ] Prepare presentation slides
- [ ] Practice demo for defense

**Deliverables:**
- Working web demo
- GitHub repository with code
- Technical documentation
- Academic report with literature review
- 15-minute presentation + Q&A

---

### Option B: Two Semesters (32 Weeks) - Team of 3-4

#### Semester 1: Core System (Weeks 1-16)
Same as Option A, but with additional features:
- Support PDF script upload (using PyPDF2)
- Add 10 emotions instead of 5
- Build better UI with animations
- Add more sophisticated mapping logic

#### Semester 2: Advanced Features (Weeks 17-32)
- [ ] Fine-tune emotion detection model on screenplay corpus
- [ ] Add "beat" level analysis (sub-scene granularity)
- [ ] Implement basic style profiles (2-3 styles)
- [ ] Add character-level emotion tracking
- [ ] Create visualization of emotional arc over full script
- [ ] User study with 20+ participants
- [ ] Publish findings as conference paper/poster

**Additional Deliverables:**
- Research paper for publication
- Comprehensive user study results
- More polished, feature-rich demo

---

## KEY RESEARCH QUESTIONS (For Academic Rigor)

### Primary Research Question
"Can automated NLP systems accurately infer appropriate cinematographic parameters from screenplay text to match human expert recommendations?"

### Sub-Questions
1. What is the correlation between detected emotions and expert-recommended visual parameters?
2. How does model performance vary across different screenplay genres?
3. What level of granularity (scene vs beat) produces most useful recommendations?
4. Can rule-based systems compete with ML approaches for this domain-specific task?

### Evaluation Methodology
- **Quantitative:** Accuracy, precision, recall of emotion detection
- **Qualitative:** Survey 10+ film students/professionals on recommendation quality
- **Comparative:** Your system vs baseline (random recommendations)
- **Case Study:** Deep dive on 3 famous screenplay scenes

---

## MINIMAL VIABLE DEMO (What Impresses Judges)

### Demo Script (3 minutes)
1. **Problem Statement** (30 sec): Show challenge of pre-visualization for indie filmmakers
2. **Upload Script** (30 sec): Upload sample screenplay scene
3. **Show Analysis** (90 sec):
   - Comprehensive emotion detection (20+ emotions displayed)
   - Multi-layered emotion intensity graph over scene timeline
   - Rich color palette with primary/secondary/accent colors
   - Detailed lighting parameters (7+ dimensions visualized)
   - Complete camera package (angles + movement + composition)
   - Interactive visualization allowing exploration of recommendations
4. **Validation** (30 sec): Show comparison with actual film stills

### Wow Factor Elements
- 🎨 Beautiful color palette visualization
- 📊 Emotion intensity graph over time
- 🎬 Side-by-side: Your recommendation vs actual movie frame
- 💡 "Explain reasoning" feature showing why each recommendation was made

---

## BUDGET & RESOURCES

### Zero-Budget Options
| Need | Free Solution | Cost |
|------|---------------|------|
| AI Model | Hugging Face (local) | $0 |
| Backend Hosting | Render.com free tier | $0 |
| Frontend Hosting | Vercel/Netlify | $0 |
| Database | SQLite | $0 |
| Domain | yourproject.vercel.app | $0 |
| **TOTAL** | | **$0** |

### Optional Small Budget ($50-100)
| Upgrade | Option | Cost |
|---------|--------|------|
| Better AI | OpenAI GPT-3.5-turbo (limited use) | $20 |
| Custom Domain | yourproject.com | $12/year |
| Better Hosting | Railway Pro (if needed) | $20 |
| Film Theory Books | Used textbooks | $30 |

### Resources You Need
- **Development:** Laptop (any modern laptop works)
- **Knowledge Sources:** 
  - Library access to film textbooks (free)
  - Online cinematography articles (free)
  - YouTube cinematography tutorials (free)
- **Validation:** Film department students/professors (free consultation)

---

## LEARNING OUTCOMES & SKILLS GAINED

### Technical Skills
- ✅ Full-stack web development (React + Python)
- ✅ REST API design and implementation
- ✅ Natural Language Processing with transformers
- ✅ Data modeling and schema design
- ✅ Software testing and validation
- ✅ Git version control and documentation

### Domain Knowledge
- ✅ Cinematography principles
- ✅ Film theory and visual storytelling
- ✅ Screenplay formatting and structure
- ✅ Color theory in film
- ✅ Lighting techniques

### Research Skills
- ✅ Literature review and synthesis
- ✅ Experimental design and evaluation
- ✅ User study methodology
- ✅ Academic writing and presentation
- ✅ Critical analysis of AI/ML systems

### Professional Skills
- ✅ Project management
- ✅ Requirements analysis
- ✅ Technical documentation
- ✅ Presentation and communication
- ✅ Interdisciplinary collaboration

---

## GRADING RUBRIC ALIGNMENT

### Typical Capstone Criteria
| Criterion | How This Project Excels | Weight |
|-----------|------------------------|--------|
| **Technical Complexity** | Full-stack + AI/ML + domain-specific algorithms | 30% |
| **Innovation** | Novel application of NLP to cinematography | 20% |
| **Execution Quality** | Working demo, clean code, tests | 20% |
| **Documentation** | Comprehensive technical + academic docs | 15% |
| **Presentation** | Visual demo, clear explanation | 15% |

### Competitive Advantages
- **Interdisciplinary:** Combines CS, AI, and Film Studies
- **Practical Impact:** Real-world application for filmmakers
- **Demonstrable:** Visual output is impressive and easy to understand
- **Publishable:** Novel enough for student research conferences
- **Portfolio-Worthy:** Great project for job applications

---

## RISK MITIGATION (Academic Version)

### Risk: Emotion Detection Accuracy Too Low
**Mitigation:** 
- Set realistic expectation: 60-70% accuracy is publishable for new domain
- Focus on "interesting failures" as learning points
- Compare to human disagreement rates (film is subjective!)

### Risk: Too Ambitious for Timeline
**Mitigation:**
- Prioritize working demo over perfect system
- Use version control: v1.0 = basic, v1.1 = stretch goals
- Document "future work" section for features you didn't build

### Risk: Limited Film Theory Knowledge
**Mitigation:**
- Interview film professors for 1-hour consultation
- Use existing cinematography textbooks as authoritative sources
- Focus on widely-accepted principles (less controversy)

### Risk: Hardware Limitations
**Mitigation:**
- Use DistilBERT (10x smaller than BERT, runs on CPU)
- Process scripts offline, store results (not real-time)
- Google Colab for GPU access if needed (free)

---

## SAMPLE SCENES FOR TESTING

### Test Dataset (Collect These)
1. **Happy Scene:** Opening of "La La Land" (joy, color, movement)
2. **Sad Scene:** End of "Her" (melancholy, desaturation, static)
3. **Tense Scene:** Bank robbery in "Heat" (anxiety, harsh lighting, handheld)
4. **Romantic Scene:** Notebook kiss (intimacy, soft light, close-ups)
5. **Action Scene:** Bourne chase sequence (energy, quick cuts, wide angles)

### Ground Truth Collection
- Watch actual scenes
- Note actual color grading, lighting, camera choices
- Compare your system's recommendations to reality
- Calculate accuracy metrics

---

## DELIVERABLES CHECKLIST

### Code Deliverables
- [ ] GitHub repository (public, well-organized)
- [ ] README with setup instructions
- [ ] Requirements.txt (Python) and package.json (Node)
- [ ] At least 20 unit tests
- [ ] Code comments and docstrings
- [ ] .gitignore and clean commit history

### Documentation Deliverables
- [ ] Technical documentation (architecture, API docs)
- [ ] User guide (how to use the demo)
- [ ] Academic report (15-20 pages with citations)
- [ ] Presentation slides (15 minutes)
- [ ] Demo video (3-5 minutes, uploaded to YouTube)

### Research Deliverables
- [ ] Literature review (10+ sources)
- [ ] Methodology description
- [ ] Evaluation results with metrics
- [ ] Discussion of limitations and future work
- [ ] Conclusion and contributions

### Demo Deliverables
- [ ] Live website (public URL)
- [ ] Sample output files (JSON reports)
- [ ] Test cases with expected outputs
- [ ] Screenshots and visualizations

---

## RECOMMENDED PROJECT STRUCTURE (Simplified)

```
msi-vpe-capstone/
├── README.md
├── ARCHITECTURE.md
├── REPORT.md (academic writeup)
│
├── backend/
│   ├── app/
│   │   ├── main.py (FastAPI app)
│   │   ├── parser.py (Fountain parser)
│   │   ├── emotion_detector.py (Hugging Face model)
│   │   ├── visual_mapper.py (emotion → visual rules)
│   │   └── schemas.py (Pydantic models)
│   ├── tests/
│   │   ├── test_parser.py
│   │   ├── test_emotion.py
│   │   └── test_mapper.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── ScriptUploader.jsx
│   │   │   ├── EmotionGraph.jsx
│   │   │   ├── ColorPalette.jsx
│   │   │   └── Recommendations.jsx
│   │   └── api/client.js
│   ├── package.json
│   └── vite.config.js
│
├── knowledge-base/
│   ├── emotion_color_map.json
│   ├── cinematography_rules.json
│   └── sources.md (citations)
│
├── sample-scripts/
│   ├── happy_scene.fountain
│   ├── sad_scene.fountain
│   └── tense_scene.fountain
│
└── docs/
    ├── literature_review.md
    ├── methodology.md
    └── evaluation_results.md
```

**Estimated Lines of Code:** 3,000-5,000 (vs 50,000+ for professional version)

---

## STRETCH GOALS (If Ahead of Schedule)

### Easy Additions (1-2 weeks each)
- [ ] Export recommendations as PDF report
- [ ] Add example film frames for each recommendation
- [ ] Support dialogue-only analysis (ignore action lines)
- [ ] Add confidence scores to all recommendations

### Medium Additions (2-4 weeks each)
- [ ] Fine-tune emotion model on IMDB screenplay corpus
- [ ] Add "comparative analysis" (compare two scenes side-by-side)
- [ ] Build simple admin panel to edit mapping rules
- [ ] Add genre detection (automatically adjust recommendations by genre)

### Ambitious Additions (4+ weeks)
- [ ] Create annotated dataset of 100+ scenes for research
- [ ] Build Chrome extension for inline script analysis
- [ ] Add collaborative features (share analyses with team)
- [ ] Write and submit paper to student research conference

---

## SUCCESS CRITERIA

### Minimum for Passing (B/B+)
- ✅ Working demo with 5 emotions
- ✅ 50%+ emotion detection accuracy
- ✅ Rule-based visual mapping that makes sense
- ✅ Clean code with basic tests
- ✅ Complete documentation
- ✅ Successful presentation

### Excellence Criteria (A/A+)
- ✅ 70%+ emotion detection accuracy
- ✅ Validation study with 10+ participants
- ✅ Beautiful, polished UI
- ✅ Novel insights or findings
- ✅ Publication-ready research component
- ✅ Strong technical implementation
- ✅ Impressive demo that "wow"s judges

### Extra Credit Potential
- 📄 Submit to student research conference
- 🏆 Win departmental best project award
- 💼 Strong enough for job portfolio
- 🌟 Open-source community interest
- 📚 Cite-able contribution to field

---

## COMPARISON: CAPSTONE VS PROFESSIONAL

| Aspect | Professional Version | Capstone Version |
|--------|---------------------|------------------|
| **Timeline** | 30 weeks (7 months) | 16 weeks (1 semester) |
| **Cost** | $3,400/1k analyses + $675/mo infra | $0-50 total |
| **AI Models** | Claude Opus, GPT-5, DeepSeek R1+ | DistilBERT (free) |
| **Features** | 15 major features, 150+ tasks | 4 core features, 40 tasks |
| **Emotions** | 30+ emotion taxonomy | 5 core emotions |
| **Formats** | .fdx, .fountain, .pdf | .fountain only |
| **Output** | USD, JSON, XML | JSON report |
| **Integration** | UE5, Unity, workflows | Standalone web app |
| **Infrastructure** | Kubernetes, Neo4j, Weaviate | SQLite, local |
| **Team** | 4-5 engineers | 1-4 students |
| **Outcome** | Production SaaS | Research proof-of-concept |

---

## FINAL RECOMMENDATIONS

### For Solo Student (16 weeks)
**Focus on:** Fountain parser → Emotion detection → Basic mapping → Simple web UI
**Skip:** Advanced ML, multiple formats, complex deployment
**Goal:** Solid B+ to A- with clean execution

### For Pair/Team (16 weeks)
**Add:** Better UI, validation study, more emotions, PDF support
**Goal:** A to A+ with publication potential

### For Two-Semester Project
**Semester 1:** Complete MVP as above
**Semester 2:** User study, paper writing, advanced features
**Goal:** Conference publication + portfolio centerpiece

---

## GETTING STARTED CHECKLIST

### Week 1 Actions
- [ ] Discuss scope with advisor (show them this document)
- [ ] Form team if applicable
- [ ] Setup GitHub repository
- [ ] Choose tech stack (stick to recommendations above)
- [ ] Find 3 film theory sources from library
- [ ] Install development environment
- [ ] Write 1-page project proposal

### First Milestone (Week 4)
- [ ] Fountain parser working
- [ ] Can detect emotions in sample text
- [ ] Basic mapping rules documented
- [ ] 5 sample screenplay scenes collected

### Questions to Ask Advisor
1. Is interdisciplinary collaboration with Film department possible?
2. Can we recruit film students for validation study?
3. Is 16 weeks realistic or should we plan for 32?
4. Are there any budget resources available?
5. What are the specific deliverables required?

---

## CONCLUSION

This capstone version is:
- ✅ **Achievable** in 16-32 weeks with student resources
- ✅ **Impressive** enough for excellent grades and portfolio
- ✅ **Educational** with strong learning outcomes
- ✅ **Free** or nearly free to build and deploy
- ✅ **Novel** with research/publication potential
- ✅ **Demonstrable** with visual, compelling demo

**Core Innovation Preserved:** The fundamental research question—can AI map screenplay emotions to visual parameters?—remains intact. You're just proving the concept rather than building a production system.

**Next Step:** Review this with your advisor, adjust scope based on semester length and team size, then begin Week 1 tasks.

---

**Document Status:** READY FOR ACADEMIC REVIEW  
**Recommended For:** CS/Software Engineering/HCI Capstone  
**Difficulty Level:** Advanced (suitable for strong students)  
**Wow Factor:** High (visual domain, AI application, interdisciplinary)

*Good luck with your capstone! This is a publishable, portfolio-worthy project. 🎬🤖*
