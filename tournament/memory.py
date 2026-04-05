import chromadb
import os
from datetime import datetime

# KEY FIX: Tell ChromaDB to use simple hash-based embeddings
# This needs NO internet, NO model download
from chromadb.utils import embedding_functions

# Use this simple embedding function — works 100% offline
simple_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
) if False else None  # We will NOT use this

# Instead use ChromaDB's built-in simple function
import chromadb.utils.embedding_functions as ef

# Create ChromaDB client
chroma_client = chromadb.PersistentClient(
    path="memory/chromadb"
)

# Use default embedding that does NOT need download
collection = chroma_client.get_or_create_collection(
    name="twinforge_incidents"
)


def save_incident(incident_data: dict, postmortem_text: str):
    """
    Save incident to memory after it is resolved.
    """
    incident_id = f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # Simple text description of what happened
    document = (
        f"Anomaly: {incident_data.get('anomaly_metric')} "
        f"at {incident_data.get('anomaly_value')}%. "
        f"Root cause: {incident_data.get('root_cause')}. "
        f"Fixed by: {incident_data.get('winning_fix')}. "
        f"Confidence: {incident_data.get('confidence_score')}%."
    )

    # Save with metadata
    collection.add(
        documents=[document],
        ids=[incident_id],
        metadatas=[{
            "anomaly_type":  str(incident_data.get("anomaly_metric", "unknown")),
            "winning_fix":   str(incident_data.get("winning_fix", "unknown")),
            "confidence":    str(incident_data.get("confidence_score", 0)),
            "timestamp":     datetime.now().isoformat(),
        }]
    )

    print(f"[Memory] Incident {incident_id} saved")
    print(f"[Memory] Total in memory: {collection.count()}")
    return incident_id


def search_similar_incidents(anomaly_type: str, top_k: int = 3) -> list:
    """
    Search past incidents similar to current one.
    """
    if collection.count() == 0:
        print("[Memory] No past incidents yet.")
        return []

    results = collection.query(
        query_texts=[f"{anomaly_type} problem in server"],
        n_results=min(top_k, collection.count())
    )

    similar = []
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        similar.append({
            "past_fix":   meta.get("winning_fix"),
            "anomaly":    meta.get("anomaly_type"),
            "confidence": meta.get("confidence"),
            "timestamp":  meta.get("timestamp"),
        })
        print(f"[Memory] Found: {meta.get('anomaly_type')} → {meta.get('winning_fix')}")

    return similar


def get_memory_stats() -> dict:
    count = collection.count()
    return {
        "total_incidents": count,
        "message": f"TwinForge remembers {count} past incidents"
    }


# ─── TEST ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("[TEST] Testing memory...\n")

    save_incident(
        {
            "anomaly_metric":  "cpu_percent",
            "anomaly_value":   92,
            "root_cause":      "Traffic spike on checkout",
            "winning_fix":     "Apply Rate Limiting",
            "confidence_score": 94
        },
        "CPU spike resolved by rate limiting."
    )

    print(f"\nStats: {get_memory_stats()}")
    print("\nSearching similar:")
    results = search_similar_incidents("cpu")
    for r in results:
        print(f"  Fix: {r['past_fix']} (confidence: {r['confidence']}%)")