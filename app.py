import streamlit as st
import os

# Pagina configuratie
st.set_page_config(
    page_title="Anesthesie Literatuur & Boeken",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Anesthesie Literatuur Databank")
st.markdown("Welkom! Dit is de centrale bibliotheek voor boeken, richtlijnen en artikelen van de dienst anesthesie. Iedereen kan hier documenten aan toevoegen en doorzoeken.")

# Mappen aanmaken als ze nog niet bestaan
os.makedirs("data/literatuur", exist_ok=True)

# Twee tabbladen: 1. Bibliotheek & Upload, 2. AI Vraagbaak
tab1, tab2 = st.tabs(["📖 Bibliotheek & Upload", "🤖 AI Vraagbaak"])

# --- TAB 1: BIBLIOTHEEK & UPLOAD ---
with tab1:
    st.header("Boeken & Artikelen Beheren")
    
    # Bestand uploaden
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

# --- TAB 2: AI VRAAGBAAK ---
with tab2:
    st.header("🤖 AI Vraagbaak")
    st.markdown("Stel vragen over de toegevoegde boeken en artikelen in de literatuurbank.")
    
    user_query = st.text_input("Typ je vraag (bijv. 'Wat zegt de literatuur over de aanpak van een moeilijke luchtweg?'):")
    
    if st.button("Verstuur vraag"):
        if user_query:
            with st.spinner("AI doorzoekt de literatuur..."):
                # Hier kun je de koppeling met Gemini / NotebookLM API maken
                st.success(f"**Antwoord van de AI** (op basis van de wereldliteratuur voor: *'{user_query}'*):")
                st.write("De AI haalt hier straks de relevante passages uit de geüploade boeken en artikelen op om je van een onderbouwd antwoord te voorzien.")
        else:
            st.warning("Voer eerst een vraag in.")
