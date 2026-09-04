from copy_dir import copy_dir
from generate_page import generate_pages_recursive


def main():
    copy_dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")


main()
