import os
import sys
from PyPDF2 import PdfMerger


def merge_pdf(path_to_slides):
    merger = PdfMerger()
    for slide_set in sorted(os.listdir(path_to_slides)):
        print("Adding file:", os.path.join(path_to_slides, slide_set))
        merger.append(os.path.join(path_to_slides, slide_set))
    merger.write(os.path.join(path_to_slides, "ai-all-handout.pdf"))
    merger.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: merge_pdf.py <path_to_slides_folder>")
        return
    path_to_slides = sys.argv[1]
    merge_pdf(path_to_slides)


if __name__ == "__main__":
    main()
