#!/usr/bin/env python3
"""Rebuild bank icon VTF files from PNG sources. Requires: pip install srctools pillow"""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from srctools.vtf import ImageFormats, VTF, VTFFlags

HERE = Path(__file__).resolve().parent
ICON_SIZE = 256
ICONS = ("widthdraw", "deposit", "safety_deposit", "send_money", "bank_icon")

VTF_FLAGS = (
	VTFFlags.EIGHTBITALPHA
	| VTFFlags.NO_MIP
	| VTFFlags.NO_LOD
	| VTFFlags.CLAMP_S
	| VTFFlags.CLAMP_T
)


def rgba_to_bgra(image: Image.Image) -> bytes:
	pixels = bytearray(image.tobytes())

	for index in range(0, len(pixels), 4):
		pixels[index], pixels[index + 2] = pixels[index + 2], pixels[index]

	return bytes(pixels)


def build_icon(name: str) -> None:
	png_path = HERE / f"{name}.png"
	vtf_path = HERE / f"{name}.vtf"

	if not png_path.exists():
		raise FileNotFoundError(png_path)

	image = Image.open(png_path).convert("RGBA")
	image = image.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)

	vtf = VTF(ICON_SIZE, ICON_SIZE, fmt=ImageFormats.BGRA8888)
	vtf.flags = VTF_FLAGS
	frame = vtf.get()
	frame.copy_from(rgba_to_bgra(image), ImageFormats.BGRA8888)

	with vtf_path.open("wb") as handle:
		vtf.save(handle)

	print(f"Wrote {vtf_path.name} ({vtf_path.stat().st_size} bytes, flags={vtf.flags!r})")


def main() -> None:
	for icon in ICONS:
		build_icon(icon)


if __name__ == "__main__":
	main()
