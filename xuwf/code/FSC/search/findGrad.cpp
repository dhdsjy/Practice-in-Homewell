#include "mex.h"

#define p(i,j) pp[i+len*j]
#define f(i,j) ff[i+len*j]
#define g(i,j) gg[i+len*j]

void mexFunction( int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]){
    double *dp;
    
    /*  create a pointer to the input matrix x */
    double * x = mxGetPr(prhs[0]);
    
    /*  create a pointer to the input matrix x */
    int W = (int) mxGetScalar(prhs[1]);
    
    /*  create a pointer to the input matrix f */
    double * ff = mxGetPr(prhs[2]);
    
    /*  create a pointer to the input matrix g */
    double * gg = mxGetPr(prhs[3]);
    
    /*  create a pointer to the input matrix p */
    double * pp = mxGetPr(prhs[4]);
    
    /*  get the dimensions of the matrix input s */
    int len = (int)mxGetM(prhs[0]);
    int nT = len/W;
    int M = (int)mxGetN(prhs[2]);
    
    //  set the output pointer to the output matrix 
    double *obj;
    plhs[0] = mxCreateDoubleMatrix(1, 1, mxREAL);
    obj = mxGetPr(plhs[0]);
    *obj = 0;
    
    //  create a C pointer to a copy of the output matrix 
    double *grad;	
    plhs[1] = mxCreateDoubleMatrix(len, 1, mxREAL);
    grad = mxGetPr(plhs[1]);
    
    //  Main Program 
    double m = 0, mm = 0, fx = 0, px = 0, mg = 0, mf = 0, mp = 0;
    int i = 0, j = 0, k= 0;
    double *ax = new double[M];
    
    // The Objective function
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
    *obj = m/(fx*fx) + m/(px*px);
    
    // The gradient
    for (i=0; i<nT; i++){
        for(k=0; k<M; k++){  // Finding ax
            ax[k] = 0;
            for(j=0; j<W; j++){
                ax[k] += g(W*i+j, k)*x[W*i+j];
            }
        }
        for (j=0; j<W; j++){
            mf = 0;   mp = 0;   mg = 0;
            for(k=0; k<M; k++){
                mg += g(W*i+j, k)*ax[k];
                mf += f(W*i+j, k);
                mp += p(W*i+j, k);
            }
            grad[W*i+j] = 2*mg/(fx*fx) + 2*mg/(px*px) - 2*m*mf/(fx*fx*fx) - 2*m*mp/(px*px*px);
        }
    }
    
    delete [] ax;
    return;
}