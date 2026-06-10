from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)


def chunk_text(text: str) -> list[str]:
    return splitter.split_text(text)
