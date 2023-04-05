import re

import frontmatter
from langchain.docstore.document import Document


class MarkdownSplitter:
    def __init__(self) -> None:
        pass

    def split_markdown(self, file_path: str) -> list:
        """Splits a markdown string into a list of markdown strings."""
        sections = []
        with open(file_path, "r") as f:
            markdown = f.read()
            chunks = re.findall(
                # Need to edit this regex to not catch comments in code blocks
                # Need to deal with frontmatter somehow and title/h1 not being in text
                # Need to use frontmatter slug if it exists
                r"^#+\s+(.*?)\n(.*?)(?=\n#|\Z)",
                markdown,
                flags=re.DOTALL | re.MULTILINE,
            )
            for chunk in chunks:
                if chunk[0] and chunk[1]:
                    sections.append(
                        {
                            "title": chunk[0],
                            "content": chunk[1],
                            "slug": self.slugify(chunk[0]),
                        }
                    )
        return sections

    def slugify(self, string: str) -> str:
        return (
            string.lower()
            .strip()
            .replace(" ", "-")
            .replace(":", "")
            .replace("*", "")
            .replace("'", "")
            .replace('"', "")
            .replace("’", "")
            .replace("‘", "")
            .replace("?", "")
            .replace("!", "")
            .replace("(", "")
            .replace(")", "")
            .replace(".", "")
            .replace("/", "")
            .replace("&", "and")
            .replace("`", "")
            .replace("“", "")
            .replace("”", "")
        )

    def create_documents(self, file_path: str) -> list:
        """Creates a list of langchain documents from a markdown file."""
        documents = []
        sections = self.split_markdown(file_path)

        fm = frontmatter.loads(open(file_path).read())
        slug = ""
        if fm.get("slug"):
            slug = fm["slug"]
            file_path = re.sub(r"[^/]+$", slug, file_path)

        for section in sections:
            documents.append(
                Document(
                    page_content=section["content"],
                    metadata={
                        # TODO test that this works!
                        # It probably needs to be joined to the root path
                        "source": file_path,
                        "slug": section["slug"],
                        "title": section["title"],
                    },
                )
            )
        return documents
