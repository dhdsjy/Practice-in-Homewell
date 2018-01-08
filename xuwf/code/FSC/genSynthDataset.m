% This script runs one of the synthetic dataset generators to generate a
% dataset for the experiments.
% You can also use "synthGen" and "synthGen2".

addpath('./algos/')

MaxShift = 4;   % Maximum shift in the deformation 
T = 90;         % Length of time series
N = 75;        % Number of time series: 25 per class
sig = 0.1;      % Noise standard deviation

[tensor, label] = synthGen3(MaxShift, T, sig, N);
% This is actually a matrix for univariate time series.  We can have
% multivariate ones too.

save('synth.mat', 'tensor', 'label')