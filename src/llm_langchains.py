import os
import sys
import logging
import httpx

from langchain_openai import OpenAI
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
from langchain_community.tools import YouTubeSearchTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))


def check_package(package_name):
    try:
        __import__(package_name)
        print(f"The package '{package_name}' is installed.")
        return True
    except ImportError:
        print(f"The package '{package_name}' is not installed.")
        return False


class LLM(object):
    def __init__(self, memory_window=8):
        self.memory = ConversationBufferWindowMemory(
            k=memory_window, memory_key="chat_history", return_messages=True
        )

        self.llm = OpenAI(
            openai_api_base=os.environ.get("OPENAI_API_BASE"), 
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            # for some reason openai_proxy didn't work for me, therefore I used http_client https://python.langchain.com/v0.2/docs/integrations/llms/openai/
            http_client=httpx.Client(proxies=os.environ.get("OPENAI_PROXY")),
            temperature=0.7, model=os.environ.get("OPENAI_MODEL", "GPT-4o")
        )

        self.chain = self._init_chain()

    def _init_agent(self):
        # https://python.langchain.com/docs/integrations/tools/openweathermap
        skils = []
        if check_package("pyowm"):
            skils.append("openweathermap-api")
        if check_package("arxiv"):
            skils.append("arxiv")
        if check_package("duckduckgo-search"): # requires curl-impersonate that is not available for armv7
            skils.append("ddg-search")
        if check_package("wikipedia"):
            skils.append("wikipedia")

        tools = load_tools(skils)
        tools.append(YouTubeSearchTool())
       
        agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            memory=self.memory,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
        )
        return agent

    def _init_chain(self):
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    """You are voice assistant Jarvis created by Dennis Vashchuk \
                    If you don't know the answer, just say that you don't know. \
                    Use three sentences maximum and keep the answer concise"""
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt, memory=self.memory, verbose=True)
        return chain

    def ask(self, prompt):      
        response = self.chain.invoke({"input": prompt})
        return response['text'] if 'text' in response else 'output'
  
           