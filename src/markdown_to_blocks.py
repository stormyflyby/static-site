def markdown_to_blocks(text: str) -> list[str]:
    blocks = [s.strip() for s in text.split("\n\n")]
    return list(filter(lambda s: len(s) > 0, blocks))
