from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)


class LLM(object):
    def __init__(self, api_key: str, memory_window=8):
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template("""You are voice assistant Jarvis. \
                    If you don't know the answer, just say that you don't know. \
                    Use three sentences maximum and keep the answer concise"""
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

        memory = ConversationBufferWindowMemory(k=memory_window, memory_key="chat_history", return_messages=True)

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
        
        llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7, model="gpt-3.5-turbo")
        self.conversation = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)
        # self.conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

    def ask(self, prompt):
        return self.conversation(prompt)['text']
