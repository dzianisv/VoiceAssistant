from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory


class LLM(object):
    def __init__(self, api_key: str, memory_window=8):
        memory = ConversationBufferWindowMemory(k=memory_window)

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                            },
                        },
                        "required": ["location"],
                    },
                },
            }
        ]
        
        llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7, model="gpt-3.5-turbo").bind(tools=tools)
        self.conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

    def ask(self, prompt):
        return self.conversation.predict(input=prompt)
