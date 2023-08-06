#ifndef LIBKNOT_H
#define LIBKNOT_H

#include <boost/math/tools/polynomial.hpp>
#include "libpreprocess.h"

using namespace std;
using namespace boost::math::tools;

//*DEFAULT values of parameteres - one MAY CHANGE them
const int TRY_DEFAULT = 200;    // In the case of RANDOM methods of closing chain -
                                // how many random closures we take into account to calculate (probabilistic) knot's type.
const int CLOSURE_DEFAULT = 0;  // Use --help to see the options.

const int DENS_DEFAULT = 1;     // In the case of calculating knotting fingerprint (whole matrixes of knot's types for all subchains, --type==2)
const int LEV_DEFAULT = 0;      // with density (DENS) and level (LEV) one may regulate how precise results he wants to get,
                                // values 1 and 0 means that each point of the matrix will be checked.
                                // If you want to get results faster and the structure is not strongly knotted we suggest to choose density = 7 and level = 20.
//(Precisely: DENS - we first calculate knot types only for whole chain and for chain with cut multiple of DENS atoms from both ends. Then if some subchain
// is knotted with probability >LEV %, we calculate knot types of all "neigbour" subchains).

// ***NIE DZIALA jako domyslny argument MainFindKnots :/
const string FILEOUT_DEFAULT = "KNOTS_out"; // The name of file where knotting fingerprint (for option --type==2) will be written.


//*Do NOT change KNOTS_AMOUNT
const int KNOTS_AMOUNT = 42;    // The number of knot types we can recognize in this package (we have their Alexander polynomials written in our "library" - array
                                // <Knots> in whichKnot.cpp - coppied on the bottom of this file)
                                // (number of knots + 3: PROBLEM (problem during projecting), INSIDE (bonds of chain "inside" the structure), NO (we do not have that polynomial in our "library")).


// In libpreprocess.h:
// struct PointR3, ChainAtom


int MainFindKnots(char * infilename, char * outfilename,
               int type = 0, int control_dist = false,  int closure = CLOSURE_DEFAULT, int uTRY = TRY_DEFAULT, int density = DENS_DEFAULT, int level = LEV_DEFAULT);
// Reads chain from file (named <infilename>) and in the case of <type==0> calculates the knot type and writes it on stdout, while in the case of <type==2> calculates
// whole knotting fingerprint and writes results to the file (named <outfilename>). Use --help to check the rest of arguments.

// -------------------------------------------------------

int FindKnotFingerprint(const vector<ChainAtom> & chain, char * outfilename,
                  int density = DENS_DEFAULT, int level = LEV_DEFAULT, int closure = CLOSURE_DEFAULT, int uTRY_AMOUNT = TRY_DEFAULT, int knotnames = 1, int max_cross = 15);
// Calculates knotting fingerprint (<type==2>) for <chain> and writes it to the file <file_to_write>.  Use --help to check the rest of arguments.
// You can draw knotting fingerprint running (...) with <file_to_write> as an argument.

string FindKnotFingerprint_string(const vector<ChainAtom> & chain,
                  int density = DENS_DEFAULT, int level = LEV_DEFAULT, int closure = CLOSURE_DEFAULT, int uTRY_AMOUNT = TRY_DEFAULT, int knotnames = 1, int max_cross = 15);

int FindMajorKnot( const vector<ChainAtom> & chain, int knots[KNOTS_AMOUNT], int closure = CLOSURE_DEFAULT, int uTRY_AMOUNT = TRY_DEFAULT );
// Calculates the knot type of whole <chain> - writes in array <knots> how many times each knot type appeared among all closures (i.e. knots[3]=14 means that knot 5_1 appeared
// in 14 closures, since Knots[3].name=="51") -
// to get the name of knot from array <knots> (like "4_1(79%) 0_1(13%) 8_21(5%) 6_1(3%)") one needs to call next function GiveTheNameOfKnot( knots ).
//
// The difference with the function MainFindKnots(): 1).the structure is already read into the <chain>, 2).the <type> is determined (=0), 3).and the results are in array - you need
// to call other function (GiveTheNameOfKnot()/_Matrix()) to get the name in readable form.

// -------------------------------------------------------
// -------------------------------------------------------

string GiveTheNameOfKnot ( int knots[KNOTS_AMOUNT] );
// Gives the name of knot for array <knots> (which you can obtain with function FindMajorKnot()), in readable format (like "41(79%) 01(13%) 821(5%) 61(3%)").

string GiveTheNameOfKnot_Matrix ( int knots[KNOTS_AMOUNT] );
// As previous one - gives the name of knot for array <knots> (which you can obtain with function FindMajorKnot()) - BUT in other format,
// the same as you get in the knotting fingerprint matrix (not so readable, like "2 77 0 0 0 0 41 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 01 0 0 821 61 1 76").

// -------------------------------------------------------

int FindTheKnot( vector<ChainAtom> chain );
// Returns id (in array <Knots>) of a knot created by <chain> - we treat here <chain> as closed one (maybe we closed it before), the result is deterministic.

string FindTheKnot_poly_string( vector<ChainAtom> chain, int max_cross );
// Returns the string with Alexander polynomial coefficients of a knot created by <chain> - we treat here <chain> as closed one (maybe we closed it before), the result is deterministic.

bool FindTheKnot_poly( vector<ChainAtom> chain, vector<int> & det, double & det_d);

bool FindTheKnot_poly_polynomial( vector<ChainAtom> chain, polynomial<int> & det, double & det_d);

// Calculates the Alexander polynomial of a knot created by <chain> (treated as a closed one), returns:
// 1 (true): Success, Alexander polynomial for a knot in variable <det>;
// 0 (false): Structure was too complicated to calculate Alexander Polynomial, we calculated its value in t=-3 and give it in variable <det_d>; 
//then we found polynomial with such value in t=-3 - among Alexander polynomials of knots up to 8 crossings, if such exists;

void PrintsPoly (polynomial<int> poly);
// Prints polynomial.

//int CalculatesPoly (polynomial<int> poly, int t);
int CalculatesPoly (vector<int> poly_v, int t);
// Returns value of poly in t


/*
 THE NAMES OF KNOTS WHICH WE IDENTIFY - DEFINED IN WHICHKNOT.CPP
Knots[0].name = UNKNOT;
Knots[1].name = "31";
Knots[2].name = "41";
Knots[3].name = "51";
Knots[4].name = "52";
Knots[5].name = "61";
Knots[6].name = "62";
Knots[7].name = "63";
Knots[8].name = "71";
Knots[9].name = "72";
Knots[10].name = "73";
Knots[11].name = "74";
Knots[12].name = "75";
Knots[13].name = "76";
Knots[14].name = "77";
Knots[15].name = "81";
Knots[16].name = "82";
Knots[17].name = "83";
Knots[18].name = "84";
Knots[19].name = "85";
Knots[20].name = "86";
Knots[21].name = "87";
Knots[22].name = "88";
Knots[23].name = "89";
Knots[24].name = "810";
Knots[25].name = "811";
Knots[26].name = "812";
Knots[27].name = "813";
Knots[28].name = "814";
Knots[29].name = "815";
Knots[30].name = "816";
Knots[31].name = "817";
Knots[32].name = "818";
Knots[33].name = "819";
Knots[34].name = "820 | 31 # 31";
Knots[35].name = "821 | 31 # 41";
Knots[36].name = "91";
Knots[37].name = "31 # 51";
Knots[38].name = "31 # 52";

Knots[KNOTS_AMOUNT-3].name = UNKNOWN;
Knots[KNOTS_AMOUNT-2].name = "Problem with projecting";
Knots[KNOTS_AMOUNT-1].name = INSIDE;
 */


#endif
