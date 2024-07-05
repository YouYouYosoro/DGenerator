import os
import toml
import datetime
from openai import OpenAI
from zhipuai import ZhipuAI
from volcenginesdkarkruntime import Ark
from http import HTTPStatus
from dashscope import Application
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

def load_config():
    global project_dir
    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    global config_dir
    config_dir = project_dir + "/config/"  # 配置文件

    global api_config
    api_config = toml.load(config_dir + "api.toml")  # 加载API配置
    global kimi_key
    kimi_key = api_config["KIMI"]["kimi_key"]
    global kimi_base
    kimi_base = api_config["KIMI"]["kimi_base"]
    global deepseek_key
    deepseek_key = api_config["DEEPSEEK"]["deepseek_key"]
    global deepseek_base
    deepseek_base = api_config["DEEPSEEK"]["deepseek_base"]
    global chatglm_key
    chatglm_key = api_config["CHATGLM"]["chatglm_key"]
    global chatglm_base
    chatglm_base = api_config["CHATGLM"]["chatglm_base"]
    global doubao_access_key
    doubao_access_key = api_config["Doubao-lite-32k"]["doubao_access_key"]
    global doubao_secret_access_key
    doubao_secret_access_key = api_config["Doubao-lite-32k"]["doubao_secret_access_key"]
    global doubao_key
    doubao_key = api_config["Doubao-lite-32k"]["doubao_key"]
    global doubao_endpoint
    doubao_endpoint = api_config["Doubao-lite-32k"]["doubao_endpoint"]
    global qwen_app_id
    qwen_app_id = api_config["Qwen-Turbo"]["qwen_app_id"]
    global qwen_key
    qwen_key = api_config["Qwen-Turbo"]["qwen_key"]
    global xing_huo_key
    xing_huo_key = api_config["XunFei-XingHuo"]["xing_huo_key"]
    global xing_huo_base
    xing_huo_base = api_config["XunFei-XingHuo"]["xing_huo_base"]
    global xing_huo_appid
    xing_huo_appid = api_config["XunFei-XingHuo"]["xing_huo_appid"]
    global xing_huo_secret_key
    xing_huo_secret_key = api_config["XunFei-XingHuo"]["xing_huo_secret_key"]

    global generator_config
    generator_config = toml.load(config_dir + "generator.toml")
    global generator_model
    generator_model = generator_config["GENERATOR"]["generator_model"]
    global main_areas
    main_areas = generator_config["GENERATOR"]["main_areas"]
    global needs
    needs = generator_config["GENERATOR"]["needs"]
    global key_words
    key_words = generator_config["GENERATOR"]["key_words"]
    global character_style
    character_style = generator_config["GENERATOR"]["character_style"]
    global language_style
    language_style = generator_config["GENERATOR"]["language_style"]

    global gender
    gender = generator_config["PERSONALINFO"]["gender"]
    global age
    age = generator_config["PERSONALINFO"]["age"]
    global height
    height = generator_config["PERSONALINFO"]["height"]
    global weight
    weight = generator_config["PERSONALINFO"]["weight"]
    global bmi
    bmi = generator_config["PERSONALINFO"]["bmi"]
    global medical_history_bool
    medical_history_bool = generator_config["PERSONALINFO"]["medical_history_bool"]
    global medical_history
    medical_history = generator_config["PERSONALINFO"]["medical_history"]
    global target
    target = generator_config["PERSONALINFO"]["target"]


def toml_to_str():
    str = f'我的个人信息如下：性别：{gender}，年龄：{age}岁，身高：{height}厘米，体重：{weight}千克，BMI：{bmi}，{medical_history_bool}既往病史，{medical_history if medical_history else ""}，我的健康目标是：{target}'
    return str

def generate_by_models(model, str, food):
    result = None
    print("***正在生成***\n")
    if "moonshot-v1-8k" in model:
        client = OpenAI(api_key=kimi_key, base_url=kimi_base)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"你是一个优秀的专业的营养师与厨师,你擅长根据客户的信息给出合理科学的饮食方案"},
                {"role": "user",
                 "content": f"{str}, 另外我今天想吃的食物是：{food}，请根据我的个人信息与想吃的食物给出科学合理的菜品信息与烹饪方法，然后列出该菜品里面用到的所有食材每100克所含的能量与营养成分，然后描述一下这些食材的药用价值与健康价值" +
                            f"请在描述完健康价值之后立即停止回答"}
            ])
        # 打印 response 的内容，用于调试
        print(response)
        if hasattr(response, 'choices') and response.choices:
            answer = response.choices[0].message.content
        else:
            answer = None
        return answer

    elif "glm-4-flash" in model:
        client = ZhipuAI(api_key=chatglm_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"你是一个优秀的专业的营养师与厨师,你擅长根据客户的信息给出合理科学的饮食方案"},
                {"role": "user",
                 "content": f"{str}, 另外我今天想吃的食物是：{food}，请根据我的个人信息与想吃的食物给出科学合理的菜品信息与烹饪方法，然后列出该菜品里面用到的所有食材每100克所含的能量与营养成分，然后描述一下这些食材的药用价值与健康价值" +
                            f"请在描述完健康价值之后立即停止回答"}
            ])
        # 打印 response 的内容，用于调试
        print(response)
        if hasattr(response, 'choices') and response.choices:
            answer = response.choices[0].message.content
        else:
            answer = None
        return answer

    elif "deepseek-chat" in model:
        client = OpenAI(api_key=deepseek_key, base_url=deepseek_base)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"你是一个优秀的专业的营养师与厨师,你擅长根据客户的信息给出合理科学的饮食方案"},
                {"role": "user",
                 "content": f"{str}, 另外我今天想吃的食物是：{food}，请根据我的个人信息与想吃的食物给出科学合理的菜品信息与烹饪方法，然后列出该菜品里面用到的所有食材每100克所含的能量与营养成分，然后描述一下这些食材的药用价值与健康价值" +
                            f"请在描述完健康价值之后立即停止回答"}
            ])
        # 打印 response 的内容，用于调试
        print(response)
        if hasattr(response, 'choices') and response.choices:
            answer = response.choices[0].message.content
        else:
            answer = None
        return answer

    elif "Doubao-lite-32k" in model:
        client = Ark(ak=doubao_access_key, sk=doubao_secret_access_key, api_key=doubao_key)

        completion = client.chat.completions.create(
            model=f"{doubao_endpoint}",
            messages=[
                {"role": "system", "content": f"你是一个优秀的专业的营养师与厨师,你擅长根据客户的信息给出合理科学的饮食方案"},
                {"role": "user",
                 "content": f"{str}, 另外我今天想吃的食物是：{food}，请根据我的个人信息与想吃的食物给出科学合理的菜品信息与烹饪方法，然后列出该菜品里面用到的所有食材每100克所含的能量与营养成分，然后描述一下这些食材的药用价值与健康价值" +
                            f"请在描述完健康价值之后立即停止回答"}
            ])
        print(completion.choices[0].message.content)
        answer = completion.choices[0].message.content
        return answer

    elif "Qwen-Turbo" in model:
        response = Application.call(app_id=f'{qwen_app_id}',
                                    prompt=f"{str}, 另外我今天想吃的食物是：{food}，请根据我的个人信息与想吃的食物给出科学合理的菜品信息与烹饪方法，然后列出该菜品里面用到的所有食材每100克所含的能量与营养成分，然后描述一下这些食材的药用价值与健康价值" +
                            f"请在描述完健康价值之后立即停止回答",
                                    api_key=f'{qwen_key}',
                                    )

        if response.status_code != HTTPStatus.OK:
            print(
                'request_id=%s, code=%s, message=%s\n' % (response.request_id, response.status_code, response.message))
        else:
            print('request_id=%s\n output=%s\n usage=%s\n' % (response.request_id, response.output, response.usage))
            return response.output.text

    elif "generalv3.5" in model:
        spark = ChatSparkLLM(
            spark_api_url=xing_huo_base,
            spark_app_id=xing_huo_appid,
            spark_api_key=xing_huo_key,
            spark_api_secret=xing_huo_secret_key,
            spark_llm_domain='generalv3.5',
            streaming=False,
        )
        messages = [ChatMessage(
            role="user",
            content=f"{str}, 另外我今天想吃的食物是：{food}，请根据我的个人信息与想吃的食物给出科学合理的菜品信息与烹饪方法，然后列出该菜品里面用到的所有食材每100克所含的能量与营养成分，然后描述一下这些食材的药用价值与健康价值" +
                            f"请在描述完健康价值之后立即停止回答"
        )]
        handler = ChunkPrintHandler()
        a = spark.generate([messages], callbacks=[handler])
        print(a)
        answer = a.generations[0][0].text
        return answer




