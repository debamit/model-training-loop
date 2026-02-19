**My Intuition**:

when I think of modern day LLM training.
I think of it like this:
LLMs are pre-trained on the vast majority of basic internet data. (Evidence: large models use self-supervised objectives like next-token or masked-token prediction on web-scale corpora — e.g. Common Crawl, books, code — which is what GPT/BERT-style pretraining does.)
Then reinforcement learning happens with experts. (Evidence: teams collect human demonstrations and preference rankings, train a reward model, and use RL — often PPO — to align the model to those preferences; this is the RLHF approach used in recent models.)
Where most model makers take what people are saying when they interact with their models and then use experts to come up with better ways to approach those problems. (Evidence: usage data plus curated expert feedback guide supervised fine-tuning and iterative policy updates so the model behaves more helpfully and safely.)
Explain the training process.
Be concise and short

**Idea (Personal Code only evolving Personal Assistant)**: 
How do we replicate this whole process but in an Agent.
I talk to an agent locally; I tell it my preferences, what I think of the world, and what should be considered the right answer and source of truth.
Then, at night or any other scheduled time, it reviews the conversation and searches the internet or the chain (on-chain) for information or evidence to answer the same problems or questions it encountered during the day with the user.

It can then present metrics and highlights about what it learned and how its understanding of the user's preferences evolved.
The user can choose whether or not to update a `Weights-n-Biases.md` file.

**Weights and Biases**:
Agent creates goals (weights):
Eg:
- user's goal is to make a payment
- user's goal is to create a travel plan, etc.

The agent creates a goal if one does not already exist, then records the Journeys (biases).

At first the agent performs the task (makes tool calls and generates an answer), then it documents the journey.
Eg:
Goal: user's goal is to make a payment
Journey: made the payment with their Capital One VISA card, and recorded the LLM workflow used to achieve the task — which tool calls were made and which sources were checked.

OR
Goal: user's goal is to create a travel plan
Journey:
- (Journey requirements) looked up road-trip information, searched three options, and targeted trips within the specified budget.
- (Journey path) the LLM workflow used, tool calls made, sources checked, and the outcome.

Once goals exist, the agent can run a scheduled exploration job to research other tool calls and options. In exploration mode (higher temperature) the aim is to discover alternative payment methods or different trip options, then update the `Weights-n-Biases.md` file with new journey paths.

So next time the user asks about the same thing, the LLM can show additional options and may adjust which sources it prioritizes or tweak biases accordingly.
