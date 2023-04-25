from markdown_crawler import MarkdownCrawler


def test_should_split_markdown_at_headings():
    test_dir = "./test-docs/guides/best-practices/materializations/"
    crawler = MarkdownCrawler(test_dir)

    docs = crawler.crawl_and_make_docs()

    assert len(docs) == 21


def test_should_create_id_based_on_hashed_filename_and_content():
    test_dir = "./test-docs/guides/best-practices/materializations/"
    crawler = MarkdownCrawler(test_dir)

    docs = crawler.crawl_and_make_docs()

    assert docs[0].metadata["id"] == crawler.hash_string(
        f"{docs[0].metadata['source']}{docs[0].page_content}"
    )
