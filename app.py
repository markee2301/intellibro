import streamlit as st
from PyPDF2 import PdfReader
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
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception: #If PDF is empty. Don't print error message.
            continue  # Skip to the next PDF document
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,
        chunk_overlap=1000,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    try:
        # Ensure the API key is available in the session state
        if 'api_key' in st.session_state and st.session_state.api_key:
            # Pass the API key directly to OpenAIEmbeddings
            embeddings = OpenAIEmbeddings(openai_api_key=st.session_state.api_key)
            vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
            return vectorstore
        else:
            # Handle the case where the API key is not provided
            st.error("⚠️ Please provide your API key.")
            return None
    except IndexError:
        #Error message if PDF contain image.
        error_message = "An error occurred while processing your documents. Please consider reading and following the Developers' note above and try again."
        st.error(error_message)
        return None
    except Exception:
        # Error message if API Key is incorrect.
        error_message = "An error occurred. Please check your API key and try again."
        st.error(error_message)
        return None

def get_conversation_chain(vectorstore):

    try:
        llm = ChatOpenAI(temperature=0.2, model="gpt-4", api_key=st.session_state.api_key)
        memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain
    except AttributeError: #If there is an error in the retriever. Don't print error message.
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
    st.set_page_config(page_title="IntelLibro", page_icon="icon.png")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    user_question = st.chat_input("Ask your questions here:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.header("IntelLibro :book: :books:")
        api_key = st.text_input("Enter your OpenAI API key.👇", type="password")
        # Access and store API key
        if api_key:
            st.session_state.api_key = api_key
        else:
            st.error("⚠️ Please provide your API key.")
            st.markdown("No API Key? Get yours [here!](https://platform.openai.com/api-keys)", unsafe_allow_html=True)
        st.markdown("To know more about IntelLibro. Visit our website [here!](https://intellibro.netlify.app/)", unsafe_allow_html=True)

        st.subheader("📤 UPLOAD YOUR DOCUMENTS")
        if not api_key:
            pdf_docs = st.file_uploader("⚠️ Document/s must be in PDF format.\n\n✔️ Please submit text-based PDFs.\n\n❌ Scanned images of text are not supported.", disabled=True, type=["pdf"], accept_multiple_files=True)
            #Disable Upload Button if no File/s selected
            if pdf_docs is None or len(pdf_docs) == 0:
                st.button("UPLOAD", disabled=True)

        else:
            pdf_docs = st.file_uploader("⚠️ Document/s must be in PDF format.\n\n✔️ Please submit text-based PDFs.\n\n❌ Scanned images of text are not supported.", type=["pdf"], accept_multiple_files=True)
            #Disable Upload Button if no File/s selected
            if pdf_docs is None or len(pdf_docs) == 0:
                st.button("UPLOAD", disabled=True)

            else:
                if st.button("UPLOAD"):
                    # Validate each uploaded document
                    all_files_valid = True
                    for pdf_doc in pdf_docs:
                        if not pdf_doc.name.lower().endswith('.pdf'):
                            st.error(f"ERROR: '{pdf_doc.name}' is not a PDF file.")
                            all_files_valid = False
                            break  # Stop processing further if any invalid file is found
                
                    if all_files_valid:
                        # Process the uploaded PDF files if all files are valid
                        with st.spinner("Processing..."):
                            # get pdf text
                            raw_text = get_pdf_text(pdf_docs)

                            # get the text chunks
                            text_chunks = get_text_chunks(raw_text)

                            # create vector store
                            vectorstore = get_vectorstore(text_chunks)

                            # create conversation chain
                            st.session_state.conversation = get_conversation_chain(vectorstore)

        st.text("Developed by:\n\n</>💻 Navarro, Mark Anthony B.\n\n🕵🏽 Tadena, Juluis S.\n\n🕵🏽 Felizario, Jay C.\n\n🕵🏽 Solijon, Jessie\n\n\n\n🤙Contact Us🤙\n\n📧 itsmark2301@gmail.com\n\nⓕ facebook.com/markee2301")
if __name__ == '__main__':
    main()