from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

class LLM(object):
    def __init__(self, openai_api_key: str, memory_window=8):
        llm_model = "gpt-3.5-turbo"
        self.memory = ConversationBufferWindowMemory(k=memory_window)               
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7, model=llm_model)
        self.conversation = ConversationChain(
            llm=self.llm, 
            memory = self.memory,
            verbose=False
        )

    def ask(self, prompt):
        return conversation.predict(input=prompt)
