import streamlit as st
import os
import google.generativeai as genai

# Pagina configuratie
st.set_page_config(
    page_title="Anesthesie Literatuur & Ask Dr. Soetens",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Anesthesie Literatuur Databank")
st.markdown("Welkom! Dit is de centrale bibliotheek voor boeken, richtlijnen en artikelen van de dienst anesthesie.")

# API Sleutel configuratie via de Sidebar of Streamlit Secrets
st.sidebar.header("⚙️ Instellingen")
api_key = st.sidebar.text_input("Google Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("Voer je Gemini API Key in om Dr. Soetens te activeren.")

# Mappen aanmaken als ze nog niet bestaan
os.makedirs("data/literatuur", exist_ok=True)

# Twee tabbladen: 1. Bibliotheek & Upload, 2. Ask Dr. Soetens
tab1, tab2 = st.tabs(["📖 Bibliotheek & Upload", "🩺 Ask Dr. Soetens"])

# --- TAB 1: BIBLIOTHEEK & UPLOAD ---
with tab1:
    st.header("Boeken & Artikelen Beheren")
    
    uploaded_file = st.file_uploader("Upload een PDF of document:", type=["pdf", "txt", "docx"])
    if uploaded_file is not None:
        file_path = os.path.join("data/literatuur", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Bestand '{uploaded_file.name}' succesvol toegevoegd aan de literatuur!")

    st.markdown("---")
    st.subheader("Beschikbare Documenten in de Databank")
    
    lit_files = os.listdir("data/literatuur")
    if lit_files:
        for file in lit_files:
            st.text(f"📄 {file}")
    else:
        st.info("Nog geen literatuur geüpload. Upload hierboven het eerste bestand.")

# --- TAB 2: ASK DR. SOETENS ---
with tab2:
    st.header("🩺 Ask Dr. Soetens")
    st.markdown("Stel een klinische of wetenschappelijke vraag. Dr. Soetens geeft advies op basis van de geüploade literatuur.")
    
    user_query = st.text_input("Typ je vraag voor Dr. Soetens (bijv. 'Wat is het beleid bij een moeilijke intubatie?'):")
    
    if st.button("Vraag het Dr. Soetens"):
        if not api_key:
            st.error("Vul eerst je Gemini API Key in via de sidebar links.")
        elif user_query:
            with st.spinner("Dr. Soetens overlegt met de literatuur..."):
                try:
                    # We gebruiken het snelle en slimme Gemini model
                    model = genai.GenerativeModel('gemini-3.8-flash')
                    
                    # Zoek naar lokale bestanden om mee te sturen als context
                    context_tekst = ""
                    lit_files = os.listdir("data/literatuur")
                    
                    # Lezen van tekstbestanden / upload context als demo
                    for file in lit_files:
                        if file.endswith(".txt"):
                            with open(os.path.join("data/literatuur", file), "r", encoding="utf-8") as f:
                                context_tekst += f"\n--- Bron: {file} ---\n" + f.read()

                    prompt = f"""
                    Je bent Dr. Soetens, een doorgewinterde specialist anesthesie. 
                    Beantwoord de volgende vraag op een professionele, klinische en wetenschappelijk onderbouwde manier, passend bij een academische/perifere dienst anesthesie.
                    
                    Beschikbare literatuur context:
                    {context_tekst}
                    
                    Vraag van de collega: {user_query}
                    """
                    
                    response = model.generate_content(prompt)
                    st.success("**Advies van Dr. Soetens:**")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"Er is een fout opgetreden bij het raadplegen van de AI: {e}")
        else:
            st.warning("Voer eerst een vraag in.")
