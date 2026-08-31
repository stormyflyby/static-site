class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, props: {{{self.props_to_html()} }})"

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        result = ""
        for prop_name, prop_value in self.props.items():
            result += f' {prop_name}="{prop_value}"'
        return result
