import os
import pytest
import pytest_asyncio

from fai_backend.files.file_parser import ParserFactory
from fai_backend.vector.memory import InMemoryChromaDB
from fai_backend.files.service import FileUploadService
from fai_backend.vector.service import VectorService

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PDF_PATH = os.path.join(CURRENT_DIR, 'test_data/Bevprogram_Raa_1991_sbf.pdf')


@pytest.fixture(scope='session')
def document_elements():
    pdf_parser = ParserFactory.get_parser(TEST_PDF_PATH)
    return pdf_parser.parse(TEST_PDF_PATH)


@pytest.fixture(scope='session')
def document_elements_from_multiple_files() -> list[str]:
    test_data_path = (CURRENT_DIR / 'test_data' / 'multiples').as_posix()
    file_service = FileUploadService("")
    return file_service.parse_files(test_data_path)


@pytest_asyncio.fixture
async def vector_db():
    db = InMemoryChromaDB()
    yield db
    await db.reset()


@pytest_asyncio.fixture
async def vector_service(vector_db):
    return VectorService(vector_db)


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


@pytest.mark.asyncio
async def test_vectorize_multiple_files_then_query_correct_result(document_elements_from_multiple_files,
                                                                  vector_service):
    documents = document_elements_from_multiple_files
    collection_name = "test_collection_multiple_files"
    expected_doc = ["Hur anmäler jag?", "Behöver jag bygglov?"]

    await vector_service.create_collection(collection_name)
    await vector_service.add_documents_without_id_to_empty_collection(collection_name, documents)

    query_text = "Vad är ett komplementbostadshus?"
    results = await vector_service.query_from_collection(
        collection_name=collection_name,
        query_texts=[query_text])

    assert results["documents"] == [expected_doc], f"The query did not return the expected document {expected_doc}."
