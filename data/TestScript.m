clear all
close all
clc

% changes between monday and tuesday measurements: smart-pulse turned off
% and as a result, the cell size was fixed to 0.05 and blanking zone 0.05
% monday, the cellsize was 0.02 (check smmary.cell_size)

load('C:\\Users\\Sanne de Smet\\Documents\\Master_Watermanagement\\Q4\\Fieldwork\\2019_05_13_ADCP\\Sontek\\Tuesday afternoon\\20051003144213.mat')
[r1,r2,r3]=size(WaterTrack.Velocity);
Velocity    = WaterTrack.Velocity;                                    % velocity, columns: x,y,z,error (difference between vertical velocity component and from the two pairs of opposing beams)
Vprofile    = reshape(mean(Velocity(:,1,:),2),r1,r3);                 % velocity profile in x direction (first column)
Vprofile_mean = reshape(sqrt(Velocity(:,1,:).^2+Velocity(:,2,:).^2),r1,r3); % ~ Summary.Mean_Vel(:,1)
Vmean       = Summary.Mean_Vel(:,1); % = -nanmean(Vprofile,1);         % average velocity averaged over the depth
Depth       = Summary.Depth;         % = BottomTrack.VB_Depth;        % total depth for each vertical beam
Cells       = Summary.Cells;                                          % number of cells for each vertical beam
Discharge   = Summary.Total_Q;                                        % discharge
Track       = Summary.Track;                                          % location of the ADCP (XY coordinates)
Distance    = cumsum([0;sqrt(diff(Track(:,1)).^2+diff(Track(:,2)).^2)]);    % double check this calculation
blankzone   = 0.11; % = 0.06 (transducer depth) + 0.05 (blanking zone)
vbeam    =220; % choose the location of a vertical sample
Cellsize = System.Cell_Size;
Cells    = Summary.Cells;
Depth_profile = -cumsum(ones(Cells(vbeam),1))*Cellsize(vbeam);
Depth_vel = Cells.*Cellsize;

figure(1)
subplot(2,3,[1,2])
imagesc(Vprofile_mean(1:30,:),[0 0.3])
colorbar
hold on
plot([vbeam,vbeam],[30,0],'--r')
title('Velocity profile [m/s]')

subplot(2,3,6)
plot(Vprofile_mean(1:Cells(vbeam),vbeam),Depth_profile)
xlabel('Velocity [m/s]')
ylabel('Depth [m]')
title('Velocity profile at red dashed line')
ylim([-0.7,0])

subplot(2,3,[4,5])
plot(Distance,-Depth,'r')
hold on
plot(Distance,-Depth_vel-blankzone,'k')
plot([Distance(vbeam),Distance(vbeam)],[-Depth(vbeam),0],'--r')
legend('Max depth','Vel depth','Vert profile selection')
title('Depth profile')
ylabel('Depth [m]')
xlabel('Distance [m]')
ylim([-0.7,0])

% figure(2)
% subplot(2,1,1)
% plot(Vmean)
% hold on
% plot(nanmean(Vprofile_mean))
% 
% subplot(2,1,2)
% plot(Vmean,nanmean(Vprofile_mean),'.')