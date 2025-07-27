import streamlit as st
import requests

# ---- Page Config ----
st.set_page_config(page_title="Multi-Model Chatbot", layout="centered")
st.title("🤖 Multi-Model Chatbot")

# ---- Model Options ----
MODEL_OPTIONS = {
    "Gemini Pro (Google)": "gemini-pro",
    "LLaMA 2 7B": "llama2-7b",
    "LLaMA 2 13B": "llama2-13b",
    "GPT-4 (OpenAI)": "gpt-4",
    "Claude 3 Haiku (Anthropic)": "claude-3-haiku",
    "Command R+": "command-r-plus",
    "Mixtral 8x7B": "mixtral-8x7b",
    "Phi-3 Mini": "phi-3-mini"
}

# ---- Secrets for API keys ----
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
# Add other APIs as needed

# ---- Session State ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = list(MODEL_OPTIONS.values())[0]

# ---- Sidebar ----
with st.sidebar:
    model_name = st.selectbox("Choose a model", list(MODEL_OPTIONS.keys()))
    st.session_state.selected_model = MODEL_OPTIONS[model_name]
    st.markdown("---")
    if st.button("🔁 Clear Chat"):
        st.session_state.chat_history = []

# ---- User Input ----
user_input = st.chat_input("Say something...")

# ---- Display Chat History ----
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# ---- Send Prompt ----
if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("bot"):
        with st.spinner("Thinking..."):
            model = st.session_state.selected_model
            if model == "gemini-pro":
                bot_reply = call_gemini_api(user_input, GOOGLE_API_KEY)
            else:
                bot_reply = f"*Demo response for `{model}`: (API not yet integrated)*"

            st.markdown(bot_reply)

    st.session_state.chat_history.append({"role": "bot", "text": bot_reply})

# ---- Gemini API Function ----
def call_gemini_api(prompt, api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, headers=headers, params=params, json=data)
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return "❌ Error parsing Gemini response."
    else:
        return f"❌ Error from Gemini API: {response.text}"
