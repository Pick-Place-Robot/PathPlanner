
from Interpolation_backend import*
from Kinematics_backend import*
from lib_imports import*
from tkinter import messagebox
import scipy.io

#%matplotlib qt
master = Tk()
master.wm_iconbitmap('ArduinoCodeGenerator.ico')
master.iconbitmap('ArduinoCodeGenerator.ico')
master.geometry("1000x700")
master.title("Interpolation function")
#master = Frame(root)


space = 40;
offset = 140;

cursor_fg=0;
cursor_x=[];
cursor_y=[];
cursor_z=[];
cursor_control=0;


"""
x=[];
y=[];
z=[];
base=[];
shoulder=[];
elbow=[];
radius=[];
velocity=[];
check_post = [];
gripper = [];
i=1;
"""

def open_file():
    global master,x,y,z,base,shoulder,elbow,radius,velocity,check_post,gripper,i,Lb;
    
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Robot File","*.pkl"),("all files","*.*")))
    for j in range(len(x)):
        #print(Lb)
        Lb.delete(0)
    if filename!="":
        
        [x,y,z,base,shoulder,elbow,radius,velocity,check_post,gripper,i] = pickle.load( open( filename, "rb" ) )
        #print([x,y,z,base,shoulder,elbow,radius,velocity,check_post,gripper,i])

        for j in range(0,len(x)):
            Lb.insert(j,'Point '+str(j+1));
        master.filename=filename;
def save(): 
    gen_path();
    global master,x,y,z,base,shoulder,elbow,radius,velocity,check_post,gripper,i,flag;
    global x_uni,y_uni,z_uni,time,points,check_post_unique,gripper_unique,theta0_val,theta1_val,theta2_val,flag;
    files = [('All Files', '*.*'),  
             ('Python Files', '*.py'), 
             ('Text Document', '*.txt ')] 
    if hasattr(master,'filename'):
        #messagebox.showinfo("Warning","This will overwrite file " + os.path.basename(master.filename));  
        #print('in has filename')
        file_path=os.path.dirname(master.filename)
        file_name=os.path.basename(master.filename)
        pickle.dump( [x,y,z,base,shoulder,elbow,radius,velocity,check_post,gripper,i], open( master.filename, "wb" ) )
        scipy.io.savemat(master.filename+'.mat',{'x':x_uni, 'y':y_uni, 'z':z_uni, 'time':time,'base':theta0_val, 'elbow':theta2_val,'shoulder':theta1_val,'check_post':check_post_unique,'gripper':gripper_unique,'flag':flag})
    else:
        
        filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",initialfile="temp.pkl",filetypes = (("Robot File","*.pkl"),("all files","*.*")))
        if filename!="":
            #filename=os.path.splitext(filename)[0];
            master.filename=filename;#+".pkl";
            pickle.dump( [x,y,z,base,shoulder,elbow,radius,velocity,check_post,gripper,i], open( master.filename, "wb" ) )
            scipy.io.savemat(master.filename+'.mat',{'x':x_uni, 'y':y_uni, 'z':z_uni,'time':time, 'base':theta0_val, 'elbow':theta2_val,'shoulder':theta1_val,'check_post':check_post_unique,'gripper':gripper_unique,'flag':flag}) 
def saveas(): 
    gen_path();
    global master,x,y,z,base,shoulder,elbow,radius,velocity,check_post,gripper,i,flag;
    global x_uni,y_uni,z_uni,time,points,check_post_unique,gripper_unique,theta0_val,theta1_val,theta2_val,flag;
    
    if hasattr(master,'filename'):
        filename=os.path.dirname(master.filename);
    else:
        filename="";
        
    filename =  filedialog.asksaveasfilename(initialdir = filename+"/",initialfile="temp.pkl",title = "Select file",filetypes = (("Robot File","*.pkl"),("all files","*.*")))
    if filename!="":
        #filename,file_extension=os.path.splitext(filename)[0];
        #if file!="":
        master.filename=filename;
        pickle.dump( [x,y,z,base,shoulder,elbow,radius,velocity,check_post,gripper,i], open( master.filename, "wb" ) )
        scipy.io.savemat(master.filename+'.mat',{'x':x_uni, 'y':y_uni, 'z':z_uni,'time':time, 'base':theta0_val, 'elbow':theta2_val,'shoulder':theta1_val,'check_post':check_post_unique,'gripper':gripper_unique,'flag':flag})
def new():
    global master,x,y,z,base,shoulder,elbow,radius,velocity,check_post,gripper,i,Lb;
    delattr(master, "filename")
    #master.filename="";
    for j in range(i-1):
        #print(Lb)
        Lb.delete(0)
    x=[];y=[];z=[];base=[];shoulder=[];elbow=[];radius=[];velocity=[];check_post=[];gripper=[];i=1;

    
def donothing():
    messagebox.showinfo("About","This Program is a copyrighted program of BAL used to aid path planning © 2020")  

def viewrobotparams():
    global a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,master;
    #print(a0,a1)
    #master2 = Tk()
    
    master2=tk.Toplevel(master)
    master2.geometry("300x150")
    master2.title("Robot Parameters")
    space =43;
    v_space=20;
    h_space = 100;
    y_or=20;
    x_or=50;
    a0_lab = Label(master2,text = "a0",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
    a0_lab.place(x=x_or,y=y_or+0*v_space)
    v0 = StringVar()
    e0=tk.Entry(master2,width = 8,text='2',textvariable=v0)
    e0.place(x=x_or+space,y=y_or+0*v_space)
    v0.set(str(a0))

    a1_lab = Label(master2,text = "a1",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
    a1_lab.place(x=x_or,y=y_or+1*v_space)
    v1 = StringVar()
    e1=tk.Entry(master2,width = 8,text='2',textvariable=v1)
    e1.place(x=x_or+space,y=y_or+1*v_space)
    v1.set(str(a1))

    a2_lab = Label(master2,text = "a2",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
    a2_lab.place(x=x_or,y=y_or+2*v_space)
    v2 = StringVar()
    e2=tk.Entry(master2,width = 8,text='2',textvariable=v2)
    e2.place(x=x_or+space,y=y_or+2*v_space)
    v2.set(str(a2))

    a3_lab = Label(master2,text = "a3",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
    a3_lab.place(x=x_or,y=y_or+3*v_space)
    v3 = StringVar()
    e3=tk.Entry(master2,width = 8,text='2',textvariable=v3)
    e3.place(x=x_or+space,y=y_or+3*v_space)
    v3.set(str(a3))

    a4_lab = Label(master2,text = "a4",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
    a4_lab.place(x=x_or,y=y_or+4*v_space)
    v4 = StringVar()
    e4=tk.Entry(master2,width = 8,text='2',textvariable=v4)
    e4.place(x=x_or+space,y=y_or+4*v_space)
    v4.set(str(a4))


    d0_lab = Label(master2,text = "d0",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
    d0_lab.place(x=x_or+h_space,y=y_or+0*v_space)
    vd0 = StringVar()
    ed0=tk.Entry(master2,width = 8,text='2',textvariable=vd0)
    ed0.place(x=x_or+space+h_space,y=y_or+0*v_space)
    vd0.set(str(d0))

    d1_lab = Label(master2,text = "d1",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
    d1_lab.place(x=x_or+h_space,y=y_or+1*v_space)
    vd1 = StringVar()
    ed1=tk.Entry(master2,width = 8,text='2',textvariable=vd1)
    ed1.place(x=x_or+space+h_space,y=y_or+1*v_space)
    vd1.set(str(d1))

    d2_lab = Label(master2,text = "d2",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
    d2_lab.place(x=x_or+h_space,y=y_or+2*v_space)
    vd2 = StringVar()
    ed2=tk.Entry(master2,width = 8,text='2',textvariable=vd2)
    ed2.place(x=x_or+space+h_space,y=y_or+2*v_space)
    vd2.set(str(d2))

    d3_lab = Label(master2,text = "d3",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
    d3_lab.place(x=x_or+h_space,y=y_or+3*v_space)
    vd3 = StringVar()
    ed3=tk.Entry(master2,width = 8,text='2',textvariable=vd3)
    ed3.place(x=x_or+space+h_space,y=y_or+3*v_space)
    vd3.set(str(d3))

    d4_lab = Label(master2,text = "d4",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
    d4_lab.place(x=x_or+h_space,y=y_or+4*v_space)
    vd4 = StringVar()
    ed4=tk.Entry(master2,width = 8,text='2',textvariable=vd4)
    ed4.place(x=x_or+space+h_space,y=y_or+4*v_space)
    vd4.set(str(d4))
    #print(vd4.get())
    
    def new_m2():
        global a0,a1,a2,a3,a4,d0,d1,d2,d3,d4;
        a0=0;a1=0;a2=0;a3=0;a4=0;d0=0;d1=0;d2=0;d3=0;d4=0;
    
    def open_file_m2():
        pass
    def save_m2():
        pass
    def saveas_m2():
        pass
    
    menubar = Menu(master2)
    file = Menu(menubar, tearoff=0)  
    file.add_command(label="New",command=new_m2)  
    file.add_command(label="Open",command=open_file_m2) 
    file.add_command(label="Save",command=save_m2)  
    file.add_command(label="Save as...",command=saveas_m2)  
    menubar.add_cascade(label="File", menu=file,font = ('Helvetica', 14)) 
    file.add_separator()  
    file.add_command(label="Exit", command=master2.destroy)
    master2.config(menu=menubar)
    master2.mainloop()

    
menubar = Menu(master)
file = Menu(menubar, tearoff=0)  
file.add_command(label="New",command=new)  
file.add_command(label="Open",command=open_file) 
file.add_command(label="Save",command=save)  
file.add_command(label="Save as...",command=saveas)  
menubar.add_cascade(label="File", menu=file,font = ('Helvetica', 14)) 
file.add_separator()  
file.add_command(label="Exit", command=master.destroy)

viewmenu = Menu(menubar, tearoff=0)
trace_sel =tk.IntVar();
viewmenu.add_checkbutton(label="Cursor Trace", onvalue=1, offvalue=0, variable=trace_sel)
#c4 = tk.Checkbutton(master, text='Trace on',onvalue=1, offvalue=0,variable=trace_sel,font = "Helvetica 8 bold italic")
#c4.place(x=400,y=offset-115)
viewmenu.add_command(label="Robot Parameters", command=viewrobotparams)
menubar.add_cascade(label="View", menu=viewmenu,font = ('Helvetica', 14))

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)


 
master.config(menu=menubar)

def cursor_fig_update1(evt):
    global cursor_fg,ax,cursor_x,cursor_y,cursor_z;
    
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,[w1.get()*10],[w2.get()*10],[w3.get()*10],c)

    if flag==0:
        col = 'black';
    else:
        col = 'red';

    if cursor_fg==0:
        ax.plot3D([w1.get()],[w2.get()], [w3.get()], '+',color=col, linewidth=2, markersize=8)
        cursor_fg=1;
    else:
        if cursor_control==0:
            if trace_sel.get():
                cursor_x.append(w1.get());
                cursor_y.append(w2.get());
                cursor_z.append(w3.get());
                ax.plot3D([w1.get()],[w2.get()], [w3.get()], '+',color=col, linewidth=2, markersize=8)
            else:
                cursor_x=[];cursor_y=[];cursor_z=[];
                ax.lines[0].set_xdata([w1.get()]);
                ax.lines[0].set_ydata([w2.get()]);
                ax.lines[0].set_3d_properties(zs=[w3.get()])
                ax.lines[0].set_color(col)
        canvas.draw()
   
        
def cursor_fig_update2(evt):         
    global cursor_fg,ax;
    temp=ForwKin(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,base_sc.get()*np.pi/180,shoulder_sc.get()*np.pi/180,elbow_sc.get()*np.pi/180,c-(elbow_sc.get()+shoulder_sc.get())*np.pi/180)
    x_temp=temp[0,3];
    y_temp=temp[1,3];
    z_temp=temp[2,3];


    if cursor_fg==0:
        ax.plot3D([x_temp/10],[y_temp/10], [z_temp/10], '+',color='black', linewidth=2, markersize=8)
        cursor_fg=1;
    else:
        if cursor_control:
            if trace_sel.get():
                ax.plot3D([x_temp/10],[y_temp/10], [z_temp/10], '+',color='black', linewidth=2, markersize=8)
            else:
                ax.lines[0].set_xdata([x_temp/10]);
                ax.lines[0].set_ydata([y_temp/10]);
                ax.lines[0].set_3d_properties(zs=[z_temp/10])
                ax.lines[0].set_color('black')

        canvas.draw()
       

def updateValuecoord(evt):
    global cursor_control;
    cursor_control=1;
    temp=ForwKin(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,base_sc.get()*np.pi/180,shoulder_sc.get()*np.pi/180,elbow_sc.get()*np.pi/180,c-(elbow_sc.get()+shoulder_sc.get())*np.pi/180)
    x_temp=temp[0,3];
    y_temp=temp[1,3];
    z_temp=temp[2,3];
    w1.set(x_temp/10)
    w2.set(y_temp/10)
    w3.set(z_temp/10)
        
def updateValueang(evt):
    global cursor_control;
    cursor_control=0;
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,[w1.get()*10],[w2.get()*10],[w3.get()*10],c)
    base_sc.set(theta0_val[0]*180/np.pi);
    shoulder_sc.set(theta1_val[0]*180/np.pi)
    elbow_sc.set(theta2_val[0]*180/np.pi)

c=-(np.pi/2-0.9216);
HOME = [-93.8300/10,-867.9700/10, -104.4900/10,-1.57078563609664,-0.000105189596320974,0.0587509834071706,c];
def default(evt):
    global HOME;
    w1.set(HOME[0]);
    w2.set(HOME[1]);
    w3.set(HOME[2]);
    base_sc.set(HOME[3]*180/np.pi);
    shoulder_sc.set(HOME[4]*180/np.pi);
    elbow_sc.set(HOME[5]*180/np.pi);
    


def clear_plot(ax,canvas):
    for i in range(len(ax.lines)-1):
        del ax.lines[-1];
    canvas.draw()
    
def cursor_cont_update1(evt):
    global cursor_control;
    cursor_control=0;

def cursor_cont_update2(evt):
    global cursor_control;
    cursor_control=1;
    
pos_sel = tk.IntVar();

clearplot_button=tk.Button(master,width=10,height=1,text="Clear plot",command=lambda:clear_plot(ax,canvas),bg="Red",font = "Helvetica 10 bold italic")
clearplot_button.place(x = 300,y=offset-120)


theta0_lab = Label(master,text = "Base angle",bg="white",relief=tk.SUNKEN,width = 10,height=1,font = "Helvetica 8 bold italic");
theta0_lab.place(x=10,y=offset-20*5)
base_sc = Scale(master, from_=-360, to=360,length=150,repeatdelay=10, orient=HORIZONTAL,resolution=0.1,command=cursor_fig_update2)
base_sc.set(HOME[3]*180/np.pi)
base_sc.place(x=80,y=offset-40*3)
base_dim = Label(master,text = "deg",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
base_dim.place(x=235,y=offset-20*5)

base_sc.bind("<ButtonRelease-1>", updateValuecoord)
base_sc.bind("<ButtonPress-1>", cursor_cont_update2)

theta1_lab = Label(master,text = "Shoulder",bg="white",relief=tk.SUNKEN,width = 10,height=1,font = "Helvetica 8 bold italic");
theta1_lab.place(x=10,y=offset-20*3)
shoulder_sc = Scale(master, from_=-360, to=360,length=150,repeatdelay=10, orient=HORIZONTAL,resolution=0.1,command=cursor_fig_update2)
shoulder_sc.set(HOME[4]*180/np.pi)
shoulder_sc.place(x=80,y=offset-40*2)
shol_dim = Label(master,text = "deg",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
shol_dim.place(x=235,y=offset-20*3)

shoulder_sc.bind("<ButtonRelease-1>", updateValuecoord)
shoulder_sc.bind("<ButtonPress-1>", cursor_cont_update2)

theta2_lab = Label(master,text = "Elow angle",bg="white",relief=tk.SUNKEN,width = 10,height=1,font = "Helvetica 8 bold italic");
theta2_lab.place(x=10,y=offset-20*1)
elbow_sc = Scale(master, from_=-360, to=360,length=150,repeatdelay=10, orient=HORIZONTAL,resolution=0.1,command=cursor_fig_update2)
elbow_sc.set(HOME[5]*180/np.pi)
elbow_sc.place(x=80,y=offset-40*1)
elb_dim = Label(master,text = "deg",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
elb_dim.place(x=235,y=offset-20*1)

elbow_sc.bind("<ButtonRelease-1>", updateValuecoord)
elbow_sc.bind("<ButtonPress-1>", cursor_cont_update2)

x_pos = Label(master,text = "X-position",bg="white",relief=tk.SUNKEN,width = 10,height=1,font = "Helvetica 8 bold italic");
x_pos.place(x=10,y=offset+20)
w1 = Scale(master, from_=-90, to=90,length=150,repeatdelay=1, orient=HORIZONTAL,resolution=0.1,command=cursor_fig_update1)
w1.set(-9.3)
w1.place(x=80,y=offset+0)
w1.bind("<ButtonRelease-1>", updateValueang)
w1.bind("<ButtonPress-1>", cursor_cont_update1)

x_pos_dim = Label(master,text = "cm",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
x_pos_dim.place(x=235,y=offset+20)
x_pos.bind('<Button-1>', default)

y_pos = Label(master,text = "Y-position",bg="white",relief=tk.SUNKEN,width = 10,height=1,font = "Helvetica 8 bold italic");
y_pos.place(x=10,y=offset+20+space)
y_pos.bind('<Button-1>', default)

w2 = Scale(master, from_=-90, to=90,length=150,repeatdelay=1, orient=HORIZONTAL,resolution=0.1,command=cursor_fig_update1)
w2.set(-86.7)
w2.place(x=80,y=offset+0+space)
w2.bind("<ButtonRelease-1>", updateValueang)
w2.bind("<ButtonPress-1>", cursor_cont_update1)

y_pos_dim = Label(master,text = "cm",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
y_pos_dim.place(x=235,y=offset+20+space)

z_pos = Label(master,text = "Z-position",bg="white",relief=tk.SUNKEN,width = 10,height=1,font = "Helvetica 8 bold italic");
z_pos.place(x=10,y=offset+20+2*space)
z_pos.bind('<Button-1>', default)
w3 = Scale(master, from_=-90, to=90,length=150,repeatdelay=1, orient=HORIZONTAL,resolution=0.1,command=cursor_fig_update1)
w3.set(-10.4)
w3.place(x=80,y=offset+0+2*space)
w3.bind("<ButtonRelease-1>", updateValueang)
w3.bind("<ButtonPress-1>", cursor_cont_update1)

z_pos_dim = Label(master,text = "cm",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
z_pos_dim.place(x=235,y=offset+20+2*space)

fig = Figure(figsize=plt.figaspect(1)*1, dpi=120)
ax = fig.add_subplot(111,projection='3d')
ax.mouse_init()

canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
canvas.draw()
ax.mouse_init()
ax.set_xlim(-100,100)
ax.set_ylim(-100,100)
ax.set_zlim(-100,100)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('UR3 Robot')
canvas.get_tk_widget().place(x=300,y=offset+10-100)
toolbar = NavigationToolbar2Tk(canvas,master)
toolbar.place(x=300,y=offset+10-100)
toolbar.configure(background='white')
toolbar.update()


global i,x,y,z;

x=[];
y=[];
z=[];
base=[];
shoulder=[];
elbow=[];
radius=[];
velocity=[];
check_post = [];
gripper = [];
i=1;
flag=0;

flag_points_plot=-1;
def add_point(Lb,w1,w2,w3,ax,canvas):
    global i,x,y,z,radius,check_post,gripper,base,shoulder,elbow,flag_points_plot;
    for j in range(len(ax.lines)-1):
        del ax.lines[-1]
    Lb.insert(i,'Point '+str(i))
    x.append(w1.get());
    y.append(w2.get());
    z.append(w3.get());
    base.append(base_sc.get());
    elbow.append(elbow_sc.get());
    shoulder.append(shoulder_sc.get());
    
    radius.append(0);
    check_post.append(0);
    gripper.append(0);

    velocity.append(10);
    #print(flag_points_plot)

    
    ax.plot3D(x, y, z, color='green', marker='o', linewidth=2, markersize=5)
    
    for item in range(1,len(radius)-1):
        if(radius[item]>0):
            p1 = np.array([x[item-1],y[item-1],z[item-1]]);
            p2 = np.array([x[item],y[item],z[item]]);
            p3 = np.array([x[item+1],y[item+1],z[item+1]]);
            [arc_val,time]=arc(p1,p2,p3,10,radius[item],0,0.1,0.1,10);
            ax.plot3D(arc_val[0,:], arc_val[1,:], arc_val[2,:], color='yellow', linewidth=2, markersize=5)
    canvas.draw()
    i+=1;
    
def update_radius(radius,w4):
    value = Lb.curselection();
    itr=value[0];
    radius[itr]=w4.get();
    
def del_point(Lb,w1,w2,w3,ax,canvas):
    global i,x,y,z,base,shoulder,elbow;
    value = Lb.curselection()
    Lb.delete(value[0])
    itr=value[0];
    del x[itr];
    del y[itr];
    del z[itr];
    del base[itr];
    del shoulder[itr];
    del elbow[itr];
    del radius[itr];
    del velocity[itr];
    del gripper[itr];
    del check_post[itr];
    for j in range(len(ax.lines)-1):
        del ax.lines[-1]
    ax.plot3D(x, y, z, color='green', marker='o', linewidth=2, markersize=5)
    
    for item in range(1,len(radius)-1):
                #Commenting the below if gives a feature
                if item!=itr:
                    if(radius[item]>0):
                        p1 = np.array([x[item-1],y[item-1],z[item-1]]);
                        p2 = np.array([x[item],y[item],z[item]]);
                        p3 = np.array([x[item+1],y[item+1],z[item+1]]);
                        [arc_val,time]=arc(p1,p2,p3,10,radius[item],0,0.1,0.1,10);
                        ax.plot3D(arc_val[0,:], arc_val[1,:], arc_val[2,:], color='yellow', linewidth=2, markersize=5) 
            #print('plotting')
            #canvas.draw()
    canvas.draw()

def update_point(Lb,w1,w2,w3,ax,canvas):
    global i,x,y,z;
    value = Lb.curselection()
    #Lb.delete(value[0])
    itr=value[0];
    x[itr]=w1.get();
    y[itr]=w2.get();
    z[itr]=w3.get();
    for j in range(len(ax.lines)-1):
        del ax.lines[-1]
    ax.plot3D(x, y, z, color='green', marker='o', linewidth=2, markersize=5)
    canvas.draw()

def CurSelect(evt):
    global cursor_control;
    cursor_control=0;
    for j in range(len(ax.lines)-1):
        del ax.lines[-1]
   
   
    value = Lb.curselection()
    itr=value[0];

    var.set(check_post[itr])
    var2.set(gripper[itr])
    base_sc.set(base[itr])
    elbow_sc.set(elbow[itr])
    shoulder_sc.set([shoulder[itr]])
    w1.set(x[itr])
    w2.set(y[itr])
    w3.set(z[itr])
    w4.set(radius[itr])
    base_sc.set
    
    ax.plot3D(x, y, z, color='green', marker='o', linewidth=2, markersize=5)
    ax.plot3D([x[itr]], [y[itr]], [z[itr]], color='red', marker='o', linewidth=2, markersize=7)
    
    for item in range(1,len(radius)-1):
        if(radius[item]>0):
            p1 = np.array([x[item-1],y[item-1],z[item-1]]);
            p2 = np.array([x[item],y[item],z[item]]);
            p3 = np.array([x[item+1],y[item+1],z[item+1]]);
            [arc_val,time]=arc(p1,p2,p3,10,radius[item],0,0.1,0.1,10);
            ax.plot3D(arc_val[0,:], arc_val[1,:], arc_val[2,:], color='yellow', linewidth=2, markersize=5)

    canvas.draw()
    

add_button=tk.Button(master,width=10,height=1,text="Add Point",command=lambda:add_point(Lb,w1,w2,w3,ax,canvas),bg="green",font = "Helvetica 10 bold italic")
add_button.place(x = 10,y=offset+20+3*space)

update_button=tk.Button(master,width=10,height=1,text="Update Point",command=lambda:update_point(Lb,w1,w2,w3,ax,canvas),bg="light blue",font = "Helvetica 10 bold italic")
update_button.place(x = 105,y=offset+20+3*space)

del_button=tk.Button(master,width=10,height=1,text="Delete Point",command=lambda:del_point(Lb,w1,w2,w3,ax,canvas),bg="Red",font = "Helvetica 10 bold italic")
del_button.place(x = 200,y=offset+20+3*space)

Lb = Listbox() 
Lb.place(x = 40,y=offset+20+4*space) 
Lb.bind('<<ListboxSelect>>',CurSelect)

def update_fig(evt):
    global ax,flag;
    value = Lb.curselection()
    
    if(len(value)>=1):
        #print(radius)
        itr=value[0];
        
        if(itr-1>=0 and len(x)>itr+1):
            #print('Hell')
            for j in range(len(ax.lines)-1):
                del ax.lines[-1]
                
            p1 = np.array([x[itr-1],y[itr-1],z[itr-1]]);
            p2 = np.array([x[itr],y[itr],z[itr]]);
            p3 = np.array([x[itr+1],y[itr+1],z[itr+1]]);
            [arc_val,time]=arc(p1,p2,p3,10,w4.get(),0,0.1,0.1,10);
            ax.plot3D(x, y, z, color='green', marker='o', linewidth=2, markersize=5)
            ax.plot3D([x[itr]], [y[itr]], [z[itr]], color='red', marker='o', linewidth=2, markersize=7)
            ax.plot3D(arc_val[0,:], arc_val[1,:], arc_val[2,:], color='yellow', linewidth=2, markersize=5)
            
            for item in range(1,len(radius)-1):
                #Commenting the below if gives a feature
                if item!=itr:
                    if(radius[item]>0):
                        p1 = np.array([x[item-1],y[item-1],z[item-1]]);
                        p2 = np.array([x[item],y[item],z[item]]);
                        p3 = np.array([x[item+1],y[item+1],z[item+1]]);
                        [arc_val,time]=arc(p1,p2,p3,10,radius[item],0,0.1,0.1,10);
                        ax.plot3D(arc_val[0,:], arc_val[1,:], arc_val[2,:], color='yellow', linewidth=2, markersize=5) 
            #print('plotting')
            canvas.draw()
          

def velocity_update():
    global x,velocity,w5;
    velocity=[];
    temp_val=w5.get();
    if len(x)>1:
        for i in range(2*(len(x)-2)+1):
            velocity.append(temp_val);

        #print(velocity)
# Radius Slider
w4 = Scale(master, from_=0, to=60,length=160, orient=VERTICAL,resolution=1,command=update_fig)
w4.place(x=155,y=offset+0+4.5*space)

#Velocity Slider
w5 = Scale(master, from_=1, to=30,length=150, orient=HORIZONTAL,resolution=1)
w5.place(x=80,y=offset+0+9*space)

#check_post_lab = Label(master,text = "Check Post",bg="white",relief=tk.SUNKEN,width = 9,height=1,font = "Helvetica 8 bold italic");
#check_post_lab.place(x=10,y=0+9*space)
def check_post_sel():
    global check_post,c1,Lb,var;
    
    value = Lb.curselection()
    if len(value)>0:
        #print('hello')
        check_post[value[0]]=var.get();
        
def grip_sel():
    global check_post,c2,Lb,var2;
    value = Lb.curselection()
    if len(value)>0:
        #print('hello')
        gripper[value[0]]=var2.get();

def angle_check(theta):
    temp=0;
    for i in range(1,len(theta)):
        temp1=theta[i]-theta[i-1];
        
        if (temp1>0.1*2*np.pi):
            temp=-2*np.pi;
        elif (temp1<-0.1*2*np.pi):
            temp=2*np.pi;
        theta[i]=theta[i]+temp;
    return theta
def gen_path():
    
    global velocity,check_post,gripper,x_uni,y_uni,z_uni,time,points,check_post_unique,gripper_unique,theta0_val,theta1_val,theta2_val,flag
    velocity_update();
    points = np.vstack((np.array(x),np.array(y),np.array(z)));
    #print(np.shape(points))
    #print(np.shape(radius[1:-1]))
    #print(check_post,check_post_unique)
    points = points.T;
    [x_uni,y_uni,z_uni,time,check_post_unique,gripper_unique] =Interpolation_main(points,radius[1:-1],velocity,check_post,gripper)
    [theta0_val,theta1_val,theta2_val,flag]=IK(a0,a1,a2,a3,a4,d0,d1,d2,d3,d4,x_uni*10,y_uni*10,z_uni*10,c);
    theta0_val=angle_check(theta0_val);
    theta1_val=angle_check(theta1_val);
    theta2_val=angle_check(theta2_val);
    ind = np.where(flag==1)[0];
    #print(x_uni[ind])
    if len(ind)>0:
        ax.plot3D(x_uni[ind,0], y_uni[ind,0], z_uni[ind,0],'x', color='red', linewidth=2, markersize=2)
        canvas.draw()
    #plt.plot(check_post_unique)
def disp_path():
    
    global x_uni,y_uni,z_uni,time,points,check_post_unique,gripper_unique,theta0_val,theta1_val,theta2_val,flag
    gen_path();
    plt.plot(time,x_uni);
    plt.plot(time,y_uni);
    plt.plot(time,z_uni);
    plt.xlabel('time (s)');
    plt.ylabel('Coordinates (mm)');
    plt.legend(['x','y','z'])
    plt.title('Coordinates vs Time')
    #plt.show()
    plt.figure()
    plt.plot(time,theta0_val);
    plt.plot(time,theta1_val);
    plt.plot(time,theta2_val);
    plt.xlabel('time (s)');
    plt.ylabel('Theta (radians)');
    plt.legend(['Theta0','Theta1','Theta2'])
    plt.title('Angles vs Time')
    #plt.show()
    plt.figure()
    plt.plot(time,check_post_unique);
    plt.plot(time,gripper_unique);
    plt.xlabel('time (s)');
    plt.ylabel('Check Post/Gripper mode');
    plt.legend(['Check Post','Gripper mode'])
    plt.show()
    
var = tk.IntVar()
c1 = tk.Checkbutton(master, text='Check Post',onvalue=1, offvalue=0, command=check_post_sel,variable=var,font = "Helvetica 8 bold italic")
c1.place(x=10,y=offset+5+8.5*space)

var2 = tk.IntVar()
c2 = tk.Checkbutton(master, text='Gripper',onvalue=1, offvalue=0, command=grip_sel,variable=var2,font = "Helvetica 8 bold italic")
c2.place(x=150,y=offset+5+8.5*space)

vel_label = Label(master,text = "Velocity",bg="white",relief=tk.SUNKEN,width = 9,height=1,font = "Helvetica 8 bold italic");
vel_label.place(x=10,y=offset+0+9.5*space)
vel_pos_dim = Label(master,text = "cm/s",bg="white",relief=tk.SUNKEN,width = 5,height=1,font = "Helvetica 8 bold italic");
vel_pos_dim.place(x=235,y=offset+0+9.5*space)
upd_vel_button=tk.Button(master,width=13,height=1,text="Update Velocity",command=velocity_update,bg="brown",font = "Helvetica 8 bold italic")
upd_vel_button.place(x = 10,y=offset+0+10*space)

gen_path_button=tk.Button(master,width=13,height=1,text="Generate Path",command=gen_path,bg="green",font = "Helvetica 10 bold italic")
gen_path_button.place(x = 10,y=offset+0+11*space)

#home_button=tk.Button(master,width=13,height=1,text="Go Home",command=gen_path,bg="green",font = "Helvetica 10 bold italic")
#home_button.place(x = 10,y=0+11*space)

disp_path_button=tk.Button(master,width=13,height=1,text="Display Path",command=disp_path,bg="green",font = "Helvetica 10 bold italic")
disp_path_button.place(x = 130,y=offset+0+11*space)

rad_label = Label(master,text = "Radius (cm)",bg="white",relief=tk.SUNKEN,width = 10,height=1,font = "Helvetica 8 bold italic");
rad_label.place(x=210,y=offset+20+5.5*space)

upd_radius_button=tk.Button(master,width=13,height=1,text="Update Radius",command=lambda:update_radius(radius,w4),bg="brown",font = "Helvetica 7 bold italic")
upd_radius_button.place(x = 202,y=offset+20+6.1*space)

master.mainloop()
