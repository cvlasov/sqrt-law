% --------------------------------------------------------------------
% Conversion from ASCII header-less table in a text file to .mat file
% --------------------------------------------------------------------
% fea_file: string with the relative path of the .fea file
% mat_file: string with the relative path where the .mat file
%           should be saved
function txt_to_mat(fea_file, mat_file)

% Whitespace is the default separator, so no need to pass
% a delimiter argument since the feature file is tab-separated.
features = importdata(fea_file);

rowheaders = 'rowheaders';
names = 'names';
textdata = 'textdata';
F = 'F';
data = 'data';

% Modify fields to match those expected by the classifier
features = rmfield(features,rowheaders);
[features.(names)] = features.(textdata);
features = rmfield(features,textdata);
[features.(F)] = features.(data);
features = rmfield(features,data);

% Display the names and structure of the fields
features

% Save as .mat file
save(mat_file, 'features');
clear features;

end
