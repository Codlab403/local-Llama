from backend.src.models.document import Document
from backend.src.models.node import Node


def test_document_model_minimal():
    d = Document(id="doc1", filename="file.txt")
    assert d.id == "doc1"
    assert d.filename == "file.txt"


def test_node_model_full():
    n = Node(id="n1", doc_id="doc1", page=1, snippet="hello", embedding=[0.1, 0.2], metadata={"k": "v"})
    assert n.id == "n1"
    assert n.doc_id == "doc1"
    assert n.page == 1
    assert n.snippet == "hello"
    assert isinstance(n.embedding, list)
from backend.src.models.document import Document
from backend.src.models.node import Node


def test_document_model_defaults():
    d = Document(id="doc1", filename="sample.pdf")
    assert d.id == "doc1"
    assert d.filename == "sample.pdf"
    assert d.uploaded_at is None
    assert d.status is None


def test_node_model_validation_and_defaults():
    n = Node(id="n1", doc_id="doc1", snippet="hello world")
    assert n.id == "n1"
    assert n.doc_id == "doc1"
    assert n.page is None
    assert n.snippet == "hello world"
    assert n.embedding is None
    assert n.metadata is None
from backend.src.models.document import Document
from backend.src.models.node import Node


def test_document_model():
    d = Document(id="d1", filename="f.txt", uploaded_at=None)
    assert d.id == "d1"


def test_node_model():
    n = Node(id="n1", doc_id="d1", snippet="hello")
    assert n.doc_id == "d1"
