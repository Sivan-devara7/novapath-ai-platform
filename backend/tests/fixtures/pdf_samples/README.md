# PDF Samples Fixture Directory

Place physical export PDF files here to test hyperlink extraction against real documents:
- `word_resume.pdf` (Exported from Microsoft Word)
- `gdocs_resume.pdf` (Exported from Google Docs)
- `canva_resume.pdf` (Exported from Canva)

`backend/tests/test_pdf_links.py` will automatically detect and validate any `.pdf` files located in this directory.
