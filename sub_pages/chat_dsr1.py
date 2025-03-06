import logging
import os
import random
import uuid

import sentry_sdk
import streamlit as st

# from wrapper.search import search_web
from wrapper.edge_tts import TextToSpeechConverter
from wrapper.llm import need_web_search, llmdsr1_answer,llmdsv3_answer
from wrapper.supabase import add_chat_data

preset_questions = [
    "如何摆脱长期的焦虑和负面情绪？",
    "如何疗愈童年创伤对现在生活的影响？",
    "为什么总是无法拒绝他人？",
    "如何停止过度思考和自我攻击？",
    "为什么在人际关系中感到孤独或被忽视？",
    "如何调节过度敏感或易怒的情绪反应？",
    "如何摆脱拖延和内耗带来的压力？",
    "为什么总是感到不安全或需要掌控一切？",
    "如何疗愈亲密关系中的依赖和矛盾？",
    "如何找到自己的价值感并建立内在力量？",
]





def get_random_questions():
    return random.sample(preset_questions, 3)


def get_chat_history() -> str:
    # Skip the first welcome message.
    return "\n\n".join(
        [f'{msg["role"]}: {msg["content"]}' for msg in st.session_state.messages[1:]]
    )


# Generate a session ID if it doesn't exist
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())  # Generates a unique ID

if "messages" not in st.session_state:
    preset_questions = get_random_questions()
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": f"""
            嗨，{st.session_state.username},你好，让我们来开启一次疗愈之旅！你有任何问题都可以随时来咨询我~比如：\n
            1. {preset_questions[0]}
            2. {preset_questions[1]}
            3. {preset_questions[2]}
            """,
        }
    ]


def render_ui():
    st.header(":material/school: 我是DeepSeekR1")
    st.caption("""
               有什么需要，放马过来～
               """)

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if question := st.chat_input(placeholder="在这里输入你的问题..."):
        st.chat_message("user").write(question)

        with st.spinner("正在思考中..."):
            search_result = ""
            # if need_web_search(question):
            #     search_result = search_web(question)

            stream_answer = llmdsr1_answer(
                question, get_chat_history(),
                search_result=search_result,
                username=st.session_state.username)

        answer = st.chat_message("assistant").write_stream(stream_answer)

        # if os.getenv("APP_AUDIO_AUTOPLAY_IN_CHAT") == "true":
        #     _, audio_col = st.columns([3, 2])
        #     converter = TextToSpeechConverter()
        #     audio_col.audio(converter.convert(answer), autoplay=True)

        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        add_chat_data(st.session_state.session_id, question,answer, int(st.session_state.uid))


try:
    render_ui()
except Exception as e:
    sentry_sdk.capture_exception(e)
    logging.exception(e)
    st.error("Oops! Something went wrong.")
