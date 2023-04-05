from markdown_splitter import MarkdownSplitter

markdown_splitter = MarkdownSplitter()


def test_should_split_markdown_at_headings():
    test_doc = "./test-docs/guides/best-practices/materializations/materializations-guide-1-guide-overview.md"

    sections = markdown_splitter.split_markdown(test_doc)

    assert len(sections) == 3
    assert sections[0]["title"] == "Learning goals"
    assert sections[1]["title"] == "Prerequisites"
    assert sections[2]["title"] == "Guiding principle"
