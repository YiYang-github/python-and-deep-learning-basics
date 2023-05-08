#值得注意的问题: dataclass 在python版本小于3.7时没法使用，需要格外下载

import PyPDF2
import re

# Open the PDF file and create a PDF reader object
pdf_file = open('example1.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Get the number of pages in the PDF file
num_pages = pdf_reader.getNumPages()

# Search for the REFERENCES section and extract the text
references = ''
appendix_found = False
ref_found = False

for page_num in range(num_pages):
    page = pdf_reader.getPage(page_num)
    text = page.extractText()
    text = re.sub(r'\d+$', '', text)

    if ref_found and 'APPENDIX' in text.upper():
        appendix_found = True

    if appendix_found:
        break

    if ref_found:
        references += text

    match = re.search(r'REFERENCES\s*(.*)', text, re.DOTALL)
    if match:
        references += match.group(1)
        ref_found = True

authors = []
titles = []
publications = []

ref = re.split(r"[.?]",references)
print(ref[1:10])
