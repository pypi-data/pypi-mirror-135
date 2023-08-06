#ifndef LIBPREPROCESS_H
#define LIBPREPROCESS_H

using namespace std;

//*ToPoly
const double MIN_DIST_ATOMS = 3.4;	// minimal distance between next atoms in the origin chain which is OK for a protein chain (smaller one may signal problem with data)
const double MAX_DIST_ATOMS = 4.2;	// maximal...
//const double EPS = 0.01;             // precision of comparisons of double numbers
const double EPS = 0.00001;             // precision of comparisons of double numbers
const string OK = "OK";
const double R_close1chain_DEF = 1.25;	// used while closing chains (1 chain: R = 1.25*RadiusOfChain(chain), as in the Knotprot; chainS: R = 1.02*DiameterOfStructure(vComp), as in the LinkProt, 27.09.2019) 
const double R_closeChains_DEF = 1.02;

//NOT PUBLIC in ToPoly
const int FULEREN_POINTS = 60;		// how many points on the fuleren (in the structure "fuleren", being initialized in function FillFulerenData() 
                                        // and being used while closing chains and projecting them into the plane )
const int UNIFORM_POINTS = 400;		// ... - in the structure uniform (as the previous one; could be used instead of fuleren points)

//*ToPoly
struct PointR3
{
	double x,y,z;
};
//*ToPoly
struct ChainAtom        // basic structure used in ToPoly for analyze of entanglement of chains    
{
	PointR3 A; 
	int id;     
};
//*ToPoly (DO NOT WANT to make next two structs public - but we have to if we make available "ProjectChain()"
struct CrossingShort    // auxiliary structure to keep an eye on crossings between edges in some projection of chain; 
                        //- more specifically, there exists "vc" - a vector of all Crossings (other type of struct, with more information)
                        // and each Edge keeps an information which of those Crossings include it - as a vector of ids of those Crossings in "vc";
                        // a vector can be sorted due to the location of Crossings on the Edge using parameter "alpha";
{
	short id;       // id of corresponding Crossing in "vc"
	double alpha;   // alpha \in [0,1] informs about location of Crossing on the Edge (1 - on the beginning of Edge);
};
//*ToPoly
struct Edge             // after projecting chain(s) onto the plane we keep it as a vector of Edges - having all chains together and keeping here later additional info about crossings
{
	PointR3 A,B;
	vector<CrossingShort> cross;    // *description is by the definition of struct CrossingShort
        int comp;       // nr of component (important if we analyze link - structure composed by few components) 
};

//NOT ToPoly
//COMPARING DOUBLE
bool CompareEq (double d1, double d2);

bool CompareGt (double d1, double d2);

bool CompareGeq (double d1, double d2);

double Dist (PointR3 A, PointR3 B);
// -------------------------------------------------------

void FillFulerenData(); 
// fills some structures (arrays of points <fuleren> and <uniform>) used while randomly closing and projecting chain(s);
// needs to be done before you call functions: 1. ProjectChain(), 2-10. ChloseChain_...(), CloseChains_...()
// *** 09.2019: now this is a part of the above functions, do not need to be called separately;


//*ToPoly

vector<ChainAtom> ChainRead(char * filename, bool & unable);
// reads chain from the file in format XYZ (named <filename>) and returns vector of ChainAtom-s, used in other functions;
// it also returns info if we could open the file and its format was OK (XYZ) - in variable <unable>;

vector<ChainAtom> ChainRead_fromString(string const& source, bool & unable);
// similar to ChainRead but reads from string <source>, not from file;

string ChainWrite_toString( const vector<ChainAtom> & chain, bool out_xyz = true );
// returns string representing <chain> in format XYZ - or PDB if the last argument is false;

void ChainWrite( char * filename, const vector<ChainAtom> & chain, bool out_xyz = true );
// writes <chain> into file (named <filename>) in format XYZ - or PDB if the last argument is false;

// -------------------------------------------------------

int CutChain( vector<ChainAtom> & chain, int start, int end);
// cuts atoms from ends of <chain> so that indexes of first and last atom in the sequence will be from range <start,end>;

string CheckDistancesBetweenAtoms ( vector<ChainAtom> chain);
// checks if all next atoms in <chain> are located in the distance from interval [MIN_DIST_ATOMS, MAX_DIST_ATOMS];
// returns <OK> or "HEAD: broken protein between..." with info about first pair of atoms with "wrong" dinstance;

// -------------------------------------------------------
//////////////////////////////////////////////////////////

// ALL FUNCTIONS CLOSING CHAIN/CHAINS
// add to <chain> some atoms (1,2 or many along the big sphere - with R=10*(diameter of structure) - surrounding structure) to close it.
// They choose those additional atoms in different ways:

int CloseChain_OUT( vector<ChainAtom> & chain, double r = R_close1chain_DEF );
// MANY additional atoms, chosen in a DETERMINICTIC way, method "out of the center of mass":
// adds long arms to the ends of <chain> in the direction going out from the center of mass of structure through those ends,
// then connects those arms along the big sphere;

int CloseChain_2points( vector<ChainAtom> & chain, double r = R_close1chain_DEF );
// MANY additional atoms, chosen in a RANDOM way:
// connects each end with different, randomly chosen point on the big sphere and those points are connected along the big sphere;

int CloseChain_1point( vector<ChainAtom> & chain, double r = R_close1chain_DEF );
// 1 additional atom, chosen in a RANDOM way:
// connects both ends with the same, randomly chosen point on the big sphere;

int CloseChain_1direction( vector<ChainAtom> & chain );
// 2 additional atoms, chosen in a RANDOM way:
// chooses randomly one point on the big sphere and this point determines the direction (vector) which we add long arms to both ends in,
// then those arms are connected with one segment;

int CloseChain_1direction_NoRandom( vector<ChainAtom> & chain, int nr = 0);
// 2 additional atoms, chosen in a DETERMINISTIC way:
// similar to previous CloseChain_1direction() but the point on the big sphere is chosen from above (it is fuleren[nr]);

// ----------
// ANALOGOUS FUNCTIONS FOR LINKS
// The only difference between using them and using previous functions for each chain (component) separately is R of the big sphere -
// here we are sure that all chains are closed outside of the structure (including other chains);

int CloseChains_OUT( vector< vector<ChainAtom> > & vComp, double r = R_closeChains_DEF );
// CloseChain_OUT_Link

int CloseChains_2points( vector< vector<ChainAtom> > & vComp, double r = R_closeChains_DEF );
// CloseChain_F_Link_2points

int CloseChains_1point( vector< vector<ChainAtom> > & vComp, double r = R_closeChains_DEF );
// CloseChain_F_Link_1point

int CloseChains_1direction( vector< vector<ChainAtom> > & vComp );
// CloseChain_F_Link_1direction

// -------------------------------------------------------

int ChainReduce(vector<ChainAtom> & chain, bool closed = true);
// reduces <chain> using KMT algorithm - for closed chains it doesn't change the topology;
// <closed> causes that we threat <chain> as closed, with connected ends;
// returns the length of <chain> after reduction;
// (while KMT - if "bond is touching the triangle exactly on the border", then we treat it as it would be an intersection - so we don't delete the vertex)

int ChainsReduce(vector< vector<ChainAtom> > & vComp, bool closed = true);
// similar to ChainReduce(), but reduces chains from all components (<vComp>) simultaneously, we need it for links;
// returns sum of lengths of all components after reduction;

// -------------------------------------------------------

vector<Edge> ProjectChain(const vector<ChainAtom> & chain, int dir = 0, bool closed = true);
// projects <chain> into the plane according to chosen direction <dir> (i.e. the direction is defined by the point in array <fuleren>, fuleren[dir]);
// returns vector of Edges, <closed> causes that we add to this vector Edge connecting two ends of <chain>;


#endif


