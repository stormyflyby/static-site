from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list["HTMLNode"], props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, props: {{{self.props_to_html()} }})"

    def to_html(self):
        if not self.tag:
            raise ValueError("parent HTML node does not have required tag")
        if not self.children:
            raise ValueError("parent HTML node does not have required children")
        start_tag = f"<{self.tag}>"
        close_tag = f"</{self.tag}>"
        if self.props:
            start_tag = start_tag[:-1] + f"{self.props_to_html()}>"
        body = ""
        for child in self.children:
            body += child.to_html()
        return start_tag + body + close_tag
