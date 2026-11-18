import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="QuietRoute JNNCE", layout="wide")

# Paste your entire HTML code from Claude inside this multi-line string
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>QuietRoute - JNNCE</title>
    <!-- Your HTML/Tailwind/Leaflet code goes here -->
</head>
<body>
    <h1>QuietRoute App</h1>
    <!-- Replace this entire block with the code Claude gave you -->
</body>
</html>
"""

# Render the HTML inside Streamlit
components.html(html_code, height=800, scrolling=True)
