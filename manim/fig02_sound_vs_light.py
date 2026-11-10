"""그림 2. 번개와 천둥 — 소리는 느껴지는데 빛은 느껴지지 않는다."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from style.theme import *

DIST_KM = 1.0
C_LIGHT = 299_792.458   # km/s
C_SOUND = 0.343         # km/s


class Fig02(Scene):
    def construct(self):
        self.add(heading("1 km 밖에서 번개가 치면",
                         "빛과 소리가 내게 닿기까지 걸리는 시간"))

        x0, x1, y = -5.2, 5.2, 1.25
        bolt = Polygon([0.15, 0.9, 0], [-0.35, 0.05, 0], [0.0, 0.05, 0],
                       [-0.2, -0.9, 0], [0.4, 0.25, 0], [0.05, 0.25, 0],
                       stroke_width=0, fill_color=GOLD, fill_opacity=1)
        bolt.move_to([x0, y + 0.2, 0])
        me = VGroup(Circle(0.17, stroke_width=0, fill_color=FG, fill_opacity=1),
                    RoundedRectangle(corner_radius=0.12, width=0.36, height=0.6,
                                     stroke_width=0, fill_color=FG,
                                     fill_opacity=1)).arrange(DOWN, buff=0.04)
        me.move_to([x1, y + 0.1, 0])
        ground = Line([x0 - 0.8, y - 0.8, 0], [x1 + 0.8, y - 0.8, 0],
                      color=FAINT, stroke_width=3)
        brace = DoubleArrow([x0, y - 1.15, 0], [x1, y - 1.15, 0], buff=0,
                            color=DIM, stroke_width=2, tip_length=0.18)
        dist = kr("1 km", 22, DIM).next_to(brace, DOWN, buff=0.12)
        self.add(ground, bolt, me, brace, dist)

        t_light = DIST_KM / C_LIGHT
        t_sound = DIST_KM / C_SOUND
        rows = VGroup()
        for name, col, t, txt in [
            ("빛", GOLD, t_light, f"{t_light * 1e6:.1f} 마이크로초  (0.0000033초)"),
            ("소리", CYAN, t_sound, f"약 {t_sound:.1f}초"),
        ]:
            label = kr(name, 28, col, BOLD)
            arrow = Arrow([x0 + 0.9, 0, 0], [x1 - 0.5, 0, 0], buff=0, color=col,
                          stroke_width=5, tip_length=0.25)
            val = kr(txt, 26, FG)
            rows.add(VGroup(label, arrow, val))
        for i, r in enumerate(rows):
            yy = -1.75 - i * 1.0
            r[1].shift(UP * yy)
            r[0].next_to(r[1], LEFT, buff=0.3)
            r[2].next_to(r[1], UP, buff=0.08)
        self.add(rows)

        ratio = t_sound / t_light
        self.add(footnote(f"빛은 소리보다 약 {ratio / 1e4:.0f}만 배 빠르다. "
                          "천둥이 늦게 오는 것은 느껴져도, 번개가 늦게 오는 것은 느낄 수 없다."))
