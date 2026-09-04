import re


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if re.match(r"^# .+$", line):
            return line[2:].strip()
    raise ValueError("markdown contains no h1 header")
