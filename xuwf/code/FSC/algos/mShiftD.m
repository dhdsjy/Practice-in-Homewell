function [warped, wid] = mShiftD(tensor, target, tid, maxSh)
% The tensor is NxTxM tensor
% Target is TxM
[N, T, M] = size(tensor);
score = zeros(N, M, 2*maxSh+1);
for m = 1:M
    for s = 1:(2*maxSh+1)
        sh = 1+ maxSh - s;
        index = 1:T;
        index = sh + index((index> -sh) & (index <= T-sh));
        shifted = shiftTS(target(:, m), sh);
        temp = squeeze(tensor(:, :, m))*shifted;
        mag = sum(squeeze(tensor(:, index, m)).^2, 2);
        score(:, m, s) = abs(temp)./sqrt(mag);
    end
end
fscore = squeeze(sum(score, 2));
[~, ix] = sort(max(fscore, [], 2), 'descend');
ix(ix == tid) = []; 
wid = ix(1);
[~, sid] = max(fscore(wid, :));
warped = shiftTS(squeeze(tensor(wid, :, :)), sid - maxSh - 1);