from io import StringIO
import sys;
import MolDisplay
import time
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
        
        '/template/about.html': ('text/html', 'template/about.html'),
        '/template/home.html': ('text/html', 'template/home.html'),
        # '/template/modifyElements.html': ('text/html', 'template/modifyElements.html'),
        '/template/uploadSDF.html': ('text/html', 'template/uploadSDF.html'),
        # '/template/viewMolecules.html': ('text/html', 'template/viewMolecules.html'),

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
        '/template/img/4649486-200.png': ('image/png', 'template/img/4649486-200.png'),
        '/template/img/molecule2.jpg': ('image/jpg', 'template/img/molecule2.jpg'),
        '/template/img/Xm19kO.jpg': ('image/jpg', 'template/img/Xm19kO.jpg'),
        '/template/img/elementpic1.jpg': ('image/jpg', 'template/img/elementpic1.jpg'),
        '/template/img/molpic4.jpg': ('image/jpg', 'template/img/molpic4.jpg'),
        '/template/img/molpic5.jpg': ('image/jpg', 'template/img/molpic5.jpg'),
        '/template/img/water.png': ('image/png', 'template/img/water.png'),
        '/template/img/caffeine.png': ('image/png', 'template/img/caffeine.png'),
        '/template/img/cortisol.png': ('image/png', 'template/img/cortisol.png'),
        '/template/img/creatine.png': ('image/png', 'template/img/creatine.png')

    }

    def do_GET(self):
        if self.path == "/template/viewMolecules.html":
            # Connect to the database
            db = molsql.Database(reset=False)
            db.create_tables()
            cursor = db.conn.cursor()
            cursor2 = db.conn.cursor()

            # Query the database for the data
            cursor.execute("SELECT * FROM Molecules")
            rows = cursor.fetchall()


            # Generate the HTML table with the data
            table_rows = ""
            for row in rows:
                print(row[0])
                print(row[1])
                # molID = cursor.execute("""SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?""", (row[1],))
                # print(molID)
                # data = cursor2.fetchall()
                # print(data)
                # Get the number of atoms in the molecule
                num_atoms_query = f"SELECT COUNT(*) FROM MoleculeAtom WHERE MOLECULE_ID={row[0]}"
                num_atoms = cursor.execute(num_atoms_query).fetchone()[0]
                num_bonds_query = f"SELECT COUNT(*) FROM MoleculeBond WHERE MOLECULE_ID={row[0]}"
                num_bonds = cursor.execute(num_bonds_query).fetchone()[0]
                # Generate the table row with the atom count
                table_rows += f"<tr><td>{row[0]}</td><td><button onclick='showSvg(\"{row[1]}\"); document.getElementById(\"selected-element\").textContent = \"{row[1]}\"; document.getElementById(\"rotate-form\").style.display = \"block\";'>{row[1]}</button></td><td>{num_atoms}</td><td>{num_bonds}</td></tr>"
            with open("template/viewMolecules.html", "r") as f:
                html = f.read()
            html = html.replace("<!-- This is where you will populate the table with data from the database -->", table_rows)

            # Send the response back to the client
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path.startswith("/getMoleculeSVG"):
            # Get the name of the molecule from the request URL
            svg_name = self.path.split("/")[-1]
            # Get the SVG data from the database
            db = molsql.Database(reset=False)
            mol = db.load_mol( svg_name )
            mol.sort()
            fp = open( "template/svgs/" + svg_name + ".svg", "w" );
            string = mol.svg()
            print(string)
            fp.write( mol.svg());
            # Send the SVG data back to the client
            self.send_response(200)
            self.send_header("Content-type", "image/svg+xml")
            self.end_headers()
            self.wfile.write(bytes(string, "utf-8"))

            # self.wfile.write(string.encode())
            fp.close();
        elif self.path.startswith("/getMoleculeRotatedSVG"):
            print("HERE1")
            # Get the name of the molecule from the request URL
            svg_name = self.path.split("/")[-1]
            print(svg_name)
            # Get the SVG data from the database
            # db = molsql.Database(reset=False)
            # mol = db.load_mol( svg_name )
            # mol.sort()
            # fp = open( "template/svgs/temp.svg", "w" );
            # string = mol.svg()
            # print(string)
            # fp.write( mol.svg());
            # Send the SVG data back to the client
            fp = open("template/svgs/" + svg_name +"_rotated.svg", "r")
            content = fp.read()
            fp.close()
            # Send the SVG data back to the client
            self.send_response(200)
            self.send_header("Content-type", "image/svg+xml")
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))

            # self.wfile.write(string.encode())
            fp.close();
        elif self.path == "/template/modifyElements.html":
            print("HEELLOOO")
            # Connect to the database
            db = molsql.Database(reset=False)
            db.create_tables()
            cursor = db.conn.cursor()

            # Query the database for the data
            cursor.execute("SELECT * FROM Elements")
            rows = cursor.fetchall()

            # Generate the HTML table with the data
            table_rows = ""
            for row in rows:
                table_rows += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>"
            # Replace the placeholder in the HTML file with the generated table rows
            with open("template/modifyElements.html", "r") as f:
                html = f.read()
            html = html.replace("<!-- This is where you will populate the table with data from the database -->", table_rows)

            # Send the response back to the client
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path in self.file_paths:
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
        if self.path == "/template/rotate":
            print("HERE2")

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = parse_qs(body.decode())
            print(data)

            x = data['xVal'][0]
            y = data['yVal'][0]
            z = data['zVal'][0]
            element_name = data['element'][0]

            # Print the values for testing
            print("Element Name: ", element_name)
            print("X: ", x)
            print("Y: ", y)
            print("Z: ", z)

            db = molsql.Database(reset=False)
            mol = db.load_mol( element_name )
            mol.sort()
            mol.rotateX(float(x))
            mol.rotateY(float(y))
            mol.rotateZ(float(z))
            fp = open( "template/svgs/" + element_name + "_rotated.svg", "w" );
            string = mol.svg()
            fp.write( mol.svg());
            
            db.conn.commit()
            db.conn.close()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            success_message = "<html><body><h1>Success!</h1><a href='/template/modifyElements.html'>Back</a></body></html>" 
            self.wfile.write(success_message.encode())
        if self.path == "/template/addelement":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            print("body")
            print(body)
            data = parse_qs(body.decode())
            
            element_number = data['element_number'][0]
            element_name = data['element_name'][0]
            element_code = data['element_code'][0]
            color1 = data['color1'][0][1:]
            color2 = data['color2'][0][1:]
            color3 = data['color3'][0][1:]
            radius = data['radius'][0]

            db = molsql.Database(reset=False)
            db.create_tables(); 
            cursor = db.conn.cursor()
            
            cursor.execute(f'''SELECT * FROM Elements WHERE ELEMENT_NO = {element_number}''')
            number_exists = cursor.fetchone()
            cursor.execute("SELECT * FROM Elements WHERE ELEMENT_NAME = ?", (element_name,))
            name_exists = cursor.fetchone()
            cursor.execute("SELECT * FROM Elements WHERE ELEMENT_CODE = ?", (element_code,))
            code_exists = cursor.fetchone()

            if number_exists or name_exists or code_exists:
                 # If element_number already exist, send error response
                db.conn.close()
                print(f"Element with number {element_number} already exists .")
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                error_message = "<html><body><h1>Error!</h1><a href='/template/modifyElements.html'>Back</a></body></html>" 
                self.wfile.write(error_message.encode())
            else:
                db['Elements'] = ( element_number, element_code, element_name, color1, color2, color3, radius ) #may need to remove the hastag from colour vars 
                db.conn.commit()
                db.conn.close()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                success_message = "<html><body><h1>Success!</h1><a href='/template/modifyElements.html'>Back</a></body></html>" 
                self.wfile.write(success_message.encode())
            # # Send a response back to the client
            # self.send_response(200)
            # self.send_header("Content-type", "text/plain")
            # self.end_headers()
            # self.wfile.write(bytes("<h3>Success</h3>", "utf-8"))

        elif self.path == "/template/removeelement":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = parse_qs(body.decode())
            element_number = data['element_number'][0]

            db = molsql.Database(reset=False)
            db.create_tables(); 
            cursor = db.conn.cursor()

            # Deleting single record now
            cursor.execute("SELECT * FROM Elements WHERE ELEMENT_NO = ?", (element_number,))
            result = cursor.fetchone()
            if result:
                # If element_number exists, delete the record and send success response
                cursor.execute(f'''DELETE FROM Elements WHERE ELEMENT_NO = {element_number}''')
                db.conn.commit()
                db.conn.close()
                print(f"Element with number {element_number} deleted successfully.")
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                success_message = "<html><body><h1>Success!</h1><a href='/template/modifyElements.html'>Back</a></body></html>" 
                self.wfile.write(success_message.encode())
            else:
                # If element_number doesn't exist, send error response
                db.conn.close()
                print(f"Element with number {element_number} does not exist.")
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                error_message = "<html><body><h1>Error!</h1><a href='/template/modifyElements.html'>Back</a></body></html>" 
                self.wfile.write(error_message.encode())
        elif self.path == "/template/molecule":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            fp = body.decode()
            split_string = fp.split('\n')
            new_string = '\n'.join(split_string[4:])

            db = molsql.Database(reset=False)
            db.create_tables(); 
            # db.element_name()
            # create a cursor object
            cursor = db.conn.cursor()

            # execute the SELECT statement
            cursor.execute("SELECT ELEMENT_CODE FROM Elements")

            # fetch all the results
            results = cursor.fetchall()

            print("element_code from elements table:")
            # print the element names
            for result in results:
                print(result[0])

            # # close the cursor and database connections
            # cursor.close()

            #remove this before submitting
            # db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 ) 
            # db['Elements'] = ( 6, 'C', 'Carbon',   '808080', '010101', '000000', 40 ) 
            # db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 ) 
            # db['Elements'] = ( 8, 'O', 'Oxygen',   'FF0000', '050000', '020000', 40 )
            
            filename_pattern = r'filename="([\w\s]+)\.\w+"'
            filename_match = re.search(filename_pattern, str(split_string))
            # filename = ""
            if filename_match:
                filename = filename_match.group(1)
                print(filename)
            # mol = MolDisplay.Molecule()
            # mol.parse(StringIO(new_string))
            # mol.sort()
            # svg_string = mol.svg()
            # self.wfile.write(svg_string.encode())
            # fp=open("mol_files/water.sdf")

            # cursor.execute('''SELECT NAME from Molecules WHERE NAME=?''', (filename,))
            # exists = cursor.fetchall() 
            # if not exists:
            # db.helper(filename)
            # db.add_molecule(filename, StringIO(new_string))
            # mol = db.load_mol( filename )
            # mol.sort()
            # svg_string = mol.svg()
            # self.send_response(200)
            # self.send_header("Content-type", "text/plain")
            # self.end_headers()
            # self.wfile.write(svg_string.encode())

            try:
                db.add_molecule(filename, StringIO(new_string))
                mol = db.load_mol( filename )
                mol.sort()
                svg_string = mol.svg()
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
            except (AttributeError, IOError, KeyError, ValueError) as e:
                print("error:", e)
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                db.delete_molecule(filename)
                # cursor.execute("DELETE FROM Molecules WHERE MOLECULE_ID = (SELECT MAX(MOLECULE_ID) FROM Molecules)")
                db.conn.commit()
                # return

            # db.helper(filename)

            # mol = db.load_mol( filename )
            # mol.sort()
            # svg_string = mol.svg()
            # self.send_response(200)
            # self.send_header("Content-type", "text/plain")
            # self.end_headers()


            # else:
            #     self.send_response(404)
            #     self.send_header("Content-type", "text/plain")
            #     self.end_headers()
            self.wfile.write(bytes("uploaded successfully", "utf-8"))
            # self.wfile.write(svg_string.encode())
        elif self.path == "template/viewMolecules":
            print("HELLO")
            db = molsql.Database(reset=False)
            db.create_tables(); 
            cursor = conn.execute('PRAGMA table_info(Molecules)')
            for row in cursor.fetchall():
                print(row)

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