function data = tracy3_convert_dynap_xy_from_trackcpp(filename)

nr_header_lines = 13;
filename = '/home/fac_files/code/python/trackc++/tests/dynap_xy_out.txt';
tdata = importdata(filename, ' ', nr_header_lines); tdata = tdata.data;

data = zeros(size(tdata,1), 5);
data(:,1) = tdata(:,3);  % x
data(:,2) = tdata(:,5);  % y
no_plane_sel = (tdata(:,11) == 0);
x_plane_sel  = (tdata(:,11) == 1);
y_plane_sel  = (tdata(:,11) == 2);
data(no_plane_sel,3) = -1;
data(x_plane_sel, 3) =  1;
data(y_plane_sel, 3) =  2;
data(:,4) = tdata(:,10);  % lost_turn

