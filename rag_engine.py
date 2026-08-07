import chromadb

# Local-ah 'chroma_db' nu oru folder-la database-ah save pandrom
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Policies-ah store panna oru collection create pandrom
collection = chroma_client.get_or_create_collection(name="company_policies")

def load_policies_to_db():
    # Already data iruntha marubadiyum load panna thevaiyilla
    if collection.count() > 0:
        return

    # Namma create panna policies.txt file-ah read pandrom
    with open("data/policies.txt", "r") as file:
        content = file.read()
    
    # Paragraph paragraph-ah pirikirom
    policies = content.split("\n\n")
    
    # Ovvoru policy-ayum vector database-la add pandrom
    for i, policy in enumerate(policies):
        if policy.strip():
            collection.add(
                documents=[policy],
                ids=[f"policy_{i}"]
            )
    print("ChromaDB: Policies loaded successfully!")

def get_relevant_policy(ticket_text: str):
    # Customer ticket-ku match aagura policy-ah thedi edukurom (Semantic Search)
    results = collection.query(
        query_texts=[ticket_text],
        n_results=1
    )
    
    if results['documents'] and results['documents'][0]:
        return results['documents'][0][0]
    return "No specific policy found."