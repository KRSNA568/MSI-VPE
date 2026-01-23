# MSI-VPE Frontend

A professional-grade React application for screenplay emotion analysis and visual planning recommendations.

## Features

### Three-Pane Pro Layout
Inspired by professional video editing software (Premiere Pro, Final Cut):

1. **Left Pane - Script Source**
   - Drag & drop `.fountain` file upload
   - Real-time script preview
   - File validation and processing

2. **Center Pane - Emotional Analysis Timeline**
   - Interactive emotional intensity graphs
   - Scene and beat segmentation
   - Pacing analysis visualization
   - Clickable timeline for detailed inspection

3. **Right Pane - Intent Inspector**
   - Detailed visual recommendations per beat
   - Cinematography guidelines (camera angles, movements, lenses)
   - Lighting setup specifications
   - Color palette swatches
   - Export functionality

## Tech Stack

- **React 18** - Component architecture
- **Vite** - Fast development and builds
- **TailwindCSS** - Dark mode pro-app styling
- **Recharts** - Data visualization
- **Axios** - API communication
- **React Dropzone** - File upload UX
- **Lucide React** - Icon system

## Getting Started

### Prerequisites
- Node.js 20+
- npm 10+

### Installation
```bash
npm install
```

### Development
```bash
npm run dev
# Frontend runs at http://localhost:5173
```

### Build
```bash
npm run build
npm run preview  # Preview production build
```

### Testing
```bash
npm run test      # Run tests
npm run test:ui   # Run tests with UI
```

## Design Philosophy

### Dark Mode Pro-App Theme
- Editor background: `#1e1e1e`
- Panel background: `#252526`
- Accent blue: `#007acc`
- Accent purple: `#6b21a8`

### Typography
- **UI Text**: Inter (sans-serif)
- **Code/Data**: Fira Code (monospace)

### Layout
- Fixed top navigation bar with workflow stages
- Three vertical panes with resizable borders (future)
- Dense information display for professional users
- Hover states and transitions for interactivity

## API Integration

The frontend connects to the MSI-VPE backend API:

```javascript
// .env
VITE_API_URL=http://localhost:8000/api/v1
```

### API Endpoints Used
- `POST /analyze` - Submit screenplay for analysis
- `GET /jobs/{job_id}` - Retrieve analysis results

## Component Structure

```
src/
├── App.jsx                      # Main three-pane layout
├── components/
│   ├── ScriptUploader.jsx       # File upload & preview
│   ├── EmotionTimeline.jsx      # Central timeline visualization
│   └── IntentInspector.jsx      # Right pane details
├── services/
│   └── api.js                   # Backend API service
├── index.css                    # Global styles & Tailwind
└── main.jsx                     # App entry point
```

## Future Enhancements

- [ ] Resizable panes
- [ ] Style profile presets (Noir, High Saturation)
- [ ] Export to PDF/JSON/XML
- [ ] Real-time collaboration
- [ ] Scene comparison view
- [ ] Confidence score overlays
- [ ] Film frame examples

## License

MIT - Academic Capstone Project
