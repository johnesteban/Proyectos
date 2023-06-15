function G = mykernel(U,V)
    %global lam
    lam=0.75; 
    m=size(U,1);
    n=size(V,1);
    for j=1:m
        xj=U(j,:);
        for k=1:n
            xk=V(k,:);
            G(j,k)=lam*xj*xk'+(1-lam)*exp(-(norm(xj-xk',2))^2);
        end
    end
end