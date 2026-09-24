scan_a = readtable("scan_posA.csv");
x_a = scan_a.x;
y_a = scan_a.y;

figure;
plot(x_a, y_a, '.', MarkerSize=15, Color='r')

xlabel('x(m)')
ylabel('y(m)')
title('Scan A Points')
grid on;

scan_b = readtable("scan_posB.csv");
x_b = scan_b.x;
y_b = scan_b.y;

figure;
plot(x_b, y_b, '.', MarkerSize=15)

xlabel('x(m)')
ylabel('y(m)')
title('Scan B Points')
grid on;

%on same figure
figure;
plot(x_a, y_a, '.', MarkerSize=15, Color='r')
hold on;
plot(x_b, y_b, '.', MarkerSize=15, Color='b');
legend('Scan A', 'Scan B');
xlabel('x(m)')
ylabel('y(m)')
title('Scan A vs Scan B Points')
grid on;
hold off;
