from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    PLAIN_TEXT = "plain_text"
    BOLD_TEXT = "bold_text"
    ITALIC_TEXT = "italic_text"
    CODE_TEXT = "code_text"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode") -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    tag = None
    text = text_node.text
    props = None
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            # No change
            tag = None
        case TextType.BOLD_TEXT:
            tag = "b"
        case TextType.ITALIC_TEXT:
            tag = "i"
        case TextType.CODE_TEXT:
            tag = "code"
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("Link node does not have required URL")
            tag = "a"
            props = {"href": text_node.url}
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("Image node does not have required URL")
            tag = "img"
            text = ""
            props = {"src": text_node.url, "alt": text_node.text}
    return LeafNode(tag, text, props)
