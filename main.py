from ingestion.youtube_loader import load_youtube_video
from preprocessing.cleaner import clean_transcript
from preprocessing.chunker import chunk_text
from vectorstore.langchain_store import LangChainVectorStore
from graph.graph import build_graph


def main():
    print("1. Provide YouTube URL")
    print("2. Paste transcript manually")

    choice = input("Choose option (1/2): ").strip()

    if choice == "1":
        url = input("Enter YouTube URL: ").strip()
        data = load_youtube_video(youtube_url=url)
    else:
        data = load_youtube_video()

    cleaned_text = clean_transcript(data["content_text"])
    chunks = chunk_text(cleaned_text)

    vector_store = LangChainVectorStore()
    vector_store.build_from_chunks(chunks)

    graph = build_graph(vector_store)

    print("\nAgentic system ready. Ask anything (type EXIT to quit).\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.upper() == "EXIT":
            break

        result = graph.invoke({"user_input": user_input})

        if result.get("answer"):
            print("\nAnswer:\n", result["answer"])
        elif result.get("quiz"):
            print("\nQuiz:\n", result["quiz"])
        elif result.get("summary"):
            print("\nSummary:\n", result["summary"])

        print("-" * 60)


if __name__ == "__main__":
    main()
