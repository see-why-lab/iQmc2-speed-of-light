"""그림 10. 공간에서의 회전과 시공간에서의 '회전'(로런츠 변환)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from spacetime import *

THETA_END = 30 * DEGREES
V_END = 0.5
R = 1.7   # 축 길이


class Fig10(Scene):
    def construct(self):
        self.add(heading("몸을 돌리는 것과 달리는 것은 닮았다",
                         "둘 다 '좌표를 읽는 방법'만 바뀐다"))

        lo = np.array([-4.0, -0.35, 0])
        ro = np.array([3.2, -0.35, 0])
        k = ValueTracker(0.0)   # 0 → 1 로 진행

        def base_axes(o, lx, ly):
            ax = Arrow(o + LEFT * R, o + RIGHT * R, buff=0, color=FG, stroke_width=3, tip_length=0.2)
            ay = Arrow(o + DOWN * R, o + UP * R, buff=0, color=FG, stroke_width=3, tip_length=0.2)
            return VGroup(ax, ay,
                          MathTex(lx, color=FG, font_size=34).next_to(ax, RIGHT, buff=0.1),
                          MathTex(ly, color=FG, font_size=34).next_to(ay, UP, buff=0.1))

        # ── 왼쪽: 공간 회전 ──────────────────────────────────────────────
        self.add(kr("공간에서 몸을 돌리면", 24, FG, BOLD).move_to(lo + UP * 2.3))
        self.add(Circle(1.2, color=FAINT, stroke_width=2.5).move_to(lo))
        self.add(base_axes(lo, "x", "y"))

        def rot_axes():
            th = k.get_value() * THETA_END
            ex = np.array([np.cos(th), np.sin(th), 0])
            ey = np.array([-np.sin(th), np.cos(th), 0])
            a1 = Arrow(lo - ex * R * 0.9, lo + ex * R * 0.9, buff=0, color=CYAN, stroke_width=3, tip_length=0.2)
            a2 = Arrow(lo - ey * R * 0.9, lo + ey * R * 0.9, buff=0, color=CYAN, stroke_width=3, tip_length=0.2)
            return VGroup(a1, a2,
                          MathTex("x'", color=CYAN, font_size=34).move_to(lo + ex * (R * 0.9 + 0.3)),
                          MathTex("y'", color=CYAN, font_size=34).move_to(lo + ey * (R * 0.9 + 0.3)))

        self.add(always_redraw(rot_axes))
        p_ang = 62 * DEGREES
        self.add(Dot(lo + 1.2 * np.array([np.cos(p_ang), np.sin(p_ang), 0]), radius=0.09, color=GOLD))
        self.add(kr("x² + y² 은 그대로", 20, DIM).move_to(lo + DOWN * 2.15))
        self.add(MathTex(r"x' = x\cos\theta + y\sin\theta", r"\\",
                         r"y' = -x\sin\theta + y\cos\theta",
                         color=FG, font_size=30).move_to(lo + DOWN * 2.95))

        # ── 오른쪽: 로런츠 변환 ─────────────────────────────────────────
        self.add(kr("시공간에서 달리면", 24, FG, BOLD).move_to(ro + UP * 2.3))
        hyp = VGroup()
        s = 0.85
        for sign in (1, -1):   # (ct)² - x² = s² 의 위·아래 가지
            hyp.add(ParametricFunction(
                lambda a, sg=sign: ro + np.array([s * np.sinh(a), sg * s * np.cosh(a), 0]),
                t_range=[-1.2, 1.2], color=FAINT, stroke_width=2.5))
        self.add(hyp)
        self.add(DashedLine(ro + np.array([-R, -R, 0]) * 0.95, ro + np.array([R, R, 0]) * 0.95,
                            color=GOLD, stroke_width=2.5, dash_length=0.1))
        self.add(kr("빛", 20, GOLD, BOLD).move_to(ro + np.array([R, R, 0]) * 0.95 + RIGHT * 0.3))
        self.add(base_axes(ro, "x", "ct"))

        def lor_axes():
            v = k.get_value() * V_END
            n = R * 0.9 / np.sqrt(1 + v * v)
            et = np.array([v, 1, 0]) * n
            ex = np.array([1, v, 0]) * n
            a1 = Arrow(ro - ex, ro + ex, buff=0, color=CYAN, stroke_width=3, tip_length=0.2)
            a2 = Arrow(ro - et, ro + et, buff=0, color=CYAN, stroke_width=3, tip_length=0.2)
            return VGroup(a1, a2,
                          MathTex("x'", color=CYAN, font_size=34).move_to(ro + ex * 1.17),
                          MathTex("ct'", color=CYAN, font_size=34).move_to(ro + et * 1.17))

        self.add(always_redraw(lor_axes))
        a0 = 0.45
        self.add(Dot(ro + np.array([s * np.sinh(a0), s * np.cosh(a0), 0]), radius=0.09, color=GOLD))
        self.add(kr("(ct)² − x² 은 그대로", 20, DIM).move_to(ro + DOWN * 2.15))
        self.add(MathTex(r"x' = \gamma\,(x - vt)", r"\\",
                         r"t' = \gamma\,(t - vx/c^{2})",
                         color=FG, font_size=30).move_to(ro + DOWN * 2.95))

        # 가운데: y → i·ct
        mid = (lo + ro) / 2 + UP * 0.2
        self.add(Arrow(mid + LEFT * 0.75, mid + RIGHT * 0.75, buff=0, color=DIM, stroke_width=3, tip_length=0.2))
        self.add(MathTex(r"y \;\to\;", r"i", r"\,ct", font_size=38, color=FG)
                 .set_color_by_tex("i", GOLD).move_to(mid + UP * 0.45))
        self.add(kr("허수 i 하나 차이", 18, DIM).move_to(mid + DOWN * 0.4))

        # 정지 이미지는 마지막 프레임, GIF에서는 축이 접히는 과정을 보여준다
        self.play(k.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(1.0)
        self.play(k.animate.set_value(0.0), run_time=1.5, rate_func=smooth)
        self.play(k.animate.set_value(1.0), run_time=0.01)
