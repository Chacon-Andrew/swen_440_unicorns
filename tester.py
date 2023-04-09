import http.server
import socketserver
import requests
import time
import socket
import mimetypes
from ftplib import FTP

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

def test_performance():

    with FTP("seappserver2.rit.edu") as ftp:
        # Upload a file to the Document Repository and record the time of the process
        start_time = time.time()
        ftp.login("ftp_w006", "ftp_w006_password")
        with open('Application_L_Page_001.png', 'rb') as f:
            ftp.storbinary('STOR Application_L_Page_001.png', f)
        upload_time = time.time() - start_time
        print(f'File upload time: {upload_time:.2f}s')

        # Use the OCR Service to extract text from the uploaded file and record the time of the process
        start_time = time.time()
        response = requests.post('https://seappserver2.rit.edu/api/ProcessFile?ocrlib=std', files={'file': open('Application_L_Page_001.png', 'rb')})
        if response.status_code == 200:
            with open('Application_L_Page_001.txt', 'wb') as f:
                f.write(response.content)
        ocr_time = time.time() - start_time
        print(f'OCR time: {ocr_time:.2f}s')

        # Use the Parser Service to extract keywords from the text file and record the time of the process
        start_time = time.time()
        response = requests.post('https://seappserver2.rit.edu/api/ExtractKeywords', files={'file': open('Application_L_Page_001.txt', 'rb')})
        if response.status_code == 200:
            print(response.json()) #This can be commented out if need be
        parser_time = time.time() - start_time
        print(f'Parser time: {parser_time:.2f}s')

def test_interoperability():
    with FTP("seappserver2.rit.edu") as ftp:
        ftp.login("ftp_w006", "ftp_w006_password")
        conn = socket.create_connection(("seappserver2.rit.edu", 80))
        response = requests.get("https://seappserver2.rit.edu/DMService/api/ListFiles")
        print(response)
        #print(str(response.content, 'utf-8'))
        response2 = requests.get("https://seappserver2.rit.edu/DMService/api/DownloadFile?fileName=Application_L_Page_002.png")
        print(response2)
        form_data = {'fileName': open('swen_440_unicorns/Application_L_Page_002.png', 'rb')}
        response3 = requests.post("http://seappserver2.rit.edu/OCRService/api/ProcessFile?ocrLib=std", files=form_data)
        print(response3)
        print(response3.content)
        form_data_2 = {'fileName': open("file.txt", 'wb').write(response3.content)}
        response4 = requests.post("http://seappserver2.rit.edu/parserservice/api/ReadForm", files=form_data_2)
        print(response4)
        print(response4.content)


def test_utilization():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

def main():
    #start = time.time()
    test_performance()
    test_interoperability()
    #end = time.time()


if __name__=="__main__":
    main()