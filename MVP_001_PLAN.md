I think we need to work on the basic multiturn deepagent.
Make it a bit more robust before we continue on the Explorer agent.

PLAN:
 first :
 
Fix existing tech debt.

The model and provider should be configurable.
Look at https://github.com/HKUDS/nanobot for inspiration .
still use Langchain to connect to the provider , but I like to config json 
architecture that can be read and used to connect.

Most LLM providers support either OpenAI compatible or Anthropic compatible responses, including the ones served locally .
so implementing those two should be enough.


 Second:
Persistant storage.
Currently the conversations are store in-memory.
Write output to file .
Research using this link on how to implement
https://docs.langchain.com/oss/python/deepagents/backends
I think we need to use the FileSytemBackend for this.

