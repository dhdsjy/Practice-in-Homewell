function [tSeries, label] = synthGen(MaxShift, T, sig, N)
B = 3;
% N = 150;

b = [T/4, T/2, T*3/4];

Basis = exp( - (ones(B, 1)*(1:T) - b'*ones(1, T)).^2/70  );
% plot(Basis')
tSeries = zeros(N, T);

Bases = [Basis(1, :); Basis(2, :)];
for i = 1:N/3
    shifts = randi(MaxShift*2, 2, 1) - MaxShift;
    weights = randn(2, 1);
    weights = weights + sign(weights);
    for j = 1:2
        ind = (1:T) + shifts(j);
        ind2 = find( (ind > 0) & (ind < T+1) );
        tSeries(i, ind(ind2)) = tSeries(i, ind(ind2)) + weights(j)*Bases(j, ind2);
    end
end

Bases = [Basis(2, :); Basis(3, :)];
for i = N/3+1:2*N/3
    shifts = randi(MaxShift*2, 2, 1) - MaxShift;
    weights = randn(2, 1);
    weights = weights + sign(weights);
    for j = 1:2
        ind = (1:T) + shifts(j);
        ind2 = find( (ind > 0) & (ind < T+1) );
        tSeries(i, ind(ind2)) = tSeries(i, ind(ind2)) + weights(j)*Bases(j, ind2);
    end
end

Bases = [Basis(3, :); Basis(1, :)];
for i = 2*N/3+1:N
    shifts = randi(MaxShift*2, 2, 1) - MaxShift;
    weights = randn(2, 1);
    weights = weights + sign(weights);
    for j = 1:2
        ind = (1:T) + shifts(j);
        ind2 = find( (ind > 0) & (ind < T+1) );
        tSeries(i, ind(ind2)) = tSeries(i, ind(ind2)) + weights(j)*Bases(j, ind2);
    end
end

tSeries = tSeries + sig*randn(N, T);

label = zeros(N, 1);
label(1:N/3) = 1;
label(N/3+1:2*N/3) = 2;
label(2*N/3+1:N) = 3;