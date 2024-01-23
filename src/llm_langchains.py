from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

class LLM(object):
    def __init__(self, api_key: str, memory_window=8):
        llm_model = "gpt-3.5-turbo"
        self.memory = ConversationBufferWindowMemory(k=memory_window)               
        self.llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7, model=llm_model)
        self.conversation = ConversationChain(
            llm=self.llm, 
            memory = self.memory,
            verbose=False
        )

    def ask(self, prompt):
        return self.conversation.predict(input=prompt)
