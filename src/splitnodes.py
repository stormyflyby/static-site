from extract_element import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    if len(old_nodes) == 0:
        return []
    if not delimiter:
        raise ValueError("delimiter must be a non-empty string")
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        text_for_new_nodes = old_node.text.split(delimiter)
        if len(text_for_new_nodes) > 1 and len(text_for_new_nodes) % 2 == 0:
            raise SyntaxError(f'closing delimiter "{delimiter}" expected')
        for i in range(len(text_for_new_nodes)):
            if len(text_for_new_nodes[i]) == 0:
                continue
            if i % 2 == 0:
                new_type = old_node.text_type
                url = old_node.url
            else:
                new_type = text_type
                url = None
            new_nodes.append(TextNode(text_for_new_nodes[i], new_type, url))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    if len(old_nodes) == 0:
        return []
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        remaining_text = old_node.text
        for alt, src in images:
            [text_for_new_node, remaining_text] = remaining_text.split(
                f"![{alt}]({src})", 1
            )
            if len(text_for_new_node) > 0:
                new_nodes.append(
                    TextNode(text_for_new_node, old_node.text_type, old_node.url)
                )
            new_nodes.append(TextNode(alt, TextType.IMAGE, src))
        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, old_node.text_type, old_node.url))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    if len(old_nodes) == 0:
        return []
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        images = extract_markdown_links(old_node.text)
        remaining_text = old_node.text
        for alt, src in images:
            [text_for_new_node, remaining_text] = remaining_text.split(
                f"[{alt}]({src})", 1
            )
            if len(text_for_new_node) > 0:
                new_nodes.append(
                    TextNode(text_for_new_node, old_node.text_type, old_node.url)
                )
            new_nodes.append(TextNode(alt, TextType.LINK, src))
        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, old_node.text_type, old_node.url))
    return new_nodes
