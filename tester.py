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
    response_API = requests.post('https://seappserver2.rit.edu/api/ProcessFile?ocrlib={std}')
    print(response_API.status_code)

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
    start = time.time()
    test_interoperability()
    end = time.time()
    print(end - start)

if __name__=="__main__":
    main()