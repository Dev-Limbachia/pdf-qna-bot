import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("pdf_chunks")

def store_and_query_chunks(chunks, embeddings, question):
    ids = [str(i) for i in range(len(chunks))]
    collection.delete(ids=ids)  # clear previous session
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    results = collection.query(query_texts=[question], n_results=4)
    return results['documents'][0]

