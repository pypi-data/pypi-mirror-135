#ifndef LIBGLN_H
#define LIBGLN_H

#include "libpreprocess.h"
#include "../surfaces/GLN.h"

const int TRY_DEFAULT = 200;
const int PREC_DECIMAL_DEFAULT = 3;

using namespace std;
//using namespace boost::math::tools;

// for rough time and space complexity analise, N := max( len(chain1), len(chain2) )

double LinkingOneSegment( PointR3 A1, PointR3 A2, PointR3 B1, PointR3 B2 );
// returns GLN value between two single segments [A1,A2] and [B1,B2]

double gln( const vector<ChainAtom> & chain1, const vector<ChainAtom> & chain2, int begin1 = -1, int end1 = -1, int begin2 = -1, int end2 = -1 );
// returns GLN value between two chains, possibly only their parts chain1[begin1-end1] and chain2[begin2-end2]
// space and time O(N^2)

double gln( char * filename1, char * filename2, int begin1 = -1, int end1 = -1, int begin2 = -1, int end2 = -1 );
// as previous one but chains are not already read from the files

string max_gln( const vector<ChainAtom> & chain1, const vector<ChainAtom> & chain2, int density = -1, int prec = PREC_DECIMAL_DEFAULT, int begin1 = -1, int end1 = -1, int begin2 = -1, int end2 = -1 );
// returns string with GLN value between two chains and additionally some information about maximal |GLN|(!) values between fragments of chains;
// 1). if one does not give "density" parameter then maximal GLN values between one whole chain and all fragments of the second chain are calculated;
//     then shorter fragments of chains with still high GLN value (i.e. >=80% of the highest) are indicated; in brackets ids of fragments of chains;
//     space and time O(N^2); exemplary output:
// wh: 2.88521 max_wh_comp1: 3.1587 (28,850) shorter: 2.53055 (184,197) max_wh_comp2: 3.29664 (35,946) shorter: 2.64296 (53,306)
// 2). if one gives density parameter, then the function additionally searches for the local maximum between all fragments of both chains -
//     time is O(N^4), memory is O(N^2) for density=1, and O((N/density)^4),..., for any density - the function checks GLN between fragments starting and ending in ids only of form k*density (k*density + id of first atom in the analized chain);
//     exemplary output:
//wh: 2.88521 max_wh_comp1: 3.1587 (28,850) shorter: 2.53055 (184,197) max_wh_comp2: 3.29664 (35,946) shorter: 2.64296 (53,306) maxTotalDense(10): 3.19762 (31-971, 31-371) shorterDense: 2.62736 (51-321, 171-201)

string max_gln( char * filename1, char * filename2, int density = -1, int prec = PREC_DECIMAL_DEFAULT, int begin1 = -1, int end1 = -1, int begin2 = -1, int end2 = -1 );
// as previous one but chains are not already read from the files

double average_gln( const vector<ChainAtom> & chain1, const vector<ChainAtom> & chain2, int tryAmount = TRY_DEFAULT, int begin1 = -1, int end1 = -1, int begin2 = -1, int end2 = -1 );
// returns average GLN value between chain1[begin1-end1] and chain2[begin2-end2], <tryAmount> times randomly closed - both ends of each component connected to ONE point on the ig sphere;
// before using this function one needs to call FillFulerenData();

double average_gln( char * filename1, char * filename2, int tryAmount = TRY_DEFAULT, int begin1 = -1, int end1 = -1, int begin2 = -1, int end2 = -1 );
// as previous one but chains are not already read from the files

vector< vector <double> > gln_matrix( const vector<ChainAtom> & loop, const vector<ChainAtom> & tail, int begin1 = -1, int end1 = -1, int begin2 = -1, int end2 = -1 );
// returns matrix of GLN values between whole loop and all fragments of tail (size of matrix is len(tail) x len(tail))

//double** gln_matrix1( const vector<ChainAtom> & loop, const vector<ChainAtom> & tail, int begin1 = -1, int end1 = -1, int begin2 = -1, int end2 = -1 );
// returns matrix of GLN values between whole loop and all fragments of tail (size of matrix is len(tail) x len(tail))

#endif
