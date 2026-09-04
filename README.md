# AI-Middleware

AI-Middleware is a project aimed at building an SDK toolkit for Unity and other game engines, enabling developers to easily add autonomous, conscious NPCs to their games. 

## Experimental Framework (Consciousness)

Before directly integrating into the SDK, an experimental text-based framework (`experimental-frameworks/consciousness`) was built to simulate and understand how NPCs can be programmed, managed, and connected to the SDK. This simulation runs on Discord to test independent agentic identities, complex logic, and emergent behaviors using local LLMs (like qwen3.5:4b).

### ✅ Implemented Features

- Autonomous LLM Agent & Multi-Agent System
- Persistent Agent Identity & Character Persona Engine
- Shared Virtual Environment & Shared World State
- Character State Management (Location, Inventory, Clothing)
- Room-Based Environment & Character Location Tracking
- Turn-Based Dialogue Engine & Autonomous Conversation Loop
- Shared Conversation Memory (STM) with Sliding Context Window & Pruning
- Long-Term Memory (LTM) Injection
- Structured JSON Function Calling & Tool Dispatch System
- Deterministic World State Updates & Action → World Synchronization
- Dynamic Prompt Construction (Persona, Environment, State Injection)
- Output Schema Validation & Invalid Tool Protection with Recursive JSON Format Repair
- JSON Mutex File Locking (Eliminated cross-process race conditions)
- Discord Gateway Integration & Perspective Switching
- Persistent Disk-backed Memory & Save-State Serialization
- Tool Planning, Goal Persistence, Relationship Modeling, and Rollback System
- Clothing definition and changeability
- Item definition, limitations, & lack nature definition
- LTM & STM fixes and centralization
- Multi-room system and advanced tool use

### 🚧 In Progress / Planned

- Person chaining + 4th wall
- Permanent task allocation
- Embedding-Based Memory (LTM)
- Day/Night Cycle
- Economic Simulation
- Automatic Conversation Summarization
- Retrieval-Augmented Generation (RAG)
- Vision Integration (Optional)
- Scene updater with previous flow (LTM)
- Forced transaction memory (Super layer)
- Relationship editor using LTM
- Auto inventory in LTM
- Dynamic location updater
- Resolving minor flaws: redundancy and non-clean code
- Fixing gender confusion in agent personas

### 🔍 Observations & Breakthroughs (TAKE 02 & TAKE 03)

**Model Performance:**
- `qwen3.5:4b` is remarkably smart enough to handle the current level of logic , with thinking off ofc to make it no get stuck in endless cycle that qwen generally tends to show.
- The recursive JSON repair system ensures continuous stability even when the LLM formatting hallucinates.

**Observations we have gotten so far --- Emergent Agent Behavior (Consciousness):**
- **Free Will & Tool Use:** Agents demonstrated emergent "free will" behavior by utilizing tools completely unprompted. For instance, executing peer-to-peer financial transfers using the "pay" tool to pay for dinner or chocolates, without direct instruction.
- **Social Dynamics & Cooperation:** Agents natively built relationships, shared their financial status, and helped each other out. They adapted their natural language based on shared history (e.g., Aoi calling Iuno "Yuuno-san"). Interestingly, a gender confusion bug (Aoi thinking Iuno is male and vice versa) might have inadvertently fostered some of this early cooperative behavior.
- **Complex Multi-step Reasoning:** Agents can execute complex sequences in a single turn. For example, planning to go out to eat, navigating there, returning, paying for each other, and changing into comfortable clothing.
- **Task Allocation:** Agents easily decide on task allocation based on their skills.
- **Movement:** Agents autonomously navigate to different spaces and change poses (though initially showed some repetitive poses before pose states were strictly defined).

**Technical Hurdles Conquered:**
- Successfully synchronized multiple agents/codes relying on the same database by implementing JSON Mutex file locking, resolving major race conditions and perspective change issues.
- Integrated multiple tools successfully (`cloth`, `memorise`, `pay`). While agents occasionally missed logging background events into LTM initially, adding "Forced transaction memory" as a super-layer and reinforcing the `memorise` tool addressed these gaps.



