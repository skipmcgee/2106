#!/usr/bin/env python3

##################################################################################
#
# Created by Skip McGee for DJC2 20.2 AKA "The Looters"
#
#
##################################################################################


from PyPDF2 import PdfFileReader
import logging
import logging.handlers
import os
import urllib.request

global page_total, error_count, pdfpagedict, error_string, file_name, file_path

class PDF_Document:
    """ Actions that need to occur to process a PDF document into Python """
    def __init__(self):
        self.file = ""
        self.error_count = 0
        self.pdfpagedict = {}

    def __str__(self):
        """ Class PDF_Document consists of the actions required to import a PDF Document into a Python dictionary """

    def __repr__(self):
        """ input(filepath), try open(pdf, 'rb') """

    def auto_input(self):
        """ Automatically input a filepath, check date to ensure file is updated if neccessary """
        try:
            self.url = f"https://www.irs.gov/pub/irs-pdf/f2106.pdf"
            self.file_name = self.url.split("/")[-1]
            with urllib.request.urlopen(self.url) as self.file_Obj:
                self.file_Obj = PdfFileReader(self.file_Obj)
                self.pdfinfo = self.file_Obj.getDocumentInfo()
                self.page_total = int(self.file_Obj.numPages)
                for page in range(self.page_total):
                    page = int(page)
                    self.pageobj = self.file_Obj.getPage(page)
                    print(self.pageobj)
                    self.pdfpagedict[page] = self.pageobj.extractText()
            return self.pdfpagedict
        except Exception as error:
            self.error_string = f"Error encountered in method auto_input: "
            self.error_count += 1
            print(self.error_string, error, "Error_count={self.error_count}", sep="\n")
            logging.warning(self.error_string, error, "error_count =", self.error_count)
            exit(1)

    def manual_input(self):
        """ Manually input a filepath, test user input to ensure file exists and can be read """
        try:
            self.file_path = str(input("Enter a filepath to the pdf you would like to use: "))
            self.file_name = self.file_path.split("/")[-1]
            with open(self.file_path, 'rb') as self.file_Obj:
                self.file_Obj = PdfFileReader(self.file_Obj)
                self.pdfinfo = self.file_Obj.getDocumentInfo()
                self.page_total = int(self.file_Obj.numPages)
                self.pdfpagedict = {}
                for page in range(self.page_total):
                    page = int(page)
                    self.pageobj = self.file_Obj.getPage(page)
                    print(self.pageobj)
                    self.pdfpagedict[page] = self.pageobj.extractText()
            return self.pdfpagedict
        except FileNotFoundError as error:
            print("This filepath does not appear to be correct, please try again.")
            self.error_count += 1
            logging.warning("This filepath does not appear to be correct, please try again.", error, "error_count =", self.error_count)
            self.manual_input()
        except Exception as error:
            self.error_string = f"Error encountered in manual_input method: "
            print(self.error_string, error)
            self.error_count += 1
            logging.warning("Error encountered in manual_input method: ", error, "error_count =", self.error_count)
            exit(1)

class LogFormatter(logging.Formatter, PDF_Document):
    """ Basic system log message generator to identify error for troubleshooting """
    def __init__(self):
        super().__init__()

    def format(self, record):
        result = super().format(record)
        return "ufeff" + result

    def log_object(self):
        handler = logging.handlers.SysLogHandler('/dev/log')
        formatter = logging.Formatter()
        handler.setFormatter(formatter)
        pdfscraper_log = logging.getLogger()
        pdfscraper_log.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
        pdfscraper_log.addHandler(handler)

    def log_message_begin(self):
        logging.info(
            f"'running_process'='pdfscraper.py', 'originating_process'={__name__}")

    def log_message_end(self):
        logging.info(
            f"'running_process'='pdfscraper.py', 'originating_process'={__name__}, 'error_message'={self.error_string},"
            f" 'error_count'={self.error_count}\n")


def main():
    log_obj = LogFormatter()
    log_obj.log_object()
    log_obj.log_message_begin()
    doc_obj = PDF_Document()
    doc_obj.manual_input()
    log_obj.log_message_end()
    if exit(1):
        print(f"{doc_obj.error_string}, error count = {doc_obj.error_count}")
        log_obj.log_message_end()
        exit(1)
    else:
        exit(0)


# Call the main function
if __name__ == "__main__":
    main()
