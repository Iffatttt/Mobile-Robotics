%assuming values for lambda and amplitude
lambda = 6;
a = 3;
T = 8;
R = 5;
w = 0.4;
%sweeping t for one rev of A in 1000 points
t = linspace(0,(2*pi)/w, 1000);
% A and B positions were calculated in notebook
x_b= -(1/sqrt(2))*((lambda*t)/T + a*sin((2*pi*t)/T));
y_b= (1/sqrt(2))*((lambda*t)/T - a*sin((2*pi*t)/T));
x_a =R*cos(w*t);
y_a = R*sin(w*t);
%calculating distance between A and B at every t
dist = sqrt((x_b-x_a).^2 + (y_b-y_a).^2);
%taking the min distance and its t during one full rev of A
[d_min, idx] = min(dist);
t_min = t(idx);
fprintf('A and B were closest at time t = %fs with distance %fm', t_min,
d_min);
