import os

from extract_title import extract_title
from markdown_to_html import markdown_to_html_node


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        target_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(entry_path) and entry[-3:] == ".md":
            target_file = target_path[:-3] + ".html"
            generate_page(entry_path, template_path, target_file)
        elif os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, target_path)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_file:
        markdown_content = from_file.read()
    with open(template_path) as template_file:
        template_content = template_file.read()
    html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)
    dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(dest_path, mode="w") as dest_file:
        dest_file.write(template_content)
