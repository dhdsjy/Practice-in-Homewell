function CC = ftscOGA(tensor, par)
% The input is NxTxM tensor
N = size(tensor, 1);
nk = par.neighbor;
C = fdtw(tensor, par);
CC = C.*(ones(N)-eye(N));
for i = 1:N
    [~, ix] = sort(CC(i, :), 'descend');
    CC(i, setdiff(1:N, ix(1:nk))) = 0;
end

end