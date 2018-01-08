function tsOut = shiftTS(ts, s)
% This functions shifts the time series 'ts' by 's' steps to right
% ts is a TxM matrix
tsOut = 0*ts;
T = size(ts, 1);
ind = (1:T) + s;
ind2 = find( (ind > 0) & (ind < T+1) );
tsOut(ind(ind2), :) = ts(ind2, :);
end