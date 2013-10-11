function values = getcellstruct(CELLARRAY,field,index,varargin)
%GETCELLSTRUCT retrieves the field values MATLAB cell array of structures 
%
% VALUES = GETCELLSTRUCT(CELLARRAY,'field',INDEX,M,N)
%
% VALUES = GETCELLSTRUCT(CELLARRAY,'field',INDEX,M) can be used 
%   for row vectors. For column vectors use 
% VALUES = GETCELLSTRUCT(CELLARRAY,'field',INDEX,1,M) instead
%
% VALUES = GETCELLSTRUCT(CELLARRAY,'field',INDEX) is the same as 
%   GETCELLSTRUCT(CELLARRAY,'field',index,1,1) if the field data
%   is a scalar
% 
% VALUES = GETCELLSTRUCT(CELLARRAY,'field',INDEX) is a MATLAB cell array
% 	 of strings if specified fields contain strings.


% See also SETCELLSTRUCT FINDCELLS 
if(~iscell(CELLARRAY) || ~isstruct(CELLARRAY{1}) || isempty(CELLARRAY))
   error('The first argument must be a non-empty cell array of structures') 
end
% Chechk if the second argument is a string
if(~ischar(field))
   error('The second argument ''field'' must be a character string')
end

switch nargin
   case 5,
      M = varargin{1};
      N = varargin{2}; 
   case 4,
      M = 1;
      N = varargin{1};
   case 3,
      M = 1;
      N = 1;
   otherwise 
      error('Incorrect number of inputs');
end % switch


NV = length(index);

if(isnumeric(CELLARRAY{index(1,1)}.(field)))
   values = zeros(NV,1);
   for I = 1:NV
      values(I) = CELLARRAY{index(I)}.(field)(M,N);
   end 
elseif(ischar(CELLARRAY{index(1,1)}.(field)))
   values = cell(NV,1);
   for I = 1:NV
      values{I} = CELLARRAY{index(I)}.(field);
   end 
else
   error('The field data must be numeric or character array') 
end



