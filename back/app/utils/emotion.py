from dataclasses import dataclass

@dataclass
class EmotionState:
    affinity:int = 60
    energy:int = 70

    def update_with(self, user_text:str, sent_score:float):
        # 간단한 규칙: 긍정 +, 부정 -
        delta_aff = int(sent_score * 10)   # [-10, +10]
        delta_eng = 2 if len(user_text) < 120 else -1
        # 자연감소/상승 보정
        self.affinity = max(0, min(100, self.affinity + delta_aff))
        self.energy = max(0, min(100, self.energy + delta_eng))

    def to_level(self) -> int:
        # 관계 레벨 규칙
        if self.affinity >= 90: return 3
        if self.affinity >= 75: return 2
        return 1
