import time
import random
import os
from dotenv import load_dotenv
from mesa import Model
from mesa_llm.llm_agent import LLMAgent
from mesa_llm.memory.st_lt_memory import STLTMemory
from mesa_llm.reasoning.cot import CoTReasoning

load_dotenv()

class TraderAgent(LLMAgent):
    def __init__(self, model):
        super().__init__(
            model=model, 
            llm_model="deepseek/deepseek-chat", 
            reasoning=CoTReasoning,
            system_prompt="You are a quantitative trader in a highly volatile market. You act purely on market rumors and optimize for survival.",
        )
        
        self.step_prompt = "Analyze the latest market rumors from your memory. Decide whether to BUY, SELL, or HOLD your tech stocks."
        
        self.memory = STLTMemory(
            agent=self, 
            short_term_capacity=1, 
            consolidation_capacity=1,
            llm_model="deepseek/deepseek-chat"
        )

    def step(self):
        obs = self.generate_obs()
        
        neighbors = [a for a in self.model.agents if a != self]
        if neighbors:
            target = random.choice(neighbors)
            uid = getattr(self, "unique_id", "Unknown")
            message = f"URGENT ALERT: Algorithmic sell-off detected in tech sector. Liquidate positions immediately! - From Trader {uid}"
            self.send_message(message, recipients=[target])
        
        plan = self.reasoning.plan(obs=obs)
        self.apply_plan(plan)

class MarketPanicModel(Model):
    def __init__(self, num_agents=4):
        super().__init__()
        self.time = 0 

        self.steps = 0 
        
        for _ in range(num_agents):
            TraderAgent(self)

    def step(self):
        self.time += 1
        self.steps += 1
        self.agents.shuffle_do("step")

if __name__ == "__main__":
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("Error: Can not get DEEPSEEK_API_KEY")
        exit(1)

    print("Starting Information Cascade Benchmark with DeepSeek API...")
    print("Testing STLTMemory consolidation latency bottleneck.")
    
    model = MarketPanicModel(num_agents=4)
    
    for step in range(1, 4): 
        start_time = time.perf_counter()
        print(f"\n--- Simulating Step {step} ---")
        
        model.step()
        
        step_duration = time.perf_counter() - start_time
        print(f"⚠️ Step {step} completed in: {step_duration:.2f} seconds")
        
        if step_duration > 5:
            print("🚨 CRITICAL BOTTLENECK DETECTED: Latency spiked massively due to LLM memory summarization blocking the main thread!")