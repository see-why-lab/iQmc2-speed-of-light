"""그림 7. 광속 개념의 세 단계."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from style.theme import *


class Fig07(Scene):
    def construct(self):
        self.add(heading("빛의 속도, 세 번 바뀐 생각"))

        stages = [
            ("갈릴레오 시대까지", "무한", "절대적", "켜는 순간 어디에나 닿는다", DIM, DIM),
            ("측정 기술의 발달", "유한", "상대적", "그렇다면 쫓아가면 느려 보여야 한다", GOLD, DIM),
            ("마이컬슨–몰리 이후", "유한", "절대적", "쫓아가도 언제나 같은 속도다", GOLD, CYAN),
        ]
        cards = VGroup()
        for when, a, b, note, ca, cb in stages:
            box = panel(3.9, 3.9)
            w = kr(when, 22, DIM).next_to(box.get_top(), DOWN, buff=0.35)
            big = VGroup(kr(a, 46, ca, BOLD), kr("하면서", 20, DIM), kr(b, 46, cb, BOLD))
            big.arrange(DOWN, buff=0.2).move_to(box.get_center() + UP * 0.1)
            n = kr(note, 18, FG).next_to(box.get_bottom(), UP, buff=0.35)
            cards.add(VGroup(box, w, big, n))
        cards.arrange(RIGHT, buff=0.75).move_to(DOWN * 0.4)
        self.add(cards)
        for i in range(2):
            self.add(Arrow(cards[i].get_right(), cards[i + 1].get_left(), buff=0.12,
                           color=DIM, stroke_width=3, tip_length=0.2))

        self.add(footnote("세 번째 칸이 모순처럼 보인다는 것이, 특수 상대성 이론의 출발점이다."))
