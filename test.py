import streamlit as st
import streamlit.components.v1 as components

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
