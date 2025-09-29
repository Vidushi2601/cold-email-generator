import os
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_groq import ChatGroq

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://www.metacareers.com/jobs/1070147800777577")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            llm=ChatGroq(api_key=os.environ['GROQ_API_KEY])
                         chain=Chain(llm=llm)
            jobs = llm.extract_jobs(data)
            for job in jobs:
                if not isinstance(job, dict):
                    st.error(f"Invalid job format: {job}")
                    continue

                raw_skills = job.get('skills', {})
                if isinstance(raw_skills, dict):
                    skills = set(skill for category in raw_skills.values() for skill in category)
                elif isinstance(raw_skills, list):
                    skills = set(raw_skills)
                elif isinstance(raw_skills, str):
                    skills = set(raw_skills.split(','))
                else:
                    st.error(f"Unexpected skills format: {raw_skills}")
                    continue

                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

    create_streamlit_app(chain, portfolio, clean_text)

