#include "mex.h"
#include <cmath>

#define p(i,j) pp[i+len*j]
#define f(i,j) ff[i+len*j]
#define g(i,j) gg[i+len*j]

double objective(double *, int, double *, double *, double *, int, int );
double gradNewt(double *, double *, int, double *, double *, double *,int, int, double );
double newton(double *, double*, int, double *, double *, double *, int, int, double );

const int nS = 20;
#define DBL_EPSILON 1e-10

void mexFunction( int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]){
    /*  create a pointer to the input matrix x */
    double * x = mxGetPr(prhs[0]);
    
    /*  create a pointer to the input matrix x */
    double * s = mxGetPr(prhs[1]);
    
    /*  create a pointer to the input matrix x */
    int W = (int) mxGetScalar(prhs[2]);
    
    /*  create a pointer to the input matrix f */
    double * ff = mxGetPr(prhs[3]);
    
    /*  create a pointer to the input matrix g */
    double * gg = mxGetPr(prhs[4]);
    
    /*  create a pointer to the input matrix p */
    double * pp = mxGetPr(prhs[5]);
    
    /*  get the dimensions of the matrix input s */
    int len = (int)mxGetM(prhs[0]);
    int nT = len/W;
    int M = (int)mxGetN(prhs[3]);
    
    /*  create a C pointer to a copy of the output matrix */
    double *sol;	
    plhs[0] = mxCreateDoubleMatrix(len, 1, mxREAL);
    sol = mxGetPr(plhs[0]);
    
    /*  Main Program */
    double m = 0, mm = 0, obj=0, objS= 0, gamma=0, gam = 0;
    int i = 0, j = 0;
    
    // The Linesearch code is here
    double *z = new double[len];
    double *y = new double[len];
    for(i=0; i<len; i++){ z[i] = s[i] - x[i]; }
    
    gamma = 0;
    objS = objective(x, W, ff, gg, pp, nT, M);
    for(j=1; j<=nS; j++){
        gam = j/(double(nS));
        // Compute the vector
        for(i=0; i<len; i++){  y[i] = x[i] + gam*z[i];   }
        // Compute the objective
        obj = objective(y, W, ff, gg, pp, nT, M);
        // Decision
        if( obj < objS ){
            gamma = gam;
            objS = obj;
        }
    }
    //mexPrintf("%f\t%f.\n", objS, gamma);
    
    // Final refinement
    gamma = newton(x, s, W, ff, gg, pp,  nT, M, gamma);
    for(i=0; i<len; i++){  sol[i] = x[i] + gamma*z[i];   }
    
    delete[] z;
    delete[] y;
    return;
}
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% */
inline double objective(double * x, int W, double * ff, double *gg, double *pp, int nT, int M){
    double m = 0, fx = 0, px = 0, mm = 0;
    int i = 0, j = 0, k = 0, len = W*nT;
    
    for (i=0; i<nT; i++){
        for(k=0; k<M; k++){
            mm = 0;
            for (j=0; j<W; j++){
                mm += g(W*i+j, k)*x[W*i+j];
                fx += f(W*i+j, k)*x[W*i+j];
                px += p(W*i+j, k)*x[W*i+j];
            }
            m += mm*mm;
        }
    }
    return m/(fx*fx) + m/(px*px);
}
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% */
inline double newton(double *x, double*s, int W, double *ff, double *gg, double *pp,  int nT, int M, double gamma){
    int i=0, maxIter = 50;
    double ep = 1.0e-3;
    double gammaNew = 0;
    for (i=0; i< maxIter; i++){
        gammaNew = gamma - gradNewt(x, s, W, ff, gg, pp, nT, M, gamma);
        if (gammaNew < 0){
            gammaNew = 0;
        }else if (gammaNew > 1) {
            gammaNew = 1;
        }
        if(fabs(gammaNew - gamma) < ep){
            break;
        }
        gamma = gammaNew;
    }
    return gamma;
}
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% */
inline double gradNewt(double *x, double*s, int W, double *ff, double *gg, double*pp, int nT, int M, double gamma){
    double obj = 0, grad = 0;
    int i=0, j=0, k=0, len = W*nT;
    double m1=0, m2=0, m3=0, gy=0, gz=0, a2=0, a1=0, b2=0, b1=0;
    // Compute y and z
    double *y = new double[W*nT];
    double *z = new double[W*nT];
    for (i=0; i<nT; i++){
        for (j=0; j<W; j++){
            y[W*i+j] = x[W*i+j] + gamma*(s[W*i+j] - x[W*i+j]);
            z[W*i+j] = s[W*i+j] - x[W*i+j];
        }
    }
    
    for (i=0; i<nT; i++){
        for (k=0; k<M; k++){
            gy = 0;   gz = 0;
            for (j=0; j<W; j++){
                gy += g(W*i+j, k)*y[W*i+j];
                gz += g(W*i+j, k)*z[W*i+j];
                
                a1 += f(W*i+j, k)*y[W*i+j];
                a2 += f(W*i+j, k)*z[W*i+j];
                b1 += p(W*i+j, k)*y[W*i+j];
                b2 += p(W*i+j, k)*z[W*i+j];
            }
            m1 += (gz*gz);
            m2 += (gy*gz);
            m3 += (gy*gy);
        }
    }
    
    obj = 2*m2/(a1*a1) - 2*m3*a2/(a1*a1*a1) + 2*m2/(b1*b1) - 2*m3*b2/(b1*b1*b1);
    grad = 2*m1/(a1*a1) - 2*(a2/(a1*a1*a1))*( 4*m2 - 3*a2*m3/a1 )
         + 2*m1/(b1*b1) - 2*(b2/(b1*b1*b1))*( 4*m2 - 3*b2*m3/b1 );
    
    if(fabs(grad) <= DBL_EPSILON){ 
        return 0;
    }
    
    delete [] y;
    delete [] z;
    return obj/grad;
}