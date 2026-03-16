# Information Cascade & Memory Latency Benchmark

## 1. Concept & Motivation
As part of my GSoC 2026 learning process, I built this model to investigate how `mesa-llm` handles high-frequency, multi-agent interactions. Specifically, I simulated a financial market panic (Information Cascade) spreading among quantitative traders using the **DeepSeek API**.

I wanted to test the friction points between traditional ABM discrete-event scheduling and LLM context window management in a high-pressure communication scenario.

## 2. Experimental Setup
- **Scenario:** 4 Trader Agents passing a critical market crash rumor ("Algorithmic sell-off detected in tech sector").
- **Framework Limitations Pushed:** I deliberately used `STLTMemory` with a highly constrained capacity (`short_term_capacity=1`, `consolidation_capacity=1`). This configuration aggressively simulates what inevitably happens during a long-running simulation: the short-term buffer fills up and triggers LLM-based consolidation.
- **Reasoning:** `CoTReasoning` (Chain-of-Thought)
- **API Backend:** `deepseek/deepseek-chat` via litellm.

## 3. What I Discovered (The Architectural Bottleneck)
Running this model exposed a critical architectural friction point where the framework's synchronous design clashes with LLM latency.

### 3.1 Exponential Latency Bloat
Below is the performance data from my latest benchmark run:

```text
⚠️ Step 1 completed in: 67.82 seconds
🚨 CRITICAL BOTTLENECK DETECTED: Latency spiked massively...

--- Simulating Step 2 ---
⚠️ Step 2 completed in: 0.00 seconds (Buffer recently cleared)

--- Simulating Step 3 ---
⚠️ Step 3 completed in: 98.06 seconds
🚨 CRITICAL BOTTLENECK DETECTED: Latency spiked massively...

```

**Observation:** A single time step for just 4 agents took **98.06 seconds** to complete. The delay is not caused by the agents' "reasoning," but rather by the synchronous, blocking LLM API calls inside `_update_long_term_memory()`. The entire Mesa event loop halts to wait for the LLM to generate summary strings for each agent whose memory buffer is full.

### 3.2 Emergent Behavior & Hallucination

Beyond the latency, the simulation showcased fascinating but dangerous emergent behavior caused by the current memory architecture:

* **Herd Behavior:** Agent 2 received a rumor from Agent 3 and immediately shifted from a "HOLD" stance to an "URGENT SELL," amplifying the panic.
* **Self-fulfilling Prophecy (Echo Chamber):** In a striking display of memory degradation, **Agent 3 received an "URGENT ALERT" from itself** via its consolidated memory. It failed to recognize the rumor originated from its own previous step, treated it as a confirmed market signal, and decided to `SELL` based on its own echo.

## 4. Conclusion & Link to Proposal

Building this model proved firsthand that relying on active LLM generation for memory maintenance (Summarization) cannot scale for multi-agent social simulations. The network I/O overhead and blocking nature destroy Mesa's performance budget.

This hands-on experiment perfectly validates the architectural hypothesis I published in **[Architecture RFC #190]** (Resolving Step Latency). To push `mesa-llm` to production readiness, we must decouple memory consolidation from LLM generation entirely.

**Proposed Solution:** Transition to a dependency-free, pure-NumPy Vector RAG retrieval mechanism. This would:

1. Drop the memory maintenance latency to $O(1)$ locally.
2. Prevent main-thread blocking.
3. Preserve the exact fidelity of rumors by avoiding lossy "summaries of summaries."

---

## 📂 Supplementary Materials
* **[Full Execution Log](./model_trace.log):** Contains the complete step-by-step trace of agent reasoning and communication.
* **[Benchmark Script](./model.py):** The source code to reproduce this latency spike.
