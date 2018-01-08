function [warped, wid] = mWarp(tensor, target, tid, maxSh)
% The tensor is NxTxM tensor
% Target is TxM
[N, ~, M] = size(tensor);
score = zeros(N, M);
for m = 1:M
    score(:, m) = sWarpFast(target(:, m), squeeze(tensor(:, :, m))', maxSh);
end
fscore = sum(score, 2);
[~, ix] = sort(fscore, 'descend');
ix(ix == tid) = []; 
wid = ix(1);
warped = 0*target;
for m = 1:M
    warped(:, m) = sWarp(target(:, m), squeeze(tensor(wid, :, m))', maxSh);
end