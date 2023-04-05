import http.server
import socketserver
import requests
import time

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

def test_performance():
    response_API = requests.post('https://seappserver2.rit.edu/api/ProcessFile?ocrlib=std')
    print(response_API.status_code)

def test_interoperability():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

def test_utilization():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

def main():
    start = time.time()
    test_performance()
    end = time.time()
    print(end - start)

if __name__=="__main__":
    main()