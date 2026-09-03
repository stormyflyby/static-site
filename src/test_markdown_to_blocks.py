import unittest

from markdown_to_blocks import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
