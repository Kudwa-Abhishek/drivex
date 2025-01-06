import streamlit as st
import pandas as pd
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.docstore.document import Document
from streamlit_tags import st_tags
import matplotlib.pyplot as plt
import seaborn as sns


# Set up OpenAI API key
OPENAI_API_KEY = "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"

# Configure Streamlit app
st.set_page_config(page_title="Document Q&A", layout="wide")

st.title("Document Q&A Application")
st.write("Upload an Excel document, and ask questions based on its content!")

# Step 1: Document Upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file:
    st.write(f"Uploaded file name: {uploaded_file.name}")
    try:
        # Attempt to read the file
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.write("Document Content Preview:")
        st.dataframe(df)
        
        # Convert DataFrame to text and prepare the Document for AI processing
        document_text = df.to_string(index=False)
        doc = Document(page_content=document_text)

        # Ensure df is defined before visualizations
        st.write("### Interactive Data Visualizations:")
        
        # Visualization: Bar Chart of Departments
        st.write("#### Employee Count by Department:")
        plt.figure(figsize=(10, 5))
        sns.countplot(y="Department", data=df, palette="viridis")
        st.pyplot(plt)

        # Visualization: Salary Distribution
        st.write("#### Salary Distribution:")
        plt.figure(figsize=(10, 5))
        sns.histplot(df["Salary"], kde=True, color="blue", bins=10)
        st.pyplot(plt)
        
    except Exception as e:
        st.error(f"Failed to process the file. Error: {str(e)}")

    # Step 3: Q&A Functionality
    st.write("### Ask Questions Based on the Document:")
    default_questions = [
        "What is the total salary?",
        "Who is in the IT department?",
        "What is the average age of employees?",
    ]
    user_question = st_tags(
        label="Enter your question:",
        text="Type a question or select from suggestions",
        value=[],
        suggestions=default_questions,
        key="autocomplete",
    )

    if user_question:
        question = " ".join(user_question)
        with st.spinner("Processing your question..."):
            llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
            qa_chain = load_qa_chain(llm, chain_type="stuff")
            response = qa_chain.run(input_documents=[doc], question=question)
        st.success("Question processed successfully!")
        st.write("#### Answer:")
        st.write(response)
