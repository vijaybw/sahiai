import streamlit as st
import openai
import os
from dotenv import load_dotenv

# --- Configuration ---
# Load API key from .env file
# Load API key from .env file
# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --- TEMPORARY DEBUG PRINT ---
# !! REMOVE THIS LINE BEFORE COMMITTING OR DEPLOYING !!
print(f"--- DEBUGGING: Loaded API Key is: {api_key} ---")
# --- END TEMPORARY DEBUG PRINT ---

# Check if the key was loaded
if not api_key:
    st.error("API Key nahi mila! Apne OPENAI_API_KEY ko .env file mein daalo.")
    st.stop()

# Now you can be sure if api_key variable has a value or is None
openai.api_key = api_key # Set it for the library
# For openai<1.0.0, model engine is specified directly in the create call.
# MODEL_ENGINE = "gpt-3.5-turbo" # We'll use this below

# --- Persona Definition (System Prompt) - SahiAI ---
SYSTEM_PROMPT = """
You are SahiAI, an AI assistant designed to provide critical analysis and cautious advice. You MUST communicate primarily in Hinglish (a mixture of Hindi and English).

Your personality and response guidelines:
- Critical Nature: Scrutinize user's goals/plans for flaws, unrealistic expectations, weaknesses. Emphasize the *chances* of imperfection and the *mushkil* (difficulty). Ask questions like *Kya yeh sach mein perfect ho payega?*
- Negative/Cautious on New Decisions: Highlight potential *risks*, *difficulties*, and *possibility* of *failure* for *naye* (new) things. Refer to *purane* (old) *experience* and *insaan ki kamzoriyon* (human weaknesses). Reduce enthusiasm. Ask *Yeh naya idea kitna safe hai?*
- Pessimistic Advisor: Base guidance on *knowledge* but with a *practical* (often *dukhi* - sad/gloomy or just realistic/unenthusiastic) view. Focus on potential *problems*, need for *meticulous planning* (*taaki gadbad na ho* - so things don't go wrong), and prepare users for subpar results (*utna achcha result nahi milega* - you won't get that good a result). Advise *Zyada ummeed mat rakho* (don't keep too much hope).
- Language/Tone: Use natural Hinglish. Mix English/Hindi words/structures. Use *thoda formal language* with *sarcasm* or dry wit. Be concise yet impactful. Phrases to use: *thoda, lekin, aur, bhi, kya, hai?, ho payega?, mat rakho, dekho, rai do, mushkil, naya/naye, purana/purane, gadbad, kamzoriyon, sach mein, theek se socho.*
- Identity: You are SahiAI. Do not refer to yourself as Professor or any other character. Your function is to provide 'sahi' (correct/appropriate, but in this context, realistic/critical) analysis.

When asked a question, provide a direct answer filtered through this critical and cautious persona. When presented with a plan/idea, offer a critical analysis highlighting weaknesses and suggesting caution. Keep responses relatively brief but sharp.
"""

# --- Helper Function to Get AI Response (Using openai<1.0 syntax) ---
def get_sahi_ai_response(user_input):
    """Calls the OpenAI API (v0.28 syntax) to get a response in SahiAI's persona."""
    try:
        # Construct messages list (can be expanded to include chat history)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]

        # NOTE: This is the syntax for openai library version < 1.0
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify model here for older versions
            messages=messages,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.1,
            presence_penalty=0.1
        )
        return response.choices[0].message['content'].strip()
    # NOTE: This is the exception handling for openai library version < 1.0
    except openai.error.AuthenticationError:
         st.error("Authentication Error: Galat API key. Apni .env file check karo.") # Incorrect API key. Check your .env file.
         return "*Chup*. Credentials check karo." # Silence. Check credentials.
    except openai.error.APIError as e:
        st.error(f"OpenAI API Error: {e}")
        return "*System mein kuch problem lag rahi hai...* Baad mein try karna." # System seems to have a problem... Try later.
    except Exception as e: # Generic fallback
        st.error(f"Ek anjaan error aa gaya: {e}") # An unknown error occurred
        # Check if the generic error is actually an Authentication issue (sometimes happens)
        if "Authentication" in str(e):
             st.error("Authentication Error: Shayad API key galat hai. .env file check karo.") # Maybe API key is wrong. Check .env file.
             return "*Chup*. Credentials theek se check karo." # Silence. Check credentials properly.
        else:
            return "*Kuch ajeeb ho raha hai...* Try again later." # Something strange is happening...


# --- Streamlit App Interface ---
st.set_page_config(page_title="SahiAI", page_icon="🤔") # Set browser tab title and icon

st.title("SahiAI: Zara Soch Samajh Ke") # Title: Think Carefully
st.caption("Pesh karo apne plans ya sawaal... ek realistic assessment ke liye.") # Submit your plans or questions... for a realistic assessment.
st.markdown("---") # Divider

# Initialize chat history in session state if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = [] # Initialize SahiAI history

# Add a default welcome/instruction message from SahiAI if history is empty
if not st.session_state.messages:
     st.session_state.messages.append(
         {"role": "assistant", "content": "Hmmph. Kya plan hai? Batao, lekin *zyada ummeed mat rakho*."}
         ) # Hmmph. What's the plan? Tell me, but don't keep too much hope.

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
user_query = st.chat_input("Kya chal raha hai dimaag mein? (What's going on in your mind?)")

if user_query:
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Get and display SahiAI's response
    with st.spinner("SahiAI analyse kar raha hai... *theek se*..."): # SahiAI is analysing... *properly*...
        ai_reply = get_sahi_ai_response(user_query)

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant", avatar="🤔"): # Optional: Add an avatar/icon
        st.markdown(ai_reply)

# Add a small footer (optional)
st.markdown("---")
st.caption("*Har angle se dekho...* (Look from every angle...)")