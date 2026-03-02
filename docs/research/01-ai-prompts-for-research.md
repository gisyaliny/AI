# AI Prompts & Skills for Academic Research

This tutorial is a curated collection of **battle-tested AI prompts** designed to accelerate your academic research workflow. Whether you need to add citations to a manuscript, generate publication-quality figures, build conference slides, or polish your writing, these prompts will turn any modern LLM (Claude, ChatGPT, Gemini, DeepSeek, etc.) into a powerful research assistant.

> **Prerequisites**: Access to an LLM with a "thinking" or "extended reasoning" mode (e.g., Claude with Extended Thinking, ChatGPT o1/o3, Gemini 2.5 Pro, DeepSeek R1). A web-search-enabled mode is strongly recommended for citation tasks.

---

## 1. Auto-Citing a Manuscript Paragraph

This is perhaps the single most time-saving prompt for researchers. You paste in a paragraph of your draft, and the AI finds real, high-quality papers and inserts in-text citations naturally.

### The Prompt (Copy & Paste Ready)

```text
You are an expert academic research assistant. I will provide you with a paragraph
(or multiple paragraphs) from my manuscript draft. Your job is to:

Step 1: Analyze the key claims, arguments, methodologies, or factual statements in
        each paragraph that require scholarly backing.

Step 2: Use your search tools to find relevant, high-quality academic papers for each
        claim. Selection criteria:
        - Prefer peer-reviewed journal articles or top-tier conference papers.
        - Prioritize papers with high citation counts (>50 citations preferred).
        - Strongly prefer papers published within the last 5 years (2021 or later).
        - Include foundational/seminal works if they are critical to the claim,
          even if older.

Step 3: Insert in-text citations into my text where they fit naturally. Use the
        author-year format, e.g., (Smith et al., 2023). Do NOT alter my original
        wording or argumentation — only add citations.

Step 4: Compile a complete, well-formatted reference list at the end. Use
        [GB/T 7714—2015 / APA 7th / IEEE] format (pick one or specify yours).

Step 5: If a claim cannot be supported by a real, verifiable source, flag it with
        [CITATION NEEDED] and briefly explain why.

Output the revised paragraphs with citations, followed by the full reference list.

---
Here is my manuscript text:

[PASTE YOUR PARAGRAPH(S) HERE]
```

### Tips for Best Results
- **Always enable web search / deep research mode.** Without it, the LLM may hallucinate fake papers.
- **Specify your citation format** (APA, IEEE, GB/T 7714, Chicago, etc.) explicitly.
- **Verify every citation.** Cross-check DOIs on Google Scholar or Semantic Scholar. AI can still fabricate plausible-sounding references.
- **Batch wisely.** Feed 2–3 paragraphs at a time, not an entire 20-page paper, for higher accuracy.

---

## 2. Literature Review Synthesis

When you've collected 10–20 papers but need help synthesizing their findings into a coherent narrative:

### The Prompt

```text
You are an expert academic writer. I will provide you with summaries (or abstracts) 
of multiple research papers. Your task is to:

1. Identify the main themes, trends, and debates across these papers.
2. Group the papers thematically (not chronologically).
3. Write a coherent literature review section (approximately 500–800 words) that:
   - Highlights agreements and contradictions among findings.
   - Identifies clear research gaps.
   - Uses smooth transitions between themes.
   - Includes in-text citations in (Author, Year) format.
4. End with a brief paragraph summarizing the overall gap that my research addresses.

Discipline: [e.g., GIScience / Remote Sensing / Urban Computing]
Target journal style: [e.g., Annals of the AAG / IJGIS / Nature Communications]

---
Paper Summaries:

[PASTE ABSTRACTS OR SUMMARIES HERE]
```

---

## 3. Generating Publication-Quality Research Figures

### 3.1 Methodology Flowchart / Framework Diagram

Use this prompt to generate a clean, publication-ready methodology diagram:

```text
You are a scientific illustration expert. Create a detailed Mermaid diagram (or
TikZ/LaTeX code) for the following research methodology:

Research Title: [Your Title]
Methodology Steps:
1. [Data Collection — describe sources]
2. [Preprocessing — describe transformations]
3. [Model/Algorithm — describe approach]
4. [Validation — describe metrics]
5. [Output — describe deliverables]

Requirements:
- Use a top-to-bottom flowchart layout.
- Group related steps into labeled subgraphs (e.g., "Data Preparation", "Modeling").
- Use clean, professional styling suitable for a journal publication.
- Add brief annotations on arrows to describe data flow.
```

### 3.2 Comparison / Results Table as a Figure

```text
Convert the following experimental results into a professional, publication-ready 
comparison table formatted in LaTeX (booktabs style). Include:
- Bold text for the best-performing values in each metric column.
- A descriptive caption.
- Footnotes for any abbreviations.

Results:
[PASTE YOUR RAW RESULTS HERE]
```

### 3.3 AI Image Generation for Conceptual Figures

When you need a conceptual illustration (e.g., for a graphical abstract), use this prompt template for image generation tools (DALL-E, Midjourney, Stable Diffusion):

```text
A clean, professional scientific illustration showing [DESCRIBE THE CONCEPT].
The diagram should include:
- [Element 1 with description]
- [Element 2 with description]
- [Arrows/connections showing relationships]
Style: flat vector illustration, white background, suitable for an academic journal.
Color palette: muted blues, greens, and grays. No photorealistic elements.
Resolution: high-resolution, print-quality.
```

> ⚠️ **Important**: Many journals now require disclosure of AI-generated figures. Always check your target journal's AI policy before submission.

---

## 4. Creating Conference Presentation Slides

### 4.1 Generating a Slide Outline

```text
You are a presentation design expert for academic conferences. Create a detailed 
slide-by-slide outline for a [15/20]-minute research presentation.

Paper Title: [Your Title]
Key Contributions: [List 2-3 main contributions]
Target Audience: [e.g., GIScience researchers, interdisciplinary AI+Geography]

Structure the outline as:
1. Title Slide (title, authors, affiliations, conference name)
2. Motivation & Problem Statement (2 slides)
3. Related Work & Research Gap (1–2 slides)
4. Methodology (3–4 slides, one per major step)
5. Results & Discussion (3–4 slides, key figures + interpretation)
6. Conclusions & Future Work (1 slide)
7. Acknowledgements & Q&A (1 slide)

For each slide, provide:
- A clear slide title
- 3–4 bullet points of key content
- Suggested visual (chart type, diagram, or screenshot)
- Speaker notes (2–3 sentences of what to say)
```

### 4.2 Converting a Paper Section into Slide Content

```text
Convert the following paper section into concise presentation slide content.
Rules:
- Maximum 4 bullet points per slide, each under 15 words.
- Suggest one visual per slide (chart/diagram/image type).
- Write brief speaker notes explaining each slide in conversational tone.
- Remove all jargon that a non-specialist audience wouldn't understand,
  or add a brief parenthetical explanation.

---
Paper Section:
[PASTE SECTION TEXT HERE]
```

---

## 5. Writing Enhancement Prompts

### 5.1 Academic Tone Polishing

```text
You are an expert academic editor for [journal name, e.g., Nature Communications].
Rewrite the following paragraph to:
- Improve clarity and conciseness.
- Use formal academic tone appropriate for the target journal.
- Fix any grammatical errors.
- Strengthen hedging language where claims are not fully proven
  (e.g., "suggests" instead of "proves").
- Keep the original meaning and argumentation intact.

Do NOT add new content or citations. Only polish the language.

---
Original Paragraph:
[PASTE HERE]
```

### 5.2 Abstract Generator

```text
Based on the following paper sections, write a structured abstract of 
approximately [150–250] words. Follow this structure:
1. Background (1–2 sentences): Why is this problem important?
2. Gap (1 sentence): What is missing in existing research?
3. Method (2–3 sentences): What did you do?
4. Results (2–3 sentences): What did you find? Include key quantitative metrics.
5. Significance (1 sentence): Why does this matter?

---
[PASTE INTRO, METHODS, AND RESULTS SECTIONS HERE]
```

---

## 6. Responding to Peer Review Comments

```text
You are an experienced academic author. I will give you a reviewer's comment and 
the relevant section of my manuscript. Help me draft a professional, respectful, 
and thorough point-by-point response.

For each comment:
1. Acknowledge the reviewer's concern.
2. Explain what changes were made (or why no change was needed).
3. Quote the revised text if applicable.
4. If additional experiments or analysis were performed, summarize them.

Tone: professional, grateful, and confident without being defensive.

---
Reviewer Comment:
[PASTE COMMENT]

Relevant Manuscript Section:
[PASTE SECTION]
```

---

## 7. Quick Reference: Recommended Tools

| Task | Recommended AI Tools |
| :--- | :--- |
| Citation & Literature Search | Semantic Scholar, Elicit, Consensus, Scite.ai |
| Writing & Polishing | Claude (Extended Thinking), ChatGPT o3, Gemini 2.5 Pro |
| Methodology Diagrams | Mermaid.js, draw.io, Lucidchart AI, TikZ/LaTeX |
| Scientific Figures | BioRender, Matplotlib + AI assist, GraphPad Prism |
| Conceptual Illustrations | DALL-E 3, Midjourney, Stable Diffusion, Illustrae |
| Presentation Slides | Gamma.app, Beautiful.ai, Canva Magic Design, Slidesgo |
| Peer Review Response | Claude, ChatGPT (with paper context) |

---

## 8. Curated Resources & Further Reading

### AI-Powered Research & Writing Tools
- [Semantic Scholar](https://www.semanticscholar.org/) — Free AI-powered academic search engine with citation graphs and paper recommendations.
- [Elicit](https://elicit.com/) — AI research assistant that finds papers, extracts claims, and synthesizes findings automatically.
- [Consensus](https://consensus.app/) — Search engine that uses AI to extract answers directly from peer-reviewed scientific papers.
- [Scite.ai](https://scite.ai/) — Shows how a paper has been cited (supporting, contrasting, or mentioning) by other publications.
- [Connected Papers](https://www.connectedpapers.com/) — Visual tool to explore academic paper similarity graphs and discover related work.

### Scientific Figure & Illustration Tools
- [BioRender](https://www.biorender.com/) — AI-powered scientific figure creation with thousands of pre-built icons and templates.
- [Illustrae](https://illustrae.co/) — AI-assisted scientific illustration platform for publication-ready visuals.
- [Mermaid.js Live Editor](https://mermaid.live/) — Free online editor for creating flowcharts, sequence diagrams, and Gantt charts with code.
- [draw.io (diagrams.net)](https://app.diagrams.net/) — Free, open-source diagramming tool for methodology flowcharts and architecture diagrams.
- [SciDraw](https://sci-draw.com/) — AI prompt templates and guidance for generating scientific figures.

### Presentation & Slide Tools
- [Gamma.app](https://gamma.app/) — AI-powered presentation builder that generates polished decks from text prompts.
- [Beautiful.ai](https://www.beautiful.ai/) — Smart slide design tool with auto-formatting and professional templates.
- [Slidesgo](https://slidesgo.com/ai-presentations) — Free AI presentation maker with academic and research templates.
- [Canva Magic Design](https://www.canva.com/magic-design/) — AI-generated presentations with drag-and-drop customization.

### Prompt Engineering Guides
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) — Official best practices for crafting effective prompts.
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — Claude-specific prompting strategies and techniques.
- [Learn Prompting](https://learnprompting.org/) — Free, open-source course covering prompt engineering fundamentals and advanced techniques.

### Academic Writing with AI (Articles & Tutorials)
- [Nature: Tools such as ChatGPT threaten transparent science](https://www.nature.com/articles/d41586-023-00107-z) — Nature's perspective on responsible AI use in research.
- [Paperpal](https://paperpal.com/) — AI-powered academic writing assistant with grammar, citation, and consistency checks.
- [Ref-N-Write](https://www.ref-n-write.com/) — Academic paraphrasing and writing tool with a phrase bank from published papers.

---

## Knowledge Quiz

**Q1: Why is it critical to enable "web search" or "deep research" mode when using the citation prompt?**
<details>
<summary>Answer</summary>
Without web search, the LLM generates responses purely from its training data and may "hallucinate" — fabricating papers that look realistic but don't actually exist. Web search mode forces the model to verify sources against live databases like Google Scholar or Semantic Scholar.
</details>

**Q2: What is the risk of directly using AI-generated figures in a journal submission without disclosure?**
<details>
<summary>Answer</summary>
Many top journals (Nature, Science, IEEE, etc.) now require explicit disclosure of any AI-generated content, including figures. Failure to disclose can lead to desk rejection, retraction, or ethical violations. Always check the target journal's AI policy.
</details>

**Q3: When responding to peer review, what tone should your reply maintain?**
<details>
<summary>Answer</summary>
The response should be professional, grateful, and confident — acknowledging the reviewer's concerns respectfully while clearly explaining the changes made or providing justification for why no changes were necessary. Avoid defensive or dismissive language.
</details>
