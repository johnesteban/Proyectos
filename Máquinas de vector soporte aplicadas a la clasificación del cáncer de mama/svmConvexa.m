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
%% Combinacion convexa
rep=200;  
tacc=0;
conf=[0 0
      0 0];
tprec=0;
trecall=0;
tf1=0;
tic
for i=1:rep    
    ind=randperm(size(x1,1),n);  
    X=[x1(ind) x2(ind)];  
    diagnostico=D.textdata(:,2); 
    y=diagnostico(ind);
    SVMmdl=fitcsvm(X,y, 'KernelFunction','mykernel','ClassNames',["M","B"]); 
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
    % Métricas de desempeño
    acc=sum(er)/nt;
    tacc=tacc+acc;
    conf=conf+confusionmat(diagRes,pred,'Order',["M","B"]);
    tp=conf(1,1);
    tn=conf(2,2);
    fn=conf(1,2);
    fp=conf(2,1);
    prec=tp/(tp+fp);
    tprec=tprec+prec;
    recall=tp/(tp+fn);
    trecall=trecall+recall;
    f1score=2*(prec*recall)/(prec+recall);
    tf1=tf1+f1score;
end
toc
                   
avgacc=tacc/rep    
avgrec=trecall/rep 
avgprec=tprec/rep 
avgf1=tf1/rep
conf