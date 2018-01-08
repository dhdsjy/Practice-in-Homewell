/** 
 * A C/MEX implementation of multivariate dynamic time warping. Has
 * the same signature as the MATLAB implementation (mdtw_matlab). Based
 * on the Wikipedia pseudocode. Runs between 10 and 100 times faster
 * than the MATLAB implementation, so use this if you can.
 *
 * To compile, simply run:
 *      mex dtw_c.c
 * in MATLAB.
 *
 * Once compiled, use it by issuing the following command in MATLAB:
 *     d = mdtw(X1,X2,R)
 * with
 *     X1:      T1xP matrix (P univariate time series of length T1)
 *     X2:      T2xP matrix (P univariate time series of length T2)
 *      R:      Sakoe-Chiba band warping constraint
 */

#include "mex.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

double mdtw(double *X1, int T1, double *X2, int T2, int P, int R)
{
    double d = 0;
    int sizediff = T1-T2>0 ? T1-T2 : T2-T1;
    double **D;
    int i, j, k;
    int j1, j2;
    double cost, discrep, temp;

    if(R!=-1 && R<sizediff) R = sizediff; /* adapt window size */

    /*
    printf("T1=%3d T2=%3d P=%3d R=%3d\n", T1, T2, P, R);
	printf("X1: %d x %d\n", T1, P);
    printf("X2: %d x %d\n", T2, P);
    int tmax = T1>T2 ? T1 : T2;
    for(i=0;i<tmax;i++)
    {
        for(j=0; j<P; j++)
        {	
        	if(i < T1)
        	{
        		printf("X1[%d,%d]=%f", i+1, j+1, X1[i+j*T1]);
        	}
        	if(i < T2) {
        		printf("\tX2[%d,%d]=%f", i+1, j+1, X2[i+j*T2]);
        	}
        	printf("\n");
        }
        
    }
    printf("---\n\n");
    */

    /* create D */
    D=(double **)malloc((T1+1)*sizeof(double *));
    for(i=0;i<T1+1;i++)
    {
        D[i]=(double *)malloc((T2+1)*sizeof(double));
    }

    /* initialization */
    for(i=0;i<T1+1;i++)
    {
        for(j=0;j<T2+1;j++)
        {
            D[i][j]=-1;
        }
    }
    D[0][0]=0;

    /* dynamic programming */
    for(i=1;i<=T1;i++)
    {
        if(R==-1)
        {
            j1=1;
            j2=T2;
        }
        else
        {
            j1= i-R>1 ? i-R : 1;
            j2= i+R<T2 ? i+R : T2;
        }
        for(j=j1;j<=j2;j++)
        {
        	cost = 0;
        	for(k=0; k<P; k++)
        	{
        		discrep = X1[i-1 + k*T1] - X2[j-1 + k*T2];
        		cost += (discrep * discrep);
        	}
            
            temp=D[i-1][j];
            if(D[i][j-1]!=-1) 
            {
                if(temp==-1 || D[i][j-1]<temp) temp=D[i][j-1];
            }
            if(D[i-1][j-1]!=-1) 
            {
                if(temp==-1 || D[i-1][j-1]<temp) temp=D[i-1][j-1];
            }
            
            D[i][j]=cost+temp;
        }
    }
    
    
    d=D[T1][T2];
    
    /* view matrix D */
    /*
    for(i=0;i<T1+1;i++)
    {
        for(j=0;j<T2+1;j++)
        {
            printf("%f  ",D[i][j]);
        }
        printf("\n");
    }
    */
    
    /* free D */
    for(i=0;i<T1+1;i++)
    {
        free(D[i]);
    }
    free(D);
    
    return d;
}

/* the gateway function */
void mexFunction( int nlhs, mxArray *plhs[],
        int nrhs, const mxArray *prhs[])
{
    double *X1, *X2;
    int T1, P1, T2, P2;
    int R, P;
    double *dp;
    
    /*  check for proper number of arguments */
    if(nrhs!=2&&nrhs!=3)
    {
        mexErrMsgIdAndTxt( "MATLAB:mdtw:nrhs",
                "Two or three inputs required.");
    }
    if(nlhs>1)
    {
        mexErrMsgIdAndTxt( "MATLAB:dmtw_c:nlhs",
                "mdtw: One output required.");
    }
    
    /* check to make sure w is a scalar */
    if(nrhs==2)
    {
        R=-1;
    }
    else if(nrhs==3)
    {
        if( !mxIsDouble(prhs[2]) || mxIsComplex(prhs[2]) ||
                mxGetN(prhs[2])*mxGetM(prhs[2])!=1 )
        {
            mexErrMsgIdAndTxt( "MATLAB:mdtw:R",
                    "mdtw: Input R must be a scalar.");
        }
        
        /*  get the scalar input w */
        R = (int) mxGetScalar(prhs[2]);
    }
    
    
    /*  create a pointer to the input matrix s */
    X1 = mxGetPr(prhs[0]);
    
    /*  create a pointer to the input matrix t */
    X2 = mxGetPr(prhs[1]);
    
    /*  get the dimensions of the matrix input s */
    T1 = mxGetM(prhs[0]);
    P1 = mxGetN(prhs[0]);
    
    /*  get the dimensions of the matrix input t */
    T2 = mxGetM(prhs[1]);
    P2 = mxGetN(prhs[1]);

    P = P1<P2 ? P1 : P2;
    if(P1 != P2)
    {
    	mexErrMsgIdAndTxt("MATLAB:mdtw:P1andP2",
						"mdtw: size(X1,2) != size(X2,2)");
    }
    
    /* printf("p1=%3d p2=%3d p=%3d\n", p1, p2, p); */

    /*  set the output pointer to the output matrix */
    plhs[0] = mxCreateDoubleMatrix( 1, 1, mxREAL);
    
    /*  create a C pointer to a copy of the output matrix */
    dp = mxGetPr(plhs[0]);
    
    /*  call the C subroutine */
    dp[0]=mdtw(X1, T1, X2, T2, P, R);
    
    return;
    
}
