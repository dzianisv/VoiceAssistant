from langchain_community.chat_models import ChatOpenAI

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

class LLM(object):
    def __init__(self, api_key: str, memory_window=8):
        memory = ConversationBufferWindowMemory(k=memory_window)               
        llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7, model="gpt-3.5-turbo")
        self.conversation = ConversationChain(
            llm=llm, 
            memory = memory,
            verbose=False
        )

    def ask(self, prompt):
        return self.conversation.predict(input=prompt)
