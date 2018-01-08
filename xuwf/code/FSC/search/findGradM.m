function [obj, grad] = findGradM(x, W, f, g, fp)
nT = length(x)/W;
M = size(f, 2);
m = zeros(1, M);
for i = 1:nT
    m = m +  (x((i-1)*W + (1:W))'*g(W*(i-1)+1:i*W, :)).^2;
end
obj = sum(m)/( sum(f'*x)^2 ) + sum(m)/( sum(fp'*x)^2);

grad = 0*x;
bx = sum(f'*x);    
px = sum(fp'*x);
for i = 1:nT
    ax = g(W*(i-1)+1:i*W, :)'*x((i-1)*W + (1:W)); 
    grad(W*(i-1)+1:i*W) = 2/(bx^2)*sum(repmat(ax', W, 1).*g(W*(i-1)+1:i*W, :), 2)...
        - 2*sum(m)*sum(f(W*(i-1)+1:i*W, :), 2)/(bx^3);
     grad(W*(i-1)+1:i*W) = grad(W*(i-1)+1:i*W) + 2/(px^2)*sum(repmat(ax', W, 1).*g(W*(i-1)+1:i*W, :), 2)...
         - 2*sum(m)*sum(fp(W*(i-1)+1:i*W, :), 2)/(px^3);
end
end
