from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/jquery.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('jquery.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/jquery.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            with open('jquery.js', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

httpd = HTTPServer(('localhost', 8000), MyHandler)
print('Server listening on localhost:8000...')
httpd.serve_forever()
