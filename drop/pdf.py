from PyPDF2 import PdfFileMerger, PdfFileReader


def merge(filenames, out):
	merger = PdfFileMerger()
	for filename in filenames:
	    merger.append(PdfFileReader(file(filename, 'rb')))
	merger.write(out)