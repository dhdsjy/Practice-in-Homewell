function [warped, wid] = mEuclid(tensor, target, tid)% tid is target's index? Yes
% The input is NxTxM tensor
[N, ~, M] = size(tensor);
score = zeros(N, M); % 75*1
for m = 1:M
    score(:, m) = squeeze(tensor(:, :, m))*target(:, m); % what's the meaning of score?
end
fscore = sum(score, 2);% according to row
[~, ix] = sort(fscore, 'descend'); % return index array
ix(ix ==tid) = []; 

wid = ix(1);% the index of best deformation 
warped = squeeze(tensor(wid, :, :)); % already exist in tensor for euclid