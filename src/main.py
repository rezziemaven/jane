import os
import shutil
from sys import argv

from markdown_parser import markdown_to_html_node, extract_title
from pathlib import Path


def main():
    basepath = argv[1] if len(argv) == 2 else "/"
    dest_path = "./public"
    template_path = "./template.html"

    copy_contents("./static", dest_path)
    generate_pages("./content", template_path, dest_path, basepath)


def copy_contents(src, dst):
    if not os.path.exists(src):
        raise Exception("❌ Source directory not found.")
    if not os.path.exists(dst):
        os.mkdir(dst)

    shutil.rmtree(dst)
    os.mkdir(dst)
    print("🗑️ Contents in destination directory deleted.")
    print(f"⚙️ Copying contents from {src} to {dst} ...")

    def copy_deep(src, dst):
        items = os.listdir(src)

        for item in items:
            src_path = os.path.join(src, item)
            if os.path.isfile(src_path):
                dst_path = shutil.copy(src_path, dst)
                print(f"Copied file from {src_path} to {dst_path}")
            else:
                dst_path = os.path.join(dst, item)
                os.mkdir(dst_path)
                copy_deep(src_path, dst_path)

    copy_deep(src, dst)
    print("✅ Copy complete.")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"⚙️ Generating page {dest_path} from {from_path} using {template_path}...")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    markdown_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html_page = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", markdown_html)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    file = Path(dest_path)
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "x") as f:
        f.write(html_page)

    print(f"✅ {dest_path} generated.")


def generate_pages(src, template_path, dst, basepath):
    if not os.path.exists(src):
        raise Exception("❌ Source directory not found.")
    if not os.path.exists(dst):
        raise Exception("❌ Destination directory not found.")

    items = os.listdir(src)

    for item in items:
        src_path = os.path.join(src, item)
        if os.path.isfile(src_path):
            html_item = item.removesuffix(".md") + ".html"
            dest_path = os.path.join(dst, html_item)
            generate_page(src_path, template_path, dest_path, basepath)
        else:
            dest_path = os.path.join(dst, item)
            os.mkdir(dest_path)
            generate_pages(src_path, template_path, dest_path, basepath)


main()
