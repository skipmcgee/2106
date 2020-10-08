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
import time
from threading import Thread

global page_total, error_count, info_error_list, warn_error_list, error_string, file_name, file_path

class PDF_Document:
    """ Actions that need to occur to process a PDF document into Python """
    def __init__(self, myurl=None, file_path=None):
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
        # Define default URLs and Filepaths
        if myurl != None:
            self.url = myurl
        else:
            self.url = f"https://www.irs.gov/pub/irs-pdf/f2106.pdf"
        if file_path != None:
            self.file_path = file_path
        else:
            self.file_path = 'f2106.pdf'
        # Define operating system version and correct for Mac users
        def my_os():
            my_os = str(platform.system())
            if my_os == 'Darwin':
                return 'Mac'
            else:
                return platform.system()
        # Ensure that default SSL certificates are valid (may affect Mac users)
        def initial_tasks():
            if my_os == 'Mac':
                try:
                    subprocess.call(["pip", "install", "--upgrade", "certificates"])
                except:
                    print("Mac user is receiving an error trying to pip install default certificates")
                    exit(1)

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

    def timer(self, delay=3, what_to_check=None):
        time.sleep(delay)
        if what_to_check != None:
            return
        print("Required input took too long, exiting")
        exit(1)

    def auto_input(self):
        """ Automatically input a filepath, check date to ensure file is updated if neccessary """
        try:
            print(f"Using hard-coded URL {self.url}")
            self.file_name = self.url.split("/")[-1]
            self.timer(delay=10, what_to_check=self.pdfpagedict)
            Thread(target = self.timer).start()
            with urllib.request.urlopen(self.url) as self.file_Obj:
                self.pdfworker(self.file_Obj)
            return self.pdfpagedict
        except Exception as error:
            self.error_count += 1
            self.error = str(error)
            self._message = f"Tried auto_input() without success, errors encountered trying to access the specified URL."
            print(f"Current error = {self.error}")
            print(self._message)
            errortup = (f"'error_in_function'={__name__}", f"'error_count'={self.error_count}",
                        f"'error_message'={self._message}", f"'error'={self.error}",)
            self.info_error_list.append(errortup)
            raise FileNotFoundError

    def coded_input(self):
        """ Try a hard-coded filepath and turn a pdf into a dictionary, if the filepath doesn't exist then
         try web scraping with auto_input() """
        try:
            if self.file_path != None:
                 with open(self.file_path, 'rb') as self.file_Obj:
                    self.pdfworker(self.file_Obj)
            return self.pdfpagedict
        except Exception as error:
            self.error = error
            print(f"Current error = {self.error}")
            self.error_count += 1
            self._message = f"Tried coded_input() without success, errors with the document filepath."
            logging.info(self._message)
            errortup = (f"'error_in_function'={__name__}", f"'error_count'={self.error_count}",
                        f"'error_message'={self._message}", f"'error'={self.error}",)
            self.info_error_list.append(errortup)
            raise FileExistsError

    def manual_input(self):
        try:
            self.timer(delay=10, what_to_check=self.file_path)
            Thread(target = self.timer).start()
            self.file_path = str(input("Enter a filepath to the pdf you would like to use: "))
            self.file_name = self.file_path.split("/")[-1]
        except Exception as error:
            self.error = str(error)
            print(f"Current error = {self.error}")
            self.error_count += 1
            self._message = f"Tried manual_input() without success, errors with the document filepath."
            errortup = (f"'error_in_function'={__name__}", f"'error_count'={self.error_count}",
                        f"'error_message'={self._message}", f"'error'={self.error}",)
            self.info_error_list.append(errortup)
            raise LookupError

    def three_inputs(self):
        try:
            self.auto_input()
        except FileNotFoundError:
            try:
                self.coded_input()
            except FileExistsError:
                try:
                    self.manual_input()
                except LookupError:
                    print("Tried auto_input(), coded_input() & manual_input() without success")
                    exit(1)

class LogFormatter(logging.Formatter, PDF_Document):
    """ Basic system log message generator to identify significant events and errors for troubleshooting """
    def __init__(self):
        self.start_time = datetime.datetime.today()
        super().__init__()
        handler = logging.handlers.SysLogHandler()
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
    doc_obj.three_inputs()
    # Final log messages for recording completion and problems
    log_obj.log_message_end(doc_obj)
    if doc_obj.error_count > 0:
        log_obj.log_message_errorsum(doc_obj.error_count)
    exit(doc_obj.error_count)


# Call the main function
if __name__ == "__main__":
    main()
