length_a = height(scan_a);
length_b = height(scan_b);
T_ab = [0 -1 1.55; 1 0 0; 0 0 1]; %B's pose from A
p_a_transformed = zeros(length_b,2);
figure;
for i=1:length_b
p = T_ab * [x_b(i); y_b(i); 1]; %B described in A frame
p_a_transformed(i,: ) = p(1:2)';
end
plot(p_a_transformed(:,1), p_a_transformed(:,2), '.', MarkerSize=15);
hold on;
plot(x_a, y_a, '.', MarkerSize=15, Color='r')
legend('Scan B in A', 'Scan A');
xlabel('x(m) in frame A');
ylabel('y(m) in frame A');
title('Scan B in frame A');
axis equal;
grid on;
hold off;
