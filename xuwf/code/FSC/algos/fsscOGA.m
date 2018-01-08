function beta = fsscOGA(tensor, tid, par) % Calculate the value of the tid column in the matrix B
% The input is NxTxM tensor
[N, T, M] = size(tensor); % number of time series; length of the time series; 
if par.neighbor > 0
    maxIter = par.neighbor;
else
    maxIter = 100;
end
objs = zeros(maxIter+1, 1);
objs(1) = norm(squeeze(tensor(tid, :, :)), 'fro')^2; % the F-norm of first example;tensor(tid,:,:) 1*90 select the tid_th sample;squeeze(tensor(tid,:,:)) 1*90;tid=10 9*1


bss = [];% the sets of  deformation
nodes = []; % [nodes, wid] ; the sets of sample (the same subspace?)
target = squeeze(tensor(tid, :, :)); % M=1,the tid sample: M!=1 Select the tid row data for each dimension and transpose it into columns
if M == 1 % how to change the M??? 
    target = target'; % col
end
gtarget = target;% col
if par.lambda == 0
    otarget = NaN;
else
    % Applying the regularization for nearest neighbor vs subspace
    % trade-off
    otarget = target./(ones(T, 1)*sqrt(sum(target.^2, 1))) / par.lambda; %sum(a,1) sum to col;and how to trade-off?
end
yhat = vec(target);% reshape target to len(target)*1 although M is not equal to 1
coeff = 0; % B
lam = 1e-8;
for i = 1:maxIter %  Select maxiter samples that are the closest to the tid sample
    switch par.distance
        case 0      % Euclidean distance
            [warped, wid] = mEuclid(tensor, target, tid);% warped is similar to sample ;wid is not know index of wraped just a qiaohe
        case 1      % Shift distance
            [warped, wid] = mShiftD(tensor, target, tid, par.window);
        case 2      % Warping distance
            [warped, wid] = mWarpFast(tensor, target, otarget, [tid, nodes], par.window, par.gurobi);%wid is the index of yhat
    end
    bss = [bss, vec(warped)]; % d(Y) (How to )select a few functions Yj to represent Yi ;maxinum: 90*maxIter  what's the bss? how to change ? after best deformation d(Y) The size of the indicated variable or array appears to be changing with each loop iteration.
    
    % Orthogonal projections
    tCoef = (bss'*bss + lam*eye(i))\(bss'*yhat);% 
    % Find residual
    target = gtarget - reshape(bss*tCoef, T, M); % change the shape of bss*tCoef to T*M R[l+1] = Y[i]-BQ
    size(bss*tCoef) % 90*1? Yes
    objs(i+1) = norm(target, 'fro')^2;
    
    % Termination rule
    if abs(objs(i)-objs(i+1))/objs(1) < par.ep
        break
    else
        coeff = tCoef;
        nodes = [nodes, wid];
    end
end % the end of for

beta = zeros(N, 1);% N*1
for i = 1:N
    beta(i) = sum(abs(coeff(nodes == i))); % B hat = argmin||Y[i]-BQ||
end

end

