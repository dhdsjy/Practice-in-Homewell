function [warped, wid] = mWarpFast(tensor, target, otarget, tid, maxSh, grbi)% maxSh is window 
% The tensor is NxTxM tensor
% Target is TxM
N = size(tensor, 1);
level = 1e8; % what's the meaning of level?
wid = 1;
target = target/norm(target, 'fro');% <R,Y>/|R,Y|^2...normalized?
if ~isnan(sum(otarget(:)))% isnan determine the illegal operation
    otarget = otarget/norm(otarget, 'fro');% otarget normlized
end
warped = 0*target;
for i = 1:N
    if ismember(i, tid);    % Filter out i itself
        continue;   
    end
    
    [obj, wrped] = sWarpFast(target, squeeze(tensor(i, :, :)), otarget, maxSh, level, grbi);
    if obj < level  %
        warped = wrped;
        level = obj;
        wid = i;
    end
end