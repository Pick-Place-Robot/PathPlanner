import numpy as np
a0 = 0;a1=-21.51;a2=374.78;a3=350.6;a4=206.76;d0=0;d1=93.83;d2=d3=d4=0;c=-(np.pi/2-0.9216);
def Transform(alpha_val,a_val,theta_val,d_val):
    d = np.eye(4);
    theta=np.eye(4);
    a=np.eye(4);
    alpha=np.eye(4);
    d[2,3]=d_val;
    theta[0:2,0:2]=np.array([[np.cos(theta_val),-np.sin(theta_val)],[np.sin(theta_val),np.cos(theta_val)]]).reshape(2,2);
    a[0,3]=a_val;
    alpha[1:3,1:3]=np.array([[np.cos(alpha_val),-np.sin(alpha_val)],[np.sin(alpha_val),np.cos(alpha_val)]]);
    T = alpha.dot(a)
    T=T.dot(theta);
    T=T.dot(d);
  
    return T;
    
def ForwKin(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,theta0,theta1,theta2,theta3):
    T1=Transform(0,a0,theta0,d0);
    T2=Transform(np.pi/2,a1,theta1,d1);
    T3=Transform(0,a2,theta2,d2);
    T4=Transform(0,a3,theta3,d3);
    T5=Transform(-np.pi/2,a4,0,d4);
    fk = T1.dot(T2).dot(T3).dot(T4).dot(T5);
    #print(T1,T2,T3,T4,T5)
    return fk;

def theta0(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,x,y,z):
    temp1 = -a0+x;
    temp2 = a0**2-2*a0*x-d1**2-2*d1*d2-2*d1*d3-d2**2-2*d2*d3-d3**2+x**2+y**2;
    temp3 = d1+d2+d3-y;
    flag=0;
    if temp2>=0:
        theta0_1= 2*np.arctan((temp1+(temp2)**0.5)/temp3);
        theta0_2= -2*np.arctan((-temp1+(temp2)**0.5)/temp3);
    else:
        theta0_2=0;
        theta0_1=0;
        flag=1;
    return [theta0_1,theta0_2,flag]

def theta1(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,x,y,z,theta0,c):

    temp1 = -a1 - a4*np.cos(c) + d4*np.sin(c) + 1.0*(a0*np.sin(theta0)**2 - a0 + x*np.cos(theta0)**2 + y*np.sin(2*theta0)/2)/np.cos(theta0);
    temp2 = -a4*np.sin(c) - 1.0*d0 - d4*np.cos(c) + 1.0*z;
    flag = 0;
    if abs((temp1**2+temp2**2-a3**2-a2**2)/(2*a2*a3))<=1:
        theta2_1=2*np.pi-np.arccos((temp1**2+temp2**2-a3**2-a2**2)/(2*a2*a3));
        theta2_2=np.arccos((temp1**2+temp2**2-a3**2-a2**2)/(2*a2*a3));
        c1 = a2 + a3*np.cos(theta2_1);
        c2 = a2 + a3*np.cos(theta2_2);
        a=-a4*np.sin(c) - 1.0*d0 - d4*np.cos(c) + 1.0*z;
        b=-a1 - a4*np.cos(c) + d4*np.sin(c) + 1.0*(a0*np.sin(theta0)**2 - a0 + x*np.cos(theta0)**2 + y*np.sin(2*theta0)/2)/np.cos(theta0);
        theta1_1 = np.arctan2(a,b)+np.arctan2((a**2+b**2-c1**2)**(0.5),c1);
        theta1_2 = np.arctan2(a,b)-np.arctan2((a**2+b**2-c2**2)**(0.5),c2);
       

    else:
        flag=1; 
        theta2_1=0;
        theta2_2=0;
        theta1_1=0;
        theta1_2=0;
    return [theta2_1,theta2_2,theta1_1,theta1_2,flag];

def IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,x,y,z,c):
    theta0_val=[];
    flag=[];
    theta1_val=[];
    theta2_val=[];
    for i in range(len(x)):
        [theta0_1,theta0_2,flag_val0]= theta0(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,x[i],y[i],z[i]);
        
        if  ~flag_val0:
            theta0_val.append(theta0_2);
            [temp2,temp4,temp3,temp5,flag_val1]=theta1(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,x[i],y[i],z[i],theta0_val[-1],c);
             
        if (flag_val0 or flag_val1)==0:
            theta2_val.append(temp4);
            theta1_val.append(temp5);
            #print(theta0_val[-1],theta1_val[-1],theta0_val[-1])
            res =ForwKin(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,theta0_val[-1],theta1_val[-1],theta2_val[-1],c-theta1_val[-1]-theta2_val[-1]);
            if np.sum(abs(res[0:3,3]-np.array([x[i],y[i],z[i]]).T))>10**-3:
                flag.append(1);
            else:
                flag.append(0);
        else: 
            theta1_val.append(0)
            theta2_val.append(0)
            flag.append(1);
        
    return [np.array(theta0_val),np.array(theta1_val),np.array(theta2_val),np.array(flag)]



if __name__ == "__main__":
    a0 = 0;a1=-21.51;a2=374.78;a3=350.6;a4=206.76;d0=0;d1=93.83;d2=d3=d4=0;c=-(np.pi/2-0.9216);
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,np.array([-93.83]),np.array([-867.97]),np.array([-104.49]),c);
    print(theta0_val[0],theta1_val[0],theta2_val[0],flag)
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,np.array([-490.1]),np.array([-442.45]),np.array([-100]),c);
    print(theta0_val[0],theta1_val[0],theta2_val[0],flag)
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,np.array([-490.1]),np.array([-442.45]),np.array([-220]),c);
    print(theta0_val[0],theta1_val[0],theta2_val[0],flag)
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,np.array([-490.1]),np.array([-442.45]),np.array([100]),c);
    print(theta0_val[0],theta1_val[0],theta2_val[0],flag)
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,np.array([-490.1]),np.array([621.45]),np.array([100]),c);
    print(theta0_val[0],theta1_val[0],theta2_val[0],flag)
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,np.array([139.7]),np.array([650.45]),np.array([100]),c);
    print(theta0_val[0],theta1_val[0],theta2_val[0],flag)
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,np.array([139.7]),np.array([650.45]),np.array([100]),c);
    print(theta0_val[0],theta1_val[0],theta2_val[0],flag)
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,np.array([139.7]),np.array([650.45]),np.array([0.5]),c);
    temp=ForwKin(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,-1.57078563609664,-0.000105189596320974,0.0587509834071706,c-0.0587509834071706+0.000105189596320974 );