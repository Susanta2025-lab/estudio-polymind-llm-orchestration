import requests
import streamlit as st

# =====================================================
# CONFIGURATION
# =====================================================

API_URL = "http://127.0.0.1:8001/query"

st.set_page_config(
    page_title="Estudio PolyMind",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    # Profile Picture
    st.image(
        "ui/assets/susanta.png",
        width=180
    )

    st.markdown(
        """
        <h3 style='text-align:center; margin-bottom:0px;'>
        Susanta Hazra
        </h3>

        <p style='text-align:center; color:gray;'>
        AI Engineer • LLM Specialist • Machine Learning Enthusiast
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.title("🧠 Estudio PolyMind")

    st.markdown(
        """
        **Multi-LLM RAG & Agent Orchestration Platform**
        """
    )

    st.markdown(
        """
        Built using:

        - LangGraph
        - ChromaDB
        - FastAPI
        - Ollama
        - Mistral
        - Qwen
        - Gemma
        - Phi
        """
    )

    st.divider()

    st.subheader("🔗 Connect")

    st.markdown(
        """
        💻 GitHub
        https://github.com/Susanta2025-lab

        💼 LinkedIn
        https://www.linkedin.com/in/susantahazra/
        """
    )

    st.divider()

    session_id = st.text_input(
        "Session ID",
        value="default"
    )

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# =====================================================
# MAIN PAGE
# =====================================================

st.title("🧠 Estudio PolyMind")

st.caption(
    "Multi-LLM RAG & Agent Orchestration Platform"
)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

# =====================================================
# USER INPUT
# =====================================================

prompt = st.chat_input(
    "Ask anything..."
)

# =====================================================
# PROCESS QUERY
# =====================================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    try:

        payload = {
            "query": prompt,
            "session_id": session_id
        }

        response = requests.post(
            API_URL,
            json=payload,
            timeout=120
        )

        result = response.json()

        answer = result.get(
            "response",
            "No response generated."
        )

        route = result.get(
            "route",
            "unknown"
        )

        model = result.get(
            "model",
            "unknown"
        )

        sources = result.get(
            "sources",
            []
        )

        with st.chat_message("assistant"):

            st.markdown(answer)

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.info(
                    f"📍 Route: {route.upper()}"
                )

            with col2:
                st.success(
                    f"🤖 Model: {model}"
                )

            if sources:

                st.subheader("📚 Sources")

                for source in sources:

                    source_name = source.get(
                        "source",
                        "Unknown"
                    )

                    chunk_id = source.get(
                        "chunk_id",
                        "-"
                    )

                    score = source.get(
                        "score",
                        0
                    )

                    st.markdown(
                        f"""
                        **Source:** {source_name}

                        - Chunk ID: {chunk_id}
                        - Score: {score}
                        """
                    )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:

        st.error(
            f"Error connecting to API: {e}"
        )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Powered by LangGraph • ChromaDB • Ollama • FastAPI • Streamlit"
)
