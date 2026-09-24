%from (i): t_min=4.89s, d_min=0.9375m
%velocity of B
vx_b = -(1/sqrt(2))*(lambda/T + a*2*pi/T*cos(2*pi*t_min/T));
vy_b = (1/sqrt(2))*(lambda/T - a*2*pi/T*cos(2*pi*t_min/T));
%vel of B expressed in A frame
th_a = w*t_min + pi/2;
R_a = [cos(th_a) -sin(th_a); sin(th_a) cos(th_a)];
v_ab = R_a' * [vx_b; vy_b];
fprintf('v_B in A = (%.3f, %.3f) m/s\n',v_ab(1), v_ab(2));
