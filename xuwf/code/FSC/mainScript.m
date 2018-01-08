%% Documentation
% This script runs the unsupervised feature extraction algorithms by
% executing "extractFeature" function.  The function implements "Functional
% Subspace Clustering" in the following paper:

% M. T. Bahadori, D. Kale, Y. Fan, and Y. Liu, 
% "Functional Subspace Clustering with Application to Time Series",  ICML 2015.

% Maintenance: mohammab@usc.edu

% It is highly recommended to use Matlab's parfor and Gurobi to solve the 
% linear program. However, if you do not have Gurobi, the code will use
% Matlab's own optimization toolbox and the code will run approximately 10x
% slower.

% You can use "genSynthDataset.m" to generate a synthetic dataset or use
% the existing "synth.mat". You are expected to obtain a clustering similar
% to "synthFSC.png" by running this code.

% The settings in this script are not the optimal settings.  They indicate
% typical settings for the algorithm. The provided synthetic dataset is 
% only for checking the basic functionality of the code; you need to generate
% the synthetic datasets using the provided scripts to get results similar 
% to the results of the paper.

% "par.algo" specifies the algorithm to be run.  To run "ssc", select 'fsc'
% and set the par.distance to 0. To run regular spectral clustering, select
% 'dtw' and set the window size to 0.

clc
clear
warning('off')

%% Setting the path
addpath(genpath('.'))
addpath('/home/xuwf/Downloads/gurobi/gurobi702/linux64/matlab/') % download the gurobi,you can
%use it

%load('/home/xuwf/xuwf/code/FSC/synth.mat')% you can select the other datas eg 
tensorA = csvread('./data_for_fsc/ready_for_experiment/A_cuttent_dataTransed_2017_97_to_1128_for_entity95401_noindex.csv');
tensorB = csvread('./data_for_fsc/ready_for_experiment/B_cuttent_dataTransed_2017_97_to_1128_for_entity95401_noindex.csv');%cuttent_dataTransed_2017_97_to_1128_for_entity95401
tensorC = csvread('./data_for_fsc/ready_for_experiment/Ctest_noindex.csv');
% normlized tensor
tensorZA = zscore(tensorA);
tensorZB = zscore(tensorB);
tensorZC = zscore(tensorC);
%tensor = cat(3,tensorZA,tensorZB,tensorZC);
tensor = tensorZC
label = csvread('./data_for_fsc/ready_for_experiment/label_for_95401_.csv')
% construct a tensor 
if exist('gurobi', 'file')
    par.gurobi = 1;
else
    par.gurobi = 0;
end

%% Settings
par.dimension = 3;              % Dimension of the embedding space; the number of subspace; how to descide the dim? it is not similar to ssc?
par.window = 2;                 % Window size of the deformation operation
par.ep = 1e-5;                  % Termination error
par.neighbor = 8;   % 8            % Number of neighbors selected for each data point
par.lambda = 0.1; % 0.1              % A trade-off parameter between subspace and 
                                % nearest neighbor assumptions
par.algo = 'fsc';            % 'fsc', 'tsc', 'gak', or 'dtw'
par.distance = 2;   %2            % 0-> Euclid, 1-> Shift, 2-> Warp
par.verbose = 1;

%% Running the algorithm
[features, lams, timeElapsed,simB, A, LapN,nF] = extractFeature(tensor, par);% when par.distance=2, lams=0 why?

%% Visualization
% The following visualization is specific to the three-class synthetic
% dataset.  Please change it when you want to use for other datasets.
% 这并没有什么意义 ，只是示例数据的可视化（只有三个维度）
subplot(2,1,1)
plot3(features(label==1, 1), features(label==1, 2), features(label==1, 3), 'or') %  plot3->plot 
hold all
plot3(features(label==0, 1), features(label==0, 2),features(label==0, 3), '^b') %  
%plot3(features(label==3, 1), features(label==3, 2), features(label==3, 3), '+g')
legend('Class 1', 'Class 2') % , 'Class 3'
xlabel('Dimension 1')
ylabel('Dimension 2')
zlabel('Dimension 3')
axis square 
grid on

% Kmeans clustering of Evaluation

idX = kmeans(features,3) % N*1的向量，存储的是每个点的聚类标号
numLabels = unique(label)

% Visualization after kmeans clustering 
subplot(2,1,2)
plot3(features(idX==1, 1), features(idX==1, 2),features(idX==1, 3), 'om' ) %  plot3->plot 
hold all
plot3(features(idX==2, 1), features(idX==2, 2),features(idX==2, 3), '*c') %  
plot3(features(idX==3, 1), features(idX==3, 2), features(idX==3, 3), '+g')
plot3(features(idX==4, 1), features(idX==4, 2), features(idX==4, 3), 'or')
plot3(features(idX==5, 1), features(idX==5, 2), features(idX==5, 3),'^b' )
legend('Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5') % 
xlabel('DimensionK 1')
ylabel('DimensionK 2')
zlabel('DimensionK 3')
axis square 
grid on
TP = 0;
TN = 0;
FP = 0;
FN = 0;
for i=1:size(label,1)
    if idX(i)==1 & label(i)==1
        TP = TP +1    
    end
    if idX(i)==2 & label(i)==0
        TN = TN + 1
    end
    if idX(i) == 1 & label(i)==0
        FP = FP + 1
    end
    if idX(i) == 2 & label(i) == 1
        FN = FN + 1
    end
end
precision = TP/(TP+FP);
recall = TP/(TP+FN);
accuracy = (TP+TN)/(TP+TN+FP+FN);
fprintf ('precision is %f\n recall is %f\n accuracy is %f\n',precision,recall,accuracy)

