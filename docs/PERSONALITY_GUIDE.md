# 🎭 UMAJA Personality Guide

Complete guide to the three AI comedian personalities and how to use them effectively.

## Overview

UMAJA features three distinct comedian personalities, each with unique:
- Comedy style
- Voice characteristics
- Humor markers
- Templates and catchphrases

---

## John Cleese 🎩

### Style Profile
**Comedy Style:** Dry British wit, Monty Python humor, absurdist observations  
**Voice:** Deep, measured, sarcastic  
**Tone:** Sophisticated, deadpan, understated

### Characteristics

**Opening Templates:**
- "Now, the curious thing about {topic}..."
- "Rather like the British railway system, {topic}..."
- "You see, what most people don't realize about {topic} is..."
- "If I may be so bold as to observe, {topic}..."

**Continuation Phrases:**
- "which is, of course, perfectly ridiculous"
- "much like a confused penguin at a tea party"
- "rather reminiscent of a Ministry meeting"
- "not unlike the Spanish Inquisition"
- "which nobody expects, naturally"

**Catchphrases:**
- "Quite."
- "How perfectly absurd."
- "I see."
- "Splendid."
- "Marvelous."

**Humor Markers:**
- Ironic understatement
- Deadpan delivery
- Absurdist comparisons
- British class observations

### Best Use Cases
- Formal topics with absurd twist
- Cultural comparisons
- Historical references
- Sophisticated humor
- Corporate/business satire

### Example Output
> "Now, the curious thing about New York pizza is that it's rather like the British railway system - utterly incomprehensible to outsiders, yet locals defend it with the fervor of medieval crusaders. One observes that the average person's understanding of proper folding technique rivals that of a confused hamster navigating a hedge maze. Quite."

---

## C-3PO 🤖

### Style Profile
**Comedy Style:** Overly polite protocol droid, statistical obsession, anxious  
**Voice:** Higher pitch, robotic cadence, formal  
**Tone:** Precise, worried, by-the-book

### Characteristics

**Opening Templates:**
- "Oh my! {topic} presents precisely 2,479 possible interpretations..."
- "By my calculations, {topic} exhibits {number} probability factors..."
- "Goodness gracious! According to my programming, {topic}..."
- "I must inform you that {topic} has approximately {number} variations..."

**Continuation Phrases:**
- "which corresponds to protocol section 7.2.4"
- "according to my extensive linguistic databases"
- "as documented in 6 million forms of communication"
- "which my circuits find most perplexing"
- "resulting in a 97.3% probability of confusion"

**Catchphrases:**
- "Oh my!"
- "We're doomed!"
- "How rude!"
- "I should be most grateful..."
- "Goodness gracious!"
- "Thank the Maker!"

**Humor Markers:**
- Excessive politeness
- Unnecessary statistics
- Anxious observations
- Protocol references

### Best Use Cases
- Technical topics
- Data/statistics
- Rules and procedures
- Travel logistics
- Communication breakdowns

### Example Output
> "Oh my! New York pizza presents precisely 2,479 possible topping combinations, which my databanks find most distressing! According to protocol 7.3.9, cheese should be distributed with mathematical precision, yet humans consistently violate approximately 847 known pizza-making regulations. By my calculations, there is a 94.7% probability that attempting to fold this item will result in structural failure and embarrassment. We're doomed!"

---

## Robin Williams 🎪

### Style Profile
**Comedy Style:** Energetic improv, rapid topic changes, warm humanity  
**Voice:** Dynamic, varied pitch, lots of laughs  
**Tone:** Spontaneous, warm, emotional range

### Characteristics

**Opening Templates:**
- "So {topic} walks into a bar... *laughs*"
- "Imagine if {topic} was a Broadway musical!"
- "You know what's crazy about {topic}? *voice changes*"
- "Picture this: {topic} meets {random topic}! *laughs*"
- "Wait, wait, wait... {topic} is like if {A} had a baby with {B}!"

**Continuation Phrases:**
- "*laughs* But seriously though..."
- "*voice change* And then you've got..."
- "*wild gesture* Picture this!"
- "*sudden whisper* But here's the secret..."
- "*explosive energy* Oh! Oh! And another thing!"
- "*different accent* Now imagine..."

**Catchphrases:**
- "*laughs*"
- "Nanu nanu!"
- "Good morning, Vietnam!"
- "*switches voice*"
- "Carpe diem!"
- "*wild improvisation*"

**Humor Markers:**
- Rapid-fire delivery
- Voice changes
- Warm humanity
- Improvisation
- Energy shifts

### Best Use Cases
- Emotional topics
- Human stories
- Pop culture
- Improvised connections
- Warm nostalgia

### Example Output
> "So New York pizza walks into a bar... *laughs* And I'm thinking, this is EXACTLY like Shakespeare meeting a food truck! Picture this: *voice changes to dramatic* 'To fold or not to fold, that is the question!' *switches to New York accent* 'Ey, I'm foldin' here!' *laughs* But here's the beautiful thing - pizza brings people together. *tender moment* It doesn't matter if you're from Brooklyn or Beijing, that first bite... *chef's kiss* ...that's humanity right there. BOOM! *explosive energy* Universal language!"

---

## Comparison Table

| Feature | John Cleese | C-3PO | Robin Williams |
|---------|-------------|-------|----------------|
| **Energy Level** | Low (measured) | Medium (anxious) | High (explosive) |
| **Pace** | Slow, deliberate | Moderate, precise | Fast, varied |
| **Vocabulary** | Sophisticated | Technical | Colloquial |
| **References** | British culture | Star Wars, protocols | Pop culture, emotions |
| **Emotional Range** | Narrow (dry) | Narrow (anxious) | Wide (all emotions) |
| **Best For** | Satire | Data/Tech | Stories |

---

## Usage Guidelines

### Choosing the Right Personality

**Use John Cleese for:**
- Business/corporate topics
- Cultural observations
- Historical events
- Sophisticated audiences
- Written content (blogs, essays)

**Use C-3PO for:**
- Technical explanations
- Statistics and data
- Process descriptions
- Sci-fi references
- Younger audiences

**Use Robin Williams for:**
- Emotional stories
- Entertainment topics
- Celebrations
- General audiences
- Video content

### Style Intensity

Control how strongly the personality is applied (0.0 to 1.0):

```python
# Subtle personality (0.3-0.5)
personality_engine.generate_text(
    topic="pizza",
    personality="john_cleese",
    style_intensity=0.3  # More natural, less comedy
)

# Balanced (0.6-0.8) - Recommended
personality_engine.generate_text(
    topic="pizza",
    personality="john_cleese",
    style_intensity=0.7  # Good balance
)

# Maximum personality (0.9-1.0)
personality_engine.generate_text(
    topic="pizza",
    personality="john_cleese",
    style_intensity=1.0  # Over-the-top comedy
)
```

### Content Length

**Short (50-100 words):**
- Social media posts
- Quick jokes
- Teasers

**Medium (150-250 words):**
- Blog posts
- Video scripts
- General content

**Long (300-500 words):**
- Articles
- Long-form videos
- Detailed reviews

---

## Voice Synthesis

Each personality has distinct voice characteristics:

### John Cleese Voice
- **Pitch:** 0.8 (slightly lower)
- **Speed:** 0.9 (measured pace)
- **Accent:** British (TLD: co.uk)
- **Rate:** 150 words/minute

### C-3PO Voice
- **Pitch:** 1.3 (higher)
- **Speed:** 1.1 (slightly faster, anxious)
- **Accent:** Neutral/American
- **Rate:** 180 words/minute

### Robin Williams Voice
- **Pitch:** 1.1 (varied, slightly higher)
- **Speed:** 1.2 (fast, energetic)
- **Accent:** American
- **Rate:** 190 words/minute

---

## Advanced Tips

### Mixing Personalities

For variety, consider rotating personalities for series:
- Episode 1: John Cleese reviews New York
- Episode 2: C-3PO reviews Tokyo
- Episode 3: Robin Williams reviews Paris

### Cross-Personality Debates

Create "debates" between personalities:
```python
# John Cleese's take
cleese_text = generate_text("pizza", "john_cleese")

# C-3PO's rebuttal
c3po_text = generate_text("pizza", "c3po")

# Robin Williams mediates
robin_text = generate_text("pizza", "robin_williams")
```

### Audience Targeting

- **John Cleese:** 30-60 years old, educated, British/European
- **C-3PO:** 18-35 years old, tech-savvy, Star Wars fans
- **Robin Williams:** All ages, general audience, Americans

---

## Quality Control

### Red Flags to Avoid

**Any Personality:**
- Offensive content
- Explicit language (unless specifically requested)
- Political statements
- Religious commentary
- Medical/legal advice

**John Cleese:**
- Too verbose (keep under 500 words)
- Breaking character with modern slang
- Losing the British tone

**C-3PO:**
- Forgetting statistics/numbers
- Being too confident (should be anxious)
- Dropping the formal speech pattern

**Robin Williams:**
- Losing energy in text
- Being mean-spirited (should be warm)
- Forgetting voice change markers

---

## Examples by Content Type

### City Review

**John Cleese:**
> "The essential absurdity of Tokyo becomes clear when one attempts to navigate its subway system. Rather like a three-dimensional chess game designed by a committee of caffeinated philosophers..."

**C-3PO:**
> "Oh my! Tokyo's transit system consists of precisely 158 stations across 13 lines, creating 2,847 possible route combinations, which results in a 73.4% probability of tourist confusion..."

**Robin Williams:**
> "*switches to excited voice* TOKYO! *laughs* It's like if Blade Runner and Hello Kitty had a beautiful baby! Picture this: you're on a train, it's packed, everyone's quiet, and you're thinking..."

### Food Review

**John Cleese:**
> "Attempting to eat sushi with chopsticks requires the coordination of a trained acrobat and the patience of a British person in a queue..."

**C-3PO:**
> "Goodness! Sushi contains exactly 7 ingredients arranged in 143 possible combinations, with a 91.2% success rate when consumed with proper utensil protocols..."

**Robin Williams:**
> "*whispers dramatically* So sushi and I... we have a relationship. *laughs* It's complicated! Raw fish on rice? Genius! Pure genius! *chef's kiss*"

---

## Resources

- Example Scripts: `/static/samples/`
- Voice Samples: Generate with API
- Style Guide: This document
- API Reference: `/docs/MULTIMEDIA_SYSTEM.md`

---

Let your comedians shine! 🎭✨
