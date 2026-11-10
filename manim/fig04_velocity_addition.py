"""그림 4. 보통의 속도는 상대적이지만, 무한히 빠른 빛은 절대적이다."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from style.theme import *

UNIT = 1.05  # 10만 km/s 당 화살표 길이


def speed_row(name, color, speed, y, x0, label=None, infinite=False):
    """로켓 하나와 속도 화살표. speed 단위는 10만 km/s."""
    g = VGroup()
    r = rocket(color, 0.55).move_to([x0, y, 0])
    tag = kr(name, 22, color, BOLD).next_to(r, LEFT, buff=0.2)
    g.add(r, tag)
    if infinite:
        a = Arrow([x0 + 0.5, y, 0], [x0 + 0.5 + 3.3 * UNIT, y, 0], buff=0,
                  color=color, stroke_width=5, tip_length=0.22)
        g.add(a, MathTex(r"\infty", color=color, font_size=44).next_to(a, RIGHT, buff=0.15))
    elif speed > 0:
        a = Arrow([x0 + 0.5, y, 0], [x0 + 0.5 + speed * UNIT, y, 0], buff=0,
                  color=color, stroke_width=5, tip_length=0.22)
        g.add(a, kr(label or f"{speed * 10}만 km/s", 20, FG).next_to(a, RIGHT, buff=0.15))
    else:
        g.add(kr("정지", 20, DIM).next_to(r, RIGHT, buff=0.25))
    return g


def photon_row(y, x0):
    dot = Dot([x0, y, 0], radius=0.11, color=GOLD)
    tag = kr("빛", 22, GOLD, BOLD).next_to(dot, LEFT, buff=0.42)
    a = Arrow([x0 + 0.5, y, 0], [x0 + 0.5 + 3.3 * UNIT, y, 0], buff=0,
              color=GOLD, stroke_width=5, tip_length=0.22)
    inf = MathTex(r"\infty", color=GOLD, font_size=44).next_to(a, RIGHT, buff=0.15)
    return VGroup(dot, tag, a, inf)


class Fig04(Scene):
    def construct(self):
        self.add(heading("속도는 누가 보느냐에 따라 달라진다 — 빛만 빼고?",
                         "갈릴레오 시대의 그림: 빛은 무한히 빠르고, 그래서 누구에게나 같다"))

        lp = panel(6.6, 4.7).move_to([-3.5, -0.45, 0])
        rp = panel(6.6, 4.7).move_to([3.5, -0.45, 0])
        self.add(lp, rp)
        self.add(kr("로켓의 속도: 상대적", 26, FG, BOLD).next_to(lp.get_top(), DOWN, buff=0.3))
        self.add(kr("무한히 빠른 빛: 절대적", 26, FG, BOLD).next_to(rp.get_top(), DOWN, buff=0.3))

        # 왼쪽: A가 볼 때 / B가 볼 때
        lx = -5.6
        self.add(kr("A가 볼 때", 20, DIM).move_to([lx + 0.25, 0.9, 0]))
        self.add(speed_row("A", FG, 0, 0.45, lx))
        self.add(speed_row("B", CYAN, 1, -0.05, lx))
        self.add(speed_row("C", FG, 2, -0.55, lx))
        self.add(Line([lx - 0.6, -0.95, 0], [lx + 4.9, -0.95, 0], color=FAINT, stroke_width=2))
        self.add(kr("B가 볼 때", 20, DIM).move_to([lx + 0.25, -1.3, 0]))
        self.add(speed_row("B", CYAN, 0, -1.75, lx))
        self.add(speed_row("C", FG, 1, -2.25, lx))

        # 오른쪽
        rx = 1.4
        self.add(kr("A가 볼 때", 20, DIM).move_to([rx + 0.25, 0.9, 0]))
        self.add(speed_row("A", FG, 0, 0.45, rx))
        self.add(photon_row(-0.3, rx))
        self.add(Line([rx - 0.6, -0.95, 0], [rx + 4.9, -0.95, 0], color=FAINT, stroke_width=2))
        self.add(kr("B가 볼 때", 20, DIM).move_to([rx + 0.25, -1.3, 0]))
        self.add(speed_row("B", CYAN, 0, -1.75, rx))
        self.add(photon_row(-2.25, rx))

        self.add(footnote("C의 속도는 20만에서 10만으로 줄지만, 무한대에서 10만을 빼도 여전히 무한대다."))
