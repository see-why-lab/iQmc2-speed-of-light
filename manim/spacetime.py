"""시공간 도표 공통 도구. 단위: 가로 x(광초), 세로 ct(광초). 빛은 45°."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from manim import *
from style.theme import *


class Diagram:
    """origin(화면 좌표)과 unit(1광초의 화면 길이)로 정의되는 시공간 도표."""

    def __init__(self, origin, unit, xmax=2.3, tmax=2.3):
        self.o = np.array(origin, dtype=float)
        self.u = unit
        self.xmax, self.tmax = xmax, tmax

    def p(self, x, ct):
        return self.o + np.array([x * self.u, ct * self.u, 0])

    def axes(self, xlabel="x", tlabel="ct", color=FG):
        ax = Arrow(self.p(-0.25, 0), self.p(self.xmax, 0), buff=0, color=color,
                   stroke_width=3, tip_length=0.2)
        at = Arrow(self.p(0, -0.25), self.p(0, self.tmax), buff=0, color=color,
                   stroke_width=3, tip_length=0.2)
        lx = MathTex(xlabel, color=color, font_size=36).next_to(ax, RIGHT, buff=0.12)
        lt = MathTex(tlabel, color=color, font_size=36).next_to(at, UP, buff=0.12)
        return VGroup(ax, at, lx, lt)

    def grid(self, n=2):
        g = VGroup()
        for i in range(1, n + 1):
            g.add(Line(self.p(i, 0), self.p(i, self.tmax - 0.15), color=FAINT, stroke_width=1.5))
            g.add(Line(self.p(0, i), self.p(self.xmax - 0.15, i), color=FAINT, stroke_width=1.5))
        return g

    def light(self, length=None):
        """원점에서 오른쪽으로 떠난 광자의 세계선."""
        m = length or min(self.xmax, self.tmax) - 0.1
        return Line(self.p(0, 0), self.p(m, m), color=GOLD, stroke_width=5)

    def moving_axes(self, v, color=CYAN, length=None):
        """속도 v(c 단위)로 움직이는 관측자의 ct'축과 x'축."""
        m = length or self.tmax - 0.1
        # ct'축: x = v·ct  /  x'축: ct = v·x  → 두 축이 빛의 선을 향해 같은 각도로 접힌다
        n = m / np.sqrt(1 + v * v) * 1.0
        t_axis = Arrow(self.p(0, 0), self.p(v * n, n), buff=0, color=color,
                       stroke_width=3, tip_length=0.2)
        x_axis = Arrow(self.p(0, 0), self.p(n, v * n), buff=0, color=color,
                       stroke_width=3, tip_length=0.2)
        return t_axis, x_axis
