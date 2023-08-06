#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <cmath>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

#include "tetrahedron.hpp"

// Current functions Feb/2020

std::vector<double> tetrahedron::_cprod(std::vector<double> a, std::vector<double> b) {
  std::vector<double> res(3);
  res[0] = a[1]*b[2]-a[2]*b[1];
  res[1] = a[2]*b[0]-a[0]*b[2];
  res[2] = a[0]*b[1]-a[1]*b[0];
  return res;
}
double tetrahedron::_dprod(std::vector<double> a, std::vector<double> b) {
  return a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
}

std::vector<std::vector<double>> tetrahedron::get_coor_intrs(   std::vector<std::vector<double> > c_tet,
                                                                std::vector<double> v_tet, std::vector<std::vector<unsigned> > v_pos,
                                                                unsigned int ph,  double thresh,
                                                                std::vector< unsigned > &l_theta ) {
// Calculation of intersections between the plane and the tetrahedron
  unsigned int n1;
  unsigned int n2;
  double theta;
  std::vector<std::vector<double> > c_theta(3);

  // local correspondence array between edges and nodes
  std::vector<std::vector< unsigned > > a_tet(6);
  for(unsigned int k=0; k < a_tet.size(); k++){ a_tet[k].resize(2); }
  a_tet[0][0]=0; a_tet[0][1]=1; a_tet[1][0]=0; a_tet[1][1]=3;
  a_tet[2][0]=0; a_tet[2][1]=2; a_tet[3][0]=1; a_tet[3][1]=3;
  a_tet[4][0]=1; a_tet[4][1]=2; a_tet[5][0]=3; a_tet[5][1]=2;

  for (unsigned int k = 0 ; k < 6 ; k++) {
    n1 = a_tet[k][0];
    n2 = a_tet[k][1];
    if(v_pos[n1][ph] != v_pos[n2][ph]) {
    // a linear interpolation ratio based on distance field values is taken as valid to locate the
    // coordinates of intersections in all directions.
    theta = (v_tet[n1]-thresh)/(v_tet[n1]-v_tet[n2]);
    for (unsigned int j=0; j < 3; j++) {
        c_theta[j].push_back( c_tet[j][n1] + ( c_tet[j][n2] - c_tet[j][n1] )*theta); }
        l_theta.push_back( k );  // the tet edge associated with each intersection is stored. It is useful later.
    }

    // check orientation of the connectivity
    if( c_theta[0].size() == 4) {
      // Compute V_02 v01 and V03
      // check that V_02xV_01 is not the same direction as V_02xV_03 to have 0-2 the diag
      // so if not, switch 1 and 2

      // STEP 0: save original c_theta
      std::vector<std::vector<double> > tmp;
      std::vector<unsigned> ltmp;
      tmp = c_theta;
      ltmp = l_theta;

      // STEP 1: first trial we spam 1 & 2
      std::vector<double> v01(3); v01[0] = c_theta[0][1] - c_theta[0][0]; v01[1] = c_theta[1][1] - c_theta[1][0]; v01[2] = c_theta[2][1] - c_theta[2][0];
      std::vector<double> v02(3); v02[0] = c_theta[0][2] - c_theta[0][0]; v02[1] = c_theta[1][2] - c_theta[1][0]; v02[2] = c_theta[2][2] - c_theta[2][0];
      std::vector<double> v03(3); v03[0] = c_theta[0][3] - c_theta[0][0]; v03[1] = c_theta[1][3] - c_theta[1][0]; v03[2] = c_theta[2][3] - c_theta[2][0];
      std::vector<double> cp21(3);
      std::vector<double> cp23(3);
      cp21 = _cprod(v02, v01);
      cp23 = _cprod(v02, v03);
      if( _dprod(cp21, cp23) > 0 ) {
        // swap 1 and 2
        c_theta[0][1] = tmp[0][2];
        c_theta[1][1] = tmp[1][2];
        c_theta[2][1] = tmp[2][2];
        c_theta[0][2] = tmp[0][1];
        c_theta[1][2] = tmp[1][1];
        c_theta[2][2] = tmp[2][1];
        l_theta[1] = ltmp[2];
        l_theta[2] = ltmp[1];
      }

      // STEP 3: second trial if still wrong we should have have swapped 1 & 3
      v01[0] = c_theta[0][1] - c_theta[0][0]; v01[1] = c_theta[1][1] - c_theta[1][0]; v01[2] = c_theta[2][1] - c_theta[2][0];
      v02[0] = c_theta[0][2] - c_theta[0][0]; v02[1] = c_theta[1][2] - c_theta[1][0]; v02[2] = c_theta[2][2] - c_theta[2][0];
      v03[0] = c_theta[0][3] - c_theta[0][0]; v03[1] = c_theta[1][3] - c_theta[1][0]; v03[2] = c_theta[2][3] - c_theta[2][0];
      cp21 = _cprod(v02, v01);
      cp23 = _cprod(v02, v03);
      if( _dprod(cp21, cp23) > 0 ) {
        // back to origin
        c_theta[0][1] = tmp[0][1];
        c_theta[1][1] = tmp[1][1];
        c_theta[2][1] = tmp[2][1];
        l_theta[1] = ltmp[1]; 
        // c_theta[0][2] = tmp[0][2];
        // c_theta[1][2] = tmp[1][2];
        // c_theta[2][2] = tmp[2][2];
        // swap 1 & 3
        c_theta[0][2] = tmp[0][3];
        c_theta[1][2] = tmp[1][3];
        c_theta[2][2] = tmp[2][3];
        c_theta[0][3] = tmp[0][2];
        c_theta[1][3] = tmp[1][2];
        c_theta[2][3] = tmp[2][2];
        l_theta[2] = ltmp[3];  
        l_theta[3] = ltmp[2];  
      }
    }
  }
  return c_theta;
}


std::vector<double> tetrahedron::get_interface( std::vector<std::vector<double> > c_tet, std::vector<std::vector<double> > c_theta,
                                                std::vector<std::vector<unsigned> > v_pos, unsigned int fd ) {
// Calculation of interface orientation
  double u1, u2, u3, v1, v2, v3, n1, n2, n3;
  n1 = 1.0; n2 = 0.0; n3 = 0.0;
  double w1, w2, w3, ntst;


  // normal obtained through cross product having 2 vectors describing the cutting plane.
  u1 = c_theta[0][1] - c_theta[0][0]; u2 = c_theta[1][1] - c_theta[1][0]; u3 = c_theta[2][1] - c_theta[2][0];
  v1 = c_theta[0][2] - c_theta[0][0]; v2 = c_theta[1][2] - c_theta[1][0]; v3 = c_theta[2][2] - c_theta[2][0];
  n1 = u2*v3-u3*v2; n2 = u3*v1-u1*v3; n3 = u1*v2-u2*v1;

  // this normal must point out to the (+) domain. A test node on the tet is taken to assess this and to correct if needed.
  w1 = c_tet[0][0] - c_theta[0][0]; w2 = c_tet[1][0] - c_theta[1][0]; w3 = c_tet[2][0] - c_theta[2][0];
  ntst = w1*n1 + w2*n2 + w3*n3;
  if( ((v_pos[0][fd]>0)&&(ntst<=0.0))||((v_pos[0][fd]==0)&&(ntst>=0.0)) ){
    n1 = -n1; n2 = -n2; n3 = -n3; }

  double norm = sqrt(pow(n1,2)+pow(n2,2)+pow(n3,2));
  std::vector<double> interface(4); // [n1, n2, n3]
  interface[0] = n1/norm;
  interface[1] = n2/norm;
  interface[2] = n3/norm;

  // compute the surface
  if( c_theta[0].size() == 3) {
    // surface is 0.5 times cross product of 2 vecotrs

    // YES we know we comute it already just above... but it's fiiiine
    double u1_1 = c_theta[0][1] - c_theta[0][0]; double u2_1 = c_theta[1][1] - c_theta[1][0]; double u3_1 = c_theta[2][1] - c_theta[2][0];
    double v1_1 = c_theta[0][2] - c_theta[0][0]; double v2_1 = c_theta[1][2] - c_theta[1][0]; double v3_1 = c_theta[2][2] - c_theta[2][0];
    double n1_1 = u2_1*v3_1-u3_1*v2_1; double n2_1 = u3_1*v1_1-u1_1*v3_1; double n3_1 = u1_1*v2_1-u2_1*v1_1;

    double s1 = 0.5 * sqrt( pow(n1_1, 2) + pow(n2_1, 2) + pow(n3_1, 2) );

    interface[3] = s1;

  } else if( c_theta[0].size() == 4) {
    // split surface in 2 triangles

    double u1_1 = c_theta[0][1] - c_theta[0][0]; double u2_1 = c_theta[1][1] - c_theta[1][0]; double u3_1 = c_theta[2][1] - c_theta[2][0];
    double v1_1 = c_theta[0][2] - c_theta[0][0]; double v2_1 = c_theta[1][2] - c_theta[1][0]; double v3_1 = c_theta[2][2] - c_theta[2][0];
    double n1_1 = u2_1*v3_1-u3_1*v2_1; double n2_1 = u3_1*v1_1-u1_1*v3_1; double n3_1 = u1_1*v2_1-u2_1*v1_1;

    double s1 = 0.5 * sqrt( pow(n1_1, 2) + pow(n2_1, 2) + pow(n3_1, 2) );

    double u1_2 = c_theta[0][1] - c_theta[0][3]; double u2_2 = c_theta[1][1] - c_theta[1][3]; double u3_2 = c_theta[2][1] - c_theta[2][3];
    double v1_2 = c_theta[0][2] - c_theta[0][3]; double v2_2 = c_theta[1][2] - c_theta[1][3]; double v3_2 = c_theta[2][2] - c_theta[2][3];
    double n1_2 = u2_2*v3_2-u3_2*v2_2; double n2_2 = u3_2*v1_2-u1_2*v3_2; double n3_2 = u1_2*v2_2-u2_2*v1_2;

    double s2 = 0.5 * sqrt( pow(n1_2, 2) + pow(n2_2, 2) + pow(n3_2, 2) );

    interface[3] = s1+s2;

  } else {
    std::cout << "wtf??? how many points to you want in your intersection? " << c_theta[0].size() << " given" << std::endl;
    interface[3] = -1.0;
  }

  return interface;

}

double tetrahedron::get_sub_volume( std::vector<std::vector<double> > c_tet, std::vector<std::vector<double> > c_theta,
		       unsigned int fd, std::vector<std::vector<unsigned> > v_pos, std::vector< unsigned > l_theta ) {
// Unified routine for tet subvolume calculation
  std::vector<std::vector<double>> tet_ref(3);
  std::vector<unsigned> np;
  std::vector<unsigned> nm;
  std::vector<std::vector<unsigned>> prmsh(3);
  double vm = 0.0;
  unsigned int ii = 0, jj = 0;

  // Recovering node position on +, - domains
  for(unsigned int k=0; k < 4; k++) { if(v_pos[k][fd] > 0) { np.push_back(k); } else{ nm.push_back(k); } }
  std::vector<std::vector< unsigned > > vx_tet(4);
  for(unsigned int k=0; k < vx_tet.size(); k++){ vx_tet[k].resize(3); }
  vx_tet[0][0]=0; vx_tet[0][1]=2; vx_tet[0][2]=1;
  vx_tet[1][0]=0; vx_tet[1][1]=3; vx_tet[1][2]=4;
  vx_tet[2][0]=2; vx_tet[2][1]=4; vx_tet[2][2]=5;
  vx_tet[3][0]=1; vx_tet[3][1]=3; vx_tet[3][2]=5;

  // 3 plane intersections case : subtet + irregular triangular prism scenario / 3-1 node partition
  // Approach: form a tet by gathering the three intersection nodes of the cutting surface
  // and the solitary tet node. if the solitary node is on the (-) domain, this is the desired volume.
  // If not, the desired volume is obtained by simple substraction to the big tet volume.
  if( c_theta[0].size() == 3 ){
    for(unsigned int j=0; j < 3; j++) {
      for(unsigned int k=0; k < 3; k++){ tet_ref[k].push_back( c_theta[k][j] ); } }
    if( nm.size() == 1 ){
      for(unsigned int k=0; k < 3; k++){ tet_ref[k].push_back( c_tet[k][nm[0]] ); }
      vm = get_volume_tet( tet_ref );
    }
    else{
      for(unsigned int k=0; k < 3; k++){ tet_ref[k].push_back( c_tet[k][np[0]] ); }
      vm = get_volume_tet( c_tet ) - get_volume_tet( tet_ref );
    }
  }
  else{
  // 4 plane intersections case : 2 irregular triangular prisms scenario / 2-2 node partition
  // Approach: the irregular prism on (-) is to be meshed with three tets (Euclid book XII, prop. 7)
  // The prmsh[tet#][node#] vector contains the node ordering for each tet *beware, it mixes numbering
  // from the big tet nodes and local quadrilateral cutting surface nodes knowing beforehand*
  // One of the diagonals of the quadrilateral cut surface must be identified for this purpose.
      prmsh[0].push_back( nm[0] ); prmsh[1].push_back( nm[1] );
      prmsh[2].push_back( nm[0] ); prmsh[2].push_back( nm[1] );
      for(unsigned int k=0; k < 4; k++){
	for(unsigned int j=0; j < 3; j++){
	  if( l_theta[k] == vx_tet[nm[0]][j] ) {
	    prmsh[0].push_back( k );
	    for(unsigned int i=0; i < 3; i++){
              if( l_theta[k] == vx_tet[np[0]][i] ) { ii = k; }	// Saving diagonal vertex
            }
          }
          else if( l_theta[k] == vx_tet[nm[1]][j] ){
	    prmsh[1].push_back( k );
            for(unsigned int i=0; i < 3; i++){
              if( l_theta[k] == vx_tet[np[1]][i] ) { jj = k; }	// Saving diagonal vertex
	    }
          }
        }
      }
      prmsh[1].push_back( ii ); prmsh[0].push_back( jj );
      prmsh[2].push_back( ii ); prmsh[2].push_back( jj );

      // Coordinates are retrieved to build a dummy tet: tet_ref[][], using prmsh[][]
      // 1st tet processing
      for(unsigned int i=0; i < 3; i++){ tet_ref[i].push_back( c_tet[i][prmsh[0][0]] ) ; }
      for(unsigned int k=0; k < 3; k++){
        for(unsigned int j=0; j < 3; j++){ tet_ref[j].push_back( c_theta[j][prmsh[0][k+1]] ); }
      }
      vm += get_volume_tet( tet_ref );
      // 2nd tet processing
      for(unsigned int i=0; i < 3; i++){ tet_ref[i][0] = c_tet[i][prmsh[1][0]] ; }
      for(unsigned int k=0; k < 3; k++){
        for(unsigned int j=0; j < 3; j++){ tet_ref[j][k+1] = c_theta[j][prmsh[1][k+1]] ; }
      }
      vm += get_volume_tet( tet_ref );
      // 3nd tet processing
      for(unsigned int k=0; k < 2; k++){
        for(unsigned int j=0; j < 3; j++){ tet_ref[j][k] = c_tet[j][prmsh[2][k]] ; }
      }
      for(unsigned int k=0; k < 2; k++){
        for(unsigned int j=0; j < 3; j++){ tet_ref[j][k+2] = c_theta[j][prmsh[2][k+2]] ; }
      }
      vm += get_volume_tet( tet_ref );

  }
  return vm;
}

double tetrahedron::get_volume_tet( std::vector<std::vector<double> > c_tet ) {
  double xa = c_tet[0][0]; double ya = c_tet[1][0]; double za = c_tet[2][0];
  double xb = c_tet[0][1]; double yb = c_tet[1][1]; double zb = c_tet[2][1];
  double xc = c_tet[0][2]; double yc = c_tet[1][2]; double zc = c_tet[2][2];
  double xd = c_tet[0][3]; double yd = c_tet[1][3]; double zd = c_tet[2][3];
  double ax = xd-xa; double bx = xd-xb; double cx = xd-xc;
  double ay = yd-ya; double by = yd-yb; double cy = yd-yc;
  double az = zd-za; double bz = zd-zb; double cz = zd-zc;
  double pvx = by*cz - bz*cy;
  double pvy = bz*cx - bx*cz;
  double pvz = bx*cy - by*cx;
  //std::cout << "volu: " << std::abs(ax*pvx+ay*pvy+az*pvz)/6.0 << std::endl;
  return std::abs(ax*pvx+ay*pvy+az*pvz)/6.0;
}

// OLD FUNCTIONS

// std::vector<double> tetrahedron::get_interface( std::vector<std::vector<double> > c_tet, std::vector<double> theta_edge, std::vector<int> me ) {
//   std::vector<std::vector<double> > c_theta; // coordinates of edge intersection
//   double u1, u2, u3, v1, v2, v3, n1, n2, n3; // compute normal with scalar product
//   n1 = 1.0; n2 = 0.0; n3 = 0.0;              // default orientation value
//   unsigned int isw = 0;                      // configuration
//   double sv = 0.0;                           // sub volume
//
//   // CASE 1 NODE ISOLATED
//   if ( (me[0]+me[1]+me[2]+me[3]+me[4]+me[5]) == 21 || // 1 node  in the paste and 3 in the aggregates
//        (me[0]+me[1]+me[2]+me[3]+me[4]+me[5]) == 12 ){ // 3 nodes in the paste and 1 in the aggregates
//     if ( ( me[0] + me[1] + me[2]) == 9 ){ // A isolated
//       isw = 0; c_theta = get_coor_theta_1n( c_tet, theta_edge, isw );
//       u1 = c_theta[0][2] - c_theta[0][0]; u2 = c_theta[1][2] - c_theta[1][0]; u3 = c_theta[2][2] - c_theta[2][0];
//       v1 = c_theta[0][1] - c_theta[0][0]; v2 = c_theta[1][1] - c_theta[1][0]; v3 = c_theta[2][1] - c_theta[2][0];
//       n1 = u3*v2-u2*v3; n2 = u1*v3-u3*v1; n3 = u2*v1-u1*v2;
//     } // end if sum = 9 A
//     else if ( (me[3] + me[0] + me[4]) == 9 ){ // B isolated
//       isw = 1; c_theta = get_coor_theta_1n( c_tet, theta_edge, isw );
//       u1 = c_theta[0][1] - c_theta[0][2]; u2 = c_theta[1][1] - c_theta[1][2]; u3 = c_theta[2][1] - c_theta[2][2];
//       v1 = c_theta[0][0] - c_theta[0][2]; v2 = c_theta[1][0] - c_theta[1][2]; v3 = c_theta[2][0] - c_theta[2][2];
//       n1 = u3*v2-u2*v3; n2 = u1*v3-u3*v1; n3 = u2*v1-u1*v2;
//     } // end if sum = 9 B
//     else if ( (me[4] + me[5] + me[2]) == 9 ){ // C isolated
//       isw = 2; c_theta = get_coor_theta_1n( c_tet, theta_edge, isw );
//       u1 = c_theta[0][1] - c_theta[0][0]; u2 = c_theta[1][1] - c_theta[1][0]; u3 = c_theta[2][1] - c_theta[2][0];
//       v1 = c_theta[0][2] - c_theta[0][0]; v2 = c_theta[1][2] - c_theta[1][0]; v3 = c_theta[2][2] - c_theta[2][0];
//       n1 = u3*v2-u2*v3; n2 = u1*v3-u3*v1; n3 = u2*v1-u1*v2;
//     } // end if sum = 9 C
//     else if ( (me[1] + me[3] + me[5]) == 9 ){ // D isolated
//       isw = 3; c_theta = get_coor_theta_1n( c_tet, theta_edge, isw );
//       u1 = c_theta[0][0] - c_theta[0][1]; u2 = c_theta[1][0] - c_theta[1][1]; u3 = c_theta[2][0] - c_theta[2][1];
//       v1 = c_theta[0][2] - c_theta[0][1]; v2 = c_theta[1][2] - c_theta[1][1]; v3 = c_theta[2][2] - c_theta[2][1];
//       n1 = u3*v2-u2*v3; n2 = u1*v3-u3*v1; n3 = u2*v1-u1*v2;
//     } else { std::cout << "WARNING: no sub case found to compute interface orientation."  << std::endl; } // end if sum = 9 D
//     sv = get_sub_volume_1n( c_tet, c_theta, isw );
//     if ( (me[0]+me[1]+me[2]+me[3]+me[4]+me[5]) == 12 ){ // switch orientation vector
//       n1 = -n1; n2 = -n2; n3 = -n3;
//     }
//   }
//
//   // CASE 2 NODES ISOLATED
//   else if ( (me[0]+me[1]+me[2]+me[3]+me[4]+me[5]) == 17 ) {
//     if ( ((me[1]+me[0]+me[2])==10) && ((me[0]+me[3]+me[4])==10) ) { // A and B in aggregates
//       isw = 0; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
//       u1 = c_theta[0][0] - c_theta[0][1]; u2 = c_theta[1][0] - c_theta[1][1]; u3 = c_theta[2][0] - c_theta[2][1];
//       v1 = c_theta[0][3] - c_theta[0][1]; v2 = c_theta[1][3] - c_theta[1][1]; v3 = c_theta[2][3] - c_theta[2][1];
//       n1 = u2*v3-u3*v2; n2 = u3*v1-u1*v3; n3 = u1*v2-u2*v1;
//     }
//     else if ( ((me[1]+me[0]+me[2])==7) && ((me[0]+me[3]+me[4])==7) ) { // A and B in paste
//       isw = 1; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
//       u1 = c_theta[0][0] - c_theta[0][1]; u2 = c_theta[1][0] - c_theta[1][1]; u3 = c_theta[2][0] - c_theta[2][1];
//       v1 = c_theta[0][3] - c_theta[0][1]; v2 = c_theta[1][3] - c_theta[1][1]; v3 = c_theta[2][3] - c_theta[2][1];
//       n1 = -1.0*(u2*v3-u3*v2); n2 = -1.0*(u3*v1-u1*v3); n3 = -1.0*(u1*v2-u2*v1);
//     }
//     else if ( ((me[0]+me[3]+me[4])==10) && ((me[4]+me[5]+me[2])==10) ) { // B and C in aggregates
//       isw = 2; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
//       u1 = c_theta[0][1] - c_theta[0][0]; u2 = c_theta[1][1] - c_theta[1][0]; u3 = c_theta[2][1] - c_theta[2][0];
//       v1 = c_theta[0][3] - c_theta[0][0]; v2 = c_theta[1][3] - c_theta[1][0]; v3 = c_theta[2][3] - c_theta[2][0];
//       n1 = u2*v3-u3*v2; n2 = u3*v1-u1*v3; n3 = u1*v2-u2*v1;
//     }
//     else if ( ((me[0]+me[3]+me[4])==7) && ((me[4]+me[5]+me[2])==7) ) { // B and C in paste
//       isw = 3; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
//       u1 = c_theta[0][1] - c_theta[0][0]; u2 = c_theta[1][1] - c_theta[1][0]; u3 = c_theta[2][1] - c_theta[2][0];
//       v1 = c_theta[0][3] - c_theta[0][0]; v2 = c_theta[1][3] - c_theta[1][0]; v3 = c_theta[2][3] - c_theta[2][0];
//       n1 = -1.0*(u2*v3-u3*v2); n2 = -1.0*(u3*v1-u1*v3); n3 = -1.0*(u1*v2-u2*v1);
//     }
//     else if ( ((me[1]+me[3]+me[5])==10) && ((me[0]+me[3]+me[4])==10) ) { // B and D in aggregates
//       isw = 4; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
//       u1 = c_theta[0][0] - c_theta[0][2]; u2 = c_theta[1][0] - c_theta[1][2]; u3 = c_theta[2][0] - c_theta[2][2];
//       v1 = c_theta[0][3] - c_theta[0][2]; v2 = c_theta[1][3] - c_theta[1][2]; v3 = c_theta[2][3] - c_theta[2][2];
//       n1 = u2*v3-u3*v2; n2 = u3*v1-u1*v3; n3 = u1*v2-u2*v1;
//     }
//     else if ( ((me[1]+me[3]+me[5])==7) && ((me[0]+me[3]+me[4])==7) ) { // B and D in the paste
//       isw = 5; c_theta = get_coor_theta_2n( c_tet, theta_edge, isw );
//       u1 = c_theta[0][0] - c_theta[0][2]; u2 = c_theta[1][0] - c_theta[1][2]; u3 = c_theta[2][0] - c_theta[2][2];
//       v1 = c_theta[0][3] - c_theta[0][2]; v2 = c_theta[1][3] - c_theta[1][2]; v3 = c_theta[2][3] - c_theta[2][2];
//       n1 = -1.0*(u2*v3-u3*v2); n2 = -1.0*(u3*v1-u1*v3); n3 = -1.0*(u1*v2-u2*v1);
//     }
//     else { std::cout << "WARNING : no sub case found to compute interface orientation."  << std::endl; }
//     sv = get_sub_volume_2n( c_tet, c_theta, isw );
//   } else {
//     std::cout << "[ERROR] no case found to compute interface orientation (sum="+std::to_string( me[0]+me[1]+me[2]+me[3]+me[4]+me[5] )+")" << std::endl;
//     exit(EXIT_FAILURE);
//     std::cout << "         it can come from the threshold being equal to the field value " << std::endl;
//   } // end if 17
//
//   double norm = sqrt(pow(n1,2)+pow(n2,2)+pow(n3,2));
//   std::vector<double> interface(4); // [V-, n1, n2, nz]
//   interface[0] = sv;
//   interface[1] = n1/norm;
//   interface[2] = n2/norm;
//   interface[3] = n3/norm;
//   return interface;
// }
//
// std::vector<std::vector<double> > tetrahedron::get_coor_theta_1n( std::vector<std::vector<double> > c_tet, std::vector<double> theta_edge, unsigned int isw) {
//   std::vector<std::vector<double> > c_theta(3);
//   if ( isw==0 ) { // node A is alone
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][1] - c_tet[k][0] )*theta_edge[0] ); } // AB
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][3] - c_tet[k][0] )*theta_edge[1] ); } // AD
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][2] - c_tet[k][0] )*theta_edge[2] ); } // AC
//   }
//   if ( isw==1 ) { // node B is alone
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][3] - c_tet[k][1] )*theta_edge[3] ); } // BD
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][1] - c_tet[k][0] )*theta_edge[0] ); } // AB
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][2] - c_tet[k][1] )*theta_edge[4] ); } // BC
//   }
//   if ( isw==2 ) { // node C is alone
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][2] - c_tet[k][1] )*theta_edge[4] ); } // BC
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][3] + ( c_tet[k][2] - c_tet[k][3] )*theta_edge[5] ); } // DC
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][2] - c_tet[k][0] )*theta_edge[2] ); } // AC
//   }
//   if ( isw==3 ) { // node D is alone
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][3] - c_tet[k][0] )*theta_edge[1] ); } // AD
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][3] - c_tet[k][1] )*theta_edge[3] ); } // BD
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][3] + ( c_tet[k][2] - c_tet[k][3] )*theta_edge[5] ); } // DC
//   }
//   return c_theta;
// }
//
// std::vector<std::vector<double> > tetrahedron::get_coor_theta_2n( std::vector<std::vector<double> > c_tet, std::vector<double> theta_edge, unsigned int isw) {
//   std::vector<std::vector<double> > c_theta(3);
//   if ( isw==0 || isw==1 ) { //AD, AC, BD and BC are cut
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][3] - c_tet[k][0] )*theta_edge[1] ); } // AD
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][2] - c_tet[k][0] )*theta_edge[2] ); } // AC
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][3] - c_tet[k][1] )*theta_edge[3] ); } // BD
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][2] - c_tet[k][1] )*theta_edge[4] ); } // BC
//   }
//   if ( isw==2 || isw==3 ) { //AB, BD, DC and AC are cut
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][1] - c_tet[k][0] )*theta_edge[0] ); } // AB
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][3] - c_tet[k][1] )*theta_edge[3] ); } // BD
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][3] + ( c_tet[k][2] - c_tet[k][3] )*theta_edge[5] ); } // DC
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][2] - c_tet[k][0] )*theta_edge[2] ); } // AC
//   }
//   if ( isw==4 || isw==5 ) { // AD, DC, AB and BC are cut
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][3] - c_tet[k][0] )*theta_edge[1] ); } // AD
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][3] + ( c_tet[k][2] - c_tet[k][3] )*theta_edge[5] ); } // DC
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][0] + ( c_tet[k][1] - c_tet[k][0] )*theta_edge[0] ); } // AB
//     for (unsigned int k=0; k < 3; k++) { c_theta[k].push_back( c_tet[k][1] + ( c_tet[k][2] - c_tet[k][1] )*theta_edge[4] ); } // BC
//   }
//   return c_theta;
// }
//
//
// double tetrahedron::get_sub_volume_1n( std::vector<std::vector<double> > c_tet, std::vector<std::vector<double> > c_theta, unsigned int isw) {
//   int s = 0;              // isw = 0 : A is isolated and B,D and C together -> shift of s=0
//   if      (isw==1) s = 1; // isw = 1 : B is isolated and A,D and C together -> shift of s=1
//   else if (isw==2) s = 2; // isw = 2 : C is isolated and A,D and B together -> shift of s=2
//   else if (isw==3) s = 3; // isw = 3 : D is isolated and A,C and B together -> shift of s=3
//   else if (isw>3) std::cout << "[tetrahedron::get_sub_volume] Error: unkown isolated case. isw = " << isw << std::endl;
//   double xa = c_theta[0][0]; double ya = c_theta[1][0]; double za = c_theta[2][0];
//   double xb = c_theta[0][1]; double yb = c_theta[1][1]; double zb = c_theta[2][1];
//   double xc = c_theta[0][2]; double yc = c_theta[1][2]; double zc = c_theta[2][2];
//   double xd =   c_tet[0][s]; double yd =   c_tet[1][s]; double zd =   c_tet[2][s];
//   double ax = xd-xa; double bx = xd-xb; double cx = xd-xc;
//   double ay = yd-ya; double by = yd-yb; double cy = yd-yc;
//   double az = zd-za; double bz = zd-zb; double cz = zd-zc;
//   double pvx = by*cz - bz*cy;
//   double pvy = bz*cx - bx*cz;
//   double pvz = bx*cy - by*cx;
//   //  std::cout << "sv1n: " << std::abs(ax*pvx+ay*pvy+az*pvz)/6.0 << std::endl;
//   return std::abs(ax*pvx+ay*pvy+az*pvz)/6.0;
// }
//
// double tetrahedron::get_sub_volume_2n( std::vector<std::vector<double> > c_tet, std::vector<std::vector<double> > c_theta, unsigned int isw) {
//   // STEP 0 - Define all 6 vertices
//   // is isw 0 || 1 : c_theta correspond to AD AC BD and BC that we are going to call edge 1 2 3 and 4
//   // is isw 2 || 3 : c_theta correspond to AB BD DC and AC that we are going to call edge 1 2 3 and 4
//   // is isw 4 || 5 : c_theta correspond to AD DC AB and BC that we are going to call edge 1 2 3 and 4
//   unsigned int s1, s2;
//   if ( (isw==0) || (isw==1) ) { s1=0; s2=1; } // vertice 1 and 2 of tetrahedron are A and B respectively
//   if ( (isw==2) || (isw==3) ) { s1=1; s2=2; } // vertice 1 and 2 of tetrahedron are B and C respectively
//   if ( (isw==4) || (isw==5) ) { s1=1; s2=3; } // vertice 1 and 2 of tetrahedron are B and D respectively
//   double x1 = c_theta[0][0];  double y1 = c_theta[1][0];  double z1 = c_theta[2][0];  // point on edge 1
//   double x2 = c_theta[0][1];  double y2 = c_theta[1][1];  double z2 = c_theta[2][1];  // point on edge 2
//   double x3 = c_theta[0][2];  double y3 = c_theta[1][2];  double z3 = c_theta[2][2];  // point on edge 3
//   double x4 = c_theta[0][3];  double y4 = c_theta[1][3];  double z4 = c_theta[2][3];  // point on edge 4
//   double xa =   c_tet[0][s1]; double ya =   c_tet[1][s1]; double za =   c_tet[2][s1]; // vertice A of origin tetrahedron
//   double xb =   c_tet[0][s2]; double yb =   c_tet[1][s2]; double zb =   c_tet[2][s2]; // vertice B of origin tetrahedron
//   // STEP 1 - Define a "centroid"
//   double xo = (x1+x2+x3+x4+xa+xb)/6.0;
//   double yo = (y1+y2+y3+y4+ya+yb)/6.0;
//   double zo = (z1+z2+z3+z4+za+zb)/6.0;
//   // STEP 2 - compute volume of each 6 tetrahedrons
//   std::vector<std::vector<double> > ctmp(3);
//   for( unsigned int i=0; i<3; i++ ) { ctmp[i].resize(4); }
//   // tetrehedron 1 : A13O
//   ctmp[0][0] = xa; ctmp[1][0] = ya; ctmp[2][0] = za;
//   ctmp[0][1] = x1; ctmp[1][1] = y1; ctmp[2][1] = z1;
//   ctmp[0][2] = x3; ctmp[1][2] = y3; ctmp[2][2] = z3;
//   ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
//   double v1 = get_volume_tet( ctmp );
//   // tetrehedron 2 : A3BO
//   ctmp[0][0] = xa; ctmp[1][0] = ya; ctmp[2][0] = za;
//   ctmp[0][1] = x3; ctmp[1][1] = y3; ctmp[2][1] = z1;
//   ctmp[0][2] = xb; ctmp[1][2] = yb; ctmp[2][2] = z3;
//   ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
//   double v2 = get_volume_tet( ctmp );
//   // tetrehedron 3 : 1A2O
//   ctmp[0][0] = x1; ctmp[1][0] = y1; ctmp[2][0] = z1;
//   ctmp[0][1] = xa; ctmp[1][1] = ya; ctmp[2][1] = za;
//   ctmp[0][2] = x2; ctmp[1][2] = y2; ctmp[2][2] = z2;
//   ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
//   double v3 = get_volume_tet( ctmp );
//   // tetrehedron 4 : 34BO
//   ctmp[0][0] = x3; ctmp[1][0] = y3; ctmp[2][0] = z3;
//   ctmp[0][1] = x4; ctmp[1][1] = y4; ctmp[2][1] = z4;
//   ctmp[0][2] = xb; ctmp[1][2] = yb; ctmp[2][2] = zb;
//   ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
//   double v4 = get_volume_tet( ctmp );
//   // tetrehedron 5 : AB2O
//   ctmp[0][0] = xa; ctmp[1][0] = ya; ctmp[2][0] = za;
//   ctmp[0][1] = xb; ctmp[1][1] = yb; ctmp[2][1] = zb;
//   ctmp[0][2] = x2; ctmp[1][2] = y2; ctmp[2][2] = z2;
//   ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
//   double v5 = get_volume_tet( ctmp );
//   // tetrehedron 6 : B42O
//   ctmp[0][0] = xb; ctmp[1][0] = yb; ctmp[2][0] = zb;
//   ctmp[0][1] = x4; ctmp[1][1] = y4; ctmp[2][1] = z4;
//   ctmp[0][2] = x2; ctmp[1][2] = y2; ctmp[2][2] = z2;
//   ctmp[0][3] = xo; ctmp[1][3] = yo; ctmp[2][3] = zo;
//   double v6 = get_volume_tet( ctmp );
//   // std::cout << "[DEBUG] x1: " << "[" << x1 << " " << y1 << " " << z1 << "]"  << std::endl;
//   // std::cout << "[DEBUG] x2: " << "[" << x2 << " " << y2 << " " << z2 << "]"  << std::endl;
//   // std::cout << "[DEBUG] x3: " << "[" << x3 << " " << y3 << " " << z3 << "]"  << std::endl;
//   // std::cout << "[DEBUG] x4: " << "[" << x4 << " " << y4 << " " << z4 << "]"  << std::endl;
//   // std::cout << "[DEBUG] xa: " << "[" << xa << " " << ya << " " << za << "]"  << std::endl;
//   // std::cout << "[DEBUG] xb: " << "[" << xb << " " << yb << " " << zb << "]"  << std::endl;
//   // std::cout << "[DEBUG] xo: " << "[" << xo << " " << yo << " " << zo << "]"  << std::endl;
//   // std::cout << "[DEBUG] v1  = " << v1 << std::endl;
//   // std::cout << "[DEBUG] v2  = " << v2 << std::endl;
//   // std::cout << "[DEBUG] v3  = " << v3 << std::endl;
//   // std::cout << "[DEBUG] v4  = " << v4 << std::endl;
//   // std::cout << "[DEBUG] v5  = " << v5 << std::endl;
//   // std::cout << "[DEBUG] v6  = " << v6 << std::endl;
//   // std::cout << "[DEBUG] sum = " << v1+v2+v3+v4+v5+v6 << std::endl;
//   // STEP 3 - return the sub volume
//   // std::cout << "sv2n: " << v1+v2+v3+v4+v5+v6 << std::endl;
//   return v1+v2+v3+v4+v5+v6;
// }
