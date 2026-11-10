"""그림 6. 마이컬슨–몰리 간섭계와 간섭무늬(예상 vs 실제)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from manim import *
from style.theme import *


def fringe_image(phase, size=420):
    """동심원 간섭무늬. I = cos²((k r² + phase) / 2). phase=0 이면 가운데가 밝다."""
    ax = np.linspace(-1, 1, size)
    x, y = np.meshgrid(ax, ax)
    r2 = x ** 2 + y ** 2
    inten = np.cos((9 * np.pi * r2 + phase) / 2) ** 2
    inten *= np.exp(-1.2 * r2)            # 가장자리로 갈수록 어두워짐
    inten[r2 > 1] = 0
    gold = np.array(hex_to_rgb(GOLD))
    bg = np.array(hex_to_rgb(BG))
    rgb = bg + (gold - bg) * inten[..., None]
    rgb[r2 > 1] = bg
    return (rgb * 255).astype(np.uint8)


class Fig06(Scene):
    def construct(self):
        self.add(heading("마이컬슨–몰리 실험",
                         "서로 수직인 두 길을 다녀온 빛을 다시 겹쳐 본다"))

        # ── 왼쪽: 간섭계 도식 ────────────────────────────────────────────
        o = np.array([-3.9, -0.6, 0])
        L = 2.3
        src = RoundedRectangle(corner_radius=0.08, width=0.8, height=0.5,
                               stroke_color=FG, stroke_width=2,
                               fill_color="#080C16", fill_opacity=1).move_to(o + LEFT * 2.4)
        bs = Line(o + np.array([-0.35, -0.35, 0]), o + np.array([0.35, 0.35, 0]),
                  color=CYAN, stroke_width=5)
        m1 = Line(o + RIGHT * L + UP * 0.45, o + RIGHT * L + DOWN * 0.45, color=FG, stroke_width=7)
        m2 = Line(o + UP * L + LEFT * 0.45, o + UP * L + RIGHT * 0.45, color=FG, stroke_width=7)
        det = RoundedRectangle(corner_radius=0.08, width=0.9, height=0.4,
                               stroke_color=FG, stroke_width=2,
                               fill_color="#080C16", fill_opacity=1).move_to(o + DOWN * 1.6)
        beams = VGroup(
            Line(src.get_right(), o, color=GOLD, stroke_width=4),
            Line(o, o + RIGHT * L, color=GOLD, stroke_width=4),
            Line(o, o + UP * L, color=GOLD, stroke_width=4),
            Line(o, det.get_top(), color=GOLD, stroke_width=4),
        )
        self.add(beams, src, bs, m1, m2, det)
        self.add(kr("광원", 20).next_to(src, DOWN, buff=0.15))
        self.add(kr("반투명 거울", 20, CYAN).next_to(bs, DR, buff=0.1).shift(RIGHT * 0.1))
        self.add(kr("거울 1", 20).next_to(m1, RIGHT, buff=0.15))
        self.add(kr("거울 2", 20).next_to(m2, UP, buff=0.15))
        self.add(kr("검출기", 20).next_to(det, DOWN, buff=0.15))
        self.add(MathTex("L", color=DIM, font_size=34).move_to(o + RIGHT * L * 0.6 + UP * 0.3))
        self.add(MathTex("L", color=DIM, font_size=34).move_to(o + UP * L / 2 + LEFT * 0.3))
        earth = Arrow(o + np.array([-2.9, 1.5, 0]), o + np.array([-1.3, 1.5, 0]), buff=0,
                      color=DIM, stroke_width=3, tip_length=0.2)
        self.add(earth, kr("지구의 운동 방향", 18, DIM).next_to(earth, UP, buff=0.1),
                 kr("초속 약 30 km", 18, DIM).next_to(earth, DOWN, buff=0.1))

        # ── 오른쪽: 간섭무늬 두 장 ───────────────────────────────────────
        for cx, phase, title, sub in [
            (1.9, np.pi, "예상", "지구의 속도가 빛에 더해진다면\n두 길의 시간이 어긋난다"),
            (5.1, 0.0, "실제 관측", "어느 방향으로 재도\n무늬는 그대로다"),
        ]:
            img = ImageMobject(fringe_image(phase)).set_resampling_algorithm(
                RESAMPLING_ALGORITHMS["cubic"])
            img.height = 2.7
            img.move_to([cx, -0.35, 0])
            ring = Circle(1.35, color=FAINT, stroke_width=2).move_to(img)
            t = kr(title, 26, FG, BOLD).next_to(img, UP, buff=0.25)
            s = Paragraph(*sub.split("\n"), font=KR_FONT, font_size=19, color=DIM,
                          alignment="center", line_spacing=0.9).next_to(img, DOWN, buff=0.25)
            self.add(img, ring, t, s)

        self.add(footnote("무늬는 설명용으로 계산한 것이다. 실제 실험은 장치를 돌리며 무늬가 이동하는지를 보았고, 이동은 없었다."))
