import os
import toml

import streamlit as st
import streamlit_antd_components as sac
from . import utils
def txt_generator():

    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    config_dir = project_dir + "/config/"  # 配置文件
    generator_config = toml.load(config_dir + "generator.toml")

    st.title("菜品推荐")
    sac.divider(label='POWERD BY FSQL', icon="lightning-charge", align='center', color='gray', key="1")
    sac.alert(
        label='| **请注意：测试版仅供内部测试用，并未制作缓存系统，切换页面会重置页面** || 如有正式需求请联系开发人员 |',
        banner=True, size='lg', radius=20, icon=True, closable=True, color='info')


    name = sac.segmented(
        items=[
            sac.SegmentedItem(label="预置信息", icon="gear-wide-connected"),
            sac.SegmentedItem(label="文案生成", icon="file-earmark-check-fill"),
        ], align='center', size='sm', radius=20, color='red', divider=False, use_container_width=True
    )

    if name == '预置信息':
        col1, col2 = st.columns([0.6, 0.4], gap="medium")
        with col1:
            with st.expander("**个人数据**", expanded=True):
                gender = st.radio(
                    "你的性别是：",
                    ['男', '女',],
                    horizontal=True,
                )
                age = st.slider("输入你的年龄", 0, 150, 20)
                height = st.slider("输入你的身高(cm)", 50.0, 250.0, 170.0, step=0.5)
                weight = st.slider("输入你的体重(kg)", 15.0, 200.0, 60.0, step=0.1)
                bmi = round((weight/(height/100)**2), 2)
                st.write(f"**你的BMI值为：{bmi}**")
                if bmi < 18.5:
                    sac.alert(
                        '偏瘦', description='你的BMI低于正常范围',
                        size='md', icon=True, closable=False, color='info'
                    )
                elif bmi >= 18.5 and bmi <= 23.9:
                    sac.alert(
                        '正常', description='你的BMI处于正常范围',
                        size='md', icon=True, closable=False, color='success'
                    )
                elif bmi >23.9:
                    sac.alert(
                        '偏胖', description='你的BMI高于正常范围',
                        size='md', icon=True, closable=False, color='info'
                    )

                medical_history_bool = st.radio(
                    "有无既往病史",
                    ['无', '有',],
                    horizontal=True,
                )
                if medical_history_bool == '无':
                    generator_config["PERSONALINFO"]["medical_history_bool"] = medical_history_bool
                else:
                    medical_history = st.text_area("输入你的既往病史", placeholder="描述一下你的既往病史，如果可以，请尽量详细")
                    generator_config["PERSONALINFO"]["medical_history_bool"] = medical_history_bool
                    generator_config["PERSONALINFO"]["medical_history"] = medical_history

                target = st.text_input("描述一下你的健康目标", placeholder="减肥、减脂、血糖控制等等")

                generator_config["PERSONALINFO"]["target"] = target
                generator_config["PERSONALINFO"]["gender"] = gender
                generator_config["PERSONALINFO"]["age"] = age
                generator_config["PERSONALINFO"]["height"] = height
                generator_config["PERSONALINFO"]["weight"] = weight
                generator_config["PERSONALINFO"]["bmi"] = bmi

            with st.expander("**选择模型**", expanded=True):
                generator_model = sac.chip(
                    items=[
                        sac.ChipItem(label='moonshot-v1-8k'),
                        sac.ChipItem(label='glm-4-flash'),
                        sac.ChipItem(label='deepseek-chat'),
                        sac.ChipItem(label='Doubao-lite-32k'),
                        sac.ChipItem(label='Qwen-Turbo'),
                        sac.ChipItem(label='generalv3.5'),
                    ], format_func='title', direction='vertical', radius='sm',
                    multiple=True, return_index=False
                )
                if generator_model:
                    generator_config["PERSONALINFO"]["generator_model"] = generator_model
                else: sac.alert(
                    label='**请选择模型**',
                    description='**选择模型不能为空**',
                    size='lg', radius=20, icon=True, closable=True, color='error')

        with col2:
            if st.button("保存所有参数", type="primary", use_container_width=True):
                with open(config_dir + '/generator.toml', 'w', encoding='utf-8') as file:
                    toml.dump(generator_config, file)
                    print(file)
                sac.alert(
                    label='**参数设置已保存**',
                    description='**未选择的部分将使用上一次的配置**',
                    size='lg', radius=20, icon=True, closable=True, color='success')

    if name == '文案生成':
        food = st.text_input('尊敬的客人您今天想吃些什么：', placeholder='如：生菜、牛肉等等')
        if st.button("给出建议", type="primary", use_container_width=True):

            print("开始生成")
            selected_models = generator_config["PERSONALINFO"]["generator_model"]
            tabs = st.tabs(selected_models)
            utils.load_config()
            str = utils.toml_to_str()

            for i, model in enumerate(selected_models):
                with tabs[i]:
                    result = utils.generate_by_models(model, str, food)
                    st.text_area("建议如下", value=result, height=500)



