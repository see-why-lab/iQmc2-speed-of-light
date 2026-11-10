"""iQ=mc² 공통 스타일. Manim 씬과 Blender 스크립트가 같은 값을 쓴다.

Blender의 내장 파이썬에는 manim이 없으므로, 색상 상수는 manim 없이도
import 할 수 있게 맨 위에 두고 manim 의존 코드는 try 블록 안에 둔다.
"""

# ── 색상 ────────────────────────────────────────────────────────────────
BG = "#04060D"      # 거의 검정에 가까운 남색 배경
FG = "#ECEFF4"      # 본문 흰색
DIM = "#7A8398"     # 보조선·부가 설명
FAINT = "#2A3040"   # 격자·패널 테두리
GOLD = "#F2B24D"    # 빛·광자
CYAN = "#8FE6E1"    # 움직이는 관측자·좌표축

KR_FONT = "Noto Sans CJK KR"


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


try:
    from manim import (BOLD, NORMAL, UP, DOWN, LEFT, RIGHT, Text, VGroup,
                       Polygon, RoundedRectangle, Scene, config)

    config.background_color = BG

    def kr(text, size=26, color=FG, weight=NORMAL):
        """한글 텍스트."""
        return Text(text, font=KR_FONT, font_size=size, color=color, weight=weight)

    def heading(text, sub=None):
        """그림 위쪽 제목(+부제)."""
        t = kr(text, 36, weight=BOLD)
        g = VGroup(t)
        if sub:
            g.add(kr(sub, 22, DIM))
            g.arrange(DOWN, buff=0.18)
        return g.to_edge(UP, buff=0.45)

    def footnote(text):
        return kr(text, 20, DIM).to_edge(DOWN, buff=0.4)

    def panel(width, height):
        return RoundedRectangle(corner_radius=0.2, width=width, height=height,
                                stroke_color=FAINT, stroke_width=2,
                                fill_color="#080C16", fill_opacity=1)

    def rocket(color=FG, scale=1.0):
        """오른쪽을 향한 단순한 로켓 아이콘."""
        body = Polygon([-0.5, -0.16, 0], [0.25, -0.16, 0], [0.6, 0, 0],
                       [0.25, 0.16, 0], [-0.5, 0.16, 0],
                       stroke_width=0, fill_color=color, fill_opacity=1)
        fin1 = Polygon([-0.5, 0.16, 0], [-0.72, 0.36, 0], [-0.28, 0.16, 0],
                       stroke_width=0, fill_color=color, fill_opacity=1)
        fin2 = Polygon([-0.5, -0.16, 0], [-0.72, -0.36, 0], [-0.28, -0.16, 0],
                       stroke_width=0, fill_color=color, fill_opacity=1)
        return VGroup(body, fin1, fin2).scale(scale)

except ImportError:  # Blender 안에서 import 될 때
    pass
