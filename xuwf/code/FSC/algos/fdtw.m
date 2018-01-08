function C = fdtw(tensor, par)
% The input is NxTxM tensor
[N, ~, M] = size(tensor);

window = par.window;
C = zeros(N, N);
for i = 1:N
    tmp = zeros(1, N);
    parfor j = 1:N
        if M == 1
            tmp(j) = mdtw(squeeze(tensor(i, :, :))', squeeze(tensor(j, :, :))', window); 
        else
            tmp(j) = mdtw(squeeze(tensor(i, :, :)), squeeze(tensor(j, :, :)), window); 
        end
    end
    C(i, :) = tmp;
end

C = C/max(C(:));
C = exp(-C);