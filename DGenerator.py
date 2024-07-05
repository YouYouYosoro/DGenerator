import streamlit as st
import streamlit_antd_components as sac

from project.TxtGenerator import txt_generator
from project.PromptManager import prompt_manager
from project.OutputManager import output_manager
from project.PersonalInformation import personal_info
from project.ApiManeger import api_maneger

st.set_page_config(
    page_title="菜品推荐",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar.container():
    menu = sac.menu(
        items=[
            sac.MenuItem('生成器', icon='book'),
            sac.MenuItem('提示词管理', icon='file-earmark-break'),
            sac.MenuItem('输出管理', icon='file'),
        ],
        key='menu',
        open_index=[1]
    )

with st.container():
    if menu == '生成器':
        txt_generator()
    elif menu == '提示词管理':
        prompt_manager()
    elif menu == '输出管理':
        output_manager()
