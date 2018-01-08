function beta = fsscOGA(tid, ep)
global tensor  % This is large, so I don't want to pass it around
% The input is NxTxM tensor
[N, ~, M] = size(tensor);
% ep = 0.1;
maxIter = 100;
objs = zeros(maxIter+1, 1);
objs(1) = norm(squeeze(tensor(tid, :, :)), 'fro')^2;

bss = [];
nodes = [];
target = squeeze(tensor(tid, :, :));
yhat = target;
lam = 1e-8;
for i = 1:maxIter
    [warped, wid] = mEuclid(tensor, target, tid);   % warped is T x M
    bss = cat(3, bss, warped);
    
    % Orthogonal projections
    tCoef = zeros(i, M);
    for m= 1:M
        X = squeeze(bss(:, m, :));
        tCoef(:, m) = (X'*X + lam*eye(i))\(X'*yhat(:,m));
        % Find residual
        target(:, m) = yhat(:, m) -  X*tCoef(:, m);
    end
    objs(i+1) = norm(target, 'fro')^2;
    
    % Termination rule
    if abs(objs(i)-objs(i+1))/objs(1) < ep
        break
    else
        coeff = sum(abs(tCoef), 2);
        nodes = [nodes, wid];
    end
end

beta = zeros(N, 1);
for i = 1:N
    beta(i) = sum(abs(coeff(nodes == i)));
end

end