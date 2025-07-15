clear;
clc;

%加载辨识参数
load("optimized_params6.mat");

hfw = 1200;
c0 = 1.128;
t = 0.0;
c1 = bestParams(1);
c2 = bestParams(2);
d1 = bestParams(3);
d2 = bestParams(4);

% 加载输入数据
load("Dfw.mat");
load("Ub.mat");
load("Ut.mat");

tf = 1000;
t_sim = 1:tf;
Dfw = [t_sim' Dfw];
Ub = [t_sim' ub];
Ut = [t_sim' ut];

%运行仿真程序
simOut = sim('Three_order_noliner1','ReturnWorkspaceOutputs', 'on');

% 获取模型输出数据
Pst_predicted = simOut.Pst_test; 
Ne_predicted = simOut.Ne_test;
hm_predicted = simOut.hm_test;

rb_predicted = simOut.rb_test;
pm_predicted = simOut.Pm_test;

%% 保存数据用于辨识测试
Dfw = Dfw(:, 2);
ub = Ub(:, 2);
ut = Ut(:, 2);
Pst = double(Pst_predicted.Data(2:end));
Ne = double(Ne_predicted.Data(2:end));
hm = double(hm_predicted.Data(2:end));
rb = double(rb_predicted.Data(2:end));
Pm = double(pm_predicted.Data(2:end));

save("test/Dfw.mat", "Dfw")
save("test/ub.mat", "ub")
save("test/ut.mat", "ut")
save("test/Pst.mat", "Pst")
save("test/Ne.mat", "Ne")
save("test/hm.mat", "hm")
save("test/rb.mat", "rb")
save("test/Pm.mat", "Pm")


% % 实际实验数据
% load("pst.mat");
% load("hm.mat");
% load("Ne.mat");
% Pst_actual = pst; % 替换为实际实验数据
% Ne_actual = Ne;
% hm_actual = hm;
% 
% % 时间数据
% time = t_sim'*4; % 替换为实际数据的时间
% 
% % 绘制Pst的比较图
% figure;
% plot(time, Pst_actual, 'r--','LineWidth',1.5,'DisplayName', 'Field data');
% hold on;
% plot(Pst_predicted.time*4, Pst_predicted.data, 'blue','LineWidth',1.5,'DisplayName', 'Identified model data');
% set(gca,'FontSize',10);
% xlabel('Time(seconds)','FontSize',9);
% ylabel('P_s_t(MPa)','FontSize',9);
% ylim([9,27]);
% xlim([0,4e3]);
% set(gcf,'unit','centimeters','position',[10,10,12,7.5]);
% set(legend,'location','best');
% legend show;
% 
% % %% 绘制Ne的比较图
% figure;
% plot(time, Ne_actual, 'r--','LineWidth',1.5, 'DisplayName', 'Field data');
% hold on;
% plot(Ne_predicted.time*4, Ne_predicted.data, 'b-','LineWidth',1.5, 'DisplayName', 'Identified model data');
% set(gca,'FontSize',10);
% xlabel('Time(seconds)','FontSize',9);
% ylabel('Ne(MW)','FontSize',9);
% ylim([120,320]);
% xlim([0,4e3]);
% set(gcf,'unit','centimeters','position',[10,10,12,7.5]);
% set(legend,'location','best');
% legend show;
% 
% % % 绘制hm的比较图
% figure;
% plot(time, hm_actual, 'r--', 'LineWidth',1.5,'DisplayName', 'Field data');
% hold on;
% plot(hm_predicted.time*4, hm_predicted.data, 'b-', 'LineWidth',1.5,'DisplayName', 'Identified model data');
% xlabel('Time(seconds)','FontSize',9);
% ylabel('h_m(kJ/kg)','FontSize',9);
% xlim([0,4e3]);
% ylim([2400,2900]);
% set(gcf,'unit','centimeters','position',[10,10,12,7.5]);
% set(legend,'location','southeast');
% legend show;
% 
% %计算相对误差大小
% dPst = Pst_predicted.data(2:end)-Pst_actual;
% dNe = Ne_predicted.data(2:end)-Ne_actual;
% dhm = hm_predicted.data(2:end)-hm_actual;
% Pst_error = dPst./Pst_actual;
% Ne_error = dNe./Ne_actual;
% hm_error = dhm./hm_actual;
% 
% %绘制误差
% times = (1:1000)*4;
% times = times';
% figure;
% area(times,hm_error);
% xlabel('Time(seconds)','FontSize',9);
% ylabel('h_m(%)','FontSize',9);
% xlim([0,3e3]);
% set(gcf,'unit','centimeters','position',[10,10,12,7.5]);
% yticks = get(gca,'YTick');
% yticklabels = arrayfun(@(hm_error) sprintf('%.0f%%',hm_error*100),yticks,'UniformOutput',false);
% set(gca,'YTickLabel',yticklabels);
% 
% figure;
% area(times,Ne_error);
% xlabel('Time(seconds)','FontSize',9);
% ylabel('Ne(%)','FontSize',9);
% xlim([0,3e3]);
% set(gcf,'unit','centimeters','position',[10,10,12,7.5]);
% yticks = get(gca,'YTick');
% yticklabels = arrayfun(@(Ne_error) sprintf('%.0f%%',Ne_error*100),yticks,'UniformOutput',false);
% set(gca,'YTickLabel',yticklabels);
% 
% figure;
% area(times,Pst_error);
% xlabel('Time(seconds)','FontSize',9);
% ylabel('P_s_t(%)','FontSize',9);
% xlim([0,3e3]);
% set(gcf,'unit','centimeters','position',[10,10,12,7.5]);
% yticks = get(gca,'YTick');
% yticklabels = arrayfun(@(Pst_error) sprintf('%.0f%%',Pst_error*100),yticks,'UniformOutput',false);
% set(gca,'YTickLabel',yticklabels);


