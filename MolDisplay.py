# import molecule;
# import os

# radius = { 
#     'H': 25,
#     'C': 40,
#     'O': 40,
#     'N': 40,
# }

# element_name = { 
#     'H': 'grey',
#     'C': 'black',
#     'O': 'red',
#     'N': 'blue',
# }

# header = """<svg version="1.1" width="1000" height="1000" 
#                     xmlns="http://www.w3.org/2000/svg">"""

# footer = """</svg>"""

# offsetx = 500
# offsety = 500


# class Atom:
#     def __init__(self, c_atom):
#         self.c_atom = c_atom
#         self.c_atom.z = c_atom.z

#     def svg(self):
#         cx = (self.c_atom.x * 100.0) + offsetx
#         cy = (self.c_atom.y * 100.0) + offsety
#         r = radius[self.c_atom.element]
#         fill = element_name[self.c_atom.element]    
#         var = (' <circle cx="%.2f" cy="%.2f" r="%d" fill="%s"/>\n' % (cx, cy, r, fill))
#         return var

#     def __str__(self):
#         return self.svg()
    


# class Bond:
#     def __init__(self, c_bond):
#         self.c_bond = c_bond
#         self.c_bond.z = c_bond.z

#     def svg(self):
#         p1x = offsetx + ((100*self.c_bond.x1) - (10*self.c_bond.dy))
#         p1y = offsety + ((100*self.c_bond.y1) + (10*self.c_bond.dx))

#         p2x = offsetx + ((100*self.c_bond.x1) + (10*self.c_bond.dy))
#         p2y = offsety + ((100*self.c_bond.y1) - (10*self.c_bond.dx)) 

#         p3x = offsetx + ((100*self.c_bond.x2) - (10*self.c_bond.dy))
#         p3y = offsety + ((100*self.c_bond.y2) + (10*self.c_bond.dx))
        
#         p4x = offsetx + ((100*self.c_bond.x2) + (10*self.c_bond.dy))
#         p4y = offsety + ((100*self.c_bond.y2) - (10*self.c_bond.dx))
#         var1 = (' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (p2x, p2y, p1x, p1y, p3x, p3y, p4x, p4y))
#         return var1

#     def __str__(self):
#         return self.svg()


# class Molecule(molecule.molecule):

#     def svg(self):
#         # Sort atoms and bonds by increasing z value
#         return_string = header

#         self.mol.sort()

#         atom_counter = self.mol.atom_no
#         bond_counter = self.mol.bond_no
#         count_atom = 0
#         count_bond = 0

#         while(count_atom != atom_counter):
#             atoms = Atom(self.mol.get_atom(count_atom))
#             bonds = Bond(self.mol.get_bond(count_bond))
#             if(self.mol.get_atom(count_atom).z < self.mol.get_bond(count_bond).z):
#                 return_string += str(atoms)
#                 count_atom +=1
#                 if(count_atom == atom_counter):
#                     for i in range(count_bond, bond_counter):
#                         bonds = Bonds(self.mol.get_bonds(i))
#                         return_string += str(bonds)
#                         count_atom +=1
#                     break
#             else:
#                 return_string += str(bonds) 
#                 count_bond += 1
#                 if(count_bond == bond_counter):
#                     for i in range(count_atom, atom_counter):
#                         atoms = Atom(self.mol.get_atom(i))
#                         return_string += str(atoms)
#                         count_atom +=1

#         return_string += footer
#         return return_string
   

#     def parse(self, file):
#         self.mol = molecule.molecule()
#         file = file.read() #added this
        
#         # Parse molecule_name from the first line
#         molecule_name = file.split('\n', 1)[0]

#         # Parse atom_no and bond_no from the fourth line
#         numbers = file.split('\n')[3].split()[:2]
#         atom_no, bond_no = map(int, numbers)

#         # Parse the x, y, and z coordinates for the atoms
#         atoms = []
#         atom_info = file.split('\n')[4:4+int(atom_no)]
#         for line in atom_info:
#             x, y, z, element = line.split()[:4]
#             self.mol.append_atom(element,float(x),float(y),float(z))

#         # Parse the bond information
#         bonds = []
#         bond_info = file.split('\n')[4+int(atom_no):4+int(atom_no)+int(bond_no)]

#         for line in bond_info:
#             atom1_idx, atom2_idx, bond_type = line.split()[:3]
#             self.mol.append_bond(int(atom1_idx), int(atom2_idx), int(bond_type))



import molecule;
import molsql
import os
import sqlite3
from io import StringIO

# radius = { 
#     'H': 25,
#     'C': 40,
#     'O': 40,
#     'N': 40,
# }

# element_name = { 
#     'H': 'grey',
#     'C': 'black',
#     'O': 'red',
#     'N': 'blue',
# }

header = """<svg version="1.1" width="1000" height="1000" 
                    xmlns="http://www.w3.org/2000/svg">"""

footer = """</svg>"""

offsetx = 500
offsety = 500

db = molsql.Database(reset = False)
radius = db.radius()
element_name = db.element_name()
header += db.radial_gradients()

class Atom:
    def __init__(self, c_atom):
        self.c_atom = c_atom
        self.c_atom.z = c_atom.z

    def svg(self):
        cx = (self.c_atom.x * 100.0) + offsetx
        cy = (self.c_atom.y * 100.0) + offsety
        r = radius[self.c_atom.element]
        fill = element_name[self.c_atom.element]    
        var = (' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (cx, cy, r, fill))
        return var

    def __str__(self):
        return self.svg()
    


class Bond:
    def __init__(self, c_bond):
        self.c_bond = c_bond
        self.c_bond.z = c_bond.z

    def svg(self):
        p1x = offsetx + ((100*self.c_bond.x1) - (10*self.c_bond.dy))
        p1y = offsety + ((100*self.c_bond.y1) + (10*self.c_bond.dx))

        p2x = offsetx + ((100*self.c_bond.x1) + (10*self.c_bond.dy))
        p2y = offsety + ((100*self.c_bond.y1) - (10*self.c_bond.dx)) 

        p3x = offsetx + ((100*self.c_bond.x2) - (10*self.c_bond.dy))
        p3y = offsety + ((100*self.c_bond.y2) + (10*self.c_bond.dx))
        
        p4x = offsetx + ((100*self.c_bond.x2) + (10*self.c_bond.dy))
        p4y = offsety + ((100*self.c_bond.y2) - (10*self.c_bond.dx))
        var1 = (' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (p2x, p2y, p1x, p1y, p3x, p3y, p4x, p4y))
        return var1

    def __str__(self):
        return self.svg()


class Molecule(molecule.molecule):

    def svg(self):
        # Sort atoms and bonds by increasing z value
        return_string = header

        atom_counter = self.atom_no
        bond_counter = self.bond_no
        count_atom = 0
        count_bond = 0

        while(count_atom != atom_counter):
            atoms = Atom(self.get_atom(count_atom))
            bonds = Bond(self.get_bond(count_bond))
            if(self.get_atom(count_atom).z < self.get_bond(count_bond).z):
                return_string += str(atoms)
                count_atom +=1
                if(count_atom == atom_counter):
                    for i in range(count_bond, bond_counter):
                        bonds = Bonds(self.get_bonds(i))
                        return_string += str(bonds)
                        count_atom +=1
                    break
            else:
                return_string += str(bonds) 
                count_bond += 1
                if(count_bond == bond_counter):
                    for i in range(count_atom, atom_counter):
                        atoms = Atom(self.get_atom(i))
                        return_string += str(atoms)
                        count_atom +=1

        return_string += footer
        return return_string
   

    def parse(self, file):
        self.mol = molecule.molecule()
        content=file.read()              #added this

        # Parse molecule_name from the first line
        molecule_name = content.split('\n', 1)[0]

        # Parse atom_no and bond_no from the fourth line
        numbers = content.split('\n')[3].split()[:2]
 
        atom_no, bond_no = map(int, numbers)

        # Parse the x, y, and z coordinates for the atoms
        atoms = []
        atom_info = content.split('\n')[4:4+int(atom_no)]
        for line in atom_info:
            x, y, z, element = line.split()[:4]
            self.mol.append_atom(element,float(x),float(y),float(z))

        # Parse the bond information
        bonds = []
        bond_info = content.split('\n')[4+int(atom_no):4+int(atom_no)+int(bond_no)]

        for line in bond_info:
            atom1_idx, atom2_idx, bond_type = line.split()[:3]
            atom1 = int(atom1_idx) -1
            atom2 = int(atom2_idx) -1
            self.mol.append_bond(int(atom1), int(atom2), int(bond_type))
