from rag.loaders.pdf_loader import load_pdf

text = load_pdf(
    "data/docs/LangGraph_Documentation.pdf"
)

print("=" * 50)
print("TEXT LENGTH:")
print(len(text))

print("=" * 50)
print("FIRST 1000 CHARS:")
print(text[:1000])
