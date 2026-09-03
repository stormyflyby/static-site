import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text: str) -> list[str]:
    blocks = [s.strip() for s in text.split("\n\n")]
    return list(filter(lambda s: len(s) > 0, blocks))


def block_to_block_type(markdown_block: str) -> BlockType:
    if re.match(r"^#{1,6} .+$", markdown_block) is not None:
        return BlockType.HEADING
    if re.match(r"^```\n(.|\s)*```$", markdown_block) is not None:
        return BlockType.CODE
    if re.match(r"^(>.*\s?)+$", markdown_block) is not None:
        return BlockType.QUOTE
    if re.match(r"^(- .*\s?)+$", markdown_block) is not None:
        return BlockType.UNORDERED_LIST
    if re.match(r"^(\d+\. .*\s?)+$", markdown_block) is not None:
        is_ordered_list = True
        lines = markdown_block.split("\n")
        for i in range(len(lines)):
            [num, _] = lines[i].split(".", 1)
            if int(num) != i + 1:
                is_ordered_list = False
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
