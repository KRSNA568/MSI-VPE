/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dark mode pro-app theme
        'editor-bg': '#1e1e1e',
        'panel-bg': '#252526',
        'panel-border': '#3c3c3c',
        'accent-blue': '#007acc',
        'accent-purple': '#6b21a8',
        'text-primary': '#cccccc',
        'text-secondary': '#858585',
        'highlight-bg': '#2d2d30',
        
        // Emotion colors
        'emotion-joy': '#fbbf24',
        'emotion-sadness': '#3b82f6',
        'emotion-anger': '#ef4444',
        'emotion-fear': '#8b5cf6',
        'emotion-surprise': '#f59e0b',
        'emotion-tension': '#dc2626',
      },
      fontFamily: {
        'mono': ['Fira Code', 'Monaco', 'Courier New', 'monospace'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
