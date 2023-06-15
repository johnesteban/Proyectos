global lam
D=importdata('wdbc.data',','); 
data=D.data; 
S=cov(data); 
[vec,val]=eig(S);
%% Varianza explicada
valor=diag(val); 
valord=sort(valor,'descend'); 
a=valord/sum(valord);
sAc=cumsum(a); 
%% Proyeccion y datos de entrenamiento
maxv=vec(:,end); 
x1=data*maxv; 
max2v=vec(:,end-1); 
x2=data*max2v; 
n=floor(size(x1,1)*0.8); 
ind=randperm(size(x1,1),n); 
X=[x1(ind) x2(ind)]; 
diagnostico=D.textdata(:,2); 
y=diagnostico(ind); 
%% Simulación Montecarlo
r=100;
v=rand(r,1); 
metricas=[];
for i=1:r
    lam = v(i);
    SVMmdl=fitcsvm(X,y, 'KernelFunction','mykernel');
    testx=[x1 x2];
    testx(ind,:)=[];
    diagRes=diagnostico;
    diagRes(ind)=[];
    pred=predict(SVMmdl,testx);
    nt=size(pred,1);
    for j=1:nt
        if pred{j}==diagRes{j} 
            er(j)=1;
        else
            er(j)=0;
       end
    end
    % Metricas de desempeño
    acc=sum(er)/nt;
    conf=confusionmat(diagRes,pred);
    tp=conf(1,1);
    tn=conf(2,2);
    fp=conf(1,2);
    fn=conf(2,1);
    prec=tp/(tp+fp);
    recall=tp/(tp+fn);
    f1score=2*(prec*recall)/(prec+recall);
    metricas=[metricas
              acc prec recall f1score];
end
I1=find(metricas(:,1)==max(metricas(:,1)));
I2=find(metricas(:,2)==max(metricas(:,2)));
I3=find(metricas(:,3)==max(metricas(:,3)));
I4=find(metricas(:,4)==max(metricas(:,4)));
metricas(I1,:);
metricas(I2,:);
metricas(I3,:);
metricas(I4,:);
v(I1);
v(I2);
v(I3);
v(I4);
%lambda=0.75