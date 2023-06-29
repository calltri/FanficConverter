import fanfic_converter
import pytest
import codecs

FULL_TEST_FILE_NAME = "test_fanfics/17HarryPotterandtheMagicalGirl.html"
FULL_HEADER_NAME = "test_fanfics\header.txt"
FULL_ENTIRE_BODY_NAME = "test_fanfics\entire_body.txt"
FULL_NUM_SECTIONS = 9

PARTITION_HEADER = "<head></head>"
BODY_START = "<body>"
BODY_END = "</body>"
PARTITION_BODY_START = "<html>" + PARTITION_HEADER + "<body>"
PARTITION_BODY_END = "</body></html>"
PARTITIONING_TEST_DATA = [
    {"test_name": "ch and p", "body_code":"<h3>chapter</h3><p></p>", "num_sections":1, 
        "sections": [PARTITION_BODY_START + "<h3>chapter</h3><p></p>" + PARTITION_BODY_END]},
    {"test_name": "ch", "body_code":"<h3>chapter</h3>", "num_sections":1, 
        "sections": [PARTITION_BODY_START + "<h3>chapter</h3>" + PARTITION_BODY_END]},
    {"test_name": "p", "body_code":"<p></p>", "num_sections":0, 
        "sections": []},
    {"test_name": "p and ch", "body_code":"<p></p><h3>chapter</h3>", "num_sections":1, 
        "sections": [PARTITION_BODY_START + "<h3>chapter</h3>" + PARTITION_BODY_END]},
    {"test_name": "ch p and ch", "body_code":"<h3>chapter</h3><p></p><h3>chapter</h3>", "num_sections":2, 
        "sections": [PARTITION_BODY_START + "<h3>chapter</h3><p></p>" + PARTITION_BODY_END,
                     PARTITION_BODY_START + "<h3>chapter</h3>" + PARTITION_BODY_END]},
    {"test_name": "ch p ch and p", "body_code":"<h3>chapter</h3><p></p><h3>chapter</h3><p></p>", "num_sections":2, 
        "sections": [PARTITION_BODY_START + "<h3>chapter</h3><p></p>" + PARTITION_BODY_END,
                     PARTITION_BODY_START + "<h3>chapter</h3><p></p>" + PARTITION_BODY_END]},
    {"test_name": "null test", "body_code":"", "num_sections":0, 
        "sections": []},
]

class TestClass:

    def test_full_isolate_header(self):
        fanfic_code = fanfic_converter.read_html_file(FULL_TEST_FILE_NAME)
        header, fanfic_code = fanfic_converter.isolate_header(fanfic_code)
        assert len(header) > 0
        assert header == fanfic_converter.read_html_file(FULL_HEADER_NAME)
        assert fanfic_code == fanfic_converter.read_html_file(FULL_ENTIRE_BODY_NAME)

    def test_partitioning(self):
        for test_data in PARTITIONING_TEST_DATA:
            print("Starting test: " + test_data["test_name"])
            sections = fanfic_converter.partition_html_into_chapters(PARTITION_HEADER, 
                                                                     BODY_START + 
                                                                     test_data["body_code"] + 
                                                                     BODY_END)
            assert len(sections) == test_data["num_sections"]
            assert sections == test_data["sections"]
            print("Passed test: " + test_data["test_name"])
            
    def test_full_partition_html_into_sections(self):
        fanfic_code = fanfic_converter.read_html_file(FULL_TEST_FILE_NAME)
        header, fanfic_code = fanfic_converter.isolate_header(fanfic_code)
        sections = fanfic_converter.partition_html_into_chapters(header, fanfic_code)
        assert len(sections) == FULL_NUM_SECTIONS
