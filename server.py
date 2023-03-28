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
    file_paths = {
        '/home.html': ('text/html', 'home.html'),
        '/jquery.js': ('application/javascript', 'jquery.js'),
        '/styles.css': ('text/css', 'styles.css'),
        '/elementForm.html': ('text/html', 'elementForm.html'),
        '/uploadSdf.html': ('text/html', 'uploadSdf.html'),

        '/template/home.html': ('text/html', 'template/home.html'),
        '/template/modifyElements.html': ('text/html', 'template/modifyElements.html'),
        '/template/uploadSDF.html': ('text/html', 'template/uploadSDF.html'),

        '/template/css/all.min.css': ('text/css', 'template/css/all.min.css'),
        '/template/css/bootstrap.min.css': ('text/css', 'template/css/bootstrap.min.css'),
        '/template/css/templatemo-new-vision.css': ('text/css', 'template/css/templatemo-new-vision.css'),
        '/template/slick/slick-theme.css': ('text/css', 'template/slick/slick-theme.css'),
        '/template/slick/slick.css': ('text/css', 'template/slick/slick.css'),

        '/template/slick/slick.min.js': ('application/javascript', 'template/slick/slick.min.js'),
        '/template/js/bootstrap.min.js': ('application/javascript', 'template/js/bootstrap.min.js'),
        '/template/js/jquery-3.4.1.min.js': ('application/javascript', 'template/js/jquery-3.4.1.min.js'),
        '/template/js/templatemo-script.js': ('application/javascript', 'template/js/templatemo-script.js'),

        '/template/img/home_background2.jpg': ('image/jpeg', 'template//img/home_background2.jpg'),
        '/template/img/modifyElementImage.jpg': ('image/jpeg', 'template//img/modifyElementImage.jpg'),
        '/template/img/home_background.jpg': ('image/jpeg', 'template//img/home_background.jpg'),
        '/template/img/203183.png': ('image/png', 'template/img/203183.png'),
        '/template/img/68084.png': ('image/png', 'template/img/68084.png'),
        '/template/img/126477.png': ('image/png', 'template/img/126477.png'),
        '/template/img/4084223-200.png': ('image/png', 'template/img/4084223-200.png'),
        '/template/img/4649486-200.png': ('image/png', 'template/img/4649486-200.png')

    }

    def do_GET(self):
        if self.path in self.file_paths:
            content_type, filename = self.file_paths[self.path]
            try:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                with open(filename, 'rb') as f:
                    self.wfile.write(f.read())
            except IOError:
                self.send_error(500, 'Internal Server Error - Cannot open file')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('<script>alert("Cannot open file");</script>'.encode('utf-8'))
        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );

    def do_POST(self):
        if self.path == "/template/addelement":
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
            self.wfile.write(bytes("<h3>Success</h3>", "utf-8"))

        elif self.path == "/template/removeelement":
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
            self.send_header("Content-type", "text/html")
            self.end_headers()
            success_message = "<html><body><h1>Success!</h1><a href='/template/modifyElements.html'>Back</a></body></html>"
            self.wfile.write(success_message.encode())



        elif self.path == "/template/molecule":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            fp = body.decode()
            split_string = fp.split('\n')
            new_string = '\n'.join(split_string[4:])

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
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            # self.wfile.write(bytes("uploaded successfully", "utf-8"))
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