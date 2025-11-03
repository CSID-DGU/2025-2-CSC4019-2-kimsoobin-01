import React from "react";

export default function ChatBox({ messages, onSpeak }) {
  return (
    <div className="chat-log">
      {messages.length === 0 && (
        <div className="small" style={{ textAlign: "center", marginTop: 40 }}>
          대화를 시작해보세요 💬
        </div>
      )}
      {messages.map((m, i) => (
        <div key={i} className={`msg ${m.role}`}>
          <div className={`bubble ${m.role}`}>
            {m.text}
            {m.role === "bot" && (
              <span className="tools">
                <button className="btn muted" onClick={() => onSpeak(m.text)}>🔊</button>
              </span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
