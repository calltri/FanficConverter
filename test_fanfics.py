import fanfic_converter
import pytest
import codecs

TEST_FILE_NAME = "test_fanfics/17HarryPotterandtheMagicalGirl.html"
HEADER_NAME = "test_fanfics\header.txt"
ENTIRE_BODY_NAME = "test_fanfics\entire_body.txt"

NUM_SECTIONS = 9
SECTION1_NAME = ""
SECTION2_NAME = ""
SECTION3_NAME = ""
SECTION8_NAME = ""





class TestClass:
    def test_isolate_header(self):
        f = codecs.open(TEST_FILE_NAME, 'r', "utf-8")
        fanfic_code = f.read()
        f.close()
        header, fanfic_code = fanfic_converter.isolate_header(fanfic_code)
        assert len(header) > 0
        assert header == fanfic_converter.read_html_file(HEADER_NAME)
        assert fanfic_code == fanfic_converter.read_html_file(ENTIRE_BODY_NAME)

    def test_partition_html_into_sections(self):
        f = codecs.open(TEST_FILE_NAME, 'r', "utf-8")
        fanfic_code = f.read()
        f.close()
        header, fanfic_code = fanfic_converter.isolate_header(fanfic_code)
        sections = fanfic_converter.partition_html_into_chapters(header, fanfic_code)
        assert len(sections) == NUM_SECTIONS
