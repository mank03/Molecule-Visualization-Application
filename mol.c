#include "mol.h"

/**
 * It takes an atom, a string, and three doubles, and sets the atom's element to the string and its x,
 * y, and z coordinates to the doubles
 * 
 * @param atom the atom structure
 * @param element The element of the atom.
 * @param x the x coordinate of the atom
 * @param y the y-coordinate of the atom
 * @param z the z-coordinate of the atom
 */
void atomset( atom *atom, char element[3], double *x, double *y, double *z ){
    strcpy(atom -> element, element);
    atom -> x = *x;
    atom -> y = *y;
    atom -> z = *z;
}

/**
 * This function copies the element, x, y, and z values from the atom structure into the variables
 * passed to the function.
 * 
 * @param atom the atom you want to get the information from
 * @param element the element of the atom
 * @param x the x coordinate of the atom
 * @param y the y coordinate of the atom
 * @param z the z coordinate of the atom
 */
void atomget( atom *atom, char element[3], double *x, double *y, double *z ){
    strcpy(element, atom->element);
    *x = atom -> x;
    *y = atom -> y;
    *z = atom -> z;
}

/**
 * It sets the bond's atoms and electron pairs
 * 
 * @param bond The bond to set.
 * @param a1 The index of the first atom in the bond.
 * @param a2 The index of the second atom in the bond.
 * @param atoms array of the atoms in the bonds
 * @param epairs The number of electron pairs in the bond.
 */
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
    bond -> a1 = *a1;
    bond -> a2 = *a2;
    bond -> atoms = *atoms;
    bond -> epairs = *epairs;

    compute_coords(bond);
}

/**
 * > This function returns the two atoms and the number of electron pairs in a bond
 * 
 * @param bond The bond to get the information from.
 * @param a1 The index of the first atom in the bond.
 * @param a2 The index of the second atom in the bond.
 * @param atoms array of the atoms in the bonds
 * @param epairs The number of electron pairs in the bond.
 */
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){
    *a1 = bond -> a1;
    *a2 = bond -> a2;
    *atoms = bond -> atoms;
    *epairs = bond -> epairs;

    
}

/**
 * This function computes the coordinates of the bond
 * 
 * @param bond The bond to get the information from.
 */
void compute_coords(bond *bond){
    // bond -> x1 = 0;
    bond -> x1 = bond -> atoms[bond->a1].x;
    bond -> y1 = bond -> atoms[bond->a1].y;
    bond -> x2 = bond -> atoms[bond->a2].x;
    bond -> y2 = bond -> atoms[bond->a2].y;

    double avg = (bond -> atoms[bond->a1].z + bond -> atoms[bond->a2].z)/2;
    
    bond -> z = avg;

    double length = sqrt((pow(bond->x2 - bond->x1,2)) + (pow(bond->y2 - bond->y1, 2)));

    bond -> len = length;

    bond -> dx = (bond -> x2 - bond -> x1) / length;
    bond -> dy = (bond -> y2 - bond -> y1) / length;
}

/**
 * It allocates memory for a molecule struct, and then allocates memory for the arrays of atoms and
 * bonds
 * 
 * @param atom_max the maximum number of atoms that can be stored in the molecule
 * @param bond_max The maximum number of bonds that can be stored in the molecule.
 * 
 * @return A pointer to a molecule struct.
 */
molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ){

    molecule *molecules = malloc(sizeof(molecule));

    molecules -> atom_max = atom_max;
    molecules -> atom_no = 0;
    molecules -> atoms = malloc(atom_max * sizeof(atom));
    molecules -> atom_ptrs = malloc(atom_max* sizeof(atom*));

    molecules -> bond_max = bond_max;
    molecules -> bond_no = 0;
    molecules -> bonds = malloc(bond_max * sizeof(bond));
    molecules -> bond_ptrs = malloc(bond_max* sizeof(bond*));
    
    if(molecules == NULL || molecules->atoms == NULL || molecules->atom_ptrs == NULL || molecules->bonds == NULL || molecules->bond_ptrs == NULL) {
        return NULL;
    }

    return molecules;
}

/**
 * It copies a molecule
 * 
 * @param src The molecule to copy.
 * 
 * @return A pointer to a molecule struct.
 */
molecule *molcopy( molecule *src ){
    molecule *molecules = molmalloc(src -> atom_max, src -> bond_max);

    for(int i = 0; i < src->atom_no; i++){
      molappend_atom(molecules, &src -> atoms[i]);
    }

    for(int i = 0; i < src->bond_no; i++){
      molappend_bond(molecules, &src -> bonds[i]);
    }

    molecules -> atom_no = src -> atom_no;
    molecules -> bond_no = src -> bond_no;

    return molecules;
}

/**
 * It frees all the memory allocated to a molecule
 * 
 * @param ptr pointer to the molecule structure
 */
void molfree( molecule *ptr ){
    free(ptr->atom_ptrs);
    free(ptr->bond_ptrs);
    free(ptr->atoms);
    free(ptr->bonds);
    free(ptr);
}

/**
 * It appends an atom to a molecule
 * 
 * @param molecule pointer to the molecule we're adding the atom to
 * @param atom the atom to be added to the molecule
 */
void molappend_atom( molecule *molecule, atom *atom ){

    if(molecule -> atom_max == molecule -> atom_no){
        if(molecule -> atom_max == 0){
            molecule -> atom_max = 1;
        }
        else{
            molecule -> atom_max *= 2;
        }
        molecule -> atoms = realloc(molecule -> atoms, molecule -> atom_max * sizeof(struct atom));
        molecule -> atom_ptrs = realloc(molecule -> atom_ptrs, molecule -> atom_max * sizeof(struct atom*));

        for(int i = 0; i < molecule -> atom_no; i++){
          molecule -> atom_ptrs[i] = &molecule -> atoms[i];
        }
    }

    molecule -> atoms[molecule -> atom_no] = *atom;
    molecule -> atom_ptrs[molecule -> atom_no] = &(molecule -> atoms[molecule -> atom_no]);
    molecule -> atom_no++;
}

/**
 * > It appends an bond to a molecule
 * 
 * @param molecule pointer to the molecule struct
 * @param bond the bond to be added to the molecule
 */
void molappend_bond( molecule *molecule, bond *bond){

    if(molecule -> bond_max == molecule -> bond_no){
        if(molecule -> bond_max == 0){
          molecule -> bond_max = 1;
        }
        else{
          molecule -> bond_max = molecule -> bond_max * 2;
        }
        molecule -> bonds = realloc(molecule -> bonds,  molecule -> bond_max * sizeof(struct bond));
        molecule -> bond_ptrs = realloc(molecule -> bond_ptrs,  molecule -> bond_max * sizeof(struct bond*));

        for(int i = 0; i < molecule -> bond_no; i++){
          molecule -> bond_ptrs[i] = &molecule -> bonds[i];
        }
    }
    
    molecule -> bonds[molecule -> bond_no] = *bond;
    molecule -> bond_ptrs[molecule -> bond_no] = &(molecule -> bonds[molecule -> bond_no]);
    molecule -> bond_no++;
}

/**
 * Compares the z values of the atoms
 * 
 * @param a pointer to the first element to be compared
 * @param b pointer to the second element to be compared
 * 
 * @return The return value is the difference between the two values.
 */
int atom_cmpfunc(const void * a, const void * b) {
    if((*(atom **)a)->z < (*(atom **)b)->z)
        return -1;
    if((*(atom **)a)->z > (*(atom **)b)->z)
        return  1;
    return 0;
}

/**
 * Compares the average of the two z values in the bond
 * 
 * @param a pointer to the first bond
 * @param b pointer to the second bond
 * 
 * @return The return value is the difference between the two values.
 */
int bond_comp (const void * a, const void * b) {
    if((*(bond **)a)->z < (*(bond **)b)->z)
        return -1;
    if((*(bond **)a)->z > (*(bond **)b)->z)
        return  1;
    return 0;
}

/**
 * It sorts the atoms and bonds of a molecule by their Z value
 * 
 * @param molecule pointer to the molecule to be sorted
 */
void molsort( molecule *molecule ){      
    qsort(molecule->atom_ptrs, molecule -> atom_no, sizeof(molecule), atom_cmpfunc);
    qsort(molecule->bond_ptrs, molecule -> bond_no, sizeof(molecule), bond_comp);
}

/**
 * > Initialize xform_matrix with a x rotation 
 * 
 * @param xform_matrix The matrix that will be initialized with the rotation.
 * @param deg The degree of rotation.
 */
void xrotation(xform_matrix xform_matrix, unsigned short deg) {
    double rad = deg * (PI / 180.0);

    printf("\n\nX ROTATION BEFORE:\n");
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            printf("xform_matrix[%d][%d] = %f\n", i , j, xform_matrix[i][j]);
        }
    }
    xform_matrix[0][0] = 1.0;
    xform_matrix[0][1] = 0.0;
    xform_matrix[0][2] = 0.0;

    xform_matrix[1][0] = 0.0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = -sin(rad);

    xform_matrix[2][0] = 0.0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);
    printf("\n\nX ROTATION AFTER:\n");
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            printf("xform_matrix[%d][%d] = %f\n", i , j, xform_matrix[i][j]);
        }
    }
}

/**
 * > Initialize xform_matrix with a y rotation 
 * 
 * @param xform_matrix The matrix that will be initialized with the rotation.
 * @param deg The degree of rotation.
 */
void yrotation(xform_matrix xform_matrix, unsigned short deg) {
    double rad = deg * (PI / 180.0);

    printf("\n\nY ROTATION BEFORE:\n");
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            printf("xform_matrix[%d][%d] = %f\n", i , j, xform_matrix[i][j]);
        }
    }

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0.0;
    xform_matrix[0][2] = sin(rad);

    xform_matrix[1][0] = 0.0;
    xform_matrix[1][1] = 1.0;
    xform_matrix[1][2] = 0.0;

    xform_matrix[2][0] = -sin(rad);
    xform_matrix[2][1] = 0.0;
    xform_matrix[2][2] = cos(rad);
    printf("\n\nY ROTATION AFTER:\n");
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            printf("xform_matrix[%d][%d] = %f\n", i , j, xform_matrix[i][j]);
        }
    }

}

/**
 * > Initialize xform_matrix with a z rotation 
 * 
 * @param xform_matrix The matrix that will be initialized with the rotation.
 * @param deg The degree of rotation.
 */
void zrotation(xform_matrix xform_matrix, unsigned short deg) {
    
    printf("\n\nZ ROTATION BEFORE:\n");
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            printf("xform_matrix[%d][%d] = %f\n", i , j, xform_matrix[i][j]);
        }
    }
    
    double rad = deg * (PI / 180.0);
    

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = -sin(rad);
    xform_matrix[0][2] = 0.0;

    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0.0;

    xform_matrix[2][0] = 0.0;
    xform_matrix[2][1] = 0.0;
    xform_matrix[2][2] = 1.0;
    
    printf("\n\nZ ROTATION AFTER:\n");
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            printf("xform_matrix[%d][%d] = %f\n", i , j, xform_matrix[i][j]);
        }
    }
}

/**
 * It takes a molecule and a transformation matrix and applies the transformation to the molecule
 * 
 * @param molecule pointer to the molecule to be transformed
 * @param matrix The transformation matrix to be applied to the molecule.
 */
void mol_xform(molecule *molecule, xform_matrix matrix) {
  int x;
  double rotate[3];
  double transform[3];

  bond *bonds;

  for(int i = 0; i < molecule -> atom_no; i++){
    x = 0;
    transform[0] = molecule -> atom_ptrs[i]->x;
    transform[1] = molecule -> atom_ptrs[i]->y;
    transform[2] = molecule -> atom_ptrs[i]->z;

    for(int i = 0; i < 3; i++){
      rotate[i] = 0.0;
    }

    for(int row = 0; row < 3; row++){
      for(int col = 0; col < 3; col++){
        rotate[x] += (transform[col]*matrix[row][col]);
      }
      x++;
    }

    molecule -> atom_ptrs[i]->x = rotate[0];
    molecule -> atom_ptrs[i]->y = rotate[1];
    molecule -> atom_ptrs[i]->z = rotate[2];
  }

    for(int i = 0; i < molecule -> bond_no; i++){
      bonds = &molecule -> bonds[i];
      compute_coords(bonds);
  }

}
