import logging
import os
import time

import sentry_sdk
import streamlit as st
from dotenv import load_dotenv

import wrapper.supabase as sb


# from wrapper.supabase import find_students, get_student_by_id

load_dotenv()


# Global setup for logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s',
    level=logging.INFO)

# Initialize Sentry
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    environment=os.getenv("SENTRY_ENV"),
)

# 初始化会话状态
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# 默认用户
# USERNAME = "admin"
# PASSWORD = "admin"
# users=[
#     {'admin':'admin'},
#     {'elise':'elise'},
#     {'123':'123'}
# ]

# if "student" not in st.session_state:
#     st.session_state.student = get_student_by_id(0)



# @st.dialog("学生列表", width="small")
# def switch_student_dialog():
#     with st.spinner("正在加载学生列表..."):
#         students = find_students()
#         options = [student['id'] for student in students]

#         def format_func(student_id):
#             student = get_student_by_id(student_id)
#             return f"{student['id']} {student['name']}({student['grade']})"

#         switch_to = st.radio(
#             "选择你的账号", options, format_func=format_func, horizontal=True,
#             index=options.index(st.session_state.student['id']),
#         )

#         if st.button("保存", type="primary", use_container_width=True):
#             if switch_to != st.session_state.student['id']:
#                 st.session_state.student = get_student_by_id(switch_to)
#                 if "messages" in st.session_state:
#                     del st.session_state.messages

#             st.rerun()

# 登录页面
def login():
    st.header("登录")
    st.divider()

    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")

    # 登录验证
    if st.button("登录"):
        
        exist_user = sb.find_user_by_username(username)
        
        if len(exist_user)>0:
            exist_user=exist_user[0]
            if password == exist_user['password']:
                st.session_state.logged_in = True

                if "username" not in st.session_state:
                    st.session_state.username = username
                if "uid" not in st.session_state:
                    st.session_state.uid = exist_user['uid']

                st.success("登录成功!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("密码错误")
        else:
            st.error("用户名或密码错误")



login_page = st.Page(login, title="登录")





# logout_page = st.Page(logout, title="退出登录")

# if st.session_state.logged_in:
#     pg = st.navigation(
#         {
#             "主要功能": [page1, page2],
#             "账户管理": [logout_page],
#         }
#     )

# pg.run()



def render_ui():
    # st.sidebar.markdown(f"姓名: {st.session_state.student['name']}")
    # st.sidebar.markdown(f"年级: {st.session_state.student['grade']}")
    # st.sidebar.markdown(f"学校: {st.session_state.student['campus']}")

    # if st.sidebar.button(":material/change_circle: 切换身份"):
    #     switch_student_dialog()

    if st.session_state.logged_in:
        if st.session_state.username=='kuma':
            page = st.navigation(
                [
                    st.Page("sub_pages/chat.py", title="元气疗愈师",default=True, 
                        icon=":material/school:"),
                    st.Page("sub_pages/logout.py", title="退出登录",
                        icon=":material/headphones:"),
                    st.Page("sub_pages/rag.py", title="RAG管理",
                        icon=":material/headphones:"),
                    st.Page("sub_pages/chat_dsr1.py", title="dsChatR1",
                        icon=":material/headphones:"),
                    st.Page("sub_pages/chat_dsv3.py", title="dsChatV3",
                        icon=":material/headphones:"),
                ]
            )
        else:
            page = st.navigation(
                [
                    st.Page("sub_pages/chat.py", title="元气疗愈师",default=True, 
                        icon=":material/school:"),
                    st.Page("sub_pages/logout.py", title="退出登录",
                        icon=":material/headphones:"),
                ]
            )
    else:
        # 默认只有login页面
        page = st.navigation([login_page])

    page.run()


try:
    render_ui()
except Exception as e:
    sentry_sdk.capture_exception(e)
    logging.exception(e)
    st.error("Oops! Something went wrong.")
