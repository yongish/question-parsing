from PyPDF2 import PdfWriter, PdfReader

inputpdf = PdfReader(open('./pdfs/2015-P6-Prelims-Chinese-CHIJ.pdf', "rb"))

# for i in range(len(inputpdf.pages)):
#     output = PdfWriter()
#     output.add_page(inputpdf.pages[i])
#     with open("document-page%s.pdf" % i, "wb") as outputStream:
#         output.write(outputStream)


output = PdfWriter()
output.add_page(inputpdf.pages[0])
output.add_page(inputpdf.pages[1])
with open("document-page.pdf", "wb") as outputStream:
    output.write(outputStream)
