syms theta1 theta2 theta3 theta4

alpha1 = 0;
alpha2 = pi/2; 
alpha3 = -pi/2;
alpha4 =pi/2;
alpha5 =0;
alpha6 = 0;
alpha7 = pi/2;

a1 = 141.33;
a2 = 0;
a3 = 0;
a4= 66.5;
a5= 92.17;
a6 = 193.66;
a7=0;


d1 = 0;
d2 = -17.0;
d3 = 0;
d4 = 0;
d5 = 0;
d6 = 0;
d7 = 0;

alp1 =0;
alp2 =90;
alp3 =0;
alp4 =0;
alp5 =90;

% t1=65.193;
% t2=45-65.193;
% t3=0;
% t4=0;
% t5=-10.6974+50;
% t6=-53.2644+10.7-58.2;
% t7=0;


% Rz1=[vertcat(horzcat(rotz(t1), [0; 0; 0]), [0 0 0 1])];
% Tz1=[vertcat(horzcat(eye(3), [0; 0; d1]), [0 0 0 1])];
% Tx1=[vertcat(horzcat(eye(3), [a1; 0; 0]), [0 0 0 1])];
% Rx1=[vertcat(horzcat(rotx(alp1), [0; 0; 0]), [0 0 0 1])]
% T1=Rz1*Tz1*Tx1*Rx1;
% Rz2=[vertcat(horzcat(rotz(t2), [0; 0; 0]), [0 0 0 1])];
% Tz2=[vertcat(horzcat(eye(3), [0; 0; d2]), [0 0 0 1])];
% Tx2=[vertcat(horzcat(eye(3), [a2; 0; 0]), [0 0 0 1])];
% Rx2=[vertcat(horzcat(rotx(alp2), [0; 0; 0]), [0 0 0 1])];
% T2=Rz2*Tz2*Tx2*Rx2;
% Rz3=[vertcat(horzcat(rotz(t3), [0; 0; 0]), [0 0 0 1])];
% Tz3=[vertcat(horzcat(eye(3), [0; 0; d3]), [0 0 0 1])];
% Tx3=[vertcat(horzcat(eye(3), [a3; 0; 0]), [0 0 0 1])];
% Rx3=[vertcat(horzcat(rotx(alp3), [0; 0; 0]), [0 0 0 1])];
% T3=Rz3*Tz3*Tx3*Rx3;
% Rz4=[vertcat(horzcat(rotz(t4), [0; 0; 0]), [0 0 0 1])];
% Tz4=[vertcat(horzcat(eye(3), [0; 0; d4]), [0 0 0 1])];
% Tx4=[vertcat(horzcat(eye(3), [a4; 0; 0]), [0 0 0 1])];
% Rx4=[vertcat(horzcat(rotx(alp4), [0; 0; 0]), [0 0 0 1])];
% T4=Rz4*Tz4*Tx4*Rx4;
% Rz5=[vertcat(horzcat(rotz(t5), [0; 0; 0]), [0 0 0 1])];
% Tz5=[vertcat(horzcat(eye(3), [0; 0; d5]), [0 0 0 1])];
% Tx5=[vertcat(horzcat(eye(3), [a5; 0; 0]), [0 0 0 1])];
% Rx5=[vertcat(horzcat(rotx(alp5), [0; 0; 0]), [0 0 0 1])];
% T5=Rz5*Tz5*Tx5*Rx5;
% 
% T05=T1*T2*T3*T4*T5


L(1) = Link('alpha', alpha1,'a', a1,'d', d1, 'offset', +60*pi/180,'standard');   
L(2) = Link('alpha', alpha2,'a', a2,'d', d2,'standard'); 
L(3) = Link('alpha', alpha3,'a', a3,'d', d3, 'standard');

L(4) = Link('alpha', alpha4,'a', a4,'d', d4,  'standard');                 
L(5) = Link('alpha', alpha5,'a', a5,'d', d5,'offset', (20*(pi/2))/90,  'standard');   

L(6) = Link('alpha', alpha6,'a', a6,'d', d6, 'offset', ((-53.27-20)*(pi/2))/90, 'standard');   
L(7) = Link('alpha', alpha7,'a', a7,'d', d7, 'offset',pi/2,'standard'); 

Spider=SerialLink(L,'name','Hexapod Leg1');
Spider.teach('rpy');