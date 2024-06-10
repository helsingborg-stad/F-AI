import os
import pytest
import pytest_asyncio

from fai_backend.files.file_parser import ParserFactory
from fai_backend.vector.memory import InMemoryChromaDB

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PDF_PATH = os.path.join(CURRENT_DIR, 'test_data/Bevprogram_Raa_1991_sbf.pdf')


@pytest.fixture(scope='session')
def document_elements():
    pdf_parser = ParserFactory.get_parser(TEST_PDF_PATH)
    return pdf_parser.parse(TEST_PDF_PATH)


@pytest_asyncio.fixture
async def vector_db():
    db = InMemoryChromaDB()
    yield db
    await db.reset()


def test_parser_with_pdf_file_then_expect_parsed_correctly(document_elements):
    first_element = str(document_elements[0]) if document_elements else ""

    expect_text = "Bevaringsprogram för Råå\n\nHELSINGBORGS MUSEUM\n\nBevaringsprogram för Råå Fastställt av kommunfullmäktige 1991-08-27\n\nHelsingborgs bevaringskommitte Helsingborgs museum"
    assert expect_text in first_element, "The PDF content was not parsed correctly."


@pytest.mark.asyncio
async def test_parse_and_vectorize_then_query_correct_result(document_elements, vector_db):
    collection_name = "test_collection"
    expected_doc_id = "0"

    await vector_db.create_collection(collection_name=collection_name)

    await vector_db.add(
        collection_name=collection_name,
        documents=[str(elem) for elem in document_elements],
        metadatas=[{"source": "my_source"} for _ in document_elements],
        ids=[str(i) for i in range(len(document_elements))]
    )

    query_text = "Bevaringsprogram för Råå"
    results = await vector_db.query(
        collection_name=collection_name,
        query_texts=[query_text],
        n_results=1
    )

    assert results["ids"] == [
        [expected_doc_id]], f"The query did not return the expected document id {expected_doc_id}."


@pytest.mark.asyncio
async def test_without_metadatas(document_elements, vector_db):
    collection_name = "test_collection"
    expected_doc_id = "0"

    await vector_db.create_collection(collection_name=collection_name)

    await vector_db.add(
        collection_name=collection_name,
        documents=[str(elem) for elem in document_elements],
        ids=[str(i) for i in range(len(document_elements))]
    )

    query_text = "Bevaringsprogram för Råå"
    results = await vector_db.query(
        collection_name=collection_name,
        query_texts=[query_text],
        n_results=1
    )

    assert results["ids"] == [
        [expected_doc_id]], f"The query did not return the expected document id {expected_doc_id}."
