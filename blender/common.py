"""Blender 장면 공통 도구.

카메라는 정면을 보는 직교 카메라이고 화면 폭을 Manim 프레임(14.222 × 8)에 맞췄다.
그래서 Blender의 (x, z) 좌표가 Manim의 (x, y) 좌표와 그대로 일치하고,
manim/overlays.py 에서 같은 숫자로 한글 라벨을 얹을 수 있다.
"""
import sys, math, pathlib
import bpy
from mathutils import Vector

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from style.theme import BG, FG, GOLD, CYAN, hex_to_rgb  # noqa: E402

FRAME_W, FRAME_H = 14.2222, 8.0


def srgb_to_linear(c):
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


def rgba(hex_color):
    return (*srgb_to_linear(hex_to_rgb(hex_color)), 1.0)


def out_path():
    argv = sys.argv
    return argv[argv.index("--") + 1] if "--" in argv else "render.png"


def setup(samples=96):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "Standard"

    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = rgba(BG)
    bg.inputs["Strength"].default_value = 1.0
    scene.world = world

    cam_data = bpy.data.cameras.new("Camera")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = FRAME_W
    cam_data.clip_end = 200
    cam = bpy.data.objects.new("Camera", cam_data)
    cam.location = (0, -40, 0)
    cam.rotation_euler = (math.radians(90), 0, 0)
    scene.collection.objects.link(cam)
    scene.camera = cam
    return scene


def render():
    path = str(pathlib.Path(out_path()).resolve())
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("rendered", path)


# ── 재질 ────────────────────────────────────────────────────────────────
def glossy(name="white", color=FG, roughness=0.28):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = rgba(color)
    b.inputs["Roughness"].default_value = roughness
    return m


def emissive(name="gold", color=GOLD, strength=3.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = rgba(color)
    b.inputs["Emission Color"].default_value = rgba(color)
    b.inputs["Emission Strength"].default_value = strength
    return m


# ── 물체 ────────────────────────────────────────────────────────────────
def _finish(mat, smooth=True):
    ob = bpy.context.active_object
    if smooth:
        bpy.ops.object.shade_smooth()
    if mat:
        ob.data.materials.append(mat)
    return ob


def sphere(loc, r, mat, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=r, location=loc)
    ob = _finish(mat)
    ob.scale = scale
    return ob


def box(loc, size, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    ob = _finish(mat, smooth=False)
    ob.scale = size
    return ob


def beam(p0, p1, radius, mat):
    """두 점을 잇는 가는 원기둥(빛줄기)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=d.length,
                                        location=(p0 + p1) / 2)
    ob = _finish(mat)
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = d.to_track_quat("Z", "Y")
    return ob


def dashed_beam(p0, p1, radius, mat, n=14, duty=0.55):
    p0, p1 = Vector(p0), Vector(p1)
    return [beam(p0.lerp(p1, i / n), p0.lerp(p1, (i + duty) / n), radius, mat) for i in range(n)]


def person(x, z_feet, height, mat, y=0.0):
    """머리(구)와 몸통(둥근 기둥)으로 된 단순한 사람."""
    head_r = height * 0.17
    body_h = height - 2 * head_r - height * 0.04
    sphere((x, y, z_feet + height - head_r), head_r, mat)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=head_r * 0.95, depth=body_h,
                                        location=(x, y, z_feet + body_h / 2))
    _finish(mat)


def area_light(loc, energy, size=6.0, color=(1, 1, 1), target=(0, 0, 0)):
    data = bpy.data.lights.new("Area", "AREA")
    data.energy, data.size, data.color = energy, size, color
    ob = bpy.data.objects.new("Area", data)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = d.to_track_quat("-Z", "Y")
    bpy.context.scene.collection.objects.link(ob)
    return ob


def point_light(loc, energy, color=(1, 1, 1), radius=0.1):
    data = bpy.data.lights.new("Point", "POINT")
    data.energy, data.color, data.shadow_soft_size = energy, color, radius
    ob = bpy.data.objects.new("Point", data)
    ob.location = loc
    bpy.context.scene.collection.objects.link(ob)
    return ob


def studio(key=2600, rim=700):
    """기본 조명: 왼쪽 위 앞의 흰 주광 + 오른쪽 뒤의 청록 보조광."""
    area_light((-7, -12, 9), key, size=9)
    area_light((9, 6, 5), rim, size=6, color=srgb_to_linear(hex_to_rgb(CYAN)))
