"""그림 5. 달 레이저 거리 측정과 코너 큐브 반사체."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import *
from mathutils import Matrix

setup()
white = glossy()
mirror = glossy("mirror", roughness=0.12)
gold = emissive()

# ── 위: 지구와 달, 왕복하는 레이저 ──────────────────────────────────────
Z = 0.95
EARTH_X, EARTH_R = -5.4, 1.3
MOON_X, MOON_R = 5.6, 0.42
sphere((EARTH_X, 0, Z), EARTH_R, white)
sphere((MOON_X, 0, Z), MOON_R, white)
x0, x1 = EARTH_X + EARTH_R + 0.05, MOON_X - MOON_R - 0.05
beam((x0, -0.1, Z + 0.12), (x1, -0.1, Z + 0.12), 0.022, gold)   # 가는 길
beam((x0, -0.1, Z - 0.12), (x1, -0.1, Z - 0.12), 0.022, gold)   # 오는 길

# ── 아래: 코너 큐브(서로 수직인 거울 세 장)와 그 안에서 세 번 반사되는 빛 ──
S = 1.5                       # 거울 한 변
T = 0.05                      # 거울 두께
# 방 모서리를 비스듬히 들여다보는 시점: 큐브 좌표의 F 방향에 카메라가 있다
F = Vector((1.0, 0.3, 0.32)).normalized()
YW = -F
ZW = (Vector((0, 0, 1)) - YW * YW.z).normalized()
XW = YW.cross(ZW)
ROT = Matrix((XW, YW, ZW)).to_4x4()
ORIGIN = Vector((-2.2, 0, -3.3))


def place(local):
    return ORIGIN + (ROT @ Vector(local))


for center, size in (((S / 2, S / 2, -T / 2), (S, S, T)),      # z = 0 면
                     ((S / 2, -T / 2, S / 2), (S, T, S)),      # y = 0 면
                     ((-T / 2, S / 2, S / 2), (T, S, S))):     # x = 0 면
    ob = box(tuple(place(center)), size, mirror)
    ob.rotation_euler = ROT.to_euler()

# 빛의 경로: 세 면에서 한 번씩 반사되면 방향이 정확히 뒤집힌다
d = Vector((-0.35, -0.7, -0.62)).normalized()
h1 = Vector((0.45, 0.5, 0.0)) * S
pts = [h1 - d * 1.6 * S]
p, v = h1.copy(), d.copy()
pts.append(p.copy())
for _ in range(2):
    v = v.copy()
    # 방금 반사된 면의 성분을 뒤집고, 다음에 닿는 면을 찾는다
    for axis in range(3):
        if abs(p[axis]) < 1e-6 and v[axis] < 0:
            v[axis] = -v[axis]
    ts = [(-p[a] / v[a], a) for a in range(3) if v[a] < -1e-9]
    t, a = min(ts)
    p = p + v * t
    p[a] = 0.0
    pts.append(p.copy())
v = v.copy()
for axis in range(3):
    if abs(p[axis]) < 1e-6 and v[axis] < 0:
        v[axis] = -v[axis]
pts.append(p + v * 1.6 * S)
for a, b in zip(pts[:-1], pts[1:]):
    beam(tuple(place(a)), tuple(place(b)), 0.02, gold)

studio()
area_light((-2, -10, 2), 120, size=5, target=tuple(ORIGIN))
render()
