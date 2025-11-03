import React, { useEffect, useRef, useState } from "react";
import { api } from "../api";

// audio Blob → base64
const toBase64 = (blob) =>
  new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onload = () => resolve(fr.result.split(",")[1]);
    fr.onerror = reject;
    fr.readAsDataURL(blob);
  });

export default function RecorderButton({ onResult, autoSend = true }) {
  const [rec, setRec] = useState(null);
  const [status, setStatus] = useState("idle");
  const chunksRef = useRef([]);

  useEffect(() => {
    return () => { if (rec && rec.state !== "inactive") rec.stop(); };
  }, [rec]);

  const start = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRec = new MediaRecorder(stream, { mimeType: "audio/webm" });
      chunksRef.current = [];
      mediaRec.ondataavailable = (e) => e.data.size && chunksRef.current.push(e.data);
      mediaRec.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        const b64 = await toBase64(blob);
        setStatus("transcribing");
        try {
          const res = await api.post("/v1/audio/stt", { audio_base64: b64, mime: "audio/webm" });
          if (onResult) onResult(res.data.text || "");
        } catch (e) {
          alert("STT 실패");
        } finally {
          setStatus("idle");
        }
      };
      mediaRec.start();
      setRec(mediaRec);
      setStatus("recording");
    } catch (e) {
      alert("마이크 권한이 필요합니다.");
    }
  };

  const stop = () => {
    if (rec && rec.state !== "inactive") {
      rec.stop();
      rec.stream.getTracks().forEach((t) => t.stop());
      setRec(null);
      setStatus("processing");
    }
  };

  const recording = status === "recording";

  return (
    <div>
      {!recording ? (
        <button className="btn warn" onClick={start}>🎙️ 말하기</button>
      ) : (
        <button className="btn danger" onClick={stop}>⏹️ 멈추기</button>
      )}
      <span className="rec-status">
        {status === "recording" && <><span className="pulse"></span>Recording…</>}
        {status === "processing" && " Processing…"}
        {status === "transcribing" && " Transcribing…"}
      </span>
    </div>
  );
}
