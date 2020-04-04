import numpy as np
def point_tangent(p1,p2,p3,r):
    # point tangent touching circle
    vec1 = p1-p2;
    vec1 = vec1/sum(vec1**2)**0.5;
    vec2 = p3-p2;
    vec2 = vec2/sum(vec2**2)**0.5;
    plane = np.cross(vec1,vec2);
    theta = np.arccos(((np.dot(vec2,vec1)+1)/2)**0.5); #half angles between both lines
    dist = r/np.tan(theta);
    p12 = p2+dist*vec1; # point on line 1,2 touched by circle
    p32 = p2+dist*vec2; # point on line 3,2 touched by circle
    return [p12,p32];
    
def theta_func(p1,p2,p3):
    #Returns Half angles beween lines p1,p2 and p3,p2 in radians
    vec1 = p1-p2;
    vec1 = vec1/sum(vec1**2)**0.5;
    vec2 = p3-p2;
    vec2 = vec2/sum(vec2**2)**0.5;
    theta = 2*(np.pi/2-np.arccos(((np.dot(vec2,vec1)+1)/2)**0.5)); #half angles between both lines
    return [theta]

def arc(p1,p2,p3,v,r,prev_time,acc_dist,dcc_dist,vel_next):
    # Generates arc data points
    n=30; # No of interpolation points
    p1=p1.T;p2=p2.T;p3=p3.T;
    vec1 = p1-p2;
    vec1 = vec1/sum(vec1**2)**0.5;
    vec2 = p3-p2;
    vec2 = vec2/sum(vec2**2)**0.5;
    plane = np.cross(vec1,vec2);
    
    theta = (np.arccos(((np.dot(vec2,vec1)+1)/2)**0.5)); #half angles between both lines
    dist = r/np.tan(theta);
    
    
    dist_travel = r*(np.pi-theta*2);
    dcc = (-vel_next**2+(v)**2)/(2*dist_travel*dcc_dist);
    t_dcc = (v-vel_next)/(dcc+10**-6);
    t_const = dist_travel*(1-dcc_dist*(dcc!=0))/v;
    t_acc=0;
    t = t_acc+t_const+t_dcc;
    time = (np.array(range(0,n+1))*t/n);


    temp2=np.dot(np.minimum(((time-t_acc)>0)*(time-t_acc),t_const),v);
    temp3=v*np.minimum(((time-t_acc-t_const)>0)*(time-t_acc-t_const),t_dcc)-np.minimum(((time-t_acc-t_const)>0)*(time-t_acc-t_const),t_dcc)*np.minimum(((time-t_acc-t_const)>0)*(time-t_acc-t_const),t_dcc)*dcc/2;
    
    theta = 2*(np.pi/2-theta);
    
    total_dist=(temp2+temp3)/dist_travel;



    
    p12 = p2+dist*vec1; # point on line 1,2 touched by circle
    p32 = p2+dist*vec2; # point on line 3,2 touched by circle
    p12_perp = np.cross(plane,vec1);
    p12_perp = p12_perp/sum(p12_perp**2)**0.5;

    center = p12+p12_perp*r; # center of circle


    theta_rot = total_dist*theta;

    arc_val = np.tile(center.reshape(3,1),(1,n+1))-r*np.tile(p12_perp.reshape(3,1),(1,n+1))*np.tile(np.cos(theta_rot.T),(3,1))-r*np.tile(vec1.reshape(3,1),(1,n+1))*np.tile(np.sin(theta_rot.T),(3,1));


    time = time+prev_time;
    return [arc_val,time];


def Interpolation(points,radius,velocity):
    points=points.T;
    [k,m]=np.shape(points);
    acc_dist = 0.1;
    dcc_dist=0.1;
    #Input data size matching
    flag=1;
    if((m-2==len(radius))and((m-2)*2+1)==len(velocity)):
        flag=0;

    m=10;
    #Interpolation generation
    n=30;#No of interpolation points
    interp_points = np.zeros(((n+1)*len(velocity),3));
    time = np.zeros(((n+1)*len(velocity),1));
    if ~(flag):
        j=0;
        t=0;


        if len(radius)>0:
            
            for k in range( 0,np.maximum(len(radius),1)):
                if k==0:
                    [p12,p32] = point_tangent(points[:,0],points[:,1],points[:,2],radius[k])
                    
                    dist = sum((p12-points[:,k])**2)**0.5;
                    acc = (velocity[j])**2/(2*dist*acc_dist);
                    dcc = -((velocity[j+1])**2-(velocity[j])**2)/(2*dist*dcc_dist);
                    t_acc = velocity[j]/acc;
                    t_dcc = (velocity[j]-velocity[j+1])/(dcc+10**-6);
                    t_const = dist*(1-acc_dist-dcc_dist*(dcc!=0))/velocity[j]; 
                    t = t_acc+t_const+t_dcc;
                    time[0:n+1] = (np.array(range(0,n+1))*t/n).reshape(n+1,1);
                    time1=(np.array(range(0,n+1))*t/n).reshape(n+1,1);
                    temp1=np.minimum(time1,t_acc)*np.minimum(time1,t_acc)/2*acc;
                    temp2=np.minimum(((time1-t_acc)>0)*(time1-t_acc),t_const)*velocity[0];
                    temp3=velocity[0]*np.minimum(((time1-t_acc-t_const)>0)*(time1-t_acc-t_const),t_dcc)-np.minimum(((time1-t_acc-t_const)>0)*(time1-t_acc-t_const),t_dcc)*np.minimum(((time1-t_acc-t_const)>0)*(time1-t_acc-t_const),t_dcc)*dcc/2;
                    total_dist=(temp1+temp2+temp3)/dist;
                    interp_points[0:n+1,:] = (np.tile(points[:,0],(n+1,1))+np.tile((p12-points[:,0])*total_dist,(1,1)));
                    j=j+1; 
                   
                else:

                    [p12,p32] = point_tangent(points[:,k],points[:,1+k],points[:,2+k],radius[k]);
                    
                [arc_val,time_1] = arc(points[:,k],points[:,k+1],points[:,k+2],velocity[j],radius[k],t,acc_dist,dcc_dist,velocity[j+1]);
                interp_points[((j)*(n+1)):(j+1)*(n+1),:] = arc_val.T;
                time[(j)*(n+1):(j+1)*(n+1)]=time_1.reshape(n+1,1);
                j=j+1;
        

                if k==len(radius)-1:
                    #Last point
                    dist = sum((points[:,k+2]-p32)**2)**0.5;
                    dcc = (velocity[j])**2/(2*dist*dcc_dist);
                    t_dcc = velocity[j]/dcc;
                    t_const = dist*(1-dcc_dist)/velocity[j];
                    t = t_dcc+t_const;
                    temp=p32+((points[:,k+2]-p32))*(1-dcc_dist);
                    interp_points[((j)*(n+1)):(j)*(n+1)+n-m+2,:] = (np.tile(p32.reshape(3,1),(1,n-m+2))+np.tile((points[:,k+2]-p32).reshape(3,1),(1,n-m+2))*np.tile(np.array(range(0,n-m+2)),(3,1))/(n-m+1)*(1-dcc_dist)).T;
                    time[((j)*(n+1)):(j)*(n+1)+n-m+2]= (np.array(range(0,n-m+2))/(n-m+1)*t_const+time_1[-1]).reshape(n-m+2,1);

                    interp_points[(j)*(n+1)+n-m+1:(j+1)*(n+1),:]=(np.tile(points[:,k+2].reshape(3,1),(1,m))-np.tile((points[:,k+2]-p32).reshape(3,1),(1,m))*np.tile((((np.array(range((m-1),-1,-1))**2/(m-1)**2)*dcc_dist).T),(3,1))).T;
                    time[(j)*(n+1)+n-m+1:(j+1)*(n+1)]= (np.array(range(0,m))/(m-1)*t_dcc+time_1[-1]+t_const).reshape(m,1);

                else:
                    [p12,p32_temp]=point_tangent(points[:,k+1],points[:,k+2],points[:,k+3],radius[k+1]);
                    dist = np.sum((p12-p32)**2)**0.5;
                    dcc = -(velocity[j+1]**2-velocity[j]**2)/(2*dist*dcc_dist);

                    t_dcc = (velocity[j]-velocity[j+1])/(dcc+10**-6);
                    t_const = dist*(1-dcc_dist*(dcc!=0))/velocity[j];
                    t = t_const+t_dcc;
                    time[((j)*(n+1)):(j+1)*(n+1)] = ((np.array(range(0,n+1))*t/(n)).T+time_1[-1]).reshape(n+1,1);
                    t_acc=0;
                    time1=(np.array(range(0,n+1))*t/n).T;
                    temp2=np.minimum(((time1-t_acc)>0)*(time1-t_acc),t_const)*velocity[j];
                    temp3=velocity[j]*np.minimum(((time1-t_acc-t_const)>0)*(time1-t_acc-t_const),t_dcc)-np.minimum(((time1-t_acc-t_const)>0)*(time1-t_acc-t_const),t_dcc)*np.minimum(((time1-t_acc-t_const)>0)*(time1-t_acc-t_const),t_dcc)*dcc/2;
                    total_dist=(temp2+temp3)/dist;
                    interp_points[((j)*(n+1)):(j+1)*(n+1),:] = ((np.tile(p32.reshape(3,1),(1,n+1))+np.tile((p12-p32).reshape(3,1),(1,n+1))*np.tile(total_dist.T,(3,1)))).T;

                t=time_1[-1]+t;
                j=j+1;
        else:
            # 2 Point Interpolation 
          
            dist = sum((points[:,1]-points[:,0])**2)**0.5;
            acc = (velocity[0])**2/(2*dist*acc_dist);
            dcc = (velocity[0])**2/(2*dist*dcc_dist);
            t_acc = velocity[0]/acc;
            t_dcc = velocity[0]/dcc;
            t_const = dist*(1-acc_dist-dcc_dist)/velocity[0];
            t = t_acc+t_const+t_dcc;
            time[:] = (np.array(range(0,n+1))*t/n).reshape(n+1,1);
      
            temp1=np.minimum(time,t_acc)*np.minimum(time,t_acc)/2*acc;
            temp2=np.minimum(((time-t_acc)>0)*(time-t_acc),t_const)*velocity[0];
            temp3=velocity[0]*np.minimum(((time-t_acc-t_const)>0)*(time-t_acc-t_const),t_dcc)-np.minimum(((time-t_acc-t_const)>0)*(time-t_acc-t_const),t_dcc)*np.minimum(((time-t_acc-t_const)>0)*(time-t_acc-t_const),t_dcc)*dcc/2;
            total_dist=(temp1+temp2+temp3)/dist;
            interp_points[0:n+1,:] = ((np.tile(points[:,0].reshape(3,1),(1,n+1))+((points[:,1]-points[:,0]).reshape(3,1))*total_dist.T)).T;
        
        x=interp_points[:,0];
        y=interp_points[:,1];
        z=interp_points[:,2];
    else:
        x=0;
        y=0;
        z=0;
        time=0;
    #print(time==np.unique(time))
    #plt.plot(time);
    #plt.plot(np.unique(time))
    return([flag,interp_points,x,y,z,time,j])
        
    
def Interpolation_main(points,radius,velocity,check,grip):
    radius=np.hstack((0,radius,0));
    pts=np.array(np.where(radius==0)[0]);
    
    interp_points=np.zeros((3,1000));
    flag=np.zeros((1,1000)).T;
    t=np.zeros((1,1000)).T;
    x=np.zeros((1,1000)).T;
    y=np.zeros((1,1000)).T;
    z=np.zeros((1,1000)).T;
    check_post = np.zeros((1,1000)).T;
    gripper = np.zeros((1,1000)).T;
    m=0;
    n=30;
    
    for i in range(0,len(list(pts.T))-1):
        
        [flag1,interp_points1,x1,y1,z1,time,j]=Interpolation(points[pts[i]:pts[i+1]+1,:],radius[pts[i]+1:pts[i+1]],velocity[np.maximum(2*(pts[i]-1)+2,0):2*(pts[i+1]-1)+1]);
        time,ind=np.unique(time,return_index = True);
        temp=np.shape(time);
        temp=temp[0];
        time=time.reshape(temp,1);
        
        print(temp)
        print(np.shape(interp_points1[ind,:]))
        flag[m:m+temp]=flag1;
        
        check_post[m] = check[pts[i]];
        print(check[pts[i]])
        check_post[m+temp-1] = check[pts[i+1]];
        gripper[m:m+temp]=grip[pts[i]]+(grip[pts[i+1]]-grip[pts[i]])/(temp-1)*(np.array(range(0,temp))).reshape(temp,1);
        
        interp_points[:,m:m+temp]=interp_points1[ind,:].T.reshape(temp,3).T;
        t[m:m+temp]=time+max(t);
        x[m:m+temp]=x1[ind].reshape(temp,1);
        y[m:m+temp]=y1[ind].reshape(temp,1);
        z[m:m+temp]=z1[ind].reshape(temp,1);
        m=m+temp;
        #plt.plot(check_post)
        #plt.show()



    #t_unique,ind=np.unique(t,return_index = True);
    #x_unique=x[ind];
    #y_unique=y[ind];
    #z_unique=z[ind];
    #check_post_unique = check_post[ind];
    #gripper_unique = gripper[ind];
    t_unique=t[0:m];
    x_unique=x[0:m];
    y_unique=y[0:m];
    z_unique=z[0:m];
    check_post_unique=check_post[0:m];
    gripper_unique = gripper[0:m];
    
    #t_unique,ind=np.unique(t_unique,return_index = True);
    #x_unique=x_unique[ind];
    #y_unique=y_unique[ind];
    #z_unique=z_unique[ind];
    #check_post_unique=check_post_unique[ind];
    #gripper_unique =gripper_unique[ind];
    
    j=0;
   
    return [x_unique,y_unique,z_unique,t_unique,check_post_unique,gripper_unique]


if __name__ =="__main__":
    points=np.array([[-93.83,-867.97,-104.49],[-490.1,-442.45,-100],[-490.1,-442.45,-220],[-490.1,-442.45,100.6],[-490.1,621.5,100],[139.7,650.5,100],[139.7,650.5,0.5]]);
    radius=np.array([0,0,0.4,0.3,0])*200;
    velocity=np.array([10,10,10,10,10,10,8,8,9,10,10])*30;
    pts=np.array(np.where(radius==0)[0])
    check=np.array([1,1,1,0,0,1,1]);
    grip=np.array([0,0,1,1,1,1,0]);

    #"""
    points =np.array([[  0,   0,   0],
     [  0,   0, -90],
     [-90,  90, -90],
     [ 90,  90,  90]]);

    radius = np.array([35, 25]);
    velocity = np.array([1, 1, 1, 1, 1]);
    check = np.array([1,0,0,1]);
    grip = np.array([0,1,0,0]);
    #"""
    [x_unique,y_unique,z_unique,t_unique,check_post_unique,gripper_unique]=Interpolation_main(points,radius,velocity,check,grip);
    #"""
    #%matplotlib qt
    plt.plot(t_unique,y_unique)
    plt.plot(t_unique,z_unique)
    plt.plot(t_unique,x_unique)
    #plt.plot(t_unique,check_post_unique)
    plt.show()
    print(np.shape(x_unique))
    #fig = Figure(figsize=plt.figaspect(1)*1, dpi=100)
    fig = plt.figure()

    ax = fig.add_subplot(111,projection='3d')
    ax.mouse_init()
    ax.set_xlim(-1000,1000)
    ax.set_ylim(-1000,1000)
    ax.set_zlim(-1000,1000)
    ax.plot3D((x_unique[:,0]),(y_unique[:,0]),(z_unique[:,0]))
    ax.plot3D(([x_unique[90,0]]),([y_unique[90,0]]),([z_unique[90,0]]),'o')
    print(t_unique[90])