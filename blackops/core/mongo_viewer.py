# -----------------------------
# core/mongo_viewer.py
# -----------------------------
import pandas as pd
import streamlit as st
from pymongo import MongoClient

class MongoDBViewer:
    def __init__(self, uri):
        self.mongo_client = MongoClient(uri)

    def view_collection(self, db_name, collection_name):
        db = self.mongo_client[db_name]
        collection = db[collection_name]
        documents = collection.find()
        for doc in documents:
            print(doc)

    @staticmethod
    def exibir_mongodb() -> None:
        """
            Exibe dados do MongoDB a partir de uma conexão com URI.

            Returns:
                Show (MongoDB Viewer): Dados exibidos no Streamlit.
        """
        st.subheader("🗄️ Visualizador de MongoDB")
        uri = st.text_input("🔗 MongoDB URI", "mongodb+srv://twitchcombopunch:6z2h1j3k9F.@clusterops.iodjyeg.mongodb.net/", type="default")

        if uri:
            try:
                client = MongoClient(uri)
                dbs = client.list_database_names()
                db_name = st.selectbox("📚 Escolha um banco de dados:", dbs)

                if db_name:
                    db = client[db_name]
                    collections = db.list_collection_names()
                    col_name = st.selectbox("📁 Escolha uma coleção:", collections)

                    if col_name:
                        col = db[col_name]
                        limit = st.slider("🔢 Número de documentos para exibir", 1, 100, 10)
                        documents = list(col.find().limit(limit))
                        if documents:
                            df = pd.DataFrame(documents).fillna("")
                            st.dataframe(df)
                        else:
                            st.info("🕵️‍♂️ Nenhum documento encontrado nesta coleção.")
            except Exception as e:
                st.error(f"Erro ao conectar ao MongoDB: {e}")