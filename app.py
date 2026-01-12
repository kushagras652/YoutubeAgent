import streamlit as st

from ingestion.youtube_loader import load_youtube_video
from preprocessing.cleaner import clean_transcript
from preprocessing.chunker import chunk_text
from vectorstore.langchain_store import LangChainVectorStore
from graph.graph import build_graph


st.set_page_config(
    page_title="Agentic YouTube Tutor",
    layout="wide"
)

st.title("🎓 Agentic YouTube Tutor")
st.write("Learn from YouTube videos using Agentic AI (LangGraph + RAG)")

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if "graph" not in st.session_state:
    st.session_state.graph = None

if "ready" not in st.session_state:
    st.session_state.ready = False

# -----------------------------
# INPUT SECTION
# -----------------------------
st.header("1️⃣ Provide Video Input")

input_type = st.radio(
    "Choose input type:",
    ["YouTube URL", "Paste Transcript"]
)

youtube_url = None
manual_text = None

if input_type == "YouTube URL":
    youtube_url = st.text_input("Enter YouTube URL")
else:
    manual_text = st.text_area(
        "Paste transcript here (required)",
        height=200
    )

# -----------------------------
# PROCESS VIDEO
# -----------------------------
if st.button("🚀 Process Video"):
    with st.spinner("Processing video..."):

        if input_type == "YouTube URL":
            data = load_youtube_video(youtube_url=youtube_url)
        else:
            data = {
                "content_text": manual_text,
                "content_source": "manual_input"
            }

        # Phase 2: Cleaning
        cleaned_text = clean_transcript(data["content_text"])

        # Phase 3: Chunking
        chunks = chunk_text(cleaned_text)

        # Phase 4: Vector Store
        vector_store = LangChainVectorStore()
        vector_store.build_from_chunks(chunks)

        # Phase 7: LangGraph
        graph = build_graph(vector_store)

        st.session_state.graph = graph
        st.session_state.ready = True

    st.success("✅ Video processed successfully!")

# -----------------------------
# INTERACTION SECTION
# -----------------------------
if st.session_state.ready:
    st.header("2️⃣ Interact With the Video")

    mode = st.radio(
        "Choose what you want to do:",
        ["Ask a Question", "Generate Quiz", "Get Summary"]
    )

    user_input = ""

    if mode == "Ask a Question":
        user_input = st.text_input("Ask your question")

    elif mode == "Generate Quiz":
        user_input = st.text_input(
            "Enter quiz topic (optional)",
            placeholder="Enter generate question answers"
        )

    elif mode == "Get Summary":
        user_input = "summarize the video"

    if st.button("▶ Run"):
        with st.spinner("Thinking..."):
            result = st.session_state.graph.invoke(
                {"user_input": user_input}
            )

        st.subheader("📤 Output")

        if result.get("answer"):
            st.text(result["answer"])

        elif result.get("quiz"):
            st.text(result["quiz"])

        elif result.get("summary"):
            st.write(result["summary"])

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built with LangGraph, LangChain & OpenAI")
