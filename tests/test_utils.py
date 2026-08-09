from io import BytesIO

from pypdf import PdfWriter

from src.utils import extract_text_from_bytes


def test_extract_text_from_bytes_pdf():
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    stream = BytesIO()
    writer.write(stream)
    stream.seek(0)

    text = extract_text_from_bytes(stream.getvalue(), "sample.pdf")
    assert text == ""
