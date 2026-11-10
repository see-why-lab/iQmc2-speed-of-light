"""그림 9. 동시성의 상대성 — B의 '지금'은 기울어져 있다 (v = 0.5c)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from spacetime import *

V = 0.5


class Fig09(Scene):
    def construct(self):
        self.add(heading("A의 '지금'과 B의 '지금'은 다르다",
                         "B는 A에 대해 광속의 절반으로 움직인다. 출발 1초 뒤, 빛은 어디에 있는가?"))

        d = Diagram(origin=[-5.6, -3.1, 0], unit=2.35, xmax=2.5, tmax=2.2)
        self.add(d.grid(2), d.axes())
        self.add(d.light(2.1))
        self.add(kr("빛", 24, GOLD, BOLD).move_to(d.p(2.02, 2.17)))

        # B의 세계선(ct'축)과 x'축
        t_ax, x_ax = d.moving_axes(V, length=2.3)
        self.add(t_ax, x_ax)
        self.add(MathTex("ct'", color=CYAN, font_size=36).next_to(t_ax.get_end(), UP, buff=0.1))
        self.add(MathTex("x'", color=CYAN, font_size=36).next_to(x_ax.get_end(), RIGHT, buff=0.1))

        # A의 시계로 1초: B는 (0.5, 1), 빛은 (1, 1)
        b_event = d.p(V, 1)
        a_now = DashedLine(d.p(0, 1), d.p(2.25, 1), color=FG, stroke_width=2.5, dash_length=0.1)
        photon_a = d.p(1, 1)
        # B의 동시선: 기울기 v 로 B의 사건을 지난다 → 빛과 (1+v, 1+v)에서 만난다
        xb = 1 + V
        photon_b = d.p(xb, xb)
        b_now = DashedLine(d.p(0.0, 1 - V * V), d.p(2.25, 1 + V * (2.25 - V)),
                           color=CYAN, stroke_width=2.5, dash_length=0.1)
        self.add(a_now, b_now)
        self.add(Dot(b_event, radius=0.09, color=CYAN),
                 Dot(photon_a, radius=0.1, color=FG),
                 Dot(photon_b, radius=0.1, color=GOLD))
        self.add(kr("B", 22, CYAN, BOLD).next_to(b_event, UL, buff=0.08))
        self.add(MathTex("1", color=DIM, font_size=30).next_to(d.p(0, 1), LEFT, buff=0.12))
        self.add(MathTex("1", color=DIM, font_size=30).next_to(d.p(1, 0), DOWN, buff=0.12))
        self.add(MathTex("2", color=DIM, font_size=30).next_to(d.p(2, 0), DOWN, buff=0.12))
        self.add(MathTex("2", color=DIM, font_size=30).next_to(d.p(0, 2), LEFT, buff=0.12))

        # 오른쪽 설명
        x_txt = 1.25
        blocks = VGroup(
            VGroup(kr("A의 '지금' (수평 점선)", 24, FG, BOLD),
                   kr("빛은 30만 km 앞, 흰 점에 있다.", 21, FG),
                   kr("B와 빛 사이는 15만 km뿐이다.", 21, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
            VGroup(kr("B의 '지금' (기울어진 점선)", 24, CYAN, BOLD),
                   kr("B에게 동시인 사건들은 x'축과 나란하다.", 21, FG),
                   kr("이 선이 빛과 만나는 곳은 금색 점,", 21, FG),
                   kr("A에게는 아직 오지 않은 미래다.", 21, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
            VGroup(kr("그래서", 24, GOLD, BOLD),
                   kr("B가 쫓아간 만큼 빛은 미래로 물러나 있고,", 21, FG),
                   kr("B가 재도 빛의 속도는 그대로다.", 21, FG)).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        blocks.move_to([x_txt, -0.6, 0], aligned_edge=LEFT)
        self.add(blocks)
