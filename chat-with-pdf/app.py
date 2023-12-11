import streamlit as st
import openai
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from styles import css, bot_template, user_template

def get_pdf_text(pdf_docs): #extract text from pdf
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text): #split texts into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks): #store the text chunks in vector
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore): #memory buffer
    llm = ChatOpenAI(model="gpt-4")

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question): #handle the user input and generate questions
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def clear_api_key(): #clear api key
    if 'api_key' in st.session_state:
        del st.session_state.api_key

def main():
    DEFAULT_API_KEY = ""
    st.set_page_config(page_title="IntelLibro", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    st.session_state.api_key = ""

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    

    with st.container():
        user_question = st.chat_input("Ask your questions here:")
        if user_question:
            handle_userinput(user_question)
    
    with st.sidebar:
        st.header("IntelLibro :books: :book:")
        if "api_key" not in st.session_state:
            st.session_state.api_key = None

        user_api_key = st.text_input(":warning: Please input your OpenAI API Key.", DEFAULT_API_KEY, type="password")
        if user_api_key:
            st.session_state.api_key = user_api_key
            openai.api_key = user_api_key
        st.subheader("UPLOAD YOUR FILE/S")
        pdf_docs = st.file_uploader(":warning:NOTE: Your document must be in PDF format.", accept_multiple_files=True)
        if st.button("UPLOAD"):
            with st.spinner("Processing..."):
                if st.session_state.api_key: #check if api key is present
                    for file in pdf_docs:
                        if file.name.endswith(".pdf"): #verify and accept PDF Files only
                            continue
                        else:
                            st.error("Please upload only PDF files.")
                            return
                    # get pdf text
                    raw_text = get_pdf_text(pdf_docs)

                    # get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # create vector store
                    vectorstore = get_vectorstore(text_chunks)

                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                else:
                    st.error("Please provide your OpenAI API key.")
                    return
        st.text("Developed by:\n\nNavarro, Mark Anthony B.\n\nTadena, Juluis S.\n\nFelizario, Jay C.\n\nSolijon, Jessie")
                
if __name__ == '__main__':
    clear_api_key() #clear api key on app start
    main()
