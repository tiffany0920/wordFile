import os
import re
from glob import glob

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output")
MEDIA_DIR = os.path.join(OUTPUT_DIR, "media")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

IMG_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def normalize_markdown_file(md_path: str) -> tuple[int, int]:
    """
    规范化单个Markdown文件中的图片链接路径。
    统一将图片引用修改为相对路径格式，确保智能文档生成器正确处理图片资源。
    返回 (总图片数量, 已修复图片数量)。
    """
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = list(IMG_PATTERN.finditer(content))
    if not matches:
        return 0, 0

    total = 0
    fixed = 0

    def should_fix(path: str) -> bool:
        # 判断图片路径是否需要规范化
        # 如果已经是media/前缀则跳过
        if path.lower().startswith("media/"):
            return False
        # 包含目录分隔符则跳过，除非以./或.\开头
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
    """
    智能文档生成器媒体文件规范化工具主函数
    扫描输出目录中的所有Markdown文件，统一规范化图片引用路径
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(MEDIA_DIR, exist_ok=True)

    md_files = glob(os.path.join(OUTPUT_DIR, "*.md"))
    total_images = 0
    total_fixed = 0

    for md in md_files:
        t, f = normalize_markdown_file(md)
        total_images += t
        total_fixed += f
        print(f"{os.path.basename(md)}: 图片数量={t}, 已修复={f}")

    print("-" * 40)
    print(f"处理结果: 总图片={total_images}, 已修复={total_fixed}")


if __name__ == "__main__":
    main()
