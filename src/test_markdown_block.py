import unittest

from markdown_block import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_padding(self):
        md = """



This is some text.


This is some _text_ in italics.
This is some more text.



- List item
- List item



"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is some text.",
                "This is some _text_ in italics.\nThis is some more text.",
                "- List item\n- List item",
            ],
        )

    def test_markdown_to_blocks_only_whitespace(self):
        md = """





"""
        self.assertListEqual(markdown_to_blocks(md), [])

    def test_markdown_to_blocks_empty(self):
        md = ""
        self.assertListEqual(markdown_to_blocks(md), [])

    def test_block_to_block_type_paragraph(self):
        md = "This is a paragraph with\nmultiple lines."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_empty(self):
        md = ""
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        md = "```\nThis is a multi-line\ncode block\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_block_to_block_type_code_no_breaks(self):
        md = "```This is a multi-line code block```"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_missing_end(self):
        md = "```\nThis is a multi-line\ncode block\n"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        md = "#### This is a heading."
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)

    def test_block_to_block_type_heading_six(self):
        md = "###### This is a heading."
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)

    def test_block_to_block_type_heading_seven(self):
        md = "####### This is a heading."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_no_space(self):
        md = "####This is a heading."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        md = "> This is\n> a quote\n>that spans\n> multiple lines."
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_block_to_block_type_empty_line(self):
        md = "> This is\n> a quote\n>\n> with multiple lines."
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_block_to_block_type_quote_invalid_end(self):
        md = "> This is\n> a quote\n>that spans\nf"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_invalid_line(self):
        md = "> This is\n> a quote\nthat spans\n> multiple lines."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_ulist(self):
        md = "- This\n- is an\n- unordered list."
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ulist_invalid_line(self):
        md = "- This\n is an\n- unordered list."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_ulist_missing_space(self):
        md = "- This\n-is an\n- unordered list."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_olist(self):
        md = "1. This is\n2. an\n3. ordered list."
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_block_to_block_type_olist_big_number(self):
        md = "1. a\n2. b\n3. c\n4. d\n5. e\n6. f\n7. g\n8. h\n9. i\n10. j\n11. k\n12. l"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_block_to_block_type_olist_wrong_number(self):
        md = "1. This is\n4. an\n3. ordered list."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_olist_missing_number(self):
        md = "1. This is\nan\n3. ordered list."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_block_to_block_type_olist_no_space(self):
        md = "1. This is\n2.an\n3. ordered list."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
