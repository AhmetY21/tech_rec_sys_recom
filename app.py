import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
import os
#from utils import history_teller  # Not needed now since we'll define a similar function inline

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(api_key=api_key),
    persist_directory="vectorstore_data"
)
# Assuming vectorstore is already defined and contains embeddings from Çatalhöyük PDF
# For example: vectorstore = Chroma.from_documents([...], embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# Define the catalhoyuk_info function
def catalhoyuk_info(question):
    """Retrieve detailed information about Çatalhöyük based on user's question."""
    # Retrieve relevant context from the vector database
    retrieved_context = retriever.get_relevant_documents(question)
    
    # Concatenate retrieved contexts
    context_text = "\n".join(doc.page_content for doc in retrieved_context)

    # System-level prompt tailored for Çatalhöyük
    system_prompt = (
        "Sen, Çatalhöyük hakkında detaylı bilgi veren bir yardımcı asistansın. Aşağıdaki soruya dayanarak "
        "Çatalhöyük ile ilgili arkeolojik, tarihi, kültürel ve yapısal özellikleri anlat. "
        "Lütfen bilgileri başlıklar, madde işaretleri ve uygun yerlerde emoji kullanarak ve Markdown formatında sun.\n\n"
        "İşte Çatalhöyük hakkında bağlam:\n\n{context}"
    )

    # Prepare messages for the OpenAI chat completion
    messages = [
        {"role": "system", "content": system_prompt.format(context=context_text)},
        {"role": "user", "content": question}
    ]
    
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages
    )
    
    return response.choices[0].message.content

api_key = os.getenv("OPENAI_API_KEY")

# Set page configuration
st.set_page_config(page_title="Çatalhöyük Rehberi", page_icon="🏺", layout="centered")

# Title
st.title("Çatalhöyük'e Sanal Tur Rehberi 🏺")

# Display embedded PDF about Çatalhöyük (ensure catalhoyuk.pdf is in the directory)
pdf_file = "catalhoyuk.pdf"
st.markdown("### Tur Rehberi")

st.markdown("---")

st.markdown("### Merak Ettiğiniz Soruyu Sorun:")
user_question = st.text_input("Çatalhöyük hakkında merak ettiğiniz herhangi bir şeyi sorun...")

if user_question.strip():
    with st.spinner("Bilgi alınıyor..."):
        output = catalhoyuk_info(user_question)
    #st.markdown("#### Cevap:")
    st.markdown(output, unsafe_allow_html=True)
else:
    st.info("Çatalhöyük hakkında bir soru girin ve Enter'a basın.")

# Footer
st.markdown("---")



'''import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from utils import history_teller
# Load environment variables from .env file
load_dotenv(override=True)

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")


# Load environment variables from .env file

client = OpenAI(api_key=api_key)

# Set page configuration
st.set_page_config(page_title="Türkiye'yi Keşfet", page_icon="🌍", layout="centered")

# Display a banner image (ensure 'turkey_banner.jpg' is in your directory)
#st.image('turkey_banner.jpg', use_column_width=True)

# Title
st.title("Bulunduğunuz Şehrin Tarihini Keşfedin🌟")


# List of cities in Turkey
cities = [
    "Istanbul", "Ankara", "Izmir", "Antalya", "Bursa",
    "Adana", "Konya", "Gaziantep", "Kayseri", "Mersin",
    "Diyarbakır", "Erzurum", "Eskişehir", "Samsun", "Trabzon"
]

# Markdown with list of cities
st.markdown("## Bulunduğunuz Şehri Seçiniz:")
#st.markdown(", ".join(cities))

# Dropdown to select a city
selected_city = st.selectbox("Şehirler:", options=["Seç"] + cities)

# Check if a valid city is selected
if selected_city != "Seç":
    # Call the history_teller function with a loading spinner
    with st.spinner(f"{selected_city} için Geçmişin İzleri Toplanıyor ..."):
        output = history_teller(selected_city)
    
    # Display the output
    st.markdown("### Şehirler İlgili Bilgiler:")
    st.markdown(output, unsafe_allow_html=True)
else:
    st.info("Lütfen Bir Şehir Seçiniz.")

# Footer
st.markdown("---")
'''