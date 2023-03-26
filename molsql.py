import os;
import sqlite3;
import MolDisplay;

class Database:
    def __init__(self, reset=False): 
        if reset:
            try:
                os.remove("molecules.db")
            except FileNotFoundError:
                pass
        self.conn = sqlite3.connect("molecules.db")

    def create_tables( self ):
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Elements
                 ( ELEMENT_NO     INTEGER NOT NULL,
                   ELEMENT_CODE   VARCHAR(3) NOT NULL,
                   ELEMENT_NAME   VARCHAR(32) NOT NULL,
                   COLOUR1        CHAR(6) NOT NULL,
                   COLOUR2        CHAR(6) NOT NULL,
                   COLOUR3        CHAR(6) NOT NULL,
                   RADIUS         DECIMAL(3) NOT NULL,
                   PRIMARY KEY (ELEMENT_CODE) );""" )

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Atoms
                 ( ATOM_ID       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   ELEMENT_CODE  VARCHAR(3) NOT NULL,
                   X             DECIMAL(7,4) NOT NULL,
                   Y             DECIMAL(7,4) NOT NULL,
                   Z             DECIMAL(7,4) NOT NULL,
                   FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements);""")

        self.conn.execute( """CREATE TABLE IF NOT EXISTS Bonds
                 ( BOND_ID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   A1           INTEGER NOT NULL,
                   A2           INTEGER NOT NULL,
                   EPAIRS       INTEGER NOT NULL);""")
        
        self.conn.execute( """CREATE TABLE IF NOT EXISTS Molecules
                 ( MOLECULE_ID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   NAME         TEXT UNIQUE NOT NULL);""")
        
        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeAtom
                 ( MOLECULE_ID  INTEGER NOT NULL,
                   ATOM_ID      INTEGER NOT NULL,
                   PRIMARY KEY(MOLECULE_ID, ATOM_ID),
                   FOREIGN KEY(MOLECULE_ID) REFERENCES Molecules,
                   FOREIGN KEY(ATOM_ID) REFERENCES Atoms );""")

        self.conn.execute( """CREATE TABLE IF NOT EXISTS MoleculeBond
                 ( MOLECULE_ID  INTEGER NOT NULL,
                   BOND_ID      INTEGER NOT NULL,
                   PRIMARY KEY(MOLECULE_ID, BOND_ID),
                   FOREIGN KEY(MOLECULE_ID) REFERENCES Molecules,
                   FOREIGN KEY(BOND_ID) REFERENCES Bonds );""")

        self.conn.commit()
                

    def __setitem__(self, table, values):
        placeholders = ", ".join(["?"] * len(values))
        query = f"INSERT OR IGNORE INTO {table} VALUES ({placeholders})"
        self.conn.execute(query, values)
        self.conn.commit()

    def add_atom(self, molname, atom):
        # Insert the atom attributes into the Atoms table
        self.conn.execute("""
            INSERT OR IGNORE INTO Atoms (ELEMENT_CODE, X, Y, Z) 
                VALUES (?, ?, ?, ?)""", 
                (atom.element, atom.x, atom.y, atom.z)
        )
        
        # Get the ID of the newly inserted atom
        atom_id = self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Insert the molecule-atom relationship into the MoleculeAtom table
        self.conn.execute("""
            INSERT OR IGNORE INTO MoleculeAtom (MOLECULE_ID, ATOM_ID) 
                VALUES ((SELECT MOLECULE_ID FROM Molecules WHERE NAME=?), ?)""",
                (molname, atom_id)
        )
        
        # Commit the changes
        self.conn.commit()

    def add_bond(self, molname, bond):
        # Insert the atom attributes into the Bonds table
        self.conn.execute("""
            INSERT OR IGNORE INTO Bonds (A1, A2, EPAIRS) 
                VALUES (?, ?, ?)""", 
                (bond.a1, bond.a2, bond.epairs) 
        )
        
        # Get the ID of the newly inserted bond
        bond_id = self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Insert the molecule-bond relationship into the MoleculeBonds table
        self.conn.execute("""
            INSERT OR IGNORE INTO MoleculeBond (MOLECULE_ID, BOND_ID) 
                VALUES ((SELECT MOLECULE_ID FROM Molecules WHERE NAME=?), ?)""",
                (molname, bond_id)
        )
        
        # Commit the changes
        self.conn.commit()

    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule()
        mol.parse(fp)

        # Insert the molecule name into the Molecules table
        self.conn.execute("""
            INSERT OR IGNORE
            INTO Molecules (NAME) 
            VALUES (?)""",
            (name,)
        )

        # Get the ID of the newly inserted molecule
        mol_id = self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        #Add all atoms to the database
        for i in range (mol.mol.atom_no):
            self.add_atom(name, mol.mol.get_atom(i))

        # Add all bonds to the database
        for i in range (mol.mol.bond_no):
            self.add_bond(name, mol.mol.get_bond(i))
            
        # Commit the changes
        self.conn.commit()
    
    def load_mol( self, name ):
        mol = MolDisplay.Molecule()
        # Retrieve the molecule ID for the given name
        mol_id = self.conn.execute("""
            SELECT MOLECULE_ID FROM Molecules
            WHERE NAME = ?""",
            (name,)
        ).fetchone()

        if mol_id is None:
            # If the molecule doesn't exist, return None
            return None

        # Retrieve all the atoms associated with the molecule
        atoms = self.conn.execute("""
            SELECT * FROM Atoms
            JOIN MoleculeAtom ON Atoms.ATOM_ID = MoleculeAtom.ATOM_ID
            WHERE MoleculeAtom.MOLECULE_ID = ?
            ORDER BY Atoms.ATOM_ID ASC""",
            mol_id
        ).fetchall()
        
        # Append each atom to the Molecule object in order of increasing ATOM_ID
        for atom in atoms:
            elem_code = atom[1]
            x, y, z = atom[2], atom[3], atom[4]
            mol.append_atom(elem_code, x, y, z)

        # Retrieve all the bonds associated with the molecule
        bonds = self.conn.execute("""
            SELECT * FROM Bonds
            JOIN MoleculeBond ON Bonds.BOND_ID = MoleculeBond.BOND_ID
            WHERE MoleculeBond.MOLECULE_ID = ?
            ORDER BY Bonds.BOND_ID ASC""",
            mol_id
        ).fetchall()

        # Append each bond to the Molecule object in order of increasing BOND_ID
        for bond in bonds:
            a1 = bond[1]
            a2 = bond[2]
            epairs = bond[3]
            mol.append_bond(a1, a2, epairs)
        
        return mol

    def radius(self):
        results = self.conn.execute("SELECT ELEMENT_CODE, RADIUS FROM Elements").fetchall()
        return {element_code: radius for element_code, radius in results}

    def element_name( self ):
        results = self.conn.execute("SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements").fetchall()
        return {element_code: name for element_code, name in results}

    def radial_gradients(self):
        # Retrieve the required data from the Elements table
        data = self.conn.execute("SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements")

        # Generate the radial gradients string
        radial_gradient_svg = ""
        for row in data:
            element_name = row[0].replace(" ", "")
            colour1 = row[1]
            colour2 = row[2]
            colour3 = row[3]
            radial_gradient_svg += f"""
            <radialGradient id="{element_name}" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
            <stop offset="0%" stop-color="#{colour1}"/>
            <stop offset="50%" stop-color="#{colour2}"/>
            <stop offset="100%" stop-color="#{colour3}"/>
            </radialGradient>"""
        return radial_gradient_svg

