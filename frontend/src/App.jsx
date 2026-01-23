import { useState } from 'react';
import { Film, Sparkles, Activity } from 'lucide-react';
import ScriptUploader from './components/ScriptUploader';
import EmotionTimeline from './components/EmotionTimeline';
import IntentInspector from './components/IntentInspector';
import apiService from './services/api';

function App() {
  const [scriptText, setScriptText] = useState('');
  const [analysisData, setAnalysisData] = useState(null);
  const [selectedBeat, setSelectedBeat] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [scriptTitle, setScriptTitle] = useState('Screenplay');

  const handleExportAll = () => {
    if (!analysisData) return;

    const exportData = {
      timestamp: new Date().toISOString(),
      script_length: scriptText.length,
      analysis: analysisData,
      metadata: {
        app_version: '1.0.0',
        export_format: 'MSI-VPE JSON v1'
      }
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `msi-vpe-full-analysis-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleScriptUpload = async (textOrFile, filename = 'Screenplay') => {
    setScriptTitle(filename);
    setLoading(true);
    setError(null);

    try {
      let result;
      
      // Check if it's a File object (PDF) or text string
      if (textOrFile instanceof File) {
        // PDF file - send via FormData to upload endpoint
        result = await apiService.uploadScriptFile(textOrFile, filename);
        // For display purposes, show a placeholder since we can't display PDF content easily
        setScriptText(`[PDF File: ${textOrFile.name}]\\n\\nPDF content extracted and analyzed.`);
      } else {
        // Text content - send to analyze endpoint
        setScriptText(textOrFile);
        result = await apiService.analyzeScript(textOrFile, filename);
      }
      
      console.log('Analysis result:', result);
      
      // Store job ID for PDF export
      if (result.job_id) {
        setJobId(result.job_id);
      }
      
      // The API returns the result directly in the response
      if (result.result) {
        // Convert result to scenes array format
        const formattedData = {
          scenes: [result.result],
          pacing: result.result.pacing_metadata
        };
        setAnalysisData(formattedData);
      } else if (result.job_id) {
        // Fallback: poll for results
        const jobResult = await apiService.getJobStatus(result.job_id);
        const formattedData = {
          scenes: [JSON.parse(jobResult.result_json)],
          pacing: JSON.parse(jobResult.result_json).pacing_metadata
        };
        setAnalysisData(formattedData);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBeatSelect = (beat) => {
    setSelectedBeat(beat);
  };

  return (
    <div className="min-h-screen bg-editor-bg">
      {/* Global Top Bar */}
      <header className="bg-panel-bg border-b border-panel-border px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Film className="w-8 h-8 text-accent-blue" />
            <div>
              <h1 className="text-xl font-bold">MSI-VPE</h1>
              <p className="text-xs text-text-secondary">Screenplay Visual Planning Engine</p>
            </div>
          </div>
          
          {/* Workflow Stages */}
          <div className="flex items-center gap-2 text-sm">
            <span className={`px-3 py-1 rounded ${scriptText ? 'bg-green-600' : 'bg-panel-border'}`}>
              Upload
            </span>
            <span className="text-text-secondary">›</span>
            <span className={`px-3 py-1 rounded ${analysisData ? 'bg-green-600' : 'bg-panel-border'}`}>
              Analysis
            </span>
            <span className="text-text-secondary">›</span>
            <span className={`px-3 py-1 rounded ${selectedBeat ? 'bg-green-600' : 'bg-panel-border'}`}>
              Refinement
            </span>
            <span className="text-text-secondary">›</span>
            <span className="px-3 py-1 rounded bg-panel-border">Export</span>
          </div>

          {/* Style Profile Selector (Future Feature) */}
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-accent-purple" />
            <select className="input text-sm">
              <option>Default Style</option>
              <option disabled>Noir (Coming Soon)</option>
              <option disabled>High Saturation (Coming Soon)</option>
            </select>
            <button
              onClick={handleExportAll}
              className="btn-secondary text-sm flex items-center gap-2"
              disabled={!analysisData}
            >
              <Film className="w-4 h-4" />
              Export All
            </button>
          </div>
        </div>
      </header>

      {/* Three-Pane Layout */}
      <div className="flex h-[calc(100vh-73px)]">
        {/* Left Pane: Script Viewer */}
        <div className="w-1/4 border-r border-panel-border overflow-hidden flex flex-col">
          <div className="panel-header flex items-center gap-2">
            <Film className="w-4 h-4" />
            <span>Script Source</span>
          </div>
          <div className="flex-1 overflow-y-auto">
            <ScriptUploader
              onScriptUpload={handleScriptUpload}
              scriptText={scriptText}
              loading={loading}
            />
          </div>
        </div>

        {/* Center Pane: Analysis Timeline */}
        <div className="flex-1 border-r border-panel-border overflow-hidden flex flex-col">
          <div className="panel-header flex items-center gap-2">
            <Activity className="w-4 h-4" />
            <span>Emotional Analysis Timeline</span>
          </div>
          <div className="flex-1 overflow-y-auto">
            {error && (
              <div className="m-4 p-4 bg-red-900/20 border border-red-600 rounded text-red-400">
                {error}
              </div>
            )}
            <EmotionTimeline
              analysisData={analysisData}
              onBeatSelect={handleBeatSelect}
              selectedBeat={selectedBeat}
              loading={loading}
            />
          </div>
        </div>

        {/* Right Pane: Intent Inspector */}
        <div className="w-1/3 overflow-hidden flex flex-col">
          <div className="panel-header flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            <span>Intent Inspector</span>
          </div>
          <div className="flex-1 overflow-y-auto">
            <IntentInspector
              selectedBeat={selectedBeat}
              analysisData={analysisData}
              jobId={jobId}
              scriptTitle={scriptTitle}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
