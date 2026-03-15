# Q&A Preparation
## AI Presentation Generator — 10 Hardest Questions + Sharp Answers

*Written for: Technical decision-makers, founders, CTOs, product leads*
*Principle: Never defend. Reframe, redirect, and close.*

---

## THE 10 HARDEST QUESTIONS

---

### Q1. "How is this different from just asking ChatGPT to write my slides?"

**Why they ask it:** They've tried ChatGPT. They got mediocre output. They think this is the same thing with a different label.

**The answer:**

"Great question — and the honest answer is: most AI slide tools *are* just ChatGPT with a different label. Here's what's different.

ChatGPT gives you text. You still paste it into PowerPoint, format it, structure it, and export it. You've saved twenty minutes on writing and lost two hours on everything else.

This tool outputs a native `.pptx` file — with layout, speaker notes, and theming — from a single command. Claude doesn't assist the process. It replaces it.

The difference is the same as between a sous chef and a recipe. One hands you instructions. The other hands you dinner."

---

### Q2. "What happens when the AI gets the content wrong?"

**Why they ask it:** They're imagining a deck going out with a hallucinated statistic in a client meeting.

**The answer:**

"The same thing that happens when a junior analyst gets it wrong — you catch it in review.

The difference is: you're reviewing a 60-second first draft, not a four-hour one. Your attention is on substance, not structure. You're catching errors, not building slides.

Every deck this tool generates is a first draft. It's designed to be reviewed. The question isn't whether AI can replace your judgment — it can't. The question is whether it can do the formatting, structure, and speaker notes so you can spend your time on what actually requires judgment. It can."

---

### Q3. "We're in a regulated industry. Can we actually send our topics to an external API?"

**Why they ask it:** Legal, compliance, or security has a standing rule about external data processing.

**The answer:**

"What goes to the API is one sentence: your topic. Not your data. Not your documents. Not your client names.

'Q3 board update' is the level of sensitivity we're talking about. If that sentence is regulated, you have larger problems than this tool.

For environments with stricter requirements — air-gapped, on-prem — the architecture is one API call. Swap the endpoint to a self-hosted model and nothing else changes. The JSON output, the themes, the pptx builder: all local."

---

### Q4. "What's the quality ceiling? Can it actually produce a deck I'd send to a client?"

**Why they ask it:** They're skeptical. They've been burned by AI hype before.

**The answer:**

"I'll answer that with a question: what's the quality ceiling of a first draft from your best analyst?

That analyst still needs your feedback, your edits, your judgment. So does this.

What the tool produces is a structured argument, not a polished final deck. It handles the 80% — structure, flow, speaker notes, formatting — so you spend your time on the 20% that actually requires you.

The clients who've seen the output don't know it was generated. The ones who've asked 'who wrote this?' — that's the ceiling."

---

### Q5. "This is impressive for simple topics. What about complex, multi-stakeholder presentations?"

**Why they ask it:** They're thinking about their hardest use case — the 40-slide QBR with three workstreams.

**The answer:**

"Two options for complex decks.

One: use the tool for the sections that are structure-heavy and low-judgment — the agenda slide, the context-setting section, the appendix. You build the sections that require your specific domain knowledge.

Two: use the `--slides` flag to feed your own JSON structure. Your data, your sections, your hierarchy — the tool handles layout, formatting, and speaker notes. You're the architect; it's the builder.

No tool should replace judgment on a 40-slide stakeholder deck. This one doesn't try to. It handles the parts of that deck that shouldn't require judgment in the first place."

---

### Q6. "What does this cost at scale? If my team of 50 uses this daily, what's the API bill?"

**Why they ask it:** They're doing the math. They're responsible for the budget.

**The answer:**

"Claude API pricing at current rates: approximately three to five cents per presentation, depending on length.

For a team of 50, one deck per person per day: roughly $1.50 to $2.50 per day. Under $1,000 a year.

Compare that to what you're currently spending on that same output in senior labor. The math takes about thirty seconds. I'll let you do it."

*[Stop. Do not do the math for them. Let the silence work.]*

---

### Q7. "Could a competitor clone this in a weekend?"

**Why they ask it:** They're thinking about defensibility. They're a founder or investor.

**The answer:**

"Yes. And so could you.

The tool is open source. That's the point. The moat isn't the code — it's the workflow integration, the institutional knowledge baked into how your team uses it, and the customization layer your developers build on top.

Every enterprise tool gets cloned. The ones that survive are the ones that become infrastructure. That's the design goal here: not a tool you use, but a system you build on."

---

### Q8. "Why would I trust an AI to represent my thinking in a boardroom?"

**Why they ask it:** This is the identity objection. They're protective of their intellectual reputation.

**The answer:**

"You wouldn't — and you shouldn't. And the tool doesn't ask you to.

It generates a frame. You fill the frame with your thinking. Every bullet point is a placeholder for your judgment. Every speaker note is a starting point for your voice.

The question is whether you'd rather start from a blank page or from a structured argument that's 80% of the way there. Nobody trusts a blank page. You trust your ability to improve on a draft.

This is a draft. You're still the author."

---

### Q9. "What if Anthropic changes its pricing or discontinues the API?"

**Why they ask it:** Vendor risk. They've been burned by API deprecations before.

**The answer:**

"It's a real risk. Here's how I think about it.

The tool makes one API call. That call is abstracted behind a single function — `generate_content()`. Swapping the model is a one-line change. OpenAI, Gemini, a self-hosted Llama — the JSON schema output is model-agnostic.

You're not locked into Anthropic. You're locked into a function signature. That's a meaningful distinction."

---

### Q10. "Why is this open source? What's the business model?"

**Why they ask it:** They're suspicious of free things. They're looking for the catch.

**The answer:**

"The business model is the same as every other developer tool that went open source: distribution.

Open source means you find it, fork it, build on it, and tell your network. It means your developers extend it without asking permission. It means adoption happens faster than any sales motion could drive it.

The value isn't in the code. It's in the presentations your team stops spending four hours on. That value accrues to you, not to a subscription."

---

## 3 BRIDGING PHRASES

*Use these when a question tries to pull you off the narrative, into a corner, or into a debate you didn't come to have.*

---

### Bridge 1 — The Reframe
**When to use:** Question attacks the tool on a specific limitation or edge case.

> **"That's exactly the right constraint to put on it — and here's how I'd think about it in that context..."**

*What it does:* Validates their intelligence, signals you've considered this, then redirects to your frame rather than defending theirs.

---

### Bridge 2 — The Acknowledge-and-Advance
**When to use:** Question raises a legitimate concern you don't have a perfect answer for.

> **"Fair point — and I won't pretend it's fully solved. What I will tell you is that the trade-off looks like this..."**

*What it does:* Honesty disarms skepticism faster than a polished deflection. Once you've conceded something real, the room trusts everything else you say.

---

### Bridge 3 — The Return
**When to use:** Question is pulling the room into a technical rabbit hole or off-topic debate.

> **"I want to come back to that — but let me anchor it to the core question first, because I think it changes the answer..."**

*What it does:* You haven't dismissed the question. You've promised to return to it while steering back to your narrative. Most of the time, the room moves on before you have to return.

---

## THE GOLDEN RULE OF Q&A

**Never answer the question they asked. Answer the question they meant.**

Every hostile question has a fear underneath it. Find the fear, address it directly, and close toward your narrative. The question "Can a competitor clone this in a weekend?" isn't about competitors — it's about defensibility and ROI. Answer that.

The presenter who wins Q&A isn't the one with the best answers. It's the one who stays on offense while the room thinks they're playing defense.
