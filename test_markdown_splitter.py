from markdown_splitter import MarkdownSplitter


def test_should_split_markdown_at_headings():
    markdown_splitter = MarkdownSplitter()
    test_doc = "./test-docs/guides/best-practices/materializations/materializations-guide-1-guide-overview.md"

    sections = markdown_splitter.split_markdown(test_doc)

    assert len(sections) == 3
    assert sections[0]["title"] == "Learning goals"
    assert sections[1]["title"] == "Prerequisites"
    assert sections[2]["title"] == "Guiding principle"


def test_should_slugify_titles():
    test_title = "This & That: A Guide to the *Best* of dbt?!"
    markdown_splitter = MarkdownSplitter()

    slug = markdown_splitter.slugify(test_title)

    assert slug == "this-and-that-a-guide-to-the-best-of-dbt"
