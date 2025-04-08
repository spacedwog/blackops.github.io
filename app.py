import streamlit as st
from streamlit_drawable_canvas import st_canvas
from modules import ciberseguranca, data_science, google_connect
from blackboard import blackboard

st.set_page_config(page_title="Sistema Integrado", layout="wide")

st.sidebar.image("assets/logo.png", width=150)
page = st.sidebar.selectbox("Menu", ["Canvas", "Cibersegurança", "Data Science", "Google", "ESP8266"])

if page == "Canvas":
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=3,
        stroke_color="#000",
        background_color="#eee",
        update_streamlit=True,
        height=400,
        width=600,
        drawing_mode="freedraw"
    )
    if canvas_result.json_data:
        blackboard.set("canvas_data", canvas_result.json_data)

elif page == "Cibersegurança":
    ciberseguranca.exibir_interface(blackboard)

elif page == "Data Science":
    data_science.exibir_interface(blackboard)

elif page == "Google":
    google_connect.exibir_interface(blackboard)

elif page == "ESP8266":
    from nodemcu_interface import controle_esp
    controle_esp()