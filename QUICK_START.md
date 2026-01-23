# MSI-VPE Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- **Backend**: Python 3.9+
- **Frontend**: Node.js 20+
- **Browsers**: Chrome, Firefox, Safari, Edge

---

## Step 1: Start the Backend

```bash
cd backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at: http://localhost:8000

---

## Step 2: Start the Frontend

```bash
cd frontend
npm run dev
```

✅ Frontend running at: http://localhost:5173

---

## Step 3: Open the Application

Open your browser and navigate to:
```
http://localhost:5173
```

---

## Step 4: Upload a Screenplay

### Option A: Use Sample Scripts
We've provided 7 sample screenplay scenes in `/sample-scripts/`:

- **tension_scene.fountain** - Police interrogation (Tension, Fear)
- **romance_scene.fountain** - Rooftop proposal (Joy, Hope, Passion)
- **despair_scene.fountain** - Hospital tragedy (Sadness, Despair)
- **triumph_scene.fountain** - Startup launch success (Euphoria, Triumph)
- **action_scene.fountain** - High-intensity combat
- **horror_scene.fountain** - Suspenseful thriller
- **simple_dialogue.fountain** - Basic conversation test

### Option B: Upload Your Own
1. Click the upload area or drag & drop
2. File must be `.fountain` or `.txt` format
3. Uses Fountain screenplay format

---

## Step 5: Explore the Results

### Left Pane: Script Source
- View your uploaded screenplay
- See script statistics
- Character count and analysis info

### Center Pane: Emotional Timeline
- **Emotional Intensity Arc**: Graph showing mood progression
- **Scene Overview**: Total scenes, beats, average pacing
- **Pacing Analysis**: Rhythm indicators (slow/moderate/fast)
- **Scene Breakdown**: Clickable beats with emotion badges

### Right Pane: Intent Inspector
- **Primary Emotion**: Dominant mood with intensity
- **Secondary Emotions**: Additional detected feelings
- **Cinematography**: Camera angles, movement, shot composition
- **Lighting Setup**: Quality, direction, temperature, contrast
- **Color Palette**: Primary/secondary colors with hex codes
- **Export**: Download beat analysis as JSON

---

## Step 6: Export Your Analysis

### Export Single Beat
1. Select a beat from the timeline
2. Click "Export Beat Analysis" in the right pane
3. Downloads: `msi-vpe-analysis-[beat-id].json`

### Export Full Analysis
1. Click "Export All" button in the top bar
2. Downloads: `msi-vpe-full-analysis-[timestamp].json`

---

## Example Workflow

```
1. Upload: tension_scene.fountain
2. Wait: ~3-5 seconds for AI analysis
3. View: Emotional intensity graph (peaks at "dead" reveal)
4. Click: Beat showing "FEAR" emotion
5. Inspect: 
   - High Angle camera (intimidation)
   - Harsh lighting (interrogation)
   - Cold blue color palette
   - Handheld movement (instability)
6. Export: JSON file with all recommendations
```

---

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -ti:8000 | xargs kill -9

# Verify Python version
python3 --version  # Should be 3.9+

# Check dependencies
pip install -r backend/requirements.txt
```

### Frontend won't start
```bash
# Check if port 5173 is in use
lsof -ti:5173 | xargs kill -9

# Verify Node version
node --version  # Should be 20+

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### "Analysis Failed" Error
- Check backend terminal for error logs
- Ensure script is in valid Fountain format
- Try a sample script first to verify system works

### No Emotions Detected
- Script may be too short (minimum ~2 lines of dialogue)
- Try scripts with more expressive dialogue
- Check backend logs for emotion detection errors

---

## Understanding the Output

### Emotion Categories
- **Primary** (6): Joy, Sadness, Anger, Fear, Surprise, Disgust
- **Secondary** (6): Tension, Melancholy, Euphoria, Anxiety, Nostalgia, Loneliness  
- **Tertiary** (8): Hope, Despair, Triumph, Betrayal, Confusion, Serenity, Dread, Passion

### Visual Recommendations
- **Camera Angles**: Low (power), High (vulnerability), Dutch (disorientation)
- **Lighting**: Soft (romance), Hard (drama), Chiaroscuro (conflict)
- **Color Theory**: Warm (passion), Cool (sadness), Desaturated (melancholy)
- **Movement**: Static (contemplation), Handheld (chaos), Dolly (revelation)

### Pacing Scores (0-10)
- **0-3**: Slow, contemplative - Static camera, long takes
- **4-6**: Moderate - Balanced camera work
- **7-10**: Fast, intense - Handheld, rapid cuts

---

## Next Steps

### For Testing
- Try all 7 sample scripts
- Compare emotion detection accuracy
- Test different screenplay formats

### For Development
- Check `/backend/TESTING.md` for running tests
- Review `/frontend/README.md` for architecture
- Explore API docs at http://localhost:8000/docs

### For Presentation
- Use `triumph_scene.fountain` for best visual demo
- Show export functionality
- Demonstrate beat-by-beat inspection

---

## API Endpoints

```
POST /api/v1/analyze
- Submit screenplay for analysis
- Returns: job_id and results

GET /api/v1/jobs/{job_id}
- Retrieve analysis status/results

GET /api/v1/health
- Health check endpoint

GET /docs
- Interactive API documentation (Swagger)
```

---

## Tips for Best Results

### Writing Fountain Scripts
```fountain
Title: Your Scene Name

INT. LOCATION - TIME

Character action and description.

CHARACTER
Dialogue goes here.
```

### Emotion Detection
- Use emotionally charged words
- Include action descriptions (trembling, smiling)
- Mix dialogue with character reactions

### Visual Mapping
- Longer scenes = better pacing analysis
- Character power dynamics affect camera angles
- Mixed emotions create richer color palettes

---

## Support

**Issues?**
- Check terminal logs (backend + frontend)
- Try sample scripts first
- Review error messages in browser console

**Documentation:**
- Backend: `/backend/TESTING.md`
- Frontend: `/frontend/README.md`
- Project Plan: `/CAPSTONE_PROJECT_PLAN.md`

---

**You're all set! 🎬 Start analyzing screenplays and mapping emotions to visuals!**
