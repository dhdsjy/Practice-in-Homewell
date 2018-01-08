% A test case for debugging the alignment function
clc
clear
close all

T1 = 10;
T2 = 10;
b1 = 3;
b2 = 5;
ts1 = zeros(1, T1);
ts1(b1:b1+1) = 1;
ts2 = zeros(1, T2);
ts2(b2:b2+1) = 1;

plot(ts1)
hold on
plot(ts2, 'r')

ts2onts1 = tsAlign(ts1', ts2', 5);

plot(ts2onts1, 'g')

deg = 3;
win = 2;
% ts2onts1 = tsAlign3(ts1', ts2', win);
profile on
[score, ts2onts1] = sWarpFast4(ts1', ts2', ts1',  win, 100);
profile off
profile viewer
plot(ts2onts1, 'm')