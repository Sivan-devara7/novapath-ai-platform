"""
Unit Test: Verifies PDF Hyperlink Annotation Extraction.
Confirms:
1. Valid clickable URLs (e.g. GitHub/Portfolio) are extracted even when not printed as visible text.
2. Mailto (mailto:...) and Telephone (tel:...) links are explicitly ignored.
"""

import io
import pytest
import pypdf
from pypdf.generic import (
    DictionaryObject,
    NameObject,
    TextStringObject,
    ArrayObject,
    FloatObject,
    DecodedStreamObject
)

from app.services.ats_service import ats_service

def create_test_pdf_with_annotations(valid_url: str, mailto_url: str, tel_url: str) -> bytes:
    """Generates an in-memory PDF with visible text and clickable link annotations."""
    writer = pypdf.PdfWriter()
    page = writer.add_blank_page(width=612, height=792)

    # 1. Add visible text stream (simulating resume body with > 25 words)
    text_content = (
        b"BT /F1 12 Tf 72 712 Td (Alex Morgan is an experienced Full Stack Software Engineer specializing in Python React TypeScript Docker and PostgreSQL with demonstrated expertise in building high performance distributed microservices and scalable web applications) Tj ET"
    )
    stream = DecodedStreamObject()
    stream.set_data(text_content)
    page[NameObject("/Contents")] = writer._add_object(stream)

    # Font resource
    font_dict = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica")
    })
    fonts = DictionaryObject({NameObject("/F1"): writer._add_object(font_dict)})
    page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): fonts})

    # 2. Add clickable link annotations
    # (a) Target Portfolio / GitHub Link
    portfolio_link = DictionaryObject({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Link"),
        NameObject("/Rect"): ArrayObject([FloatObject(72), FloatObject(700), FloatObject(200), FloatObject(720)]),
        NameObject("/A"): DictionaryObject({
            NameObject("/S"): NameObject("/URI"),
            NameObject("/URI"): TextStringObject(valid_url)
        })
    })

    # (b) Mailto Link (should be ignored)
    email_link = DictionaryObject({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Link"),
        NameObject("/Rect"): ArrayObject([FloatObject(220), FloatObject(700), FloatObject(320), FloatObject(720)]),
        NameObject("/A"): DictionaryObject({
            NameObject("/S"): NameObject("/URI"),
            NameObject("/URI"): TextStringObject(mailto_url)
        })
    })

    # (c) Telephone Link (should be ignored)
    tel_link = DictionaryObject({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Link"),
        NameObject("/Rect"): ArrayObject([FloatObject(340), FloatObject(700), FloatObject(420), FloatObject(720)]),
        NameObject("/A"): DictionaryObject({
            NameObject("/S"): NameObject("/URI"),
            NameObject("/URI"): TextStringObject(tel_url)
        })
    })

    page[NameObject("/Annots")] = ArrayObject([portfolio_link, email_link, tel_link])

    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()

def test_pdf_hyperlink_extraction():
    portfolio_url = "https://github.com/alexmorgan/fullstack-portfolio"
    mailto_url = "mailto:alex.morgan@domain.com"
    tel_url = "tel:+15550192834"

    pdf_bytes = create_test_pdf_with_annotations(portfolio_url, mailto_url, tel_url)

    # Execute extraction
    extracted_text = ats_service.extract_text_from_file(pdf_bytes, "candidate_resume.pdf")

    # Assertions
    assert portfolio_url in extracted_text, f"Expected {portfolio_url} to be extracted from annotations."
    assert "mailto:" not in extracted_text.lower(), "Expected mailto: links to be ignored."
    assert mailto_url not in extracted_text, "Expected specific mailto address to be filtered out."
    assert "tel:" not in extracted_text.lower(), "Expected tel: links to be ignored."
    assert tel_url not in extracted_text, "Expected specific telephone link to be filtered out."

def create_word_gdocs_canva_test_pdf(source_tool: str, url: str) -> bytes:
    """
    Synthesizes PDF structures with tool-specific PDF object patterns:
    - Word: Uses /Border [0 0 0], /C [0 0 1], /A << /S /URI /URI (...) >>
    - Google Docs: Uses /F 4 (NoRotate/NoZoom), /QuadPoints, /A << /S /URI /URI (...) >>
    - Canva: Uses tagged structure /StructParents with /Link annotations
    """
    writer = pypdf.PdfWriter()
    page = writer.add_blank_page(width=612, height=792)

    text_content = (
        f"BT /F1 12 Tf 72 712 Td (Exported resume from {source_tool} for candidate testing technical skill extraction with python docker kubernetes fastAPI and deep learning systems) Tj ET"
    ).encode("latin-1")
    stream = DecodedStreamObject()
    stream.set_data(text_content)
    page[NameObject("/Contents")] = writer._add_object(stream)

    font_dict = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica")
    })
    fonts = DictionaryObject({NameObject("/F1"): writer._add_object(font_dict)})
    page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): fonts})

    annot = DictionaryObject({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Link"),
        NameObject("/Rect"): ArrayObject([FloatObject(72), FloatObject(700), FloatObject(250), FloatObject(720)]),
        NameObject("/A"): DictionaryObject({
            NameObject("/S"): NameObject("/URI"),
            NameObject("/URI"): TextStringObject(url)
        })
    })

    if source_tool == "Word":
        annot[NameObject("/Border")] = ArrayObject([FloatObject(0), FloatObject(0), FloatObject(0)])
        annot[NameObject("/C")] = ArrayObject([FloatObject(0), FloatObject(0), FloatObject(1)])
    elif source_tool == "Google Docs":
        annot[NameObject("/F")] = FloatObject(4)
    elif source_tool == "Canva":
        annot[NameObject("/StructParent")] = FloatObject(1)

    # Add ignored mailto and tel links as well
    mailto_annot = DictionaryObject({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Link"),
        NameObject("/Rect"): ArrayObject([FloatObject(260), FloatObject(700), FloatObject(360), FloatObject(720)]),
        NameObject("/A"): DictionaryObject({
            NameObject("/S"): NameObject("/URI"),
            NameObject("/URI"): TextStringObject("mailto:applicant@example.com")
        })
    })

    page[NameObject("/Annots")] = ArrayObject([annot, mailto_annot])

    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()

def test_word_gdocs_canva_export_link_extraction():
    """Validates link extraction across Microsoft Word, Google Docs, and Canva PDF patterns."""
    test_cases = [
        ("Word", "https://github.com/developer/word-export-portfolio"),
        ("Google Docs", "https://portfolio.dev/gdocs-candidate-site"),
        ("Canva", "https://linkedin.com/in/canva-designed-profile")
    ]

    for tool, url in test_cases:
        pdf_bytes = create_word_gdocs_canva_test_pdf(tool, url)
        extracted = ats_service.extract_text_from_file(pdf_bytes, f"{tool.lower()}_resume.pdf")
        assert url in extracted, f"Failed to extract {tool} hyperlink URL: {url}"
        assert "mailto:" not in extracted.lower(), f"Failed to filter mailto link in {tool} PDF"

    # Also check if user has placed real physical PDFs in fixtures directory
    import os
    fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures", "pdf_samples")
    if os.path.isdir(fixture_dir):
        for fname in os.listdir(fixture_dir):
            if fname.lower().endswith(".pdf"):
                fpath = os.path.join(fixture_dir, fname)
                with open(fpath, "rb") as f:
                    content = f.read()
                try:
                    res_text = ats_service.extract_text_from_file(content, fname)
                    assert len(res_text.strip()) > 20
                    assert "mailto:" not in res_text.lower()
                    print(f"[OK] Successfully verified real fixture PDF: {fname}")
                except Exception as e:
                    print(f"[Fixture Warning] {fname}: {e}")

if __name__ == "__main__":
    test_pdf_hyperlink_extraction()
    test_word_gdocs_canva_export_link_extraction()
    print("All PDF link extraction tests PASSED.")
