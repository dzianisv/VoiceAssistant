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

        # weather_tool = Tool(
        #     name="weather", 
        #     func=OpenWeatherMapAPIWrapper(os.getenv("OPENWEATHERMAP_API_KEY")), 
        #     description="Get weather data"
        # )

        llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7, model="gpt-3.5-turbo")
        # agent = Agent(tools=[weather_tool], llm=llm, prompt=prompt, verbose=True, memory=memory)
        self.conversation = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)

    def ask(self, prompt):
        return self.conversation({'question': prompt})['text']
