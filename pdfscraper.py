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
import platform
import subprocess

global page_total, error_count, info_error_list, warn_error_list, error_string, file_name, file_path


if platform.system() == "Darwin":
    try:
        subprocess.call(["pip", "install", "--upgrade", "certificates"])
    except:
        print("MAC user is receiving an error trying to pip install default certificates")
        pass


class PDF_Document:
    """ Actions that need to occur to process a PDF document into Python """
    def __init__(self):
        self.file_name = ""
        self.file_path = ""
        self.error = ""
        self.error_count = 0
        self.pdfpagedict = {}
        self.pdfinfo = {}
        self.error_string = ""
        self.page_total = 0
        self.info_error_list = []
        self.warn_error_list = []

    def __str__(self):
        """ Class PDF_Document consists of the actions required to import a PDF Document into a Python dictionary """

    def __repr__(self):
        """ input(filepath), try open(pdf, 'rb') """

    def pdfworker(self, file_Obj):
        """ function that takes a file object and reads it into a pdf into a dictionary that python can access """
        file_Obj = PdfFileReader(file_Obj)
        self.pdfinfo = file_Obj.getDocumentInfo()
        page_total = int(file_Obj.numPages)
        self.pdfpagedict = {}
        for page in range(page_total):
            page = int(page)
            pageobj = file_Obj.getPage(page)
            self.pdfpagedict[page] = pageobj.extractText()

    def auto_input(self, url=None):
        """ Automatically input a filepath, check date to ensure file is updated if neccessary """
        try:
            if url != None:
                self.url = url
            else:
                self.url = f"https://www.irs.gov/pub/irs-pdf/f2106.pdf"
                print(f"Using hard-coded URL {self.url}")
                self.file_name = self.url.split("/")[-1]
            with urllib.request.urlopen(self.url) as self.file_Obj:
                self.pdfworker(self.file_Obj)
            return self.pdfpagedict
        except Exception as error:
            self.error_count += 1
            self.error = str(error)
            self._message = f"Error encountered in auto_input(), now falling back to manual_input() " \
                            f"requiring a user to verify and type a local file path."
            print(self.error)
            print(self._message)
            errortup = (f"'error_in_function'={__name__}", f"'error_count'={self.error_count}",
                        f"'error_message'={self._message}", f"'error'={self.error}",)
            self.info_error_list.append(errortup)
            self.manual_input()

    def coded_input(self, file_path=None):
        """ Try a hard-coded filepath and turn a pdf into a dictionary, if the filepath doesn't exist then
         try web scraping with auto_input() """
        try:
            if file_path != None:
                self.file_path = file_path
                with open(self.file_path, 'rb') as self.file_Obj:
                    self.pdfworker(self.file_Obj)
            return self.pdfpagedict
        except Exception as error:
            self.error = error
            self.error_count += 1
            self._message = f"Filepath to document was not hard-coded, attempting attempting auto_input() an " \
                                f"automated pull of document from a default URL"
            logging.info(self._message)
            errortup = (f"'error_in_function'={__name__}", f"'error_count'={self.error_count}",
                        f"'error_message'={self._message}", f"'error'={self.error}",)
            self.info_error_list.append(errortup)
            self.auto_input()

    def manual_input(self):
        try:
            self.file_path = str(input("Enter a filepath to the pdf you would like to use: "))
            self.file_name = self.file_path.split("/")[-1]
        except Exception as error:
            error = str(error)
            self.error_count += 1
            self._message = "N/A"
            errortup = (f"'error_in_function'={__name__}", f"'error_count'={self.error_count}",
                        f"'error_message'={self._message}", f"'error'={self.error}",)
            self.info_error_list.append(errortup)


class LogFormatter(logging.Formatter, PDF_Document):
    """ Basic system log message generator to identify significant events and errors for troubleshooting """
    def __init__(self):
        self.start_time = datetime.datetime.today()
        super().__init__()
        handler = logging.handlers.SysLogHandler(address='localhost')
        formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        handler.setFormatter(formatter)
        pdfscraper_log = logging.getLogger(__name__)
        pdfscraper_log.setLevel(logging.DEBUG)
        pdfscraper_log.addHandler(handler)

    def log_message_begin(self):
        begin_message = f"Beginning pdfscraper.py, 'start_time'={self.start_time}, 'originating_process'={__name__};"
        print(begin_message)
        logging.info(begin_message)

    def info_message(self, doc_obj):
        for errortup in doc_obj.info_error_list:
            print(errortup)
            logging.info(errortup)

    def warn_message(self, doc_obj):
        for errortup in doc_obj.warn_error_list:
            print(errortup)
            logging.warning(errortup)

    def log_message_end(self, doc_obj):
        if doc_obj.error_count > 0:
            self.warn_message(doc_obj)
            self.info_message(doc_obj)
        self.end_time = datetime.datetime.today()
        self.runtime = self.end_time - self.start_time
        end_message = f"Ending pdfscraper.py, 'end_time'={self.end_time}, 'run_time'={self.runtime};"
        print(end_message)
        logging.info(end_message)

    def log_message_errorsum(self, errorcount):
        errormessage = f"Sum of errors in pdfscraper.py, 'total_error_count'={errorcount};"
        logging.warning(errormessage)


def main():
    # Create log_obj for use as needed, send indicator of script initiation
    log_obj = LogFormatter()
    log_obj.log_message_begin()
    # Create doc_obj for use
    doc_obj = PDF_Document()
    doc_obj.coded_input('f2106.pdf')
    # Final log messages for recording completion and problems
    log_obj.log_message_end(doc_obj)
    if doc_obj.error_count > 0:
        log_obj.log_message_errorsum(doc_obj.error_count)
    exit(doc_obj.error_count)


# Call the main function
if __name__ == "__main__":
    main()
