import { Camera, Lightbulb, Palette, Film, Download } from 'lucide-react';

export default function IntentInspector({ selectedBeat, analysisData }) {
  if (!analysisData) {
    return (
      <div className="p-4">
        <div className="panel">
          <div className="panel-content text-center py-12">
            <Film className="w-12 h-12 mx-auto text-text-secondary mb-4" />
            <h3 className="text-lg font-medium mb-2">No Data Available</h3>
            <p className="text-sm text-text-secondary">
              Upload and analyze a screenplay to see detailed visual recommendations.
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!selectedBeat) {
    return (
      <div className="p-4">
        <div className="panel">
          <div className="panel-content text-center py-12">
            <Camera className="w-12 h-12 mx-auto text-text-secondary mb-4" />
            <h3 className="text-lg font-medium mb-2">Select a Beat</h3>
            <p className="text-sm text-text-secondary">
              Choose a beat from the timeline to see detailed cinematography and lighting recommendations.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const { emotional_arc, visual_signals } = selectedBeat;
  const primaryEmotion = emotional_arc?.primary_emotion;
  const secondaryEmotions = emotional_arc?.secondary_emotions || [];

  return (
    <div className="p-4 space-y-4">
      {/* Primary Intent Tags */}
      <div className="panel">
        <div className="panel-header">Primary Emotion</div>
        <div className="panel-content">
          {primaryEmotion ? (
            <div className="badge bg-accent-blue text-white text-sm px-3 py-1.5">
              {primaryEmotion.emotion.toUpperCase()} ({primaryEmotion.intensity}%)
            </div>
          ) : (
            <span className="text-sm text-text-secondary">No primary emotion detected</span>
          )}
          {secondaryEmotions.length > 0 && (
            <div className="mt-3">
              <div className="text-xs text-text-secondary mb-2">Secondary:</div>
              <div className="flex flex-wrap gap-2">
                {secondaryEmotions.map((em, idx) => (
                  <div
                    key={idx}
                    className="badge bg-panel-border text-text-primary text-xs px-2 py-1"
                  >
                    {em.emotion} ({em.intensity}%)
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Cinematography Recommendations */}
      {visual_signals?.cinematography && (
        <div className="panel">
          <div className="panel-header flex items-center gap-2">
            <Camera className="w-4 h-4" />
            <span>Cinematography</span>
          </div>
          <div className="panel-content space-y-4">
            {/* Shot Composition */}
            {visual_signals.cinematography.shot_composition && (
              <div>
                <div className="text-xs font-semibold text-text-secondary mb-2">SHOT COMPOSITION</div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-text-secondary">Shot Size:</span>
                    <span className="font-medium">
                      {visual_signals.cinematography.shot_composition.primary_shot_size?.toUpperCase() || 'N/A'}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-text-secondary">Depth:</span>
                    <span className="font-medium">
                      {visual_signals.cinematography.shot_composition.depth_staging || 'N/A'}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Camera Angles */}
            {visual_signals.cinematography.camera_angles && (
              <div>
                <div className="text-xs font-semibold text-text-secondary mb-2">CAMERA ANGLES</div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-text-secondary">Vertical:</span>
                    <span className="font-medium">
                      {visual_signals.cinematography.camera_angles.vertical_angle || 'Eye Level'}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-text-secondary">Horizontal:</span>
                    <span className="font-medium">
                      {visual_signals.cinematography.camera_angles.horizontal_angle || 'Frontal'}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Camera Movement */}
            {visual_signals.cinematography.camera_movement && (
              <div>
                <div className="text-xs font-semibold text-text-secondary mb-2">CAMERA MOVEMENT</div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-text-secondary">Type:</span>
                    <span className="font-medium">
                      {visual_signals.cinematography.camera_movement.movement_type || 'Static'}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-text-secondary">Speed:</span>
                    <span className="font-medium">
                      {visual_signals.cinematography.camera_movement.speed || 'Moderate'}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Lens & Focus */}
            {visual_signals.cinematography.lens_focus && (
              <div>
                <div className="text-xs font-semibold text-text-secondary mb-2">LENS & FOCUS</div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-text-secondary">Focal Length:</span>
                    <span className="font-medium">
                      {visual_signals.cinematography.lens_focus.focal_length || 'Standard'}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-text-secondary">Depth of Field:</span>
                    <span className="font-medium">
                      {visual_signals.cinematography.lens_focus.depth_of_field || 'Normal'}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Lighting Recommendations */}
      {visual_signals?.lighting && (
        <div className="panel">
          <div className="panel-header flex items-center gap-2">
            <Lightbulb className="w-4 h-4" />
            <span>Lighting Setup</span>
          </div>
          <div className="panel-content space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-text-secondary">Quality:</span>
              <span className="font-medium">
                {visual_signals.lighting.quality || 'Soft'}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-text-secondary">Direction:</span>
              <span className="font-medium">
                {visual_signals.lighting.direction || 'Three Point'}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-text-secondary">Temperature:</span>
              <span className="font-medium">
                {visual_signals.lighting.temperature || '5600K'}
              </span>
            </div>
            {visual_signals.lighting.contrast_ratio && (
              <div className="flex justify-between text-sm">
                <span className="text-text-secondary">Contrast Ratio:</span>
                <span className="font-medium">
                  {visual_signals.lighting.contrast_ratio}
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Color Palette */}
      {visual_signals?.color_palette && (
        <div className="panel">
          <div className="panel-header flex items-center gap-2">
            <Palette className="w-4 h-4" />
            <span>Color Palette</span>
          </div>
          <div className="panel-content space-y-4">
            {/* Primary Colors */}
            {visual_signals.color_palette.primary_colors && (
              <div>
                <div className="text-xs font-semibold text-text-secondary mb-2">PRIMARY</div>
                <div className="flex gap-2">
                  {visual_signals.color_palette.primary_colors.map((color, idx) => (
                    <div key={idx} className="flex-1">
                      <div
                        className="h-12 rounded border border-panel-border"
                        style={{ backgroundColor: color }}
                      />
                      <div className="text-xs text-center mt-1 font-mono">{color}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Secondary Colors */}
            {visual_signals.color_palette.secondary_colors && (
              <div>
                <div className="text-xs font-semibold text-text-secondary mb-2">SECONDARY</div>
                <div className="flex gap-2">
                  {visual_signals.color_palette.secondary_colors.map((color, idx) => (
                    <div key={idx} className="flex-1">
                      <div
                        className="h-8 rounded border border-panel-border"
                        style={{ backgroundColor: color }}
                      />
                      <div className="text-xs text-center mt-1 font-mono">{color}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Saturation & Warmth */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-text-secondary">Saturation:</span>
                <span className="font-medium">
                  {visual_signals.color_palette.saturation || 'Normal'}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-text-secondary">Warmth:</span>
                <span className="font-medium">
                  {visual_signals.color_palette.warmth || 'Neutral'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Export Button */}
      <button className="btn-primary w-full flex items-center justify-center gap-2">
        <Download className="w-4 h-4" />
        <span>Export Beat Analysis</span>
      </button>
    </div>
  );
}
