from io import StringIO
import sys;
import MolDisplay
import molsql
import re
import cgi
import os;
import sqlite3;
from urllib.parse import parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler;

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        if self.path == '/home.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('home.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/jquery.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            with open('jquery.js', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/styles.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('styles.css', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/elementForm.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('elementForm.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/uploadSdf.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('uploadSdf.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );

    def do_POST(self):
        if self.path == "/addelement":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            print("body")
            print(body)
            data = parse_qs(body.decode())
            element_number = data['element_number'][0]
            element_name = data['element_name'][0]
            element_code = data['element_code'][0]
            color1 = data['color1'][0]
            color2 = data['color2'][0]
            color3 = data['color3'][0]
            radius = data['radius'][0]

            db = molsql.Database(reset=False)
            db.create_tables(); 
            db['Elements'] = ( element_number, element_code, element_name, color1, color2, color3, radius ) #may need to remove the hastag from colour vars 
            # Do something with the form data
            # ...

            # Send a response back to the client
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Form data received", "utf-8"))

        elif self.path == "/removeelement":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = parse_qs(body.decode())
            element_number = data['element_number'][0]

            db = molsql.Database(reset=False)
            db.create_tables(); 
            cursor = db.conn.cursor()

            # Deleting single record now
            cursor.execute('''SELECT * from Elements''')
            cursor.execute(f'''DELETE FROM Elements WHERE ELEMENT_NO = {element_number}''')
            db.conn.commit()        
            db.conn.close()

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Element removed successfully", "utf-8"))

        elif self.path == "/molecule":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            fp = body.decode()
            split_string = fp.split('\n')
            print(split_string)
            new_string = '\n'.join(split_string[4:])
            self.send_response(200)
            self.send_header("Content-type", "image/svg+xml")
            self.end_headers()

            db = molsql.Database(reset=False)
            db.create_tables(); 

            db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 ) 
            db['Elements'] = ( 6, 'C', 'Carbon',   '808080', '010101', '000000', 40 ) 
            db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 ) 
            db['Elements'] = ( 8, 'O', 'Oxygen',   'FF0000', '050000', '020000', 40 )
            
            filename_pattern = r'filename="([\w\s]+)\.\w+"'
            filename_match = re.search(filename_pattern, str(split_string))

            if filename_match:
                filename = filename_match.group(1)
                print(filename)
            # mol = MolDisplay.Molecule()
            # mol.parse(StringIO(new_string))
            # mol.sort()
            # svg_string = mol.svg()
            # self.wfile.write(svg_string.encode())
            # fp=open("mol_files/water.sdf")   
            db.add_molecule( filename, StringIO(new_string))
            mol = db.load_mol( filename )
            mol.sort()
            svg_string = mol.svg()
            self.wfile.write(bytes(filename + " uploaded successfully", "utf-8"))
            # self.wfile.write(svg_string.encode())
        else:
            self.send_error(404, "File not founddd")




home_page = """
<html>
  <head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
    <script src="jquery.js"></script>
  </head>
  <body>
    <p id="p1"> paragraph 1 </p>
    <p id="p2"> hidden paragraph </p>
    <p id="p3"> paragraph 3 </p>
    <button id="b1"> Click me </button>
    <button id="b2"> Fade </button>
    <br/>
    <button id="b3" style="position:absolute;"> Annoying button </button>
    <br/>
    <input type="text" id="element_number" />
    <button id="b4"> Alert(name) </button>
    <button id="b5"> set name </button>
  </body>
</html>
"""


port = int(sys.argv[1])

if __name__ == '__main__':
    if len(sys.argv) < 2:
            print("Usage: python server.py <port>")
            sys.exit(1)
    try:
        server = HTTPServer(('localhost', port), MyHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C received, shutting down the web server")
        server.socket.close()