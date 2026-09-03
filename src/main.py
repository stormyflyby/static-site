import os
import shutil

from textnode import TextNode, TextType


def copy_dir(source: str, destination: str) -> None:
    if not os.path.exists(source):
        raise FileNotFoundError(f"source directory {source} not found")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"copying {source_path} to {dest_path}")
        else:
            copy_dir(source_path, dest_path)


def main():
    source = "static"
    destination = "public"
    copy_dir(source, destination)


main()
