import os
import re
from glob import glob

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output")
MEDIA_DIR = os.path.join(OUTPUT_DIR, "media")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

IMG_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def normalize_markdown_file(md_path: str) -> tuple[int, int]:
    """
    Normalize image links in a single markdown file.
    Returns (total_images, fixed_images).
    """
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = list(IMG_PATTERN.finditer(content))
    if not matches:
        return 0, 0

    total = 0
    fixed = 0

    def should_fix(path: str) -> bool:
        # Already media/ prefixed
        if path.lower().startswith("media/"):
            return False
        # Has directory separator – skip unless it starts with ./ or .\\
        if "/" in path or "\\" in path:
            return False
        _, ext = os.path.splitext(path)
        return ext.lower() in IMAGE_EXTS

    new_content = content

    for m in reversed(matches):  # reverse to avoid index shift
        img_path = m.group(1)
        if not should_fix(img_path):
            total += 1
            continue
        media_candidate = os.path.join(MEDIA_DIR, img_path)
        if os.path.isfile(media_candidate):
            # replace with media/filename
            start, end = m.span(1)
            new_content = new_content[:start] + f"media/{img_path}" + new_content[end:]
            fixed += 1
        total += 1

    if fixed:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(new_content)

    return total, fixed


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(MEDIA_DIR, exist_ok=True)

    md_files = glob(os.path.join(OUTPUT_DIR, "*.md"))
    total_images = 0
    total_fixed = 0

    for md in md_files:
        t, f = normalize_markdown_file(md)
        total_images += t
        total_fixed += f
        print(f"{os.path.basename(md)}: images={t}, fixed={f}")

    print("-" * 40)
    print(f"Summary: images={total_images}, fixed={total_fixed}")


if __name__ == "__main__":
    main()
