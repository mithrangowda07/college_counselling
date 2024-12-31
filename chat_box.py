import os
import streamlit as st
from groq import Groq
from fpdf import FPDF

# Streamlit page configuration
st.set_page_config(
    page_title="College Info Chatbot",
    page_icon="🎓",
    layout="centered"
)

# Retrieve and set API key from config
GROQ_API_KEY = "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"

# Validate the API key if it exists
if not GROQ_API_KEY:
    st.error("API key is missing.")
    st.stop()

# Save the API key to the environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize the Groq client with API key
try:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

# Initialize the chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("🎓 College Info Chatbot")

# Function to validate user prompt
def is_valid_prompt(prompt):
    keywords = ["college", "placement", "fee", "ranking", "infrastructure", "course", "admission"]
    return any(keyword in prompt.lower() for keyword in keywords)

# Function to create PDF
def create_pdf(content):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        encoded_content = content.encode('latin-1', 'replace').decode('latin-1')  # Handle special characters
        pdf.multi_cell(0, 10, encoded_content)
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        st.error(f"Error creating PDF: {e}")
        return None

# Display the chat history
for i, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if message["role"] == "assistant":
            response_text = message["content"]
            col1, col2 = st.columns(2)

            # Text download in column 1
            with col1:
                st.download_button(
                    label="Download as Text",
                    data=response_text,
                    file_name=f"response_{i+1}.txt",
                    mime="text/plain"
                )
            
            # PDF download in column 2
            with col2:
                pdf_bytes = create_pdf(response_text)
                if pdf_bytes:
                    st.download_button(
                        label="Download as PDF",
                        data=pdf_bytes,
                        file_name=f"response_{i+1}.pdf",
                        mime="application/pdf"
                    )

# Input field for user message
user_prompt = st.chat_input("Ask about colleges in India...")

if user_prompt:
    if is_valid_prompt(user_prompt):
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # Prepare messages for the LLM
        messages = [
            {"role": "system", "content": "You are a chatbot that provides accurate and concise information about colleges in India, including placements, fees, infrastructure, rankings, and related topics. You must not respond to queries unrelated to these topics."},
            *st.session_state.chat_history
        ]

        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages
            )

            assistant_response = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

            # Display the LLM response
            with st.chat_message("assistant"):
                st.markdown(assistant_response)

                col1, col2 = st.columns(2)
                
                # Text download in column 1
                with col1:
                    st.download_button(
                        label="Download as Text",
                        data=assistant_response,
                        file_name="response_latest.txt",
                        mime="text/plain"
                    )
                
                # PDF download in column 2
                with col2:
                    pdf_bytes = create_pdf(assistant_response)
                    if pdf_bytes:
                        st.download_button(
                            label="Download as PDF",
                            data=pdf_bytes,
                            file_name="response_latest.pdf",
                            mime="application/pdf"
                        )

        except Exception as e:
            st.error(f"Error while fetching the response from GROQ: {e}")
    else:
        st.error("Please ask questions related to colleges, such as placements, fees, infrastructure, or rankings.")
