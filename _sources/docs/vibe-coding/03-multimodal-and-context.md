# Multimodal & Context Management

This chapter introduces how Claude Code interacts with the outside world through visual inputs and the Model Context Protocol (MCP), and how to manage the AI's memory (context) for long-running projects.

## 1. What is MCP (Model Context Protocol)?

Think of Claude Code as a brilliant brain. By default, it can read and write files on your computer. But what if it needs to query your live PostgreSQL database, fetch issues from your GitHub board, read documentation from a live website, or extract Figma design tokens? 

**MCP Servers** act as the "hands and eyes" for Claude. They are standardized connectors that let Claude securely interact with external tools and data sources.

### Authentic Example Workflow: Adding a PostgreSQL MCP

Imagine you want Claude to analyze your local database structure and write a SQL migration script. 

1. **Install the MCP via CLI Wizard:**
   In your terminal, run:
   ```bash
   claude mcp add db -- npm -y @modelcontextprotocol/server-postgres postgresql://localhost/mydb
   ```
2. **Interact:**
   Once installed, you can ask Claude Code: 
   *"Use the db tool to list all tables, then write a query to find users who signed up in the last 30 days."*
3. **How it works:** Claude Code automatically calls the `db` MCP server, assesses the schema, and generates the exact query. You never have to manually paste database schemas into the chat!

## 2. Using Visuals: Multimodal Input

Sometimes, describing a UI purely with text is impossible. You can provide Claude Code directly with your design mockups or screenshots.

- **Drag and Drop**: Drag the image directly into your active terminal running Claude Code.
- **Clipboard Paste**: Copy the image and use `Ctrl + V` to paste it. *(Note: Even on macOS, you must use `Ctrl + V`, not `Command + V`, inside the terminal)*.


## 3. High-Fidelity UI Generation (The Figma MCP)

While pasting a screenshot is great for rough prototyping, an image lacks exact font sizes, hex colors, and margin data. For pixel-perfect React or HTML components, use the Figma MCP instead:

1. **Setup:** Install the official Figma MCP server (`claude mcp add figma ...`).
2. **Authenticate:** Type `/mcp`, select the Figma tool, and follow the browser authentication link.
3. **Prompt it:** *"Modify `index.html` to match the Figma mockup exactly. Here is the link: [Figma Object Link]"*
4. **Result:** Claude uses the MCP to fetch the exact design tokens (padding: 16px, background: #1A1A1A, etc.) and writes a 1:1 matching code component.

## 4. Managing AI Memory (Context)

As you chat, paste images, and call MCP tools, Claude's "context window" (its short-term memory) gets crowded. A bloated context makes the AI slower, more expensive, and prone to forgetting early instructions.

### The `/compact` Command Workflow
When you notice Claude getting sluggish after a long coding session:
1. Type `/compact` and press Enter.
2. The system intelligently summarizes the development focus, decisions, and outcomes of the current cycle.
3. It permanently discards massive intermediate data (like long error logs or the Base64 strings of previous images).
4. Response speed returns to normal, and Token costs drop dramatically! *(Use `Ctrl + O` to view the compacted summary).*

### The `/clear` Command
If you are moving on to a completely different task (e.g., from Frontend styling to Backend database design), use `/clear`. This completely eradicates the memory of the current chat, giving you a fresh, fast slate.

## 5. Version Rewind & Resuming

- **Oops, go back! (`/rewind`)**: If Claude writes bad code, type `/rewind` (or tap `ESC` twice). You can select a previous moment in the conversation and choose "Restore code and session" to undo the AI's file edits. *(Note: It cannot undo `npm install` or other shell commands).*
- **I closed the terminal! (`/resume`)**: If you accidentally close your terminal, just reopen it, type `claude`, and then type `/resume` to pick up exactly where you left off. Alternatively, start Claude with `claude -c` (Continue) to auto-load the last session.

## 6. Project Memory: CLAUDE.md

How do you give Claude permanent instructions that persist across *every* session? (e.g., "Always use TypeScript, never use classes, prefer functional components").

- **Create the file**: Run `/init` to generate a `CLAUDE.md` file in your project root.
- **Edit it**: Add your strict project guidelines. Every time Claude Code starts in this folder, it reads `CLAUDE.md` as its fundamental system prompt.

---

## Knowledge Quiz

**Q1: Why is using the Figma MCP superior to simply pasting a PNG screenshot of a design?**
<details>
<summary>Answer</summary>
A PNG image loses exact metadata like font-weight, precise padding, and exact hex colors. The MCP Server reads the raw design tokens directly from Figma's API, ensuring pixel-perfect 1:1 code reproduction.
</details>

**Q2: What happens when you run the `/compact` command after a long coding session?**
<details>
<summary>Answer</summary>
It summarizes your progress and decisions while throwing away bulky intermediate data (like long crash logs or image strings). This speeds up the AI and reduces token costs without losing the high-level project context.
</details>
