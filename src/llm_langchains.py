from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain, LLMChain

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper
from langchain.agents import initialize_agent, AgentType, load_tools

class LLM(object):
    def __init__(self, api_key: str, memory_window=8):
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template("""You are voice assistant Jarvis created by Dennis Vashchuk \
                    If you don't know the answer, just say that you don't know. \
                    Use three sentences maximum and keep the answer concise"""
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

        memory = ConversationBufferWindowMemory(k=memory_window, memory_key="chat_history", return_messages=True)

        llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7, model="gpt-3.5-turbo")
        
        # https://python.langchain.com/docs/integrations/tools/openweathermap
        tools = load_tools(["openweathermap-api"], llm)
        
        # chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)
        self.agent = initialize_agent(tools, llm=llm, memory=memory, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True)
    
    def ask(self, prompt):
        return self.agent.invoke({'input': prompt})['output']
