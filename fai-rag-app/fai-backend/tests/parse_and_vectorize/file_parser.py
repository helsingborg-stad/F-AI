import pytest
from fai_backend.files.file_parser import ParserFactory

TEST_PDF_PATH = './test_data/Bevprogram_Raa_1991_sbf.pdf'


@pytest.fixture(scope='session')
def document_elements():
    pdf_parser = ParserFactory.get_parser(TEST_PDF_PATH)
    return pdf_parser.parse(TEST_PDF_PATH)


def test_parser_with_pdf_file_then_expect_parsed_correctly(document_elements):
    first_element = str(document_elements[0]) if document_elements else ""

    expect_text = "Bevaringsprogram för Råå"
    assert expect_text in first_element, "The PDF content was not parsed correctly."
