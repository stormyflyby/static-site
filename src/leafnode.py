from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, props: {{{self.props_to_html()} }})"

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("cannot convert leaf HTML node without value to HTML")
        if not self.tag:
            return self.value
        start_tag = f"<{self.tag}>"
        close_tag = f"</{self.tag}>"
        if self.props:
            start_tag = start_tag[:-1] + f"{self.props_to_html()}>"
        return start_tag + self.value + close_tag
