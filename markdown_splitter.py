import re


class MarkdownSplitter:
    def __init__(self) -> None:
        pass

    def split_markdown(self, file_path: str) -> list:
        """Splits a markdown string into a list of markdown strings."""
        with open(file_path, "r") as f:
            markdown = f.read()
            chunks = re.findall(
                r"^#+\s+(.*?\n.*?)(?=\n#|\Z)",
                markdown,
                flags=re.DOTALL | re.MULTILINE,
            )
            print(chunks)
            return chunks
