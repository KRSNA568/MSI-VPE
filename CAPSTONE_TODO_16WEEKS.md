# MSI-VPE Capstone TODO List (16-Week Version)
## Screenplay Emotion-to-Visual Mapper - Academic Project

**Project Type:** Undergraduate/Graduate Capstone  
**Duration:** 16 weeks (1 semester)  
**Scope:** Proof-of-concept demonstration  
**Cost:** $0-50  

---

## WEEK 1-2: Research & Planning (Foundation)

### Research Phase
- [ ] Read 3 cinematography textbooks/chapters (library)
  - Recommended: "Cinematography: Theory and Practice" by Blain Brown
  - "The Five C's of Cinematography" by Joseph V. Mascelli
  - ASC articles on lighting and color
- [ ] Literature review: Find 10 academic papers on NLP + sentiment analysis
- [ ] Study Fountain screenplay format specification
- [ ] Interview 2 film students/professors about visual storytelling
- [ ] Document findings in `docs/literature_review.md`

### Project Setup
- [ ] Create GitHub repository with proper structure
- [ ] Write README.md with project description
- [ ] Create .gitignore for Python and Node
- [ ] Setup Python virtual environment (Python 3.11+)
- [ ] Install core dependencies: FastAPI, transformers, torch
- [ ] Setup React + Vite frontend project
- [ ] Write 2-page project proposal for advisor approval

### Knowledge Base Creation (COMPREHENSIVE)
- [ ] Create extensive emotion-to-color mapping (20+ emotions × 7 colors each)
  - **Primary Emotions:**
    - Joy → Warm yellows, bright oranges, sunshine gold (#FFD700, #FFA500, #FBBF24, #FEF3C7, #FB923C)
    - Sadness → Cool blues, desaturated grays, muted indigo (#4A5568, #CBD5E0, #6B7280, #94A3B8, #475569)
    - Anger → Hot reds, aggressive oranges, crimson (#DC2626, #EA580C, #B91C1C, #991B1B, #7F1D1D)
    - Fear → Cold grays, dark purples, shadow blacks (#374151, #6B21A8, #1F2937, #581C87, #3F3F46)
    - Surprise → Electric yellows, bright whites, sharp cyan (#FBBF24, #F9FAFB, #22D3EE, #FEF3C7, #E0F2FE)
    - Disgust → Sickly greens, murky browns, bile yellow (#84CC16, #78716C, #A3E635, #57534E, #BEF264)
  - **Secondary Emotions:**
    - Tension → High contrast (yellows/blacks, reds/blacks) (#FBBF24, #1F2937, #DC2626, #18181B)
    - Melancholy → Desaturated blues, lavender, soft grays (#6B7280, #C4B5FD, #9CA3AF, #A5B4FC, #E5E7EB)
    - Euphoria → Saturated magentas, bright pinks, electric blue (#EC4899, #F472B6, #3B82F6, #FB7185, #A855F7)
    - Anxiety → Queasy greens, mustard yellows, nervous grays (#A3E635, #EAB308, #71717A, #FACC15, #D4D4D8)
    - Nostalgia → Sepia tones, warm browns, faded golds (#D97706, #92400E, #F59E0B, #FBBF24, #FEF3C7)
    - Loneliness → Cold blues, empty whites, isolated grays (#334155, #F9FAFB, #64748B, #E2E8F0, #475569)
  - **Tertiary Emotions:**
    - Hope → Sunrise oranges, dawn pinks, soft golds (#FB923C, #FDA4AF, #FDE047, #FED7AA, #FEF3C7)
    - Despair → Midnight blues, charcoal, deep purples (#1E293B, #27272A, #4C1D95, #18181B, #0F172A)
    - Triumph → Victory golds, bright reds, champion blues (#F59E0B, #DC2626, #2563EB, #FBBF24, #1D4ED8)
    - Betrayal → Poison greens, blood reds, bruised purples (#65A30D, #991B1B, #6B21A8, #7C2D12, #581C87)
    - Confusion → Disorienting purples, hazy grays, unclear whites (#A78BFA, #D4D4D8, #F3F4F6, #C4B5FD, #9CA3AF)
    - Serenity → Soft blues, peaceful greens, calm beiges (#BAE6FD, #BBF7D0, #FEF3C7, #DBEAFE, #D1FAE5)
    - Dread → Deep reds, ominous blacks, shadow purples (#7F1D1D, #18181B, #581C87, #450A0A, #27272A)
    - Passion → Intense reds, deep magentas, fiery oranges (#DC2626, #BE185D, #EA580C, #C026D3, #DB2777)
- [ ] Document 50+ comprehensive cinematography rules
  - **Camera Angles (Vertical):**
    - Extreme low angle = god-like power, intimidation, monumentality
    - Low angle = power, dominance, authority, strength
    - Eye-level = neutrality, equality, reality, documentation
    - High angle = vulnerability, weakness, powerlessness, smallness
    - Extreme high angle = insignificance, helplessness, overview
    - Overhead (bird's-eye) = objectivity, fate, surveillance, map-like
    - Worm's-eye = awe, overwhelm, upward aspiration
    - Dutch angle (canted) = disorientation, unease, tension, instability
  - **Camera Angles (Horizontal):**
    - Frontal = confrontation, honesty, direct engagement
    - 3/4 angle = natural, comfortable, classical composition
    - Profile = contemplation, separation, side-taking
    - Over-the-shoulder (OTS) = conversation, perspective, involvement
    - POV (point-of-view) = subjectivity, immersion, character identification
  - **Camera Movement:**
    - Static = stability, observation, contemplation, tension
    - Pan = revelation, following, surveying environment
    - Tilt = discovery, reveal (up for power, down for fall)
    - Dolly-in = intensification, focus, increasing tension
    - Dolly-out = revelation, context, emotional distance
    - Track = following action, immersion, dynamism
    - Handheld = realism, chaos, urgency, documentary feel
    - Steadicam = smooth following, supernatural, dreamlike
    - Crane = epic scope, god's-eye, dramatic reveal
    - Zoom-in = sudden focus, aggressive attention
    - Zoom-out = sudden reveal, growing context
    - Whip pan = disorientation, time passage, shock transition
  - **Lighting Quality & Direction:**
    - Soft light = romance, nostalgia, gentleness, idealism, beauty
    - Hard light = drama, tension, reality, harshness, intensity
    - Front lighting = flat, beauty, concealing, commercial
    - Side lighting = dimension, drama, revealing texture
    - Back lighting = silhouette, mystery, separation, halo effect
    - Under lighting = horror, unnaturalness, villain reveal
    - Overhead lighting = interrogation, exposure, isolation
    - Rembrandt = classical drama, one-eye triangle highlight
    - Butterfly = glamour, beauty, centered nose shadow
    - Split = duality, conflict, half-lit face
    - Loop = versatile, slight shadow loop from nose
    - Chiaroscuro = high contrast, Baroque, dramatic shadows
  - **Lighting Temperature:**
    - Warm (2700K-3500K) = comfort, intimacy, sunset, home, nostalgia
    - Neutral (4000K-5000K) = reality, daylight, objectivity
    - Cool (5500K-8000K) = isolation, distance, clinical, moonlight, alienation
  - **Lighting Intensity & Contrast:**
    - Low-key = dramatic, mysterious, film noir, high contrast
    - High-key = bright, optimistic, comedy, low contrast, cheerful
    - Silhouette = mystery, anonymity, dramatic shape
    - Practical lights = realism, motivated lighting, depth
- [ ] Create `knowledge-base/cinematography_rules.json`
- [ ] Add citations and sources to `knowledge-base/sources.md`

---

## WEEK 3-4: Backend Foundation

### Fountain Parser Implementation
- [ ] Study Fountain format specification thoroughly
- [ ] Create `backend/app/parser.py`
- [ ] Implement regex patterns for:
  - Scene headers (INT./EXT.)
  - Character names (ALL CAPS before dialogue)
  - Dialogue (text after character name)
  - Action lines (regular paragraph text)
  - Parentheticals (text in parentheses)
- [ ] Test parser with 5 sample Fountain scripts
- [ ] Handle edge cases (empty lines, malformed scenes)
- [ ] Create unit tests in `backend/tests/test_parser.py`

### Emotion Detection Integration (COMPREHENSIVE)
- [ ] Research multiple Hugging Face emotion detection models
- [ ] Implement ensemble model approach:
  - Primary: `SamLowe/roberta-base-go_emotions` (27 emotions: admiration, amusement, anger, annoyance, approval, caring, confusion, curiosity, desire, disappointment, disapproval, disgust, embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness, optimism, pride, realization, relief, remorse, sadness, surprise)
  - Secondary: `j-hartmann/emotion-english-distilroberta-base` (7 emotions for validation)
  - Tertiary: `bhadresh-savani/distilbert-base-uncased-emotion` (6 emotions for additional coverage)
- [ ] Create `backend/app/emotion_detector.py` with ensemble logic
- [ ] Load all models and tokenizers
- [ ] Implement multi-model emotion detection:
  - Input: text string
  - Output: top 3 emotions with confidence scores, emotion intensity (0-100)
  - Support for mixed emotions (e.g., 60% joy + 30% nostalgia + 10% sadness)
- [ ] Create emotion mapping/aggregation system:
  - Map 27 Go-Emotions to your 20+ emotion taxonomy
  - Handle overlapping emotions (e.g., nervousness → anxiety, grief → sadness)
  - Combine predictions from multiple models for robustness
- [ ] Implement dialogue vs action line differentiation
  - Different emotion profiles for spoken vs descriptive text
  - Weight character dialogue higher for subjective emotions
  - Weight action lines higher for situational emotions
- [ ] Test on 20+ sample scenes covering all emotions
- [ ] Benchmark inference time (should be <2 seconds per scene for ensemble)
- [ ] Create comprehensive unit tests in `backend/tests/test_emotion.py`

### Data Schema Definition
- [ ] Create Pydantic models in `backend/app/schemas.py`:
  - `ScriptInput` (uploaded file data)
  - `Scene` (parsed scene structure)
  - `EmotionAnalysis` (detected emotion + confidence)
  - `VisualRecommendation` (color, lighting, camera)
  - `AnalysisResult` (complete output)
- [ ] Add JSON schema examples
- [ ] Validate schema with test data

---

## WEEK 5-7: Visual Mapping Logic

### Color Mapping Implementation
- [ ] Create `backend/app/visual_mapper.py`
- [ ] Implement `map_emotion_to_colors()` function
  - Input: emotion label
  - Output: 5-color palette with hex codes
- [ ] Load mapping from `knowledge-base/emotion_color_map.json`
- [ ] Add confidence weighting (blend colors for mixed emotions)
- [ ] Generate CSS-friendly color palette output
- [ ] Test with all 5 emotions

### Lighting Recommendation System (COMPREHENSIVE)
- [ ] Implement `LightingRecommendationEngine` class with 10+ parameter system
- [ ] Create `recommend_lighting_quality()` function:
  - **Soft lighting (0-33):** Diffused, gentle shadows, flattering, romantic
  - **Medium lighting (34-66):** Balanced, natural, versatile
  - **Hard lighting (67-100):** Sharp shadows, dramatic, harsh, realistic
  - Map each emotion to specific quality score with reasoning
- [ ] Create `recommend_lighting_direction()` function:
  - **Front lighting:** 0° angle, flat, concealing, beauty
  - **Three-quarter lighting:** 45° angle, dimensional, classic
  - **Side lighting:** 90° angle, dramatic, texture-revealing
  - **Rim/back lighting:** 135-180° angle, separation, silhouette, halo
  - **Under lighting:** Below subject, horror, unnatural
  - **Overhead lighting:** Above subject, interrogation, isolation
  - Support multiple light sources with ratios (key:fill:back)
- [ ] Create `recommend_color_temperature()` function:
  - **Very warm:** 2700K-3000K (candlelight, intimate, nostalgic)
  - **Warm:** 3000K-3500K (tungsten, cozy, homey)
  - **Neutral warm:** 3500K-4500K (early morning, comfortable)
  - **Neutral:** 4500K-5500K (daylight, objective, natural)
  - **Neutral cool:** 5500K-6500K (overcast, realistic)
  - **Cool:** 6500K-7500K (shade, distant, clinical)
  - **Very cool:** 7500K+ (moonlight, alien, sterile)
  - Map emotions to specific Kelvin values with precision
- [ ] Create `recommend_lighting_intensity()` function:
  - Measure in lux or foot-candles
  - **Low:** <50 lux (dark, mysterious, intimate)
  - **Medium low:** 50-200 lux (moody, dramatic)
  - **Medium:** 200-500 lux (natural indoor, comfortable)
  - **Medium high:** 500-1000 lux (bright interior, energetic)
  - **High:** >1000 lux (exterior day, high-key, commercial)
  - Consider dynamic range and exposure latitude
- [ ] Create `recommend_contrast_ratio()` function:
  - **Low contrast (2:1 to 3:1):** High-key, bright, optimistic, commercial
  - **Medium contrast (4:1 to 8:1):** Natural, balanced, versatile
  - **High contrast (16:1+):** Low-key, dramatic, film noir, mystery
  - Map to specific lighting ratio recommendations (key:fill)
- [ ] Create `recommend_shadow_characteristics()` function:
  - **Diffused shadows:** Soft edges, gentle gradient, romantic
  - **Defined shadows:** Clear edges, visible but not harsh
  - **Harsh shadows:** Sharp edges, high contrast, dramatic
  - **No shadows:** Completely filled, flat, beauty lighting
  - Consider shadow length and direction for time-of-day implications
- [ ] Implement lighting techniques database:
  - **Rembrandt lighting:** Triangle under eye, dramatic, classical
  - **Butterfly lighting:** Centered shadow under nose, glamour, beauty
  - **Split lighting:** Half face lit, duality, conflict, mystery
  - **Loop lighting:** Small shadow loop from nose, versatile, natural
  - **Broad lighting:** Illuminated side toward camera, widening
  - **Short lighting:** Shadow side toward camera, slimming, dramatic
  - **Chiaroscuro:** Extreme contrast, Baroque style, very dramatic
  - **Silhouette lighting:** Back-lit subject, shape only, mysterious
  - Map each emotion to appropriate techniques
- [ ] Create `recommend_motivated_lighting()` function:
  - Identify practical light sources (windows, lamps, fire, screens)
  - Ensure lighting feels natural and justified by scene
  - Suggest invisible vs visible light sources
- [ ] Create `recommend_lighting_modifiers()` function:
  - Suggest specific equipment: softboxes, umbrellas, flags, scrims, gels
  - Diffusion recommendations (1/4, 1/2, full, double)
  - Color gel suggestions for mood and correction
- [ ] Generate comprehensive lighting plots:
  - 3-point lighting breakdowns (key, fill, back)
  - 4-point and 5-point when needed (background, kicker)
  - Top-down diagram with light positions and intensities
  - Equipment list with specific light types
- [ ] Add detailed textual explanations:
  - Why each parameter was chosen
  - How it supports the emotion
  - Reference famous examples from cinema
  - Example: "Betrayal → Hard side lighting (85/100 hardness) at 90° from cool temperature (6500K) creating sharp, unforgiving shadows that reveal harsh truth and emotional fracture. Medium-high contrast (8:1 ratio) emphasizes the split between loyalty and deception. Motivated by practical window light. As seen in: The Godfather Part II (Fredo confrontation - Gordon Willis, ASC)"

### Camera System Implementation (COMPREHENSIVE)
- [ ] Implement `CameraRecommendationEngine` class
- [ ] Create `suggest_camera_angle()` function with 15+ angle options:
  - **Vertical:** extreme_low, low, eye_level, high, extreme_high, overhead, worms_eye, dutch
  - **Horizontal:** frontal, three_quarter, profile, over_shoulder, pov
  - Map each emotion to preferred angles with confidence scores
  - Support multiple angle recommendations with alternatives
- [ ] Create `suggest_camera_movement()` function:
  - **Options:** static, pan, tilt, dolly_in, dolly_out, track, handheld, steadicam, crane, zoom_in, zoom_out, whip_pan
  - Map emotion intensity to movement intensity
  - Consider scene pacing and narrative context
  - Example: High tension → handheld + quick pans; Serenity → slow crane + gentle movements
- [ ] Create `suggest_shot_composition()` function:
  - **Shot sizes:** ECU (extreme close-up), CU (close-up), MCU (medium close-up), MS (medium shot), MLS (medium long shot), LS (long shot), ELS (extreme long shot)
  - **Multi-character:** two_shot, three_shot, group_shot, OTS
  - Map intimacy/emotional intensity to shot size
  - Consider number of characters in scene
- [ ] Create `suggest_focal_length()` function:
  - **Wide:** 14mm, 18mm, 24mm (distortion, space, context)
  - **Normal:** 35mm, 50mm (natural perspective, versatile)
  - **Portrait:** 85mm, 105mm (flattering, shallow DoF, intimacy)
  - **Telephoto:** 135mm, 200mm+ (compression, isolation, voyeuristic)
  - Map emotional distance to focal length choice
- [ ] Create `suggest_depth_of_field()` function:
  - Shallow DoF (f/1.4-f/2.8) = intimacy, focus, dream-like
  - Medium DoF (f/4-f/8) = balanced, natural, versatile
  - Deep DoF (f/11-f/22) = clarity, context, documentary
  - Map emotion and scene type to aperture recommendations
- [ ] Implement cinematography rationale engine:
  - Generate natural language explanations for each recommendation
  - Cite cinematography principles and film examples
  - Example: "Betrayal → High angle (vulnerability) + handheld (instability) + CU (emotional reaction) + 85mm (isolated focus) | As seen in: The Godfather Part II, Fredo reveal scene"
- [ ] Add confidence scoring system:
  - Primary recommendation (90-100% confidence)
  - Alternative options (70-89% confidence)
  - Context-dependent variables flagged
- [ ] Create comprehensive camera package output:
  - JSON structure with all camera parameters
  - Visual diagram/mockup of camera setup
  - Equipment suggestions (dolly, Steadicam, crane needed?)

### Testing & Validation
- [ ] Create `backend/tests/test_mapper.py`
- [ ] Test all mapping functions with known inputs
- [ ] Verify output format consistency
- [ ] Test edge cases (neutral emotions, ambiguous text)

---

## WEEK 8-10: Backend API Development

### FastAPI Setup
- [ ] Create `backend/app/main.py` with FastAPI app
- [ ] Setup CORS middleware for frontend integration
- [ ] Add logging configuration
- [ ] Create health check endpoint: `GET /health`
- [ ] Setup error handling middleware
- [ ] Add request validation with Pydantic

### Core API Endpoints
- [ ] **POST /api/upload**
  - Accept .fountain file upload
  - Validate file format
  - Return job_id
- [ ] **POST /api/analyze**
  - Accept script text and parameters
  - Parse script into scenes
  - Run emotion detection on each scene
  - Generate visual recommendations
  - Return complete analysis result
- [ ] **GET /api/results/{job_id}**
  - Retrieve stored analysis results
  - Return JSON with all recommendations
- [ ] Add endpoint documentation with examples

### Data Storage (Simple)
- [ ] Use SQLite for storing analysis results
- [ ] Create simple database schema:
  - `analyses` table (id, script_name, created_at, result_json)
- [ ] Implement save/load functions
- [ ] Alternative: Store results as JSON files in `/data` folder

### Testing & Documentation
- [ ] Test all endpoints with Postman/HTTPie
- [ ] Write API documentation in `docs/api.md`
- [ ] Add curl examples for each endpoint
- [ ] Create integration tests
- [ ] Ensure all responses follow schema

---

## WEEK 11-13: Frontend Development

### React Setup
- [ ] Initialize Vite + React project in `frontend/`
- [ ] Install dependencies:
  - TailwindCSS for styling
  - Axios for API calls
  - Recharts for emotion graphs
  - React-Dropzone for file upload
- [ ] Setup Tailwind config
- [ ] Create component structure

### Script Upload Component
- [ ] Create `components/ScriptUploader.jsx`
- [ ] Implement drag-and-drop file upload
- [ ] Add file validation (.fountain only)
- [ ] Show upload progress indicator
- [ ] Display filename and size
- [ ] Clear/reset functionality

### Analysis Display Components
- [ ] Create `components/EmotionGraph.jsx`
  - Line graph showing emotion intensity across scenes
  - X-axis: scene number
  - Y-axis: confidence score (0-100%)
  - Color-coded by emotion type
- [ ] Create `components/ColorPalette.jsx`
  - Display 5-color palette as swatches
  - Show hex codes
  - Copy-to-clipboard functionality
  - Hover to see color names
- [ ] Create `components/LightingCard.jsx`
  - Display lighting parameters
  - Show visual icons for quality/temperature
  - Add explanation text
- [ ] Create `components/CameraCard.jsx`
  - Display camera recommendations
  - Show diagram/icon for angles
  - Add rationale text

### Main App Integration
- [ ] Create `App.jsx` with main layout
- [ ] Implement state management for analysis results
- [ ] Add loading states and spinners
- [ ] Handle error states with user-friendly messages
- [ ] Add export functionality (download JSON report)
- [ ] Make responsive for mobile/tablet/desktop

### Styling & Polish
- [ ] Design cohesive color scheme for app
- [ ] Add smooth transitions and animations
- [ ] Ensure accessibility (ARIA labels, keyboard nav)
- [ ] Test in Chrome, Firefox, Safari
- [ ] Add "About" section explaining the project

---

## WEEK 14-15: Testing & Validation

### Comprehensive Testing
- [ ] Collect 10+ diverse screenplay scenes:
  - 2 happy scenes
  - 2 sad scenes
  - 2 tense scenes
  - 2 angry scenes
  - 2 fearful scenes
- [ ] Run each scene through the system
- [ ] Document outputs in `docs/test_results.md`

### Accuracy Validation
- [ ] Watch actual film versions of test scenes
- [ ] Note real cinematography choices (color, lighting, camera)
- [ ] Compare system recommendations to actual choices
- [ ] Calculate accuracy metrics:
  - Emotion detection accuracy
  - Color palette appropriateness
  - Lighting recommendation match
  - Camera angle alignment
- [ ] Document in `docs/evaluation_results.md`

### User Study (If Possible)
- [ ] Recruit 5-10 film students for feedback
- [ ] Have them rate recommendation quality (1-5 scale)
- [ ] Collect qualitative feedback on usefulness
- [ ] Ask what improvements they'd want
- [ ] Analyze results statistically
- [ ] Document in `docs/user_study.md`

### Bug Fixes & Refinement
- [ ] Fix any bugs found during testing
- [ ] Improve error messages based on user feedback
- [ ] Optimize slow components
- [ ] Add missing edge case handling
- [ ] Polish UI based on feedback

---

## WEEK 16: Final Deliverables

### Deployment
- [ ] Deploy backend to Render.com (free tier)
- [ ] Deploy frontend to Vercel (free tier)
- [ ] Test production deployment end-to-end
- [ ] Add custom domain if budget allows
- [ ] Ensure HTTPS working correctly

### Documentation Completion
- [ ] Polish README.md with:
  - Project description
  - Demo link
  - Setup instructions
  - Screenshots
  - Tech stack details
  - Team members
- [ ] Complete technical documentation:
  - Architecture diagram
  - API documentation
  - Database schema
  - Deployment guide
- [ ] Write user guide with examples
- [ ] Add code comments and docstrings

### Academic Report
- [ ] Write final report (15-20 pages):
  - Abstract (250 words)
  - Introduction & motivation
  - Literature review (3-4 pages)
  - Methodology (3-4 pages)
  - Implementation details (4-5 pages)
  - Evaluation & results (3-4 pages)
  - Discussion & limitations (2 pages)
  - Conclusion & future work (1-2 pages)
  - References (15+ sources)
- [ ] Proofread and format properly
- [ ] Generate PDF

### Demo Video Creation
- [ ] Write demo script (3-5 minutes)
  - Introduction (30 sec)
  - Problem statement (30 sec)
  - System demonstration (2-3 min)
  - Results and validation (60 sec)
  - Conclusion (30 sec)
- [ ] Record screen capture with narration
- [ ] Edit video (add titles, transitions)
- [ ] Upload to YouTube (unlisted or public)
- [ ] Add to README

### Presentation Preparation
- [ ] Create PowerPoint/Google Slides (15-20 slides):
  - Title slide
  - Problem & motivation (2 slides)
  - Background & related work (2-3 slides)
  - System architecture (2 slides)
  - Implementation highlights (3-4 slides)
  - Demo (live or video)
  - Evaluation results (3-4 slides)
  - Lessons learned (1 slide)
  - Future work (1 slide)
  - Conclusion & questions
- [ ] Practice presentation (15 minutes + 5 min Q&A)
- [ ] Prepare for common questions:
  - Why these specific emotions?
  - How accurate is emotion detection?
  - Could this work with other languages?
  - What are main limitations?
  - How would you commercialize this?

### Final Checklist
- [ ] All code committed and pushed to GitHub
- [ ] No sensitive data (API keys, passwords) in repo
- [ ] Tests passing (run full test suite)
- [ ] Demo website live and working
- [ ] All documentation complete
- [ ] Demo video uploaded
- [ ] Presentation slides ready
- [ ] Backup plan if demo fails (screenshots, video)
- [ ] Dress rehearsal with advisor/friend

---

## STRETCH GOALS (If Ahead of Schedule)

### Easy Additions (1-2 days each)
- [ ] Add "Example Scenes" page with pre-loaded analyses
- [ ] Export recommendations as PDF report
- [ ] Add dark mode toggle to UI
- [ ] Show emotion distribution pie chart
- [ ] Add "Compare Scenes" feature

### Medium Additions (3-5 days each)
- [ ] Fine-tune emotion model on IMDB reviews
- [ ] Add genre detection (auto-adjust recommendations)
- [ ] Support PDF upload (using PyPDF2)
- [ ] Add more emotions (10 instead of 5)
- [ ] Create Chrome extension for inline analysis

### Ambitious Additions (1-2 weeks)
- [ ] Build dataset of 100+ annotated scenes
- [ ] Train custom emotion classifier on screenplay corpus
- [ ] Add collaborative features (share analyses)
- [ ] Write conference paper for submission
- [ ] Add real-time analysis (as user types)

---

## GRADING ALIGNMENT

### Technical Implementation (30%)
- ✅ Working full-stack application
- ✅ Clean, well-documented code
- ✅ Proper testing (80%+ coverage ideal)
- ✅ Follows best practices
- ✅ Deployed and accessible online

### Innovation & Research (20%)
- ✅ Novel application of NLP to cinematography
- ✅ Thorough literature review
- ✅ Clear research contribution
- ✅ Validation methodology
- ✅ Academic rigor

### Execution Quality (20%)
- ✅ System works reliably
- ✅ Accurate recommendations
- ✅ Professional UI/UX
- ✅ Meets stated requirements
- ✅ Handles edge cases

### Documentation (15%)
- ✅ Comprehensive technical docs
- ✅ Academic report with proper citations
- ✅ Clear README and setup instructions
- ✅ Code comments and docstrings
- ✅ User guide

### Presentation & Demo (15%)
- ✅ Clear, engaging presentation
- ✅ Working demo (live or video)
- ✅ Handles questions well
- ✅ Professional delivery
- ✅ Good time management

---

## SUCCESS METRICS

### Minimum Viable (B Grade)
- Working demo with 3+ emotions
- 50%+ emotion detection accuracy
- Basic visual recommendations
- Complete documentation
- Successful presentation

### Good Performance (B+ to A-)
- Working demo with 5 emotions
- 60%+ emotion detection accuracy
- Polished UI
- User validation with feedback
- Strong technical implementation

### Excellence (A to A+)
- 70%+ emotion detection accuracy
- Beautiful, professional UI
- User study with 10+ participants
- Novel insights documented
- Publication-quality research component
- Impressive demo that stands out

---

## WEEKLY CHECKPOINTS

### Week 4 Checkpoint
**Expected:** Parser working, emotion detection running, 5 test scenes collected  
**Demo:** Parse sample script and detect emotions

### Week 8 Checkpoint
**Expected:** Visual mapping complete, API endpoints working  
**Demo:** Full backend pipeline (upload → analyze → results)

### Week 12 Checkpoint
**Expected:** Frontend complete, deployed to staging  
**Demo:** Full end-to-end workflow in browser

### Week 16 Final
**Expected:** Everything complete, deployed, documented  
**Demo:** Final presentation and defense

---

## RESOURCE LINKS

### Learning Resources
- **Fountain Format:** https://fountain.io/syntax
- **Hugging Face Transformers:** https://huggingface.co/docs/transformers
- **FastAPI Tutorial:** https://fastapi.tiangolo.com/tutorial/
- **React + Vite:** https://vitejs.dev/guide/
- **Cinematography Basics:** YouTube - "Every Frame a Painting" channel

### Sample Scripts
- **Where to find:** IMSDB (Internet Movie Script Database)
- **Fountain examples:** GitHub - search "fountain screenplay examples"
- **Use public domain scripts to avoid copyright issues**

### Deployment
- **Backend:** render.com, railway.app, fly.io
- **Frontend:** vercel.com, netlify.com
- **Database:** sqlite (local), supabase.com (free PostgreSQL)

---

## CRITICAL SUCCESS FACTORS

1. **Start Early:** Don't wait until week 3 to write code
2. **Test Continuously:** Don't wait until week 14 to test
3. **Document as You Go:** Don't wait until week 16 to write docs
4. **Get Feedback Early:** Show advisor/peers by week 8
5. **Manage Scope:** Cut features if falling behind, not quality
6. **Focus on Demo:** Working demo > perfect code
7. **Backup Everything:** Git commits daily, backup database

---

## EMERGENCY SCOPE REDUCTION PLAN

### If Behind by Week 8
- ✂️ Cut: PDF support (Fountain only)
- ✂️ Cut: User study (just technical validation)
- ✂️ Keep: Core 5 emotions and basic mapping

### If Behind by Week 12
- ✂️ Cut: Advanced visualizations (just tables)
- ✂️ Cut: Database (use JSON files)
- ✂️ Keep: Working demo with basic UI

### If Behind by Week 15
- ✂️ Cut: Deployment (local demo only)
- ✂️ Cut: Polish (focus on functionality)
- ✂️ Keep: Core features working for demo day

**Remember:** Better to have a simple, working demo than a half-built complex system!

---

**Project Status:** READY TO START  
**Difficulty:** Challenging but achievable  
**Portfolio Value:** HIGH  
**Learning Value:** VERY HIGH  
**Wow Factor:** HIGH (visual + AI)  

**Good luck! This will be an impressive capstone project! 🎬✨**
