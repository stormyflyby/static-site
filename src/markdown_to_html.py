import re

from htmlnode import HTMLNode
from leafnode import LeafNode
from markdown_block import BlockType, block_to_block_type, markdown_to_blocks
from parentnode import ParentNode
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_children(text: str) -> list[HTMLNode]:
    if len(text) == 0:
        return []
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def heading_number(text: str) -> int:
    if re.match(r"^#{1,6} .+$", text) is None:
        raise ValueError("text must be a header block")
    prefix = text.split(" ", 1)[0]
    return len(prefix)


def list_to_html_node(text: str, tag: str) -> HTMLNode:
    list_items: list[HTMLNode] = []
    lines = text.split("\n")
    for line in lines:
        children = text_to_children(line)
        list_items.append(ParentNode("li", children))
    return ParentNode(tag, list_items)


def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    block_text = remove_markdown_block_syntax(block, block_type)
    match block_type:
        case BlockType.PARAGRAPH:
            new_line_to_space = block_text.replace("\n", " ")
            children = text_to_children(new_line_to_space)
            return ParentNode("p", children)
        case BlockType.HEADING:
            heading_number = heading_number(block)
            children = text_to_children(block_text)
            return ParentNode(f"h{heading_number}", children)
        case BlockType.CODE:
            code = text_node_to_html_node(TextNode(block_text, TextType.CODE_TEXT))
            return ParentNode("pre", [code])
        case BlockType.QUOTE:
            children = text_to_children(block_text)
            return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            return list_to_html_node(block_text, "ul")
        case BlockType.ORDERED_LIST:
            return list_to_html_node(block_text, "ol")


def remove_markdown_block_syntax(text: str, block_type: BlockType) -> str:
    match block_type:
        case BlockType.PARAGRAPH:
            return text
        case BlockType.HEADING:
            result = text.split(" ", 1)[1]
            return result
        case BlockType.CODE:
            return text[4:-3]
        case BlockType.QUOTE:
            lines = text.split("\n")
            lines_content: list[str] = []
            for line in lines:
                if len(line) > 1 and line[1] == " ":
                    lines_content.append(line[2:])
                else:
                    lines_content.append(line[1:])
            return "\n".join(lines_content)
        case BlockType.UNORDERED_LIST:
            lines = text.split("\n")
            lines_content = [line[2:] for line in lines]
            return "\n".join(lines_content)
        case BlockType.ORDERED_LIST:
            lines = text.split("\n")
            lines_content = [line.split(" ", 1)[1] for line in lines]
            return "\n".join(lines_content)


def markdown_to_html_node(markdown: str) -> ParentNode:
    markdown_blocks = markdown_to_blocks(markdown)
    if len(markdown_blocks) == 0:
        raise ValueError("markdown string contains no markdown blocks")
    block_html_nodes: list[HTMLNode] = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        block_html_node = block_to_html_node(block, block_type)
        block_html_nodes.append(block_html_node)
    return ParentNode("div", block_html_nodes)
