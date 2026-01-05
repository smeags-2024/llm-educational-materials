#!/usr/bin/env python3
"""
Interactive LLM Demonstration
Shows practically how pattern matching works vs knowledge retrieval
"""

import random
from typing import List, Dict, Tuple

class SimpleLLMSimulator:
    """
    A toy example showing how LLMs work with patterns, not facts
    """
    
    def __init__(self):
        # Simulated "training data" - patterns the model learned
        self.patterns = {
            "The capital of France is": {
                "Paris": 0.95,
                "London": 0.03,  # Wrong but appeared in some contexts
                "Berlin": 0.02
            },
            "Python was created by": {
                "Guido van Rossum": 0.90,
                "Dennis Ritchie": 0.05,  # Wrong - that's C
                "Linus Torvalds": 0.05   # Wrong - that's Linux
            },
            "The sun rises in the": {
                "east": 0.98,
                "west": 0.01,  # Factually wrong
                "morning": 0.01
            },
            # Fake pattern - shows hallucination
            "The 2025 Nobel Prize in Physics was won by": {
                "Dr. Sarah Chen": 0.33,  # Made up
                "Prof. Ahmed Hassan": 0.33,  # Made up
                "Dr. Jennifer Martinez": 0.34  # Made up
            }
        }
        
        self.knowledge_base = {
            "The capital of France is": "Paris",
            "Python was created by": "Guido van Rossum",
            "The sun rises in the": "east"
        }
    
    def generate_llm_style(self, prompt: str, temperature: float = 0.7) -> Tuple[str, Dict]:
        """
        Simulate LLM generation - picks from probability distribution
        Higher temperature = more random
        """
        if prompt not in self.patterns:
            return "unknown pattern", {}
        
        choices = self.patterns[prompt]
        words = list(choices.keys())
        probabilities = list(choices.values())
        
        # Apply temperature (higher = more random)
        if temperature > 0:
            # Adjust probabilities based on temperature
            adjusted_probs = [p ** (1/temperature) for p in probabilities]
            total = sum(adjusted_probs)
            adjusted_probs = [p/total for p in adjusted_probs]
        else:
            # Temperature 0 = always pick highest probability
            max_idx = probabilities.index(max(probabilities))
            adjusted_probs = [1.0 if i == max_idx else 0.0 for i in range(len(probabilities))]
        
        result = random.choices(words, weights=adjusted_probs)[0]
        
        return result, {w: f"{p*100:.1f}%" for w, p in zip(words, probabilities)}
    
    def retrieve_knowledge(self, prompt: str) -> str:
        """
        Simulate a knowledge base lookup - always returns the same correct answer
        """
        return self.knowledge_base.get(prompt, "Not found in knowledge base")
    
    def demonstrate_hallucination(self):
        """
        Show how hallucination works in practice
        """
        print("=" * 70)
        print("DEMONSTRATION: LLM Pattern Matching vs Knowledge Retrieval")
        print("=" * 70)
        
        for prompt in self.patterns.keys():
            print(f"\n📝 Prompt: '{prompt}'")
            print("-" * 70)
            
            # Show what a knowledge base would return
            correct = self.knowledge_base.get(prompt, "UNKNOWN - not in training data")
            print(f"\n✅ Knowledge Base (correct answer): {correct}")
            
            # Show LLM-style generations with different temperatures
            print(f"\n🤖 LLM Pattern Matching:")
            
            for temp in [0.0, 0.7, 1.5]:
                result, probs = self.generate_llm_style(prompt, temperature=temp)
                correct_marker = "✓" if result == correct else "✗ HALLUCINATION"
                print(f"\n   Temperature {temp}:")
                print(f"   Generated: '{result}' {correct_marker}")
                print(f"   Probability distribution: {probs}")
            
            print()
        
        print("\n" + "=" * 70)
        print("KEY INSIGHTS:")
        print("=" * 70)
        print("""
1. LLMs use PROBABILITY, not lookup
   - Same question can give different answers
   - Even wrong answers can have high probability if they appeared in training
   
2. Temperature affects randomness:
   - 0.0 = Always pick highest probability (still can be wrong)
   - 0.7 = Balanced creativity
   - 1.5 = More random, more likely to pick lower probability options
   
3. Hallucinations happen when:
   - No training data exists (guesses plausible answer)
   - Conflicting data in training (picks wrong pattern)
   - Low probability option gets sampled
   
4. The model is EQUALLY CONFIDENT when wrong
   - No built-in fact-checking
   - No "I don't know" mechanism
   - Generates plausible-sounding completions
        """)

def demonstrate_cascade_effect():
    """
    Show how one wrong word leads to cascading hallucination
    """
    print("\n" + "=" * 70)
    print("DEMONSTRATION: Cascade Effect (Chain Hallucination)")
    print("=" * 70)
    print("""
Scenario: Generating text about a fake event

Prompt: "Write about the 1847 Toronto Summit on European trade"

Step 1: Generate next word after "1847 Toronto Summit"
  Pattern match: [year] [city] [summit] → likely about politics/trade
  Generated: "on" (probability: 85%)

Step 2: Generate next word after "1847 Toronto Summit on"
  Pattern match: summit on [topic] → European, trade, peace, etc.
  Generated: "European" (probability: 60%)

Step 3: Now I'm committed to this narrative
  Each next word builds on the previous
  "The summit convened in September..."
  "Delegates from Britain, France, and Prussia..."
  "The resulting treaty established..."

Result: A completely fabricated but coherent story
Reason: Each word is plausible given the previous context
Issue: No fact-checking that 1847 Toronto Summit never happened
    """)
    
    print("\n💡 This is why I can write entire fake academic papers,")
    print("   cite non-existent sources, and invent historical events")
    print("   that sound completely legitimate!")

def demonstrate_training_data_quality():
    """
    Show how training data quality affects outputs
    """
    print("\n" + "=" * 70)
    print("DEMONSTRATION: Training Data Quality Impact")
    print("=" * 70)
    
    scenarios = [
        {
            "topic": "Vaccine Safety",
            "good_data": 1000,
            "bad_data": 10,
            "result": "95% accurate, 5% chance of anti-vax talking points"
        },
        {
            "topic": "Historical Events",
            "good_data": 5000,
            "bad_data": 100,
            "result": "98% accurate, but might mix in conspiracy theories"
        },
        {
            "topic": "Programming Best Practices",
            "good_data": 10000,
            "bad_data": 500,
            "result": "95% good practices, occasionally suggests bad patterns from Stack Overflow"
        }
    ]
    
    print("\nHow training data mix affects outputs:\n")
    
    for scenario in scenarios:
        total = scenario["good_data"] + scenario["bad_data"]
        good_pct = (scenario["good_data"] / total) * 100
        bad_pct = (scenario["bad_data"] / total) * 100
        
        print(f"Topic: {scenario['topic']}")
        print(f"  Training data composition:")
        print(f"    ✅ High-quality sources: {scenario['good_data']} instances ({good_pct:.1f}%)")
        print(f"    ❌ Low-quality sources: {scenario['bad_data']} instances ({bad_pct:.1f}%)")
        print(f"  Expected output: {scenario['result']}")
        print()
    
    print("Key Point: Even small amounts of bad data can cause problems")
    print("because the model learns ALL patterns, not just correct ones.")

def main():
    """
    Run all demonstrations
    """
    print("\n🧠 UNDERSTANDING HOW LLMs WORK")
    print("A Practical, Interactive Demonstration\n")
    
    simulator = SimpleLLMSimulator()
    
    # Run demos
    simulator.demonstrate_hallucination()
    demonstrate_cascade_effect()
    demonstrate_training_data_quality()
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("""
LLMs are powerful pattern completion systems, but:

❌ They don't "know" facts - they recognize patterns
❌ They can't verify truth - they generate plausible text  
❌ They hallucinate confidently - no uncertainty mechanism
❌ Training data quality matters, but isn't the only issue

✅ Use them for: brainstorming, drafting, coding assistance
✅ Don't use them for: fact verification, medical advice, legal counsel
✅ Always verify: critical facts, citations, technical details
✅ Combine with: human expertise, primary sources, fact-checking

For your "Truth Crisis" project:
→ AI can help analyze patterns at scale
→ But human judgment is irreplaceable for truth determination
→ No AI system can replace domain expertise and critical thinking
    """)
    
    print("\n" + "=" * 70)
    print("Try running this script to see randomness in action!")
    print("Each run will show different results due to probability sampling.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
