function [features, lams, timeElapsed, simB, A, LapN,nF] = extractFeature(tensor, par) % function output = input 
N = size(tensor, 1); % 求tensor的行数
nF = par.dimension; % Dimension of the embedding space

simB = zeros(N, N);% init相似矩阵B
tic % 计时开始
% 选择使用tsc、fsc、gak、DTW、中的一种算法
if strcmp(par.algo, 'tsc')
        simB = ftscOGA(tensor, par);
elseif strcmp(par.algo, 'fsc')
    parfor i = 1:N
        simB(:, i) = fsscOGA(tensor, i, par);% i represent the i_th col 
        if par.verbose == 1
            disp(i)
        end
    end
elseif strcmp(par.algo, 'gak')
    simB = fgak(tensor, par);
else
    simB = fdtw(tensor, par);
end
timeElapsed = toc; % 计时结束

% Create the affinity matrix

A = abs(simB) + abs(simB');

% fprintf('this is simB:\n')% i want to understand the subspace
% simB
% fprintf('this is A:\n')
% A

% % Normalized Spectral Clustering according to Ng & Jordan & Weiss
% DN = diag( 1./sqrt(sum(A)+eps) ); % 度矩阵
% LapN = DN*A*DN; % 构建拉普拉斯矩阵
% % fprintf('this is LapN:\n')
% LapNC = (LapN+LapN')/2;   % Avoiding numerical errors
% [features, lams] = eig(LapNC); %eigs(LapN, nF, 'lm'); % 'lm' 表示绝对值最大的特征值 features特征值 lams特征向量

% add for me(xuwf)
D = diag(sum(A)+eps);
LapN = D-A; 
LapN = D^(-.5)*LapN*D^(-.5);
[features0, lams0] = eig(LapN);
sort_lams = sort(diag(lams0));
if sort_lams(1)==0
    sort_lams = sort_lams(2:size(sort_lams));
end
dif = diff(sort_lams);
[ma,nF] = max(dif);
if nF ==1
    nF = 3
end
[features,lams] = eigs(LapN, 3, 'lm');







% Optional normalization
% features = features./( sqrt(sum(features.^2, 2))*ones(1, nF) );
