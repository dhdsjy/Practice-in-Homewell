function [score, aligned] = sWarpFast(ts1, cases, ots1,  win, level, grbi) % win is the window
%  ts1:  TxM
%  cases: TxM
% win: scalar
if isnan(sum(ots1(:))) == 1
    ots1 = ts1; % T*M
end

if size(cases, 1) == 1 
    cases = cases';
end

[nT1, M] = size(cases);% nT1 is T
index = win+(1:nT1);
W = (2*win+1);
score = zeros(M, 1);% what's the score is? 10^8 level?
aligned = zeros(nT1, M);% aligned is wrped?
maxIter = 50;
ep = 1e-4;
%% Setting up the constraints
A = zeros(nT1-1, W*nT1);
b = zeros(nT1-1, 1);
% The order
for i = 1:nT1 - 1
    A(i, (i-1)*W + (1:W)) = 2.^(-win:win);
    A(i, (i-1)*W + (W+1:2*W)) = -2*2.^(-win:win);
end

% They should be equal to 1
beq = ones(nT1, 1);
Aeq = zeros(nT1, W*nT1);
for i = 1:nT1
    Aeq(i, (i-1)*W + (1:W)) = 1;
end
% The boundary conditions
lb = zeros(W*nT1, 1);
ub = ones(W*nT1, 1);

% Gurobi Setup
Ag = [A;Aeq];
bg = [b;beq];
sense = [repmat('<', size(A, 1), 1); repmat('=', size(Aeq, 1), 1)];
model.A = sparse(Ag);
model.rhs = bg;
model.sense = sense;
model.lb = zeros(size(Ag, 2), 1);
model.ub = ones(size(Ag, 2), 1);
opts.OutputFlag=0;
mopts = optimoptions('linprog', 'Display', 'off');
%% Alignment for each case
f = zeros(nT1*W, M);
g = f;
fp = f;
ts2exp = [zeros(win, M); cases; zeros(win, M)];
for i = 1:nT1
    f(W*(i-1)+1:i*W, :) = -repmat(ts1(i, :), W, 1).*ts2exp( (index(i)-win):(index(i)+win), :);
    g(W*(i-1)+1:i*W, :) = ts2exp(i+(0:2*win), :);
    fp(W*(i-1)+1:i*W, :) = -repmat(ots1(i, :), W, 1).*ts2exp( (index(i)-win):(index(i)+win), :);
end

% Initialization
sol = 0.01*ones(nT1*W, 1);
for i = 1:nT1
    sol(win + 1 + (i-1)*W) = 1;
end
solnew = sol;
objs = zeros(maxIter, 1);
for k = 1:maxIter
    % Solving it
    if norm(f, 'fro') < ep   % Handling the case that the entire time series is zero
        continue
    end
    [objs(k), grad] = findGrad(sol, W, f, g, fp);
    try
        if grbi == 1      % Use Gurobi if exists
            model.obj = grad;
            model.start = sol;
            result = gurobi(model, opts);
            if strcmp(result.status, 'OPTIMAL')
                crt = result.objval;
                solnew = result.x;
            end
        else                    % Use MATLAB if Gurobi is not available.
            [solnew, crt] = linprog(grad,A,b,Aeq,beq,lb,ub, sol, mopts);
        end
    catch err                   % Should not really happen.
        fprintf('None of optimizations converged: %d.\n', k)
    end
    fprintf('test solnew and sol')% begin
    size(solnew)
    size(sol)
    [m,n] = size(solnew);
    if m == 0 & n == 0
        continue
    elseif norm(solnew-sol)/norm(sol) < ep/10 %end
        %if norm(solnew-sol)/norm(sol) < ep/10 %norm(sol) is equal to 0 ??
        score = objs(k);
        break
    end
    
    % Updating the certification
    cert = grad'*sol - crt;
    
    % Implement the line search
    sol = linesearch(sol, solnew, W, f, g, fp);% Frank-Wolfe ?
    if isnan(sum(sol)) == 1
        fprintf('Inner loop execption: %d.\n', k)
        return
    end
    
    % Termination based on (1) Certification and (2) decrease of the loss function
    if k > 1
        if objs(k) - cert > level
            score = level + 1;  % Essentially not-including the thing
            break
        else
            score = objs(k);
        end
        if abs(objs(k) - objs(k-1))/objs(1) < ep
            break
        end
        if abs(objs(k) - objs(k-1)) < ep/10
            break
        end
    end
end
for i = 1:nT1
    aligned(i, :) = g(W*(i-1)+1:i*W, :)'*sol((i-1)*W + (1:W));
end
end