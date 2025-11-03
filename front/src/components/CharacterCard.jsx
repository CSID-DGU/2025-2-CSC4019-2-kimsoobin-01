import React from "react";
import EmotionBar from "./EmotionBar";

export default function CharacterCard({ stats, onTts, latestBotMsg }) {
  const { affinity = 60, energy = 70, relation_level = 1 } = stats || {};
  return (
    <div className="card">
      <div className="char-header">
        <img
          className="char-avatar"
          src="https://images.unsplash.com/photo-1527980965255-d3b416303d12?q=80&w=400&auto=format&fit=crop"
          alt="Luca avatar"
        />
        <div>
          <div className="char-name">Luca <span className="small">AI English Partner</span></div>
          <div className="char-sub">Bright • Positive • Encouraging</div>
          <div className="small">Relation Lv.{relation_level}</div>
        </div>
      </div>

      <div className="kpis">
        <EmotionBar label="Affinity" value={affinity} />
        <EmotionBar label="Energy" value={energy} />
      </div>

      <div style={{ marginTop: 14, display: "flex", gap: 8 }}>
        <button className="btn" onClick={() => onTts(latestBotMsg || "Hello! Let's study together!")}>
          🔊 마지막 답변 듣기
        </button>
        <button className="btn muted" onClick={() => window.open("/docs", "_blank")}>API 문서</button>
      </div>
    </div>
  );
}
