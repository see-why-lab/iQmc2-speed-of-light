"""그림 1. 커버 — 지구에서 달로 뻗는 빛줄기."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import *

setup()
white = glossy()
gold = emissive()

EARTH = (-5.6, 0, -3.4)
MOON = (5.3, 3, 2.2)
sphere(EARTH, 3.0, white)
sphere(MOON, 0.75, white)

# 지구 표면에서 달까지의 빛줄기
e, m = Vector(EARTH), Vector(MOON)
d = (m - e).normalized()
beam(e + d * 3.0, m - d * 0.75, 0.035, gold)
sphere(tuple(e + d * 3.0), 0.09, gold)

studio()
point_light(tuple(e + d * 3.3 + Vector((0, -1.2, 0))), 60, srgb_to_linear(hex_to_rgb(GOLD)))
render()
