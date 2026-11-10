"""그림 3. 갈릴레오의 램프 실험 — 밤의 두 언덕."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import *

setup()
white = glossy(roughness=0.45)
gold = emissive(strength=4)
gold_soft = emissive("gold_soft", strength=2.5)

# 두 언덕: 납작하게 누른 큰 구의 윗부분만 화면에 들어온다
HILL_L = (-4.6, 0, -4.4)
HILL_R = (4.6, 0, -4.4)
sphere(HILL_L, 3.0, white, scale=(1.25, 1.0, 1.0))
sphere(HILL_R, 3.0, white, scale=(1.25, 1.0, 1.0))
TOP = -1.4   # 언덕 꼭대기의 z

# 사람과 램프
for x, lamp_dx in ((-4.6, 0.55), (4.6, -0.55)):
    person(x, TOP - 0.03, 1.15, white)
    lamp = (x + lamp_dx, -0.2, TOP + 0.5)
    sphere(lamp, 0.1, gold)
    point_light((lamp[0], lamp[1] - 0.6, lamp[2]), 55, srgb_to_linear(hex_to_rgb(GOLD)))

# 두 램프 사이를 오가는 빛
dashed_beam((-3.8, -0.2, TOP + 0.5), (3.8, -0.2, TOP + 0.5), 0.022, gold_soft, n=20)

studio(key=1500, rim=700)
render()
