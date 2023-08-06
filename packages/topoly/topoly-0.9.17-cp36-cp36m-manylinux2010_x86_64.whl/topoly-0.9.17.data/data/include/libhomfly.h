#ifndef LIBHOMFLY_H
#define LIBHOMFLY_H

#include<string>
#include "libpreprocess.h"
#include "homflyFinder.h"

using namespace std;

const int TRY_DEFAULT = 200;	// how many times we rand points on a fuleren and calculate knots;

// In libpreprocess.h:
// struct PointR3, ChainAtom

/* All functions identify all crossings composed by the structure and code them in a special way. The module enables to calculate two types of codes:
   -> needed for computation of HOMFLY-PT polynomial and then knot/link type of the structure;
   -> needed for computation of Yamada polynomial and then type of Theta-curve composed by the structure;
 
   To obtain the knot/link type based on HOMFLY-PT polynomial one needs to run two other programs: 1. <lmpoly> which computes HOMFLY-PT polynomial from coded crossings
   (as the only argument gets file with code computed by functions from this module, as an output produces file <LMKNOT.txt> with coded polynomial);
   2. <ncuc> which decodes polynomial from file <LMKNOT.txt> and identifies the name of a link in it's own "library" - prints this name on stdout in such a way:
   -> "All=1,  Types=1,  COMPLEX(100%): +3_1(100%)"  - if there was only one closure of structure (and one polynomial in <LMKNOT.txt>)
   -> "All=50, Types=3,  COMPLEX(11%):  Unlink_2(84%) +Hopf(11%) +3_1 U 0_1(5%)" - if there were many closures, like in options of random closing of the structure - here 50 closures
       (and many polynomials separated by empty lines in <LMKNOT.txt>, previously many sets of coded crossings separated by empty lines, produced by functions from this module 
        and given as an argument to <lmpoly>).
 
   Similarly - in a case of Yamada code (...)
 
   INPUT for functions in this module - list of files with components (in XYZ format) or vector of already read/loaded components. For HOMFLY-PT polynomial components
   have to be totally disjoint, for Yamada polynomial ends of components have to be joint for few components - in this case one "component" is one "arm" of theta-curve, not separate ring.
 */

// -------------------------------------------------------


int FindLinkCode(const vector<string> VInput, 
        bool yamada = false, int closure = 0, int uTRY = TRY_DEFAULT, bool noCheckIds=false, const vector<int> VParts = vector<int>() );
// Reads components from the files (their names are in <VInput>), prepares them (cuts and checks their correctness), closes them in a given way and given number of times, and identifies all crossings - 
// coded crossings writes to the file <EMCode.txt> for HOMFLY-PT polynomial - or <YCode.txt> for Yamada polynomial. Use --help to check all arguments.

string FindLinkCode_toString(const vector<string> VInput, 
        bool yamada = false, int closure = 0, int uTRY = TRY_DEFAULT, bool noCheckIds=false, const vector<int> VParts = vector<int>() );
// Exactly the same as previous function UFindLinkCode() - but result (coded crossings) returns as a string instead of writing it into the file. 

// -------------------------------------------------------

string FindLinkHomflyCode(vector< vector<ChainAtom> > vComp, 
        int closure = 0, int uTRY = TRY_DEFAULT);
// Returns as a string coded crossings consisted in structure <vComp> - for HOMFLY-PT polynomial. 
// First components are closed by a given method (<closure>).
// If <uTRY> is greater than one, then there will be many (exactly <uTRY>) sets of coded crossings separated by empty lines (one set for one closure). 

string FindLinkYamadaCode(vector< vector<ChainAtom> > vComp);
// Returns as a string coded crossings consisted in structure <vComp> - for Yamada polynomial.
// In this case we do not need to close "components", they are actually "arms" of one theta-curve. 

// -------------------------------------------------------

string FindLinkCode_1Direction( vector< vector<ChainAtom> > vComp, bool & OK, int v = 0, bool yamada = false );
// Returns as a string coded crossings consisted in structure <vComp> (components/arms are already "prepared" - cut, closed etc). 
// The structure is projected in direction <v> and if any problem occurred while projecting (like unlucky overlapping of projected curves) one gets info in variable <OK> and needs to call the function
// again with different value of <v>. 
// (direction <v> means vector fuleren[v % 60], where <fuleren> is an array of 60 points spread on a sphere) (...) - maybe needless for users)



#endif





