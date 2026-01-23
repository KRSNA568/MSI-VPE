import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, Check } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';

export default function ScriptUploader({ onScriptUpload, scriptText, loading }) {
  const onDrop = useCallback(
    (acceptedFiles) => {
      const file = acceptedFiles[0];
      if (file) {
        // For PDF files, we'll send the file directly to the server
        // For text files, we'll read and send the text
        if (file.name.toLowerCase().endsWith('.pdf')) {
          // Send PDF file directly
          onScriptUpload(file, file.name.replace(/\.pdf$/i, ''));
        } else {
          // Read text files
          const reader = new FileReader();
          reader.onload = (e) => {
            const text = e.target.result;
            const filename = file.name.replace(/\.(fountain|txt)$/i, '');
            onScriptUpload(text, filename);
          };
          reader.readAsText(file);
        }
      }
    },
    [onScriptUpload]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.fountain', '.txt'],
      'application/pdf': ['.pdf'],
    },
    multiple: false,
  });

  if (scriptText && !loading) {
    return (
      <div className="p-4 space-y-4">
        {/* Script Uploaded State */}
        <div className="flex items-center gap-2 text-green-500 bg-green-900/20 border border-green-600 rounded p-3">
          <Check className="w-5 h-5" />
          <span className="font-medium">Script Loaded</span>
        </div>

        {/* Script Preview */}
        <div className="panel">
          <div className="panel-header flex items-center justify-between">
            <span>Script Preview</span>
            <button
              onClick={() => window.location.reload()}
              className="text-xs text-accent-blue hover:underline"
            >
              Upload New
            </button>
          </div>
          <div className="panel-content">
            <pre className="text-xs font-mono text-text-secondary whitespace-pre-wrap max-h-96 overflow-y-auto">
              {scriptText.substring(0, 1000)}
              {scriptText.length > 1000 && '...'}
            </pre>
            <div className="mt-2 text-xs text-text-secondary">
              {scriptText.length} characters
            </div>
          </div>
        </div>

        {/* Beat Markers Info */}
        <div className="panel">
          <div className="panel-header">Analysis Segments</div>
          <div className="panel-content text-sm text-text-secondary">
            <p>
              The script has been segmented into scenes and beats for emotional analysis.
              Select beats from the timeline to see detailed recommendations.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4">
      {/* Upload State */}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-all duration-200
          ${
            isDragActive
              ? 'border-accent-blue bg-accent-blue/10'
              : 'border-panel-border hover:border-accent-blue/50 bg-panel-bg'
          }
          ${loading ? 'pointer-events-none opacity-50' : ''}
        `}
      >
        <input {...getInputProps()} />

        {loading ? (
          <LoadingSpinner message="Analyzing screenplay..." size="large" />
        ) : (
          <div className="space-y-4">
            <Upload className="w-12 h-12 mx-auto text-text-secondary" />
            <div>
              <p className="text-text-primary font-medium mb-2">
                {isDragActive ? 'Drop your screenplay here' : 'Drag & drop screenplay file'}
              </p>
              <p className="text-sm text-text-secondary">
                or click to browse
              </p>
            </div>
            <div className="flex items-center justify-center gap-2 text-xs text-text-secondary">
              <FileText className="w-4 h-4" />
              <span>Supports .fountain, .txt, and .pdf files</span>
            </div>
          </div>
        )}
      </div>

      {/* Instructions */}
      {!loading && (
        <div className="mt-6 space-y-4">
          <div className="panel">
            <div className="panel-header">Fountain Format</div>
            <div className="panel-content text-sm text-text-secondary space-y-2">
              <p>Upload a screenplay in Fountain format:</p>
              <div className="bg-editor-bg p-3 rounded font-mono text-xs">
                <div className="text-text-primary">INT. COFFEE SHOP - DAY</div>
                <div className="mt-2">SARAH sits alone, staring at her phone.</div>
                <div className="mt-2 ml-8">
                  <div className="text-text-primary">SARAH</div>
                  <div>I can't believe you did this.</div>
                </div>
              </div>
            </div>
          </div>

          <div className="panel">
            <div className="panel-header">What happens next?</div>
            <div className="panel-content text-sm text-text-secondary">
              <ol className="list-decimal list-inside space-y-2">
                <li>Script is parsed into scenes and beats</li>
                <li>AI detects emotions in dialogue and action</li>
                <li>Visual recommendations are generated</li>
                <li>Explore results in the timeline</li>
              </ol>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
