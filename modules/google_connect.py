import streamlit as st

def exibir_interface(bb):
    st.subheader("Integração com Google")
    st.write("Você pode usar `gspread` (Sheets), `firebase-admin` ou `google-auth`.")
    # Demonstração apenas
    if st.button("Simular conexão"):
        bb.set("google_status", "conectado")
        st.success("Conectado ao Google com sucesso.")