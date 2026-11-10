"""그림 8. 지평선 — 다가가도 언제나 같은 거리에 있다."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import *

setup()
white = glossy(roughness=0.4)
ghost = glossy("ghost", color="#8A93A6", roughness=0.6)
gold = emissive()
cyan = emissive("cyan", color=CYAN, strength=2.0)

# 지구: 아주 큰 구의 윗부분. (그림에서는 곡률과 사람 키를 크게 과장했다)
R = 9.0
C = Vector((-0.6, 0, -R - 1.2))
sphere(tuple(C), R, white)
H = 1.0   # 눈높이


def observer(angle_deg, mat, beam_mat):
    """구 위의 각도 위치에 사람을 세우고, 눈에서 지평선까지의 시선을 그린다."""
    a = math.radians(angle_deg)
    up = Vector((math.sin(a), 0, math.cos(a)))
    feet = C + up * R
    eye = C + up * (R + H)
    # 사람(기울어진 채로 서 있다)
    sphere(tuple(C + up * (R + H * 0.86)), H * 0.16, mat)
    beam(tuple(feet), tuple(C + up * (R + H * 0.68)), H * 0.15, mat)
    # 지평선: 눈에서 구에 그은 접선의 접점. 중심각 = acos(R / (R + H))
    phi = math.acos(R / (R + H))
    t = Vector((math.sin(a + phi), 0, math.cos(a + phi)))
    touch = C + t * R
    beam(tuple(eye + Vector((0, -0.3, 0))), tuple(touch + Vector((0, -0.3, 0))), 0.02, beam_mat)
    sphere(tuple(touch + Vector((0, -0.3, 0))), 0.08, beam_mat)
    return eye, touch


A0 = -22.0
PHI = math.degrees(math.acos(R / (R + H)))
observer(A0, ghost, cyan)          # 처음 서 있던 곳
observer(A0 + PHI, white, gold)    # 처음의 지평선까지 걸어간 뒤: 지평선은 다시 그만큼 앞에 있다

studio()
render()
