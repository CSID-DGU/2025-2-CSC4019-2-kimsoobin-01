import React from "react";

export default function EmotionBar({ label, value = 0, color = "primary" }) {
  const pct = Math.max(0, Math.min(100, Number(value || 0)));
  return (
    <div className="bar-wrap">
      <div className="bar-head">
        <span>{label}</span>
        <strong>{pct}%</strong>
      </div>
      <div className="bar">
        <span style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
