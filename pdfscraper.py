#!/usr/bin/env python3

##################################################################################
#
# Created by Skip McGee for DJC2 20.2 AKA "The Looters" on 20201003
#
#
##################################################################################


from PyPDF2 import PdfFileReader
import logging
import logging.handlers
import urllib.request
import datetime

global page_total, error_count, pdfpagedict, error_string, file_name, file_path

class PDF_Document:
    """ Actions that need to occur to process a PDF document into Python """
    def __init__(self):
        self.file_name = ""
        self.file_path = ""
        self.error = ""
        self.error_count = 0
        self.pdfpagedict = {}
        self.error_string = ""
        self.page_total = 0


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
                self.pdfpagedict = {}
                for page in range(self.page_total):
                    page = int(page)
                    self.pageobj = self.file_Obj.getPage(page)
                    self.pdfpagedict[page] = self.pageobj.extractText()
            return self.pdfpagedict
        except Exception as error:
            self.error_string = f"Error encountered in method auto_input: "
            self.error_count += 1
            print(self.error_string, error, sep="\n")
            self.error = error

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
                    self.pdfpagedict[page] = self.pageobj.extractText()
            return self.pdfpagedict
        except FileNotFoundError as error:
            print("This filepath does not appear to be correct, please try again.")
            self.error_count += 1
            logging.warning("This filepath does not appear to be correct, please try again.", error, "error_count =", self.error_count)
            self.error = error
            self.manual_input()
        except Exception as error:
            self.error_string = f"Error encountered in manual_input method: "
            print(self.error_string, error, sep="\n")
            self.error = error
            self.error_count += 1

class LogFormatter(logging.Formatter, PDF_Document):
    """ Basic system log message generator to identify significant events and errors for troubleshooting """
    def __init__(self):
        self.start_time = datetime.datetime.today()
        super().__init__()


    def log_object(self):
        handler = logging.handlers.SysLogHandler('/dev/log')
        formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        handler.setFormatter(formatter)
        pdfscraper_log = logging.getLogger('pdfscraper.py')
        pdfscraper_log.setLevel(logging.DEBUG)
        pdfscraper_log.addHandler(handler)

    def log_message_begin(self):
        begin_message = f"Beginning pdfscraper.py, 'start_time'={self.start_time}, 'originating_process'={__name__}"
        print(begin_message)
        logging.info(begin_message)

    def log_message_end(self):
        self.end_time = datetime.datetime.today()
        self.runtime = self.end_time - self.start_time
        end_message = f"Ending pdfscraper.py, 'end_time'={self.end_time}, 'run_time'={self.runtime}, 'originating_process'={__name__}"
        print(end_message)
        logging.info(end_message)

    def log_message_errorsum(self, error_count, error_string, error):
        errormessage = f"Sum of errors in pdfscraper.py, 'error_count' = {error_count}, '{error_string}'={error}"
        print(errormessage)
        logging.critical(errormessage)


def main():
# Create log_obj for use as needed, send indicator of script initiation
    log_obj = LogFormatter()
    log_obj.log_object()
    log_obj.log_message_begin()
# Creat doc_obj for use
    doc_obj = PDF_Document()
    doc_obj.auto_input()
# Final log messages for recording completion and problems
    log_obj.log_message_end()
    if doc_obj.error_count > 0:
        log_obj.log_message_errorsum(doc_obj.error_count, doc_obj.error_string, doc_obj.error)
    exit(doc_obj.error_count)


# Call the main function
if __name__ == "__main__":
    main()
