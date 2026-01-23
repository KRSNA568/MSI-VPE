export default function ColorSwatch({ color, label, size = 'default' }) {
  const sizes = {
    small: 'h-8',
    default: 'h-12',
    large: 'h-16',
  };

  return (
    <div className="flex-1 min-w-0">
      <div
        className={`${sizes[size]} rounded border border-panel-border shadow-sm transition-transform hover:scale-105 cursor-pointer`}
        style={{ backgroundColor: color }}
        title={`${label}: ${color}`}
      />
      <div className="text-xs text-center mt-1 font-mono text-text-secondary truncate">
        {color}
      </div>
      {label && (
        <div className="text-xs text-center text-text-secondary opacity-75">
          {label}
        </div>
      )}
    </div>
  );
}
