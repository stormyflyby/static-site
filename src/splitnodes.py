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
            else:
                new_type = text_type
            new_nodes.append(TextNode(text_for_new_nodes[i], new_type))
    return new_nodes
