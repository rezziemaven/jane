import os
import shutil

from textnode import TextNode, TextType


def main():
    copy_contents("./static", "./public")

def copy_contents(src, dst):
    # check that each path exists
    if not os.path.exists(src):
        raise Exception("❌ Source directory not found.")
    if not os.path.exists(dst):
        os.mkdir(dst)

    # delete public contents first
    shutil.rmtree(dst)
    os.mkdir(dst)
    print("🗑️ Contents in destination directory deleted.")
    print(f"⚙️ Copying contents from {src} to {dst} ...")

    def copy_deep(src, dst):
        items = os.listdir(src)
        # print(items)

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


main()
