"""그림 11. 빛이라는 지평선 — 빨리 달릴수록 광자는 그만큼 미래로 물러난다."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from spacetime import *

SPEEDS = [0.1, 0.5, 0.9]


class Fig11(Scene):
    def construct(self):
        self.add(heading("빛이라는 지평선",
                         "A의 시계로 1초가 지났을 때, 각 관측자의 '지금' 빛은 어디에 있는가"))

        d = Diagram(origin=[-6.3, -3.05, 0], unit=2.4, xmax=2.45, tmax=2.15)
        self.add(d.grid(2), d.axes())
        self.add(d.light(2.08))
        self.add(kr("빛", 24, GOLD, BOLD).move_to(d.p(2.0, 2.16)))
        self.add(DashedLine(d.p(0, 1), d.p(2.3, 1), color=DIM, stroke_width=2, dash_length=0.1))
        self.add(Dot(d.p(1, 1), radius=0.09, color=FG))
        self.add(kr("A의 지금", 18, DIM).next_to(d.p(2.05, 1), DOWN, buff=0.1))
        for i in (1, 2):
            self.add(MathTex(str(i), color=DIM, font_size=30).next_to(d.p(i, 0), DOWN, buff=0.12))

        v = ValueTracker(SPEEDS[0])

        def moving():
            vv = v.get_value()
            g = VGroup()
            # B의 세계선: 원점 → (v, 1)
            g.add(Line(d.p(0, 0), d.p(vv, 1), color=CYAN, stroke_width=3))
            g.add(Dot(d.p(vv, 1), radius=0.08, color=CYAN))
            # B의 동시선: (v,1)에서 기울기 v 로 빛의 선 (1+v, 1+v)까지
            g.add(DashedLine(d.p(vv, 1), d.p(1 + vv, 1 + vv), color=CYAN,
                             stroke_width=2.5, dash_length=0.1))
            g.add(Dot(d.p(1 + vv, 1 + vv), radius=0.1, color=GOLD))
            return g

        self.add(always_redraw(moving))

        # 정지 이미지용: 세 속도의 결과를 옅게 겹쳐 둔다
        ghosts = VGroup()
        for s in SPEEDS:
            ghosts.add(Line(d.p(0, 0), d.p(s, 1), color=CYAN, stroke_width=2, stroke_opacity=0.45))
            ghosts.add(DashedLine(d.p(s, 1), d.p(1 + s, 1 + s), color=CYAN, stroke_width=2,
                                  dash_length=0.1, stroke_opacity=0.45))
            ghosts.add(Dot(d.p(s, 1), radius=0.07, color=CYAN))
            ghosts.add(Dot(d.p(1 + s, 1 + s), radius=0.09, color=GOLD))
            ghosts.add(MathTex(f"{s}c", color=CYAN, font_size=28).next_to(d.p(1 + s, 1 + s), RIGHT, buff=0.18))

        # 오른쪽 표
        tx = 1.6
        header = VGroup(kr("B의 속도", 21, DIM), kr("B가 다가간 거리", 21, DIM),
                        kr("빛이 물러난 거리", 21, DIM))
        rows = [header]
        for s in SPEEDS:
            km = f"{s * 30:.0f}만 km"
            rows.append(VGroup(kr(f"광속의 {s * 100:.0f}%", 23, CYAN, BOLD),
                               kr(km, 23, FG), kr(km, 23, GOLD, BOLD)))
        cols_x = [tx, tx + 2.0, tx + 4.1]
        for j, r in enumerate(rows):
            for i, cell in enumerate(r):
                cell.move_to([cols_x[i], 0.9 - j * 0.75, 0])
        table = VGroup(*rows)
        rule = Line([tx - 0.9, 0.52, 0], [tx + 5.2, 0.52, 0], color=FAINT, stroke_width=2)
        self.add(table, rule)
        note = VGroup(
            kr("한 걸음 다가가면 한 걸음 물러나는 지평선처럼,", 21, FG),
            kr("빛은 쫓아간 만큼 정확히 미래 쪽으로 멀어진다.", 21, FG),
            kr("광속이 일정한 것은 그 결과다.", 21, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        note.move_to([tx - 0.9, -2.35, 0], aligned_edge=LEFT)
        self.add(note)

        for s in SPEEDS[1:]:
            self.play(v.animate.set_value(s), run_time=1.6, rate_func=smooth)
            self.wait(0.6)
        self.play(v.animate.set_value(SPEEDS[0]), run_time=1.6, rate_func=smooth)
        self.wait(0.4)
        self.add(ghosts)
        self.wait(0.01)
