import unittest

from markdown_to_html import markdown_to_html_node


class TestBlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> This is a block quote.
>
>It has multiple lines.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a block quote.\n\nIt has multiple lines.</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- This
- is
- a
- list.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This</li><li>is</li><li>a</li><li>list.</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. This
2. is
3. a
4. list.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This</li><li>is</li><li>a</li><li>list.</li></ol></div>",
        )

    def test_many_elements(self):
        md = """
This is a **paragraph**.

1. This
2. looks
45. like
7. a list _but isn't_.

```
This is some
_code_.
```

1. `This`
2. **is a** list
3. with _inline_ stuff.

- `This`
- list has some _inline_ stuff
- **too.**

> This block quote has
> `some` **inline** _things._
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><p>This is a <b>paragraph</b>.</p><p>1. This 2. looks 45. like 7. a list <i>but isn't</i>.</p><pre><code>This is some\n_code_.\n</code></pre><ol><li><code>This</code></li><li><b>is a</b> list</li><li>with <i>inline</i> stuff.</li></ol><ul><li><code>This</code></li><li>list has some <i>inline</i> stuff</li><li><b>too.</b></li></ul><blockquote>This block quote has\n<code>some</code> <b>inline</b> <i>things.</i></blockquote></div>",
        )

    def test_empty(self):
        md = """"""
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)


if __name__ == "__main__":
    unittest.main()
