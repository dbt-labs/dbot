from csv_crawler import CSVCrawler


def test_should_split_csv_into_rows_except_heading():
    test_dir = "./test-docs/"
    crawler = CSVCrawler(test_dir)

    docs = crawler.crawl_and_make_docs()

    assert len(docs) == 2313


def test_should_create_id_based_on_hashed_filename_and_content():
    test_dir = "./test-docs/"
    crawler = CSVCrawler(test_dir)

    docs = crawler.crawl_and_make_docs()

    assert docs[0].metadata["id"] == crawler.hash_string(
        f"{docs[0].metadata['source']}{docs[0].page_content}"
    )
