import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions
import PyPDF2
import json
import pandas as pd
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DocuMind: Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Google API Key", type="password", help="Get yours at aistudio.google.com")
    uploaded_files = st.file_uploader("Upload Business Documents (PDF)", type="pdf", accept_multiple_files=True)
    
    st.divider()
    st.markdown("### 👨‍💻 Developer Mode")
    st.info("Model: gemini-flash-latest")

# --- HELPER FUNCTION: RETRY LOGIC ---
def ask_gemini(model, prompt):
    """
    Wraps the API call with a retry loop. 
    If we hit a rate limit (429), we wait and try again.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return model.generate_content(prompt)
        except exceptions.ResourceExhausted:
            # If we hit the limit, wait 30 seconds and try again
            wait_time = 35 
            st.warning(f"📉 Quota limit hit. Waiting {wait_time}s before retrying (Attempt {attempt+1}/{max_retries})...")
            time.sleep(wait_time)
            continue
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return None
    
    st.error("❌ Failed after multiple retries. Please check your daily quota.")
    return None

# --- MAIN APP ---
st.title("📊 DocuMind: Business Intelligence Engine")
st.markdown("""
This tool uses **Generative AI** to convert unstructured PDF data into **structured business metrics**.
""")

if uploaded_files and api_key:
    # 1. SETUP MODEL
    try:
        genai.configure(api_key=api_key)
        # CRITICAL FIX: Using the exact name from your list
        model = genai.GenerativeModel('gemini-flash-latest')
    except Exception as e:
        st.error(f"API Key Error: {e}")
        st.stop()

    # 2. PROCESS FILES
    all_text = ""
    
    # Progress bar
    progress_text = "Processing documents..."
    my_bar = st.progress(0, text=progress_text)

    try:
        for i, uploaded_file in enumerate(uploaded_files):
            reader = PyPDF2.PdfReader(uploaded_file)
            file_text = ""
            for page in reader.pages:
                file_text += page.extract_text()
            
            # Tagging text for the AI
            all_text += f"\n--- DOCUMENT: {uploaded_file.name} ---\n{file_text}\n"
            my_bar.progress((i + 1) / len(uploaded_files), text=f"Read {uploaded_file.name}")
            
        my_bar.empty()
        st.success(f"✅ Successfully ingested {len(uploaded_files)} documents.")

    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        st.stop()

    # 3. DASHBOARD INTERFACE
    tab1, tab2, tab3 = st.tabs(["📉 Risk Dashboard", "💬 Strategic Chat", "📑 Executive Brief"])

    # --- TAB 1: RISK DASHBOARD ---
    with tab1:
        st.subheader("Automated Compliance & Risk Audit")
        
        if st.button("🚀 Run Risk Analysis"):
            with st.spinner("AI is extracting structured data..."):
                # PROMPT ENGINEERING: Force JSON output
                prompt = f"""
                Act as a Senior Risk Analyst. Analyze the following text from business documents.
                Return a valid JSON object strictly with the following keys:
                
                1. "risk_score": An integer from 0 (Safe) to 100 (High Risk).
                2. "risk_factors": A list of objects, each with "factor" (string) and "severity" (Low/Medium/High).
                3. "primary_concern": A short string summarizing the biggest issue.
                
                Do not use markdown formatting (like ```json). Just return the raw JSON string.
                
                Documents:
                {all_text}
                """
                
                # USE THE NEW RETRY FUNCTION
                response = ask_gemini(model, prompt)
                
                if response:
                    try:
                        clean_json = response.text.replace("```json", "").replace("```", "").strip()
                        data = json.loads(clean_json)
                        
                        # VISUALIZATION
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Aggregate Risk Score", f"{data['risk_score']}/100", delta_color="inverse")
                        with col2:
                            st.warning(f"**Primary Concern:** {data['primary_concern']}")

                        st.write("### Risk Severity Level")
                        risk_val = data['risk_score']
                        color = "green" if risk_val < 40 else "orange" if risk_val < 70 else "red"
                        st.progress(risk_val / 100)
                        
                        st.write("### 🚩 Detected Risk Factors")
                        if data['risk_factors']:
                            df = pd.DataFrame(data['risk_factors'])
                            st.dataframe(
                                df, 
                                column_config={
                                    "severity": st.column_config.SelectboxColumn(
                                        "Severity",
                                        options=["Low", "Medium", "High"],
                                        required=True,
                                    )
                                },
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Analysis failed to parse JSON. Try again. Error: {e}")

    # --- TAB 2: CHAT (RAG) ---
    with tab2:
        st.write("Ask questions across all uploaded files.")
        
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "I'm ready. What insights do you need?"}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Ex: 'What are the payment terms?'"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            with st.spinner("Thinking..."):
                # USE THE NEW RETRY FUNCTION
                response = ask_gemini(model, f"Context: {all_text}\n\nQuestion: {prompt}")
                if response:
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    st.chat_message("assistant").write(response.text)

    # --- TAB 3: SUMMARY ---
    with tab3:
        if st.button("Generate Executive Brief"):
            with st.spinner("Writing summary..."):
                # USE THE NEW RETRY FUNCTION
                response = ask_gemini(model, f"Write a professional executive summary of these documents.\n{all_text}")
                if response:
                    st.markdown(response.text)

elif not api_key:
    st.warning("⬅️ Please enter your Google API Key in the sidebar.")