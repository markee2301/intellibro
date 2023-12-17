import os
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from styles import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore
    except IndexError:
        error_message = "An error ocurred while processing your documents. Please consider reading the Developer's note and check your files."
        st.error(error_message)
        return None


def get_conversation_chain(vectorstore):

    try:
        llm = ChatOpenAI(model="gpt-4", api_key=st.session_state.api_key)
        memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain
    except AttributeError: #Display get_vectorstore(text_chunks) error message instead.
        return None

def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.error("Please provide API key and upload files before asking questions.")
        return
    
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="IntelLibro", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    user_question = st.chat_input("Ask your questions here:")
    if user_question:
        try:
            handle_userinput(user_question)
        except Exception as e:
            st.error(str(e))

    with st.sidebar:
        st.header("IntelLibro :book: :books:")
        api_key = st.text_input("Enter your OpenAI API key.👇", type="password")
        # Access and store API key
        if api_key:
            st.session_state.api_key = api_key
        else:
            st.error("⚠️ Please provide your API key.")

        st.subheader("📤 UPLOAD YOUR DOCUMENTS")
        pdf_docs = st.file_uploader(
            "⚠️ Document/s must be in PDF format.\n\n✔️ Please submit text-based PDFs.\n\n❌ Scanned images of text are not supported.", accept_multiple_files=True)
        if st.button("UPLOAD"):
            # Check if files are uploaded before processing
            if pdf_docs is None or len(pdf_docs) == 0:
                st.error("Please select file/s to upload.")
                return
            # Check file extensions
            for pdf_doc in pdf_docs:
                filename = pdf_doc.name
                extension = os.path.splitext(filename)[1].lower()
                if extension != ".pdf":
                    st.error(f"ERROR: '{filename}' is not a PDF file.")
                    return
            with st.spinner("Processing..."):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

        st.text("Developed by:\n\n</>💻 Navarro, Mark Anthony B.\n\n🕵🏽 Tadena, Juluis S.\n\n🕵🏽 Felizario, Jay C.\n\n🕵🏽 Solijon, Jessie\n\n\n🌐 github.com/markee2301/intellibro")
if __name__ == '__main__':
    main()