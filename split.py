from markdown_splitter import MarkdownSplitter

markdown_splitter = MarkdownSplitter()

sections = markdown_splitter.split_markdown(
    "./mini-docs/guides/best-practices/materializations/materializations-guide-1-guide-overview.md"
)
print(sections)
