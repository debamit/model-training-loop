THinking out loud 

What is the chat analysis agent should do 

Following the client , server model
Remember the client can be a human or agent and so can the server be a human or agent.
The aim is to learn from the humans feedback.

Parts of the Conversations can be categorized as

Query → Information seeking (questions, clarifications, exploring options)
Action → Task execution (requests to do something, commands)
Preferences → Context sharing (opinions, constraints, feedback, background info)

while these represent the three fundamental type of information in a conversation ,
the quality of the response id dictated by 

Sentiment: Positive, neutral, negative, frustrated
Urgency: High priority vs exploratory
Clarity: Well-defined vs ambiguous/needs clarification
Follow-up type: New topic vs continuation of previous discussion

These are more important for the server.


Why is it important to have this classification step

Responding to the Query or executing the Task 
These are both things that are done by the server
So it needs to understand what kind it is

Eg:
Query: whats the weather in LA

This is a simple query , but the journey still might depend on the if the previous turns in the conversation.
If the previous conversation was about a road trip to LA next month, the assistant should show weathe





Deep Agent Skills: Conversation simulator
                     -- should try to get a goal for the        conversation and a user  (refer to User Simulator to get a user. if not provided)
                     -- get the link to the bot to talk to (using playwright or direct API access?
                     Grab the memberId from the postgres conversation state)
                     -- then act as the user with their simulated 
                        preference and context have a multi turn conversation with a bot

                  Conversation analyzer
                   -- Analyze users intent
                        Query → Information seeking (questions, clarifications, exploring options)
                        Action → Task execution (requests to do something, commands)
                        Preferences → Context sharing (opinions, constraints, feedback, background info)

                    -- Analyze each step to measure
                        Sentiment: Positive, neutral, negative, frustrated.

                        Urgency: High priority vs exploratory.

                        Clarity: Well-defined vs ambiguous/needs clarification.

                        Follow-up type: New topic vs continuation of previous discussion

                        Would like to think this of some deviation from mean (PID style in terms of error correction.)
                    
                

                  User Context / preference simulator:



                  Evidence Builder
                    -- Use the conversation simulator mode to have a conversation .
                    -- Also ask users for evidence resources
                    specially relevant github repos,
                    any links, pdfs, swaggers etc
                    -- Takes each turn to swap off a sub agent that can go and gather evidence to either back the answer with evidence
                    or propose alternate versions with evidence


                  Skill Creator / updator 

Just cli to talk to the agent with these skills

              


