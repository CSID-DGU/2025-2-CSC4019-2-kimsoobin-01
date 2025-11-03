import React, { useMemo, useState } from "react";
import { api } from "./api";
import ChatBox from "./components/ChatBox";
import CharacterCard from "./components/CharacterCard";
import RecorderButton from "./components/RecorderButton";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ affinity: 60, energy: 70, relation_level: 1 });
  const latestBot = useMemo(() => {
    const botMsgs = [...messages].reverse().find((m) => m.role === "bot");
    return botMsgs?.text || "";
  }, [messages]);

  const sendText = async (text) => {
    if (!text.trim()) return;
    const msg = text.trim();

    setMessages((prev) => [...prev, { role: "user", text: msg }]);
    setInput("");
    setLoading(true);
    try {
      const res = await api.post("/v1/chat", {
        user_external_id: "front-user",
        message: msg
      });
      const { reply, affinity, energy, relation_level } = res.data;
      setMessages((prev) => [...prev, { role: "bot", text: reply }]);
      setStats({ affinity, energy, relation_level });
    } catch (e) {
      console.error(e);
      setMessages((prev) => [...prev, { role: "bot", text: "❌ 서버 오류가 발생했습니다." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = () => sendText(input);

  const handleTTS = async (text) => {
    try {
      const res = await api.post(
        "/v1/audio/tts",
        { text },
        { responseType: "blob" }
      );
      const url = URL.createObjectURL(res.data);
      new Audio(url).play();
    } catch (e) {
      alert("TTS 실패");
    }
  };

  const handleSTTResult = (transcript) => {
    if (!transcript) return;
    // 전송 전 확인하고 싶으면 input에 넣고 수동 전송, 자동이면 바로 send
    setInput(transcript);
    // 바로 보낼 경우:
    // sendText(transcript);
  };

  return (
    <div className="container">
      <CharacterCard stats={stats} onTts={handleTTS} latestBotMsg={latestBot} />

      <div className="card chat-wrap">
        <div className="chat-title">🎧 AI 영어 교사</div>
        <ChatBox messages={messages} onSpeak={handleTTS} />

        <div className="chat-input">
          <input
            placeholder="메시지를 입력하거나, 말하기 버튼을 누르세요…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !loading && handleSend()}
          />
          <button className="btn" onClick={handleSend} disabled={loading}>
            {loading ? "..." : "보내기"}
          </button>
          <RecorderButton onResult={handleSTTResult} />
        </div>

        <div className="small" style={{ marginTop: 6 }}>
          * 엔터키로 전송 • 🔊 버튼으로 읽어주기 • 🎙️로 말하면 자동으로 텍스트 변환
        </div>
      </div>
    </div>
  );
}
