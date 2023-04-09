import http.server
import os
import socketserver
import requests
import time
import socket
import json
import mimetypes
from ftplib import FTP
from email.mime.image import MIMEImage

# TODO: To quickly remove all the comment (#), use the key combination Ctrl + / or Command + / for Mac
# PORT = 8000
#
# Handler = http.server.SimpleHTTPRequestHandler
#
# def test_performance():
#
#     with FTP("seappserver2.rit.edu") as ftp:
#         conn = socket.create_connection(("seappserver2.rit.edu", 80))
#         # Upload a file to the Document Repository and record the time of the process
#         start_time = time.time()
#         ftp.login("ftp_w006", "ftp_w006_password")
#         with open('swen_440_unicorns/Application_L_Page_001.png', 'rb') as f:
#             ftp.storbinary('STOR Application_L_Page_001.png', f)
#         upload_time = time.time() - start_time
#         print(f'File upload time: {upload_time:.2f}s')
#
#         # Use the OCR Service to extract text from the uploaded file and record the time of the process
#         start_time = time.time()
#         response = requests.post('http://seappserver2.rit.edu/OCRService/api/ProcessFile?ocrLib=std', files={'file': open('swen_440_unicorns/Application_L_Page_001.png', 'rb')})
#         if response.status_code == 200:
#             with open('swen_440_unicorns/Application_L_Page_001.png', 'wb') as f:
#                 f.write(response.content)
#         ocr_time = time.time() - start_time
#         print(f'OCR time: {ocr_time:.2f}s')
#
#         # Use the Parser Service to extract keywords from the text file and record the time of the process
#         start_time = time.time()
#         response = requests.post('http://seappserver2.rit.edu/parserservice/api/ReadForm', files={'file': open('swen_440_unicorns/Application_L_Page_001.png', 'rb')})
#         #if response.status_code == 200:
#             #print(response.json()) #This can be commented out if need be
#         parser_time = time.time() - start_time
#         print(f'Parser time: {parser_time:.2f}s')
#
# def test_interoperability():
#     with FTP("seappserver2.rit.edu") as ftp:
#         ftp.login("ftp_w006", "ftp_w006_password")
#         conn = socket.create_connection(("seappserver2.rit.edu", 80))
#         response = requests.get("https://seappserver2.rit.edu/DMService/api/ListFiles")
#         print(response)
#         #print(str(response.content, 'utf-8'))
#         response2 = requests.get("https://seappserver2.rit.edu/DMService/api/DownloadFile?fileName=Application_L_Page_002.png")
#         print(response2)
#         form_data = {'fileName': open('swen_440_unicorns/Application_L_Page_002.png', 'rb')}
#         response3 = requests.post("http://seappserver2.rit.edu/OCRService/api/ProcessFile?ocrLib=std", files=form_data)
#         print(response3)
#         print(response3.content)
#         form_data_2 = {'fileName': open("file.txt", 'wb').write(response3.content)}
#         response4 = requests.post("http://seappserver2.rit.edu/parserservice/api/ReadForm", files=form_data_2)
#         print(response4)
#         print(response4.content)
#
#
# def test_utilization():
#     with socketserver.TCPServer(("", PORT), Handler) as httpd:
#         print("Serving at port", PORT)
#         httpd.serve_forever()


def test_connection():
    response = requests.get('http://seappserver2.rit.edu/DMService/api/ListFiles')
    for result in response.json():
        print(result["fileName"])


def process_file():
    # Define the URL for the ProcessFile endpoint
    url = 'http://seappserver1.rit.edu/OCRService/api/ProcessFile?ocrLib=std'

    # Define the path to the image file
    file_path = 'Application_L_Page_004.png'

    # Open the image file in binary read mode
    with open(file_path, 'rb') as image_file:
        # Create a dictionary of data to include in the request
        data = {
            'image': (file_path, image_file.read(), 'image/png')
        }

        # Send the POST request to the API endpoint
        response = requests.post(url, files=data)

    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON string into a Python dictionary
        with open('Application_L_Page_004_WRONG.txt', 'w') as f:
            f.write(response.text)
        data = json.loads(response.text)

        # Extract the value associated with the _text key
        text = data['_text']

        # Write the text to a file
        with open('Application_L_Page_004_CORRECT.txt', 'w') as f:
            f.write(text)
    else:
        print('Error:', response.status_code)


def parse():
    # Define the URL for the ParserService endpoint
    url = 'http://seappserver2.rit.edu/ParserService/api/ReadForm'

    # Define the path to the text file
    file_path = 'Application_L_Page_004_CORRECT.txt'

    # Include the key file in the dictionary
    files = {'file': open(file_path, 'rb')}

    # Send the POST request to the API endpoint
    response = requests.post(url, files=files)

    # Check the response status code
    if response.status_code == 200:
        print(response.text)
    else:
        print('Error:', response.status_code)

def main():
    # start = time.time()
    # test_performance()
    # test_interoperability()
    # test_interoperability()
    # end = time.time()
    test_connection()
    process_file()
    parse()


if __name__=="__main__":
    main()