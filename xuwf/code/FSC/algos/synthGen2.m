function [tSeries, label] = synthGen2(MaxShift, T, sig)
B = 3;
N = 90;

TT = T - 6*MaxShift;
ts = sin((1:TT)*pi/MaxShift);
Basis = zeros(B, T);
for i = 1:B
    Basis(i, (2*(i-1)+1)*MaxShift +((i-1)*TT/3+1:i*TT/3)) = ts((i-1)*TT/3+1:i*TT/3);
end
% plot(Basis')
tSeries = zeros(N, T);

Bases = [Basis(1, :); Basis(2, :)];
tSeries(1:N/3, :) = createOne(Bases, N, MaxShift);

Bases = [Basis(2, :); Basis(3, :)];
tSeries(N/3+1:2*N/3, :) = createOne(Bases, N, MaxShift);

Bases = [Basis(3, :); Basis(1, :)];
tSeries(2*N/3+1:N, :) = createOne(Bases, N, MaxShift);

tSeries = tSeries + sig*randn(N, T);

label = zeros(N, 1);
label(1:N/3) = 1;
label(N/3+1:2*N/3) = 2;
label(2*N/3+1:N) = 3;
end

function ts = createOne(Bases, N, MaxShift)
T = size(Bases, 2);
ts = zeros(N/3, T);
for i = 1:N/3
    shifts = randi(MaxShift) - MaxShift/2;
    weights = 0.5+ 1*abs(randn(2, 1));
%     weights = weights + sign(weights);
    for j = 1:2
        ind = (1:T) + shifts;
        ind2 = find( (ind > 0) & (ind < T+1) );
        ts(i, ind(ind2)) = ts(i, ind(ind2)) + weights(j)*Bases(j, ind2);
    end
end
end
