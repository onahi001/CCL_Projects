import streamlit as st
import streamlit.components.v1 as components

# Custom HTML and CSS
html_content = """
<style>
.container {
    position: relative;
    width: 300px;
    height: 100px;
}

#text_input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
}

#button {
    position: absolute;
    top: 30px;
    left: 0;
    width: 100%;
}
</style>

<div class="container">
    <input type="text" id="text_input" placeholder="Enter text here">
    <button id="button" onclick="sendInput()">Submit</button>
</div>

<script>
    function sendInput() {
        var userInput = document.getElementById("text_input").value;
        Streamlit.setComponentValue(userInput);
    }
</script>
"""

# Render the HTML content
user_input = components.html(html_content, height=100, scrolling=True)

# Display the input if any
#if user_input:
st.write("You entered:", user_input)
