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

# Function to calculate minimum reflux ratio
def min_reflux(alpha, xf, xd):
    Rmin = ((1/(alpha-1)) * ((xd/xf) - ((alpha*(1-xd))/(1-xf))))
    return Rmin


import streamlit as st
import streamlit.components.v1 as components

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

# app bar
# encoding the app bar logo in base64
import base64

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

image_base64 = get_image_base64("ccl_logo.png")

# Define CSS for the app bar
st.markdown(
    """
    <style>
    .appbar {
        background-color: #316BBB;
        padding: 10px 0;
        text-align: center;
        font-size: 40px;
        color: #FFFFFF;
        border-bottom: 1px solid #ddd;
    }
    .appbar img {
        height: 20px;
        margin-right: 60px;
    }
    .appbar-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div class="appbar">
        <div class="appbar-container">
            <img src="data:image/png;base64,{image_base64}" alt="Local Image">
            <span> Binary Distillation Simulator </span>
        </div>
    </div>
    """, unsafe_allow_html=True
)

# function to display distillation colummn
def distill_col (space):
    # Define CSS for the hollow rectangle and arrows
    dis_css = """
    <style>
        .container {
            position: relative;
            width: 100px;
            height: 800px;
            margin: 10px auto;
        }

        .rectangle {
            width: 100px;
            height: 400px;
            border: 5px solid #4CAF50;
            border-radius: 100px;
            background-color: transparent;
            position: relative;
            top: 30px;
            left: 0;
        }
        
        .svg-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        }
        
    </style>
    """

    # Define HTML for the hollow rectangle
    dis_html = """
    <div class="container">
        <div class="rectangle"></div>
    </div>
    """
    
    # design of upper part column
    svg = """
    <svg class="svg-overlay">
    <!-- Arrow 1 -->
    <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" 
        refX="0" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="black" />
        </marker>
    </defs>
    <line x1="279" y1="1" x2="410" y2="1" stroke="black" 
        stroke-width="2" />
    <line x1="280" y1="1" x2="280" y2="40" stroke="black" 
        stroke-width="2" />
    <circle cx="410" cy="50" r="10" stroke="black" stroke-width="2" fill="white" />
    <line x1="380" y1="70" x2="450" y2="20" stroke="black" 
        stroke-width="2"  marker-end="url(#arrowhead)"/>
    <line x1="410" y1="1" x2="410" y2="40" stroke="black" 
        stroke-width="2" />
    <line x1="410" y1="60" x2="410" y2="100" stroke="black" 
        stroke-width="2" />
    <line x1="330" y1="100" x2="500" y2="100" stroke="black" 
        stroke-width="2" marker-end="url(#arrowhead)" />
    <line x1="110" y1="230" x2="215" y2="230" stroke="black" 
        stroke-width="2" marker-end="url(#arrowhead)"/>
    """
    
    # design of lower part of column
    svg_1 = """
    <svg class="svg-overlay">
    <!-- Arrow 1 -->
    <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" 
        refX="0" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="black" />
        </marker>
    </defs>
    <line x1="279" y1="485" x2="410" y2="485" stroke="black" 
        stroke-width="2" />
    <line x1="280" y1="438" x2="280" y2="550" stroke="black" 
        stroke-width="2" marker-end="url(#arrowhead)"/>
    <circle cx="410" cy="440" r="10" stroke="black" stroke-width="2" fill="white" />
    <line x1="450" y1="410" x2="380" y2="460" stroke="black" 
        stroke-width="2"  marker-end="url(#arrowhead)"/>
    <line x1="410" y1="485" x2="410" y2="450" stroke="black" 
        stroke-width="2" />
    <line x1="410" y1="430" x2="410" y2="400" stroke="black" 
        stroke-width="2" />
    <line x1="330" y1="400" x2="411" y2="400" stroke="black" 
        stroke-width="2" />
    </svg>
    """
    
    space.markdown(dis_css + dis_html + svg + svg_1, unsafe_allow_html=True)
    



# streamlit content
blank_1, title_col, ccl_logo = st.columns([2, 3.5, 2])
space_1, space_2 = st.columns([2,2])
blank_3, plot_fig, blank_4 = st.columns([1.5, 3.5, 0.5])

#title_col.title("McCable Binary Distillation ")
#ccl_logo.image(logo)
#st.image("ccl_logo.png", )
menue = st.sidebar
menue.markdown("<h1>System Parameters<h1>", unsafe_allow_html=True)
menue.markdown("<h3>Below are Fields to Enter the System"+ 
               " Parameters of the distillation process<h3>", unsafe_allow_html=True)


def distill_pla(space, num_lines):
    pla_css = """
    <style>
        .container {
            position: relative;
            width: 100px;
            height: 800px;
            margin: 10px auto;
        }
        
        .svg-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
    </style>
    """
    
    line_spacing = 800 / (num_lines + 1)
    lines = ''

    # Add the original diagonal line
    lines += '<line x1="10" y1="10" x2="90" y2="790" stroke="black" stroke-width="2" />\n'
    
    # Add horizontal lines
    for i in range(1, num_lines + 1):
        y = i * line_spacing
        lines += f'<line x1="10" y1="{y}" x2="90" y2="{y}" stroke="black" stroke-width="2" />\n'
    
    svg_2 = f'''
    <div class="container">
        <svg width="100" height="800">
            {lines}
        </svg>
    </div>
    '''
    
    # Display the CSS in Streamlit
    space.markdown(pla_css, unsafe_allow_html=True)
    
    # Display the SVG content
    components.html(svg_2, height=800)

space_1, space_2 = st.columns([2, 2])
distill_pla(space_2, 5)  # Example: Add 5 horizontal lines


# distillation column display
distill_col(space_1)

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

try:
    plot_button=  st.button("Plot McCable")
    if plot_button:
        D, W = stream (F, xf, xd, xw)
        if n != None:
            calc_reflux = find_reflux()
            Rmin = min_reflux(alpha, xf, xd)
            xn_points, yn_points, rect_points, strip_points, q_points, no_stage = mccabe_plot (alpha, xd, xw, xf, F, calc_reflux, q)
            x_eq, y_eq = equilibrium_data(alpha=3)
            fig=x_y_plot(x_eq, y_eq, rect_points, strip_points, xn_points, yn_points, q_points, xf, q)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            space_2.pyplot(fig)
            blank_3.write(f"Calculated Reflux Ratio = {calc_reflux}")
            blank_3.write(f"The Underwood Minimum Ratio = {Rmin:.4}")
            blank_3.write(f"Number of plates = {no_stage}")
            
        elif n==0:
            Rmin = min_reflux(alpha, xf, xd)
            blank_3.write(f"The Underwood Minimum Ratio = {Rmin:.4}")
        
        else:
            xn_points, yn_points, rect_points, strip_points, q_points, no_stage = mccabe_plot (alpha, xd, xw, xf, F, reflux, q)
            x_eq, y_eq = equilibrium_data(alpha)
            fig=x_y_plot(x_eq, y_eq, rect_points, strip_points, xn_points, yn_points, q_points, xf, q)
            Rmin = min_reflux(alpha, xf, xd)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            space_2.pyplot(fig)
            blank_3.write(f"Number of plates = {no_stage}")
            blank_3.write(f"The Underwood Minimum Ratio = {Rmin:.4}")
            
except Exception as e:
    st.error(f"{e} Occured. Check your inputs")

distill_pla(space_2, n)
    
    
#xn_points, yn_points, rect_points, strip_points, q_points, no_stage = mccabe_plot (alpha=3, xd=0.95, xw=0.05, xf=0.5, F=100, R=3.591, q=0.5)
#print(no_stage)
#x_eq, y_eq = equilibrium_data(alpha=3)
#x_y_plot(x_eq, y_eq, rect_points, strip_points, xn_points, yn_points, q_points, xf=0.5, q=0.5)

