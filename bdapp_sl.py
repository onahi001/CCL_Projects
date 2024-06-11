# importing required libaries

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from scipy.optimize import minimize


# Equilibrium Curve data
def equilibrium_data (alpha = None, po_a=None, po_b=None):
    
    x_eq = np.linspace(0, 1, 51)
    if alpha != None:
        y_eq = (alpha * x_eq)/(1 + (alpha-1)*x_eq)
        return x_eq, y_eq
    
    elif po_a != None and po_b != None:
        alpha = po_a/po_b
        y_eq = (alpha * x_eq)/1 + (alpha-1)*x_eq
        return x_eq, y_eq

# calculating the q line
def yfeed(q, xf, x):
    return (((q*x)/(q-1) - (xf)/(q-1)))

# Calculating q value
def q_calc(Hv, Hf, Hl):
    q = (Hv - Hf)/(Hv-Hl)
    return q

# y Equilibrium curve Equation
def y_equil (alpha, xn):
    return (alpha * xn)/(1 + xn * (alpha - 1))

# x Equiliibrium Curve Equation
def equil (alpha, yn):
    return yn / (alpha - (alpha -1)*yn)

# Rectifying Line Equation
def rect (R, xn, xd):
    return (R/(R+1))*xn + (xd/(R+1))

# Stripping Line Equation
def strip (W, Lm, Vm, xm, xw):
    return (Lm/Vm)*xm - (W/Vm)*xw

# Stream Function
def stream (F, xf, xd, xw):
    W = (((F*xf)-(F*xd)) / (xw - xd))
    D = F - W
    return D, W

# Vapour and Liquid function
def stage_comp(F, q, R, D, W):
    Ln = R*D
    Vn = Ln + D
    Lm = Ln + (q*F)
    Vm = Lm - W
    
    return Ln, Vn, Lm, Vm
    
    
def mccabe_eqn_reflux (R):
    
    count = 0
    # calculating important variables of the rectifying and stripping equation
    Ln, Vn, Lm, Vm = stage_comp(F, q, R, D, W)
    
    # intersect of two operating lines
    intersect_x = (-(xd*Vm) - (W*xw*(R+1)))/((R*Vm) - ((R*Lm) + Lm))    # gotten from equating operating line
    #intersect_x = ((xf * (R + 1)) + (xd *(q-1)))/(R+q)                 # gotten from equating q line and rect line
    
    # setting starting values
    yn = xd
    xn = xd
    
    # iterating over the number of stages
    #while count < n:
        # computing the number of stages for Rectifying Section
    while xn > intersect_x and count < n:
            
        # Finding Equilibrium value of x
        xn = equil (alpha, yn)
            
        # the rectifying Component Line Equation
        yn = rect (R, xn, xd)
        count +=1

        
    # computing the number of stages for Stripping Section
    while xn > xw and count < n:
            
        # Finding Equilibrium value of x
        xn = equil (alpha, yn)
            
        # the stripping Component Line Equation
        yn = strip (W, Lm, Vm, xn, xw)
        count +=1        
    
    
    return abs(yn - xw)
        
# Function determining Number of Stages

def mccabe_plot (alpha, xd, xw, xf, F, R, q, D=None, W=None, Hv=None, Hf=None, Hl=None):
    # calculating missing values
    if q == None:
        q = q_calc(Hv, Hf, Hl)
    
    # calulating composition
    if D == None and W == None:
        D, W = stream(F, xf, xd, xw)
    # calculating important variables of the rectifying and stripping equation
    Ln, Vn, Lm, Vm = stage_comp(F, q, R, D, W)
    
    # setting starting values
    no_stage = 0
    yn = xd
    xn = xd
    
    # xn and yn points
    xn_points = []
    yn_points = []
    
    # an attempt to calc intersection of operating lines
    intersect_x = (-(xd*Vm) - (W*xw*(R+1)))/((R*Vm) - ((R*Lm) + Lm))
    
    # computing the number of stages for Rectifying Section
    while xn > intersect_x:
        # creating a list points for xn thyline on graph
        xn_thyline = []
        yn_thyline = []
        xn_thyline.append(xn)
        
        # creating a list points for yn thyline on graph
        yn_points.append([yn, yn])
        yn_thyline.append(yn)
        
        # Finding Equilibrium value of x
        xn = equil (alpha, yn)
        
        # creating list of all xn thyline points
        xn_thyline.append(xn)
        xn_points.append(xn_thyline)
        xn_points.append([xn, xn])
        
        # the stripping Component Line Equation
        yn = rect (R, xn, xd)
        
        # counter for number of stages
        no_stage += 1
        
        # creating list of all yn thyline points
        yn_thyline.append(yn)
        yn_points.append(yn_thyline)
        
    feed_plate = no_stage
    
    
    # computing the number of stages for Stripping Section
    xm = xn
    ym = yn
    while xm > xw:
        # creating a list points for xn thyline on graph
        xm_thyline = []
        ym_thyline = []
        xm_thyline.append(xm)
        
        # creating a list points for yn thyline on graph
        yn_points.append([ym, ym])
        ym_thyline.append(ym)
        
        # Finding Equilibrium value of x
        xm = equil (alpha, ym)
        
        # creating list of all xn thyline points
        xm_thyline.append(xm)
        xn_points.append(xm_thyline)
        xn_points.append([xm, xm])
        
        # the stripping Component Line Equation
        ym = strip (W, Lm, Vm, xm, xw)
        
        # counter for number of stages
        no_stage += 1
        
        # creating list of all yn thyline points
        ym_thyline.append(ym)
        yn_points.append(ym_thyline)

    # rect_0 finds the value of rectifying line when xn=0    
    rect_0 = (1/(R+1))*xd
    
    # strip_0 finds the value of stripping line when xn=0
    strip_xf = (Lm/Vm)*xf-(W/Vm)*xw
    
    # q_points finds the points for the q line
    if q != 1:
        #q_x = np.linspace(xd, xw, 5)
        #q_y = q/(q-1)*q_x + (1/(1-q))*xf
        q_y_p = q/(q-1)*xw + (1/(1-q))*xf
        q_x = [xf, xw]
        q_y = [xf, q_y_p]
        q_points = [q_x, q_y]
    else:
        #y_x = (alpha*xf)/(1+(alpha-1)*xf)
        q_points = [[intersect_x, intersect_x], [intersect_x, 1]]
    
    # two x and y points (at x =0, x=xd) for the rectifying line                           
    rect_points = [[0, xd], [rect_0, xd]]
    
    # two x and y points (at xn=0, xn=xd) for the stripping line
    strip_points = [[xf, xw], [strip_xf, xw]]
    
    print(feed_plate)
    #no_stage = no_stage -1 
    #return xm, ym, no_stage, feed_plate
    return xn_points, yn_points, rect_points, strip_points, q_points, no_stage
    
def x_y_plot (x_eq, y_eq, rect_points, strip_points, xn_points, yn_points, q_points, xf, q):
    forty_five_line = [0, 1]
    
    # plotting equilibrium curve
    plt.plot(x_eq, y_eq)
    #plt.scatter(x_eq, y_eq)
    
    # plotting 45 degree line
    plt.plot(forty_five_line, forty_five_line)
    
    # plotting rectifying line
    plt.plot(rect_points[0], rect_points[1])
    
    # plotting stripping line
    plt.plot(strip_points[0], strip_points[1])
    
    # plotting the stages lines
    for i in range(len(xn_points)):
        plt.plot(xn_points[i], yn_points[i])
    
    # plotting the q line
    plt.plot(q_points[0], q_points[1])
    plt.scatter(xf, xf)
    
    # display plots
    plt.show()

def find_reflux():
    res = minimize_scalar(mccabe_eqn_reflux)
    return res.x


import streamlit as st


#logo path
icon="ccl_icon.jpeg"
logo = "ccl_logo.png"

# setting page config
st.set_page_config(
    page_title= "Binary Distillation",
    page_icon=icon,
    layout="wide"
)

# creating page layout
blank_1, title_col, ccl_logo = st.columns([2, 3.5, 2])
blank_3, plot_fig, blank_4 = st.columns([1, 3.5, 1])

title_col.title("McCable Binary Distillation ")
ccl_logo.image(logo)
st.image("ccl_logo.png", )
menue = st.sidebar
menue.markdown("<h1>System Parameters<h1>", unsafe_allow_html=True)
menue.markdown("<h3>Below are Fields to Enter the System"+ 
               " Parameters of the distillation process<h3>", unsafe_allow_html=True)


# Collecting Input Values
F=menue.number_input("Enter Feed Flowrate", value=100.00)
xf=menue.slider("Composition of Feed", min_value=0.0, max_value=1.0, step=0.01)
xd=menue.slider("Composition of Distillate",min_value=0.0,max_value=1.0, step=0.01)
xw=menue.slider("Composition of Bottom", min_value=0.0, max_value=1.0, step=0.01)


col_1, col_2, col_3= menue.columns(3)
alpha=col_1.number_input("alpha",value=None)
reflux=col_2.number_input("reflux",value=None)
q=col_3.number_input("q-value",value=None)
n=menue.number_input("Number of plate",value=None)
menue.markdown("<h5>(Leave the space blank or with a zero value)<h5>", unsafe_allow_html=True)

D, W = stream (F, xf, xd, xw)

plot_button=  st.button("Plot McCable")
if plot_button:
    if n != 0 or n != None:
        calc_reflux = find_reflux()
        xn_points, yn_points, rect_points, strip_points, q_points, no_stage = mccabe_plot (alpha, xd, xw, xf, F, calc_reflux, q)
        x_eq, y_eq = equilibrium_data(alpha=3)
        fig=x_y_plot(x_eq, y_eq, rect_points, strip_points, xn_points, yn_points, q_points, xf, q)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plot_fig.pyplot(fig)
        blank_3.write(f"Calculated Reflux Ratio = {calc_reflux}")
        blank_3.write(f"Number of plates = {no_stage}")
    
    else:
        xn_points, yn_points, rect_points, strip_points, q_points, no_stage = mccabe_plot (alpha, xd, xw, xf, F, reflux, q)
        x_eq, y_eq = equilibrium_data(alpha=3)
        fig=x_y_plot(x_eq, y_eq, rect_points, strip_points, xn_points, yn_points, q_points, xf, q)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plot_fig.pyplot(fig)
        blank_3.write(f"Number of plates = {no_stage}")



    
    
#xn_points, yn_points, rect_points, strip_points, q_points, no_stage = mccabe_plot (alpha=3, xd=0.95, xw=0.05, xf=0.5, F=100, R=3.591, q=0.5)
#print(no_stage)
#x_eq, y_eq = equilibrium_data(alpha=3)
#x_y_plot(x_eq, y_eq, rect_points, strip_points, xn_points, yn_points, q_points, xf=0.5, q=0.5)