#ifndef LIBSURFACES_H
#define LIBSURFACES_H

#include "libpreprocess.h"

using namespace std;

// DEFAULT values of parameters which can be set by user
// 1. Output
const int OUT_DEFAULT = 1;      // (0,1,2,3) format of output: 0: short, 1: full, 2: full with structure info at the beginning, 3: to LassoProt;
//const int FILES_DEFAULT = 0;    // (0,1,2) IF create FILES to draw pictures with surfaces: 0: no, 1: (JSMol for surface and .py for .svg with bari), 2: (Mathematica, VMD and PDB as well);
const int FILES_DEFAULT = 0;    // (natural number with digits only 0 and 1, for instance 100011, generally "edcba", or shorter/longer) IF create FILES to draw pictures with surfaces: 
				// 0: no files, a: if .tcl and .pdb for VMD, b: if .jsm for JSMOL, c: if .m for Mathematica, d: if barricentre figure (.m and .py->svg), e: if few files with GLN 
const string FILENAME_DEFAULT = "protein_beg_end";  //string used in names of all produced files'
// 2. Computations
const int DENS_DEFAULT = 1;     // (0,1,2) density of the triangulation of surfaces (0 is the fastest and not so dense);
const double MAX_LENGTH_POLYGON = 5;    // (any) the maximal length of edges in the loop defining surface (if there are longer ones they are divided which increases density of triangulation as well; be carefull with making it too small);
const int PREC_DEFAULT = 0;     // (0,1,2) precision of computations: 0: the biggest, default for single structure, 1: middle, 2: the lowest, default for trajectories;
const int PREC_DEFAULT_TRAJ = 2;// as PREC_DEFAULT
const int LAPL_DEFAULT = 1;     // (0,1,2,3) type of laplasian that is used in the algorithm, you can read more about it in README file (changes not recommended);
// 3. Reducing "close", "uncertain" intersections between tails and the surface:
const int MIN_AMINO_DIST = 10;  // minimal distance on the tail (i.e. nr of atoms)  between next two intersections to not reduce them as "uncertain"
const int MIN_AMINO_DIST_FROM_BRIDGE = 3;                                   // -||- between intersection and bridge (closing the loop) to not reduce it as "uncertain"
const int MIN_AMINO_DIST_FROM_TAIL = 3;                                     // -||- between intersection and end of the tail to not reduce it as "uncertain"

// Input:
// - most functions expect file in XYZ format;
// - in the case of trajectories (function MainFindSurfacesTrajectory()) two formats are supported:
//  1. XYZ - chains in XYZ format separated by lines "t <nr>", where <nr> is the number of time frame (it can be real number);
//  2. XTC - typical output format from Gromacs package.


// In libpreprocess.h:
// struct PointR3, ChainAtom

struct Triangle_coord   // as Triangle, but here you do not need vector of points VP to know coordinates of the triangle
{
	PointR3 A,B,C;
};


// -------------------------------------------------------------------------------

int MainFindSurfaces ( char * infilename, int begin, int end,
                   bool control_dist = false, bool smooth = false, int smoothing_nr = 0,
                   int output = OUT_DEFAULT, int files = FILES_DEFAULT, string protein = FILENAME_DEFAULT, int prec = PREC_DEFAULT,
                   int uMIN_AMINO_DIST = MIN_AMINO_DIST, int uMIN_AMINO_DIST_FROM_BRIDGE = MIN_AMINO_DIST_FROM_BRIDGE, int uMIN_AMINO_DIST_FROM_TAIL = MIN_AMINO_DIST_FROM_TAIL, int lapl = LAPL_DEFAULT, int dens = DENS_DEFAULT );
// Reads chain from file (named <infilename>), cuts from chain atoms with ids from [<begin>,<end>] - to create loop and tails. Computes surface spanned on the loop and then
// intersections between tails and this surface. Writes on stdout lasso type of the structure, all intersections and other information. Optionally produces files to enable
// drawing of surface and whole structure (and optionally - its smoothed, "nicer" version as well). One may set many options defining precision (and time) of computations,
// format of output etc. USE --HELP to check all of them.

int MainFindSurfacesTrajectory ( char * infilename, int begin, int end,
                             int step = 1, bool control_dist = false,
                             int output = OUT_DEFAULT, int files = FILES_DEFAULT, string protein = FILENAME_DEFAULT, int prec = PREC_DEFAULT_TRAJ,
                             int uMIN_AMINO_DIST = MIN_AMINO_DIST, int uMIN_AMINO_DIST_FROM_BRIDGE = MIN_AMINO_DIST_FROM_BRIDGE, int uMIN_AMINO_DIST_FROM_TAIL = MIN_AMINO_DIST_FROM_TAIL, int lapl = LAPL_DEFAULT, int dens = DENS_DEFAULT );
// Reads trajectory from file (named <infilename>), for each time frame (actually - for one in every <step> frames) cuts from chain atoms with ids from [<begin>,<end>]
// - to create loop and tails. Computes lasso type for each frame and writes results to new file (named "traj_" + <protein> +".txt").
// One may set many options defining precision (and time) of computations, format of output etc. USE --HELP to check all of them.

// -------------------------------------------------------------------------------

string FindLasso (const vector<ChainAtom> & allchain, int begin, int end,
        int output = OUT_DEFAULT, int files = FILES_DEFAULT, string protein = FILENAME_DEFAULT, int prec = PREC_DEFAULT, 
        int uMIN_AMINO_DIST = MIN_AMINO_DIST, int uMIN_AMINO_DIST_FROM_BRIDGE = MIN_AMINO_DIST_FROM_BRIDGE, int uMIN_AMINO_DIST_FROM_TAIL = MIN_AMINO_DIST_FROM_TAIL, int lapl = LAPL_DEFAULT, int dens = DENS_DEFAULT );
// Similar to MainFindSurfaces(), but chain as already read/loaded to <allchain> and function returns the lasso type etc as a string instead of writing it on stdout.
// Additionally you cannot smooth the structure by this function - to obtain smoothed version of a structure use later RefindSmoothLasso()

string FindLinkedLasso (const vector<ChainAtom> & loop, const vector<ChainAtom> & tail,
        int output = OUT_DEFAULT, int files = FILES_DEFAULT, string protein = FILENAME_DEFAULT, int prec = PREC_DEFAULT, 
        int uMIN_AMINO_DIST = MIN_AMINO_DIST, int uMIN_AMINO_DIST_FROM_BRIDGE = MIN_AMINO_DIST_FROM_BRIDGE, int uMIN_AMINO_DIST_FROM_TAIL = MIN_AMINO_DIST_FROM_TAIL, int lapl = LAPL_DEFAULT, int dens = DENS_DEFAULT );
// The same as FindLasso(), but instead of passing whole chain and indexes of begin and end of a loop, here you pass two ready chains: <loop> and <tail>.

string RefindSmoothLasso (const vector<ChainAtom> & allchain, int begin, int end, int num_smoothing,
        int output = OUT_DEFAULT, int files = FILES_DEFAULT, string protein = FILENAME_DEFAULT, int prec = PREC_DEFAULT, 
        int uMIN_AMINO_DIST = MIN_AMINO_DIST, int uMIN_AMINO_DIST_FROM_BRIDGE = MIN_AMINO_DIST_FROM_BRIDGE, int uMIN_AMINO_DIST_FROM_TAIL = MIN_AMINO_DIST_FROM_TAIL, int lapl = LAPL_DEFAULT, int dens = DENS_DEFAULT );
// Smooths the structure and possibly produces files that enable to draw smoothed structure in different formats.
// The structure is being smoothed iteratively as long as the lasso type is unchanged, but not more than <num_smoothing> times.

string RefindSmoothLinkedLasso (const vector<ChainAtom> & loop, const vector<ChainAtom> & tail, int num_smoothing,
        int output = OUT_DEFAULT, int files = FILES_DEFAULT, string protein = FILENAME_DEFAULT, int prec = PREC_DEFAULT, 
        int uMIN_AMINO_DIST = MIN_AMINO_DIST, int uMIN_AMINO_DIST_FROM_BRIDGE = MIN_AMINO_DIST_FROM_BRIDGE, int uMIN_AMINO_DIST_FROM_TAIL = MIN_AMINO_DIST_FROM_TAIL, int lapl = LAPL_DEFAULT, int dens = DENS_DEFAULT );
// The same as RefindSmoothLinkedLasso(), but instead of passing whole chain and indexes of begin and end of a loop, here you pass two ready chains: <loop> and <tail>.

// -------------------------------------------------------------------------------

vector< Triangle_coord > GiveSurface( const vector<ChainAtom> & allchain, int begin, int end,
	int prec = PREC_DEFAULT, int option = LAPL_DEFAULT, int m = DENS_DEFAULT );
// Returns list(vector) of triangles that form minimal surface.

#endif
