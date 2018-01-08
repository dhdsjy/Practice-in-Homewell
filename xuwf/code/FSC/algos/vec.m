function vector = vec( matrix )
%VEC Summary of this function goes here
%   Detailed explanation goes here
vector = reshape(matrix, numel(matrix) , 1);% 返回matrix中元素个数

end

