import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { TrendingUp, Clock, Zap } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';

export default function EmotionTimeline({ analysisData, onBeatSelect, selectedBeat, loading }) {
  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <LoadingSpinner message="Building emotional timeline..." size="large" />
      </div>
    );
  }

  if (!analysisData || !analysisData.scenes || analysisData.scenes.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center space-y-4 max-w-md">
          <TrendingUp className="w-16 h-16 mx-auto text-text-secondary" />
          <h3 className="text-lg font-medium">No Analysis Yet</h3>
          <p className="text-sm text-text-secondary">
            Upload a screenplay to see the emotional arc visualization, pacing analysis,
            and scene-by-scene breakdowns.
          </p>
        </div>
      </div>
    );
  }

  // Process data for visualization
  const scenes = analysisData.scenes || [];
  
  // Create emotional arc data
  const emotionData = scenes.flatMap((scene, sceneIdx) => {
    if (!scene.beats || scene.beats.length === 0) {
      return [{
        name: `Scene ${sceneIdx + 1}`,
        sceneId: scene.scene_id,
        intensity: 0,
        emotion: 'neutral',
      }];
    }
    
    return scene.beats.map((beat, beatIdx) => {
      const primaryEmotion = beat.emotional_arc?.primary_emotion;
      return {
        name: `S${sceneIdx + 1}.B${beatIdx + 1}`,
        sceneId: scene.scene_id,
        beatId: beat.beat_id,
        intensity: primaryEmotion?.intensity || 0,
        emotion: primaryEmotion?.emotion || 'neutral',
        beat: beat,
      };
    });
  });

  // Get emotion color
  const getEmotionColor = (emotion) => {
    const colorMap = {
      joy: '#fbbf24',
      happiness: '#fbbf24',
      sadness: '#3b82f6',
      melancholy: '#3b82f6',
      anger: '#ef4444',
      fear: '#8b5cf6',
      anxiety: '#8b5cf6',
      surprise: '#f59e0b',
      tension: '#dc2626',
      disgust: '#10b981',
    };
    return colorMap[emotion?.toLowerCase()] || '#6b7280';
  };

  return (
    <div className="p-4 space-y-6">
      {/* Scene/Beat Segmentation Header */}
      <div className="panel">
        <div className="panel-header">Scene Overview</div>
        <div className="panel-content">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-accent-blue">{scenes.length}</div>
              <div className="text-xs text-text-secondary">Scenes</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-accent-purple">
                {scenes.reduce((sum, s) => sum + (s.beats?.length || 0), 0)}
              </div>
              <div className="text-xs text-text-secondary">Beats</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-500">
                {analysisData.pacing?.average_pace?.toFixed(1) || 'N/A'}
              </div>
              <div className="text-xs text-text-secondary">Avg Pace</div>
            </div>
          </div>
        </div>
      </div>

      {/* Emotional Arc Heatmap */}
      <div className="panel">
        <div className="panel-header flex items-center gap-2">
          <TrendingUp className="w-4 h-4" />
          <span>Emotional Intensity Arc</span>
        </div>
        <div className="panel-content">
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={emotionData}>
              <defs>
                <linearGradient id="colorIntensity" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.2}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#3c3c3c" />
              <XAxis 
                dataKey="name" 
                stroke="#858585" 
                tick={{ fill: '#858585', fontSize: 10 }}
              />
              <YAxis 
                stroke="#858585" 
                tick={{ fill: '#858585', fontSize: 10 }}
                domain={[0, 100]}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#252526',
                  border: '1px solid #3c3c3c',
                  borderRadius: '4px',
                }}
                labelStyle={{ color: '#cccccc' }}
              />
              <Area
                type="monotone"
                dataKey="intensity"
                stroke="#ef4444"
                fill="url(#colorIntensity)"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Pacing Metadata (BPM) */}
      {analysisData.pacing && (
        <div className="panel">
          <div className="panel-header flex items-center gap-2">
            <Zap className="w-4 h-4" />
            <span>Pacing Analysis</span>
          </div>
          <div className="panel-content space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-text-secondary">Rhythm</span>
              <span className="text-sm font-medium">
                {analysisData.pacing.overall_pacing || 'Moderate'}
              </span>
            </div>
            <div className="w-full bg-editor-bg rounded-full h-2">
              <div
                className="bg-accent-blue h-2 rounded-full transition-all"
                style={{
                  width: `${Math.min((analysisData.pacing.average_pace || 5) * 10, 100)}%`,
                }}
              />
            </div>
            <p className="text-xs text-text-secondary">
              {analysisData.pacing.average_pace < 3
                ? 'Slow, contemplative pacing. Static shots recommended.'
                : analysisData.pacing.average_pace > 7
                ? 'Fast, intense pacing. Handheld camera recommended.'
                : 'Moderate pacing. Balanced camera work.'}
            </p>
          </div>
        </div>
      )}

      {/* Scene & Beat List */}
      <div className="panel">
        <div className="panel-header flex items-center gap-2">
          <Clock className="w-4 h-4" />
          <span>Scene Breakdown</span>
        </div>
        <div className="panel-content space-y-2">
          {scenes.map((scene, sceneIdx) => (
            <div key={scene.scene_id} className="border border-panel-border rounded">
              <div className="bg-highlight-bg px-3 py-2 font-medium text-sm">
                Scene {sceneIdx + 1}
                {scene.location && ` - ${scene.location}`}
              </div>
              <div className="p-2 space-y-1">
                {scene.beats && scene.beats.length > 0 ? (
                  scene.beats.map((beat, beatIdx) => {
                    const primaryEmotion = beat.emotional_arc?.primary_emotion;
                    const isSelected = selectedBeat?.beat_id === beat.beat_id;
                    
                    return (
                      <button
                        key={beat.beat_id}
                        onClick={() => onBeatSelect(beat)}
                        className={`
                          w-full text-left px-3 py-2 rounded text-sm
                          transition-all duration-200
                          ${
                            isSelected
                              ? 'bg-accent-blue text-white'
                              : 'hover:bg-highlight-bg'
                          }
                        `}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-medium">Beat {beatIdx + 1}</span>
                          {primaryEmotion && (
                            <span
                              className="badge text-xs"
                              style={{
                                backgroundColor: getEmotionColor(primaryEmotion.emotion) + '20',
                                color: getEmotionColor(primaryEmotion.emotion),
                                border: `1px solid ${getEmotionColor(primaryEmotion.emotion)}`,
                              }}
                            >
                              {primaryEmotion.emotion} ({primaryEmotion.intensity}%)
                            </span>
                          )}
                        </div>
                      </button>
                    );
                  })
                ) : (
                  <div className="text-xs text-text-secondary px-3 py-2">
                    No beats detected
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
