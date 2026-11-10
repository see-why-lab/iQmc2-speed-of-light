"""Blender 렌더(build/raw/*.png) 위에 한글 라벨을 얹는 씬들.

Blender 카메라가 Manim 프레임과 같은 직교 좌표를 쓰므로,
Blender의 (x, z)를 그대로 Manim의 (x, y)로 쓰면 된다.
"""
import sys, pathlib, math
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
from PIL import Image, ImageFilter
from manim import *
from style.theme import *


def render_with_glow(name):
    """Blender 렌더를 불러와, 빛나는 부분(채도 높고 밝은 픽셀)에 번짐을 더한다."""
    img = Image.open(ROOT / "build" / "raw" / f"{name}.png").convert("RGB")
    a = np.asarray(img).astype(np.float32) / 255
    mx, mn = a.max(axis=2), a.min(axis=2)
    mask = ((mx > 0.8) & (mx - mn > 0.25)).astype(np.float32)[..., None]
    bright = Image.fromarray((a * mask * 255).astype(np.uint8))
    out = a.copy()
    for radius, gain in ((6, 0.55), (22, 0.45), (60, 0.35)):
        out += np.asarray(bright.filter(ImageFilter.GaussianBlur(radius))).astype(np.float32) / 255 * gain
    m = ImageMobject((np.clip(out, 0, 1) * 255).astype(np.uint8))
    m.height = config.frame_height
    return m


def label_line(p0, p1, color=DIM):
    return Line(p0, p1, color=color, stroke_width=2)


class Fig01(Scene):
    """커버."""
    def construct(self):
        self.add(render_with_glow("fig01_cover"))
        title = kr("빛의 속도", 84, FG, BOLD)
        sub = kr("무한에서 유한으로, 상대에서 절대로", 32, DIM)
        g = VGroup(title, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        g.to_corner(UL, buff=0.8)
        self.add(g)
        logo = MathTex("i", "Q=mc^2", font_size=44, color=FG).set_color_by_tex("i", GOLD)
        self.add(logo.to_corner(DR, buff=0.6))


class Fig03(Scene):
    """갈릴레오의 램프 실험."""
    def construct(self):
        self.add(render_with_glow("fig03_galileo_lanterns"))
        self.add(heading("갈릴레오의 램프 실험",
                         "램프 불빛이 건너편 언덕에 다녀오는 시간을 재려 했다 (1638년 기록)"))
        self.add(kr("갈릴레오", 24, FG, BOLD).move_to([-4.6, 0.15, 0]))
        self.add(kr("조수", 24, FG, BOLD).move_to([4.6, 0.15, 0]))
        self.add(kr("언덕 사이 3 km라면", 22, DIM).move_to([0, -1.35, 0]))

        rows = VGroup(
            VGroup(kr("빛이 다녀오는 시간", 24, GOLD, BOLD), kr("약 0.00002초", 24, FG)).arrange(RIGHT, buff=0.4),
            VGroup(kr("사람이 반응하는 시간", 24, CYAN, BOLD), kr("약 0.2초", 24, FG)).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, 0.75, 0])
        self.add(rows)
        self.add(kr("재려는 시간이 반응 시간의 1만 분의 1이다", 20, DIM).move_to([0, -1.8, 0]))


class Fig05(Scene):
    """달 레이저 거리 측정."""
    def construct(self):
        self.add(render_with_glow("fig05_lunar_laser"))
        self.add(heading("달까지 레이저를 쏘면",
                         "달에 놓인 반사체 덕분에 빛은 정확히 왔던 길로 돌아온다"))
        z = 0.95
        self.add(kr("지구", 24, FG, BOLD).move_to([-5.4, z - 1.65, 0]))
        self.add(kr("달", 24, FG, BOLD).move_to([5.6, z - 0.8, 0]))
        self.add(kr("평균 38만 km  ·  왕복 약 2.56초", 26, GOLD, BOLD).move_to([0.4, z + 0.5, 0]))

        txt = VGroup(
            kr("코너 큐브 반사체", 26, FG, BOLD),
            kr("서로 수직인 거울 세 장.", 22, FG),
            kr("세 면에 한 번씩 반사된 빛은", 22, FG),
            kr("들어온 방향 그대로 되돌아간다.", 22, FG),
            kr("왕복 시간을 재면 거리를 밀리미터 단위로 알 수 있다.", 20, DIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        txt.move_to([0.6, -2.0, 0], aligned_edge=LEFT)
        self.add(txt)
        self.add(kr("크기와 거리는 실제 비율이 아니다.", 18, DIM).to_corner(DR, buff=0.35))


class Fig08(Scene):
    """지평선."""
    def construct(self):
        self.add(render_with_glow("fig08_horizon"))
        self.add(heading("지평선은 다가간 만큼 물러난다",
                         "눈높이 1.7 m인 사람에게 지평선은 언제나 약 4.7 km 앞에 있다"))
        # blender/fig08_horizon.py 와 같은 기하
        R, H = 9.0, 1.0
        C = np.array([-0.6, -R - 1.2, 0])
        phi = math.acos(R / (R + H))
        a0 = math.radians(-22.0)

        def pt(angle, r):
            return C + r * np.array([math.sin(angle), math.cos(angle), 0])

        for a, name, col in ((a0, "처음 서 있던 곳", CYAN), (a0 + phi, "지평선까지 걸어간 뒤", GOLD)):
            eye, touch = pt(a, R + H), pt(a + phi, R)
            self.add(kr(name, 22, col, BOLD).next_to(eye, UP, buff=0.3))
            mid = (eye + touch) / 2
            normal = np.array([math.sin(a + phi / 2), math.cos(a + phi / 2), 0])
            self.add(kr("4.7 km", 22, col).move_to(mid + normal * 0.38))
        self.add(kr("그림에서는 지구의 곡률과 사람의 키를 크게 과장했다.", 18, DIM).move_to([0, 1.75, 0]))
