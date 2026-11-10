# 그림 재생성: `make all`, 또는 `make fig06` 처럼 하나만.
# 준비: uv venv .venv && uv pip install --python .venv/bin/python manim
#       Blender 4.2 이상 (blender 명령이 PATH에 있어야 함)

MANIM   := .venv/bin/manim
BLENDER := blender
RES     := 1920,1080

MANIM_FIGS   := fig02 fig04 fig06 fig07 fig09 fig10 fig11
BLENDER_FIGS := fig01 fig03 fig05 fig08
GIF_FIGS     := fig10 fig11

.PHONY: all manim blender gifs clean $(MANIM_FIGS) $(BLENDER_FIGS)

all: blender manim gifs
manim: $(MANIM_FIGS)
blender: $(BLENDER_FIGS)

# Manim: 마지막 프레임을 PNG로 저장한다. 씬 클래스 이름은 Fig02 형식.
$(MANIM_FIGS):
	@f=$$(ls manim/$@_*.py); cls=$$(echo $@ | sed 's/fig/Fig/'); \
	$(MANIM) render -s -r $(RES) --media_dir build -v WARNING --disable_caching $$f $$cls && \
	cp $$(find build/images -name "$$cls*.png" | head -1) out/$$(basename $$f .py).png && \
	echo "out/$$(basename $$f .py).png"

# Blender: 3D 장면을 build/raw 에 렌더링한 뒤, Manim으로 한글 라벨을 얹는다.
$(BLENDER_FIGS):
	@f=$$(ls blender/$@_*.py); cls=$$(echo $@ | sed 's/fig/Fig/'); name=$$(basename $$f .py); \
	mkdir -p build/raw && \
	$(BLENDER) --background --factory-startup --python $$f -- build/raw/$$name.png > build/raw/$$name.log 2>&1 && \
	$(MANIM) render -s -r $(RES) --media_dir build -v WARNING --disable_caching manim/overlays.py $$cls && \
	cp $$(find build/images/overlays -name "$$cls*.png" | head -1) out/$$name.png && \
	echo "out/$$name.png"

# 움직임이 핵심인 그림은 GIF도 만든다.
gifs:
	@for fig in $(GIF_FIGS); do \
	f=$$(ls manim/$${fig}_*.py); cls=$$(echo $$fig | sed 's/fig/Fig/'); name=$$(basename $$f .py); \
	$(MANIM) render -r 1280,720 --fps 30 --media_dir build -v ERROR --disable_caching $$f $$cls >/dev/null 2>&1 && \
	ffmpeg -y -loglevel error -i $$(find build/videos/$$name -name "$$cls.mp4" | head -1) \
	  -vf "fps=15,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48[p];[b][p]paletteuse=dither=none" \
	  out/$$name.gif && echo "out/$$name.gif"; done

clean:
	rm -rf build
