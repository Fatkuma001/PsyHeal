import logging
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

from .prompt_yq import SYSTEM_PROMPT_CLASSIFY, USER_PROMPT_CLASSIFY, SYSTEM_PROMPT_ANSWER, USER_PROMPT_ANSWER


def need_web_search(question: str) -> bool:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_CLASSIFY),
            ("user", USER_PROMPT_CLASSIFY),
        ]
    )

    model = get_llm_model()
    parser = StrOutputParser()

    chain = prompt_template | model | parser
    return chain.invoke({"question": question}) == "yes"


def llm_answer(question: str, chat_history: str,
               search_result: str = "",
               username: str = "Unknown") -> str:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_ANSWER),
            ("user", USER_PROMPT_ANSWER),
        ]
    )

    model = get_llm_model()
    parser = StrOutputParser()

    chain = prompt_template | model | parser
    return chain.stream(
        {
            "question": question,
            "chat_history": chat_history,
            "search_result": search_result,
            "username": username,
        }
    )

def llmdsr1_answer(question: str, chat_history: str,
               search_result: str = "",
               username: str = "Unknown") -> str:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_ANSWER),
            ("user", USER_PROMPT_ANSWER),
        ]
    )

    model = get_deepseekr1_model()
    parser = StrOutputParser()

    chain = prompt_template | model | parser
    return chain.stream(
        {
            "question": question,
            "chat_history": chat_history,
            "search_result": search_result,
            "username": username,
        }
    )

def llmdsv3_answer(question: str, chat_history: str,
               search_result: str = "",
               username: str = "Unknown") -> str:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_ANSWER),
            ("user", USER_PROMPT_ANSWER),
        ]
    )

    model = get_deepseekv3_model()
    parser = StrOutputParser()

    chain = prompt_template | model | parser
    return chain.stream(
        {
            "question": question,
            "chat_history": chat_history,
            "search_result": search_result,
            "username": username,
        }
    )

def get_llm_model():
    groq_llm = get_groq_model()
    deepseekv3_llm = get_deepseekv3_model()

    return groq_llm.with_fallbacks([deepseekv3_llm])


def get_groq_model() -> ChatGroq:
    return ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0.3, 
        max_tokens=1024,
        api_key=os.getenv("GROQ_KEY")
    )


def get_deepseekv3_model() -> ChatDeepSeek:
    return ChatDeepSeek(
        model="deepseek-chat",
        temperature=1.5,
        max_tokens=1024,
        api_key=os.getenv("DEEPSEEK_KEY")
    )

def get_deepseekr1_model() -> ChatDeepSeek:
    return ChatDeepSeek(
        model="deepseek-reasoner",
        temperature=1.5,
        max_tokens=1024,
        api_key=os.getenv("DEEPSEEK_KEY")
    )


# def get_openai_model() -> ChatOpenAI:
#     return ChatOpenAI(model="gpt-4o", temperature=0.3, max_tokens=512)
