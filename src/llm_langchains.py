import os
import sys
import logging

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
    def __init__(self, api_key: str, memory_window=8):
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    """You are voice assistant Jarvis created by Dennis Vashchuk \
                    If you don't know the answer, just say that you don't know. \
                    Use three sentences maximum and keep the answer concise"""
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

        memory = ConversationBufferWindowMemory(
            k=memory_window, memory_key="chat_history", return_messages=True
        )

        # set a proxy
        http_proxy, https_proxy = os.environ.get('HTTP_PROXY', ''), os.environ.get('HTTPS_PROXY', '')
        os.environ['HTTP_PROXY'], os.environ['HTTPS_PROXY'] = os.environ.get('OPENAI_HTTP_PROXY', ''), os.environ.get('OPENAI_HTTP_PROXY', '')
        
        llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7, model="gpt-3.5-turbo")
        # reset a proxy config
        os.environ['HTTP_PROXY'], os.environ['HTTPS_PROXY'] = http_proxy, https_proxy
         
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
        tools += [YouTubeSearchTool()]

        # chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)
        self.agent = initialize_agent(
            tools,
            llm=llm,
            memory=memory,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
        )

    def ask(self, prompt):      
        return self.agent.invoke({"input": prompt})["output"]
  
           