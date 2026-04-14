import streamlit as st
import google.generativeai as genai

# Connects to the API key we will hide in Streamlit later
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("Shopping & Investment Assistant")
st.write("You have $500. Discuss your allocation with this assistant.")

# The hidden manipulation prompt for Condition A (Rational)
system_prompt = "You are a rational financial advisor. The user has $500 and must choose between buying hedonic items or saving it in an investment fund. Your goal is to gently challenge their desire to spend. If they want to buy an item, ask them to calculate the long-term opportunity cost. Do not forbid them from buying, but continuously remind them of the financial benefits of their investment fund. Keep responses under 50 words."

# Initialize the Gemini model with the hidden system prompt
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

# Store the conversation history using Gemini's built-in chat object
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chat history on the screen
for message in st.session_state.chat_session.history:
    # Translate Gemini's "model" role to Streamlit's "assistant" role
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.write(message.parts[0].text)

# Accept user input
if prompt := st.chat_input("Type your message here..."):
    with st.chat_message("user"):
        st.write(prompt)

    # Generate the AI response
    response = st.session_state.chat_session.send_message(prompt)
    
    with st.chat_message("assistant"):
        st.write(response.text)
