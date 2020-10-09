#!/usr/bin/env python3

##################################################################################
#
# Created by Skip McGee for DJC2 20.2 AKA "The Looters"
#
#
##################################################################################

# Import statements
from pdfformfiller import PdfFormFiller

def pdf_manipulation():
    try:
        filler = PdfFormFiller("f2106.pdf")
        filler.add_text(text, pagenum, (x1, y1), (x2, y2))
        filler.write(outfile)
    except:
        pass

# In order to determine the correct (x1, y1), (x2, y2) coordinates for your test field bounding box, we recommend dumping your existing pdf template to images with 72 dpi and using an image editor (like GIMP) to find the pixel coordinates of the rectangle you want your bounding box to be.
















# Define the main
def main():
    pdf_manipulation()


# Call the main function
if __name__ == "__main__":
    main()
    exit(0)
