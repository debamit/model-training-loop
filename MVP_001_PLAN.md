Now that we have Deepagents implemented 

I am rethinking my strategy here. 
May be it's not the best idea to go against the framework of langchain deepagent.
I think the best strategy is to let langchain keep loggin the
HumanMessage, AiMessage and ToolMessage in the List[BaseMessage].

Stop loggin to weights_n_biases.md .