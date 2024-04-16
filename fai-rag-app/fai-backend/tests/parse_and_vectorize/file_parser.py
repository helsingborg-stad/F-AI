import pytest
from fai_backend.files.file_parser import ParserFactory
from fai_backend.vector.memory import InMemoryVectorDB

TEST_PDF_PATH = './test_data/Bevprogram_Raa_1991_sbf.pdf'


@pytest.fixture(scope='session')
def document_elements():
    pdf_parser = ParserFactory.get_parser(TEST_PDF_PATH)
    return pdf_parser.parse(TEST_PDF_PATH)


def test_parser_with_pdf_file_then_expect_parsed_correctly(document_elements):
    first_element = str(document_elements[0]) if document_elements else ""

    expect_text = "Bevaringsprogram för Råå"
    assert expect_text in first_element, "The PDF content was not parsed correctly."


def test_parse_and_vectorize_then_query_correct_result(document_elements):
    vector_db = InMemoryVectorDB()
    collection_name = "test_collection"
    expected_doc_id = "0"

    vector_db.add(
        collection_name=collection_name,
        documents=[str(elem) for elem in document_elements],
        metadatas=[{"source": "my_source"} for _ in document_elements],
        ids=[str(i) for i in range(len(document_elements))]
    )

    query_text = "Bevaringsprogram för Råå"
    results = vector_db.query(
        collection_name=collection_name,
        query_texts=[query_text],
        n_results=1
    )

    assert results["ids"] == [[str(0)]], f"The query did not return the expected document id {expected_doc_id}."
