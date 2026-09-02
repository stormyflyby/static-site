import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    images: list[tuple[str, str]] = []
    image_strings: list[str] = re.findall(r"!\[[^\[\]]*\]\([^\(\)]*\)", text)

    for image_string in image_strings:
        [dirty_alt, dirty_src] = image_string.split("](")
        alt = dirty_alt[2:]
        src = dirty_src[:-1]
        images.append((alt, src))

    return images


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    link_strings: list[str] = re.findall(r"(?<!!)\[[^\[\]]*\]\([^\(\)]*\)", text)

    for link_string in link_strings:
        [dirty_alt, dirty_src] = link_string.split("](")
        alt = dirty_alt[1:]
        src = dirty_src[:-1]
        links.append((alt, src))

    return links
