# My Mesa-LLM GSoC Learning Space

Welcome! I am Zhehao Zhao, a Data Science Master's student in Shanghai Jiao Tong University specializing in AI systems architecture. This repository documents my journey exploring the architectural limits of `mesa-llm` and prototyping solutions for production-grade, multi-agent social simulations. 

As per the GSoC guidelines, my core philosophy here is: **Push the framework to its absolute limits, identify the real performance bottlenecks, and architect solutions based on empirical data.**

---

## 🚀 Highlighted Models & Benchmarks

### 1. [Information Cascade & Memory Latency Benchmark](./models/information_cascade/)
* **Domain:** Quantitative Trading & Financial Panic (Information Cascade).
* **Objective:** Stress-test the existing `STLTMemory` module under high-frequency, multi-agent interaction using the DeepSeek API.
* **Key Finding (The Bottleneck):** Uncovered a severe $O(N)$ API latency bottleneck (**92.57s per step for just 4 agents**) that completely blocks the main thread. This empirically validates the urgent need for a dependency-free Vector RAG architecture, as detailed in my **[Architecture RFC #190]**.
* **Emergent Behavior:** Documented fascinating LLM hallucinations where agents succumbed to "Self-fulfilling Prophecies" due to memory consolidation degradation.

## 🤝 Peer Reviews & Collaboration

Mesa is built by the community. I actively participate in technical discussions and code reviews to ensure the framework's stability and architectural integrity, especially during the migration to Mesa 4.x.

### 🔍 Highlighted Code Reviews

* **[Mesa-Examples PR #378] - LLM Prisoner's Dilemma: Concurrency & Scientific Modeling**
  * **Context:** Reviewed a major contribution replacing rigid game theory strategies with LLM Chain-of-Thought reasoning. Evaluated strictly against the #390 Review Guidelines.
  * **Architectural Insights:** * **Concurrency & ABM Rigor:** Identified a critical "Dirty Read" vulnerability and UI-blocking $O(N)$ latency caused by sequential LLM calls. Authored a `ThreadPoolExecutor` refactor that decouples the "thinking" from "acting" phases, guaranteeing simultaneous decision-making and massive speedups.
    * **Robust Output Parsing:** Flagged a brittle string-matching logic that broke the core game mechanics due to LLM verbosity. Recommended enforcing strict JSON-guided outputs for scientific correctness.
    * **Mesa 4.0 API Compliance:** Steered the implementation away from manual state tracking toward native `model.time` attributes for seamless DataCollector integration.
  * **Outcome:** Elevated an innovative proof-of-concept into a scientifically strict, performant, and Mesa 4.0-compliant ABM template.

* **[Mesa-LLM PR #195] - Debugging & API Compatibility:**
  * **Context:** Reviewed a major update for Mesa 4.x compatibility and `__repr__` debugging enhancements.
  * **Architectural Insights:** * **Safety & Performance:** Identified potential **RecursionError** and terminal bloat risks in `LLMAgent.__repr__` when handling massive nested dictionaries. Suggested a **$O(1)$** string generation strategy using `reprlib`.
  * **Security Auditing:** Flagged potential **Sensitive Data Leakage** via `api_base` URLs in logging/repr outputs to protect user authentication tokens.
  * **Runtime Integrity:** Supported the transition away from test-mock logic (`SimpleNamespace`) in production code paths to ensure a cleaner runtime environment.

  * **Outcome:** Facilitated a safer, more robust implementation of agent inspection tools.

---
*Built for Google Summer of Code 2026.*