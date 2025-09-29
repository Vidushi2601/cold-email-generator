import os
import uuid
import pandas as pd
import chromadb


class Portfolio:
    def __init__(self, file_path="techstack_portfolios.csv"):
        # Load CSV from repo root
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        # Chroma persistent client (stores vectors in "vectorstore" dir)
        self.chroma_client = chromadb.PersistentClient(path="vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if self.collection.count() == 0:  # Load only if empty
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],              # must be list
                    metadatas=[{"links": row["Links"]}],       # must be list
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        if isinstance(skills, str):
            query_texts = [skills]
        elif isinstance(skills, (list, set)):
            query_texts = list(skills)
        else:
            return []

        results = self.collection.query(query_texts=query_texts, n_results=2)

        # Flatten metadatas into a single list of dicts
        metadatas = results.get("metadatas", [])
        return [item for sublist in metadatas for item in sublist]
