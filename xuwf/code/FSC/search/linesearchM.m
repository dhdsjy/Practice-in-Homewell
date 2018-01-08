function x = linesearchM(x, s, W, f, g, p)
z = s-x;

% Simple grid search
nS = 21;
gam = linspace(0, 1, nS);
obj = zeros(nS, 1);
obj(1) = findGrad3(x + gam(1)*z, W, f, g, p);
objS = obj(1);
gamSelected = gam(1);
for i = 2:nS
    obj(i) = findGrad3(x + gam(i)*z, W, f, g, p);
    if objS > obj(i)
        objS = obj(i);
        gamSelected = gam(i);
    end
end
%fprintf('%f\t%f.\n', objS, gamSelected)

% Now do a couple of newton's step
gamma = newton(x, s, W, f, g, p, gamSelected);
x = x + gamma *z;
end
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function gamma = newton(x, s, W, f, g, p, gamma)
maxIter = 50;
ep = 1e-3;
for i =1:maxIter
    [~, obj, grad] = gradNewt(x, s, W, f, g, p, gamma);
    gammaNew = gamma - obj/grad;
    if gammaNew < 0
        gammaNew = 0;
    elseif gammaNew > 1
        gammaNew = 1;
    end
    if abs(gammaNew - gamma) < ep
        break
    end
    gamma = gammaNew;
end

end
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [obj, grad, hess] = gradNewt(x, s, W, f, g, p, gamma)
y = x + gamma * (s-x);
z = s-x;
nT = length(f)/W;
m1 = 0; m2 = 0; m3 = 0;
a1 = sum(f'*y);  a2 = sum(f'*z);
b1 = sum(p'*y);  b2 = sum(p'*z);
for i = 1:nT
    m1 = m1 + sum((g(W*(i-1)+1:i*W, :)'*z((i-1)*W + (1:W))).^2);
    m2 = m2 + sum((g(W*(i-1)+1:i*W, :)'*y((i-1)*W + (1:W))).*(g(W*(i-1)+1:i*W, :)'*z((i-1)*W + (1:W))));
    m3 = m3 + sum((g(W*(i-1)+1:i*W, :)'*y((i-1)*W + (1:W))).^2);
end
obj = m3/(a1^2) + m3/(b1^2);
grad = 2*m2/(a1^2) - 2*m3*a2/(a1^3) + 2*m2/(b1^2) - 2*m3*b2/(b1^3);
hess = 2*m1/(a1^2) - 2*(a2/(a1^3))*( 4*m2 - 3*a2*m3/a1 )...
        + 2*m1/(b1^2) - 2*(b2/(b1^3))*( 4*m2 - 3*b2*m3/b1 );
end