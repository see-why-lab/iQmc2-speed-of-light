# iQmc2-speed-of-light

블로그 **iQ=mc²** 의 글 「빛의 속도는 어떻게 '유한하면서 절대적'이 되었나」에 쓰인 그림과, 그 그림을 만드는 코드.

- 글 원고: [post.md](post.md)
- 완성된 그림: [out/](out)

## 그림 목록

| # | 파일 | 내용 | 도구 |
|---|---|---|---|
| 1 | `fig01_cover.png` | 커버 | Blender |
| 2 | `fig02_sound_vs_light.png` | 번개와 천둥의 시차 | Manim |
| 3 | `fig03_galileo_lanterns.png` | 갈릴레오의 램프 실험 | Blender |
| 4 | `fig04_velocity_addition.png` | 속도 덧셈과 무한히 빠른 빛 | Manim |
| 5 | `fig05_lunar_laser.png` | 달 레이저 거리 측정, 코너 큐브 | Blender |
| 6 | `fig06_michelson_morley.png` | 마이컬슨–몰리 간섭계와 간섭무늬 | Manim |
| 7 | `fig07_three_stages.png` | 광속 개념의 세 단계 | Manim |
| 8 | `fig08_horizon.png` | 지평선 비유 | Blender |
| 9 | `fig09_simultaneity.png` | 동시성의 상대성 (시공간 도표) | Manim |
| 10 | `fig10_rotation_vs_lorentz.png` / `.gif` | 공간 회전과 로런츠 변환 | Manim |
| 11 | `fig11_receding_photon.png` / `.gif` | 빛이라는 지평선 | Manim |

## 다시 만들기

필요한 것: [uv](https://docs.astral.sh/uv/), Blender 4.2 이상(`blender` 명령), LaTeX, ffmpeg, Noto Sans CJK KR 글꼴.

```bash
uv venv .venv
uv pip install --python .venv/bin/python manim
make all        # 전부
make fig09      # 하나만
```

## 구조

```
style/theme.py     색상·글꼴. Manim과 Blender가 함께 쓴다
manim/             2D 그림. figNN_*.py 하나가 그림 하나
manim/overlays.py  Blender 렌더 위에 한글 라벨과 빛 번짐을 얹는다
blender/           3D 장면. figNN_*.py 하나가 그림 하나
out/               최종 PNG·GIF
```

Blender 카메라는 Manim 프레임과 같은 크기의 직교 카메라다. 그래서 Blender의 (x, z) 좌표를 그대로 Manim의 (x, y)로 써서 라벨 위치를 맞춘다.
