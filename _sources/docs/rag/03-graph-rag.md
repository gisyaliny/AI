# Graph RAG: Knowledge Graphs Meet Retrieval

Traditional RAG struggles with global questions ("How many times is X mentioned?") and loses inter-chunk relationships. **Graph RAG** solves this by building a **knowledge graph** from your documents, enabling both fine-grained and high-level reasoning.

---

## 1. The Limitations of Traditional RAG

Before diving into Graph RAG, let's understand *why* it exists:

| Problem | Example | Why Traditional RAG Fails |
| :--- | :--- | :--- |
| **Global questions** | "What are the main themes of this article?" | No single chunk answers this — the answer spans the entire document. |
| **Counting / aggregation** | "How many times is 'watermelon' mentioned?" | "Watermelon" appears across many chunks; no single chunk is "most similar." |
| **Cross-chunk reasoning** | "Does Wang prefer fruit over vegetables?" | The answer requires connecting information scattered across multiple chunks. |
| **Pronoun resolution** | Chunk 1: "Dr. Wang..." Chunk 2: "He also..." | "He" loses its reference to "Dr. Wang" after chunking. |

> **Core insight**: Traditional RAG treats every chunk as an isolated island. Graph RAG builds bridges between them.

---

## 2. What is a Knowledge Graph?

A knowledge graph is a structured representation of information as a network of **entities** (nodes) and **relationships** (edges).

**Example sentence**: *"Wang likes to eat watermelon."*

In a knowledge graph, this becomes:

```
[Wang] ---(likes to eat)---> [Watermelon]
  │                               │
  └─ type: Person                 └─ type: Fruit
```

### Formal Terminology

| Term | Meaning | Example |
| :--- | :--- | :--- |
| **Entity (Node)** | A distinct thing in your data | "Wang", "Watermelon" |
| **Relationship (Edge)** | A connection between entities | "likes to eat" |
| **Attribute / Property** | Metadata on nodes or edges | Wang.type = "Person" |
| **LPG** | Labeled Property Graph — a graph where nodes and edges can carry labels and properties | The full structure above |

---

## 3. How Graph RAG Builds the Knowledge Graph

Before LLMs, building knowledge graphs required complex NLP pipelines (NER models, dependency parsers, etc.). Graph RAG leverages LLMs to do it all with prompts.

### Step 1: Entity and Relationship Extraction

For each text chunk, Graph RAG sends a prompt to the LLM:

```text
Goal: Extract entities and relationships from the following text.

Entity types to identify: [Person, Object, Location, Event, Concept]

For each entity, provide:
- Entity name
- Entity type
- Brief description

For each relationship, provide:
- Source entity
- Target entity
- Relationship description

IMPORTANT: Only extract information explicitly stated in the text.
Do NOT invent or infer information not present.

Text:
"Wang likes to eat watermelon. Xiao Wang also likes watermelon.
The watermelon tastes sweet."
```

The LLM returns structured output like:

```
Entities:
  - Wang | Person | A person who likes watermelon
  - Xiao Wang | Person | Another person who likes watermelon
  - Watermelon | Fruit | A fruit that tastes sweet

Relationships:
  - Wang → likes to eat → Watermelon
  - Xiao Wang → likes to eat → Watermelon
  - Watermelon → has taste → Sweet
```

### Step 2: Data Gleaning (The "LLM PUA" Loop)

After the initial extraction, Graph RAG sends the results *back* to the LLM and asks:

> "Here is the knowledge graph you generated. Is there anything you missed? Any additional entities or relationships to add?"

If the LLM says yes, it adds more. Then Graph RAG asks again. This loop continues until the LLM confirms: **"I have nothing more to add."**

This iterative refinement process is called **Data Gleaning** and significantly improves extraction completeness.

### Step 3: Merging Across Chunks

After processing every chunk independently, Graph RAG **merges** entities with the same name:
- All "Wang" nodes from different chunks → merged into one "Wang" node.
- All "Watermelon" nodes → merged into one "Watermelon" node.
- Descriptions from different chunks are **concatenated**, then sent to the LLM to generate a unified, coherent summary.

```
Before merge:
  Chunk 1: Wang → "A person who likes watermelon"
  Chunk 3: Wang → "The main character who went to the market"

After merge (LLM-summarized):
  Wang → "The main character, a person who likes watermelon and went to the market"
```

---

## 4. Community Detection: Building Hierarchies

A knowledge graph for a long document can have hundreds or thousands of nodes. To make it navigable, Graph RAG applies **Leiden community detection** to cluster densely connected nodes.

```
Level 0 (Raw):     Wang ── Watermelon ── Sweet
                      │         │
                   Xiao Wang ── Peach

Level 1 (Clusters): [Food Lovers Cluster]    [Taste Cluster]
                     Wang, Xiao Wang,         Sweet
                     Watermelon, Peach

Level 2 (Abstract): [Article Overview]
                     "An article about food preferences
                      of Wang and Xiao Wang"
```

At each level, the LLM generates a **summary description** for the cluster. Crucially, these summaries can contain **inferred information** not explicitly in any single chunk:

> *"Xiao Wang only likes watermelon. Combined with Wang's preference for both watermelon and peach, we can infer that Xiao Wang does not like peach."*

This is reasoning that traditional RAG simply cannot perform.

---

## 5. Indexing: Embedding the Graph

Once the hierarchical knowledge graph is built, Graph RAG converts everything into searchable vectors:

1. **Entity descriptions** → embedded and stored in vector DB 
2. **Relationship descriptions** → embedded and stored
3. **Community summaries (each level)** → embedded and stored
4. **Original text chunks** → embedded and stored (just like traditional RAG)

---

## 6. Querying: Local Search vs. Global Search

Graph RAG offers two complementary search strategies:

### Local Search (Bottom-Up)

**Best for**: Detailed, specific questions ("What does Wang like to eat?")

1. Embed the user's question.
2. Search the **lowest-level** graph entities for the most similar matches.
3. Use the graph's mapping to pull in:
   - Connected neighboring entities and relationships
   - The original source text chunks
   - Higher-level community summaries
4. Package everything and send to the LLM.

### Global Search (Top-Down)

**Best for**: Abstract, panoramic questions ("What is the main theme of this article?")

1. Start from the **highest-level** community summaries.
2. Find the most relevant high-level clusters.
3. Drill down into their sub-communities for supporting detail.
4. Package everything and send to the LLM.

| Feature | Local Search | Global Search |
| :--- | :--- | :--- |
| Starting point | Bottom of hierarchy | Top of hierarchy |
| Strength | Precise, detail-rich answers | Broad, thematic answers |
| Example query | "What are Wang's hobbies?" | "Summarize the key themes" |

---

## 7. Graph RAG vs. Traditional RAG

| Aspect | Traditional RAG | Graph RAG |
| :--- | :--- | :--- |
| **Data structure** | Flat list of chunks | Hierarchical knowledge graph |
| **Cross-chunk reasoning** | ❌ Each chunk is isolated | ✅ Entities link across chunks |
| **Global questions** | ❌ Poor | ✅ Community summaries handle these |
| **Inferred knowledge** | ❌ Only explicit text | ✅ LLM can reason at cluster level |
| **Token cost** | 💰 Low | 💰💰💰 High (LLM used in indexing) |
| **Setup complexity** | Simple | Complex |
| **Best for** | FAQ, support docs | Research papers, reports, legal docs |

---

## 8. Getting Started with Graph RAG

### Option A: Microsoft's GraphRAG (Python)

```bash
pip install graphrag

# Initialize a project
python -m graphrag init --root ./my_project

# Index your documents (builds the knowledge graph)
python -m graphrag index --root ./my_project

# Query with local search
python -m graphrag query --root ./my_project --method local \
  --query "What does Wang like to eat?"

# Query with global search  
python -m graphrag query --root ./my_project --method global \
  --query "What are the main themes of this document?"
```

### Option B: Neo4j + LangChain

```python
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI

# Connect to Neo4j
graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="password")

# Use LLM to extract graph from documents
llm = ChatOpenAI(model="gpt-4o")
transformer = LLMGraphTransformer(llm=llm)
graph_documents = transformer.convert_to_graph_documents(documents)

# Store in Neo4j
graph.add_graph_documents(graph_documents)
```

---

## 9. When to Use Graph RAG

✅ **Use Graph RAG when:**
- Your documents are long and complex (research papers, legal contracts, technical manuals).
- Users ask questions that require cross-document reasoning.
- Global/thematic questions are common.
- Accuracy matters more than cost.

❌ **Stick with Traditional RAG when:**
- Documents are short and self-contained (FAQs, product descriptions).
- Questions are simple and fact-retrieval based.
- Budget is limited (Graph RAG consumes significantly more LLM tokens during indexing).
- Low-latency responses are critical.

---

## Read More

- [GraphRAG: Unlocking LLM Discovery on Narrative Private Data (Microsoft Research)](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/) — The original Microsoft blog post introducing Graph RAG.
- [Microsoft GraphRAG GitHub Repository](https://github.com/microsoft/graphrag) — Official open-source implementation.
- [From Local to Global: A Graph RAG Approach (Paper)](https://arxiv.org/abs/2404.16130) — The academic paper behind Microsoft GraphRAG.
- [Neo4j Graph Database](https://neo4j.com/) — Popular graph database engine for storing knowledge graphs.
- [LangChain Graph Transformers](https://python.langchain.com/docs/how_to/graph_constructing/) — Build knowledge graphs from documents using LangChain.
- [Leiden Community Detection Algorithm](https://www.nature.com/articles/s41598-019-41695-z) — The clustering algorithm used by Graph RAG.
- [Knowledge Graphs: A Comprehensive Survey](https://arxiv.org/abs/2003.02320) — Academic survey of knowledge graph techniques.

---

## Knowledge Quiz

**Q1: What is "Data Gleaning" in the Graph RAG pipeline?**
<details>
<summary>Answer</summary>
Data Gleaning is an iterative loop where Graph RAG sends the extracted knowledge graph back to the LLM and asks: "Did you miss anything? Is there more to add?" The LLM adds more entities/relationships, and the process repeats until the LLM confirms nothing is left. This improves extraction completeness.
</details>

**Q2: Why is Graph RAG significantly more expensive (in tokens) than traditional RAG?**
<details>
<summary>Answer</summary>
Traditional RAG only calls the LLM once per user query (at generation time). Graph RAG calls the LLM extensively during the INDEXING phase — for entity extraction, data gleaning loops, description merging, community summarization at every hierarchy level. The LLM cost is front-loaded into the preparation phase.
</details>

**Q3: When would you use "Global Search" instead of "Local Search" in Graph RAG?**
<details>
<summary>Answer</summary>
Use Global Search for abstract, thematic, or panoramic questions (e.g., "What are the key themes of this report?"). It starts from the top of the knowledge graph hierarchy where summaries are most abstract. Use Local Search for detailed, specific questions (e.g., "What did the author say about method X?") where you need precise, evidence-rich answers from the bottom of the hierarchy.
</details>
