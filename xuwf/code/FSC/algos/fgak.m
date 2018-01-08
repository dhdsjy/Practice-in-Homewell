function C = fgak(tensor, par)
% The input is NxTxM tensor
[N, ~, M] = size(tensor);

window = par.window;
% To compute sigma, set it to mean Euclidean distance
dist = 0;
for i = 1:N
    for j = 1:N
        dist = dist + norm(squeeze(tensor(i, :, :))-squeeze(tensor(j, :, :)), 'fro');
    end
end
sigma = 2*dist/(N^2);

C = zeros(N, N);
for i = 1:N
    tmp = zeros(1, N);
    parfor j = 1:N
        if M == 1
            tmp(j) = 2*logGAK(squeeze(tensor(i, :, :))', squeeze(tensor(j, :, :))', sigma, window)/...
                (logGAK(squeeze(tensor(i, :, :))', squeeze(tensor(i, :, :))', sigma, window)+...
                logGAK(squeeze(tensor(j, :, :))', squeeze(tensor(j, :, :))', sigma, window)); 
        else
            tmp(j) = 2*logGAK(squeeze(tensor(i, :, :)), squeeze(tensor(j, :, :)), sigma, window)/...
                (logGAK(squeeze(tensor(i, :, :)), squeeze(tensor(i, :, :)), sigma, window)+...
                logGAK(squeeze(tensor(j, :, :)), squeeze(tensor(j, :, :)), sigma, window)); 
        end
    end
    C(i, :) = tmp;
end

C = C/max(C(:));
C = exp(-C);