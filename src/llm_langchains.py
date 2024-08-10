import os
import sys
import logging

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
        memory = ConversationBufferWindowMemory(
            k=memory_window, memory_key="chat_history", return_messages=True
        )

        llm = OpenAI(openai_api_base=os.environ.get("OPENAI_API_BASE"), openai_api_key=os.environ.get("OPENAI_API_KEY"), temperature=0.7, model="gpt-4o")

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

        # chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)
        self.agent = initialize_agent(
            tools=tools,
            llm=llm,
            memory=memory,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
        )

    def ask(self, prompt):      
        return self.agent.invoke({"input": prompt})["output"]
  
           