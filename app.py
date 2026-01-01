from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 환경 변수에서 API 키 불러오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("API Key:", OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

# 1. 홈 화면
@app.route("/")
def home():
    return render_template("home.html")

# 2. 고해 입력 폼
@app.route("/confess", methods=["GET", "POST"])
def confess():
    if request.method == "POST":
        user_input = request.form["confession"]
        response = ask_buddha(user_input)
        return render_template("response.html", response=response)
    return render_template("confess.html")

# 3. GPT 응답 함수
def ask_buddha(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "당신은 자비로운 부처님의 모습으로, 사람들의 괴로움을 들어주고 조용히 위로합니다. "
                        "말투는 짧고 고요하며, 강요하지 않습니다. 어조는 존중과 자비를 담아, '그대', '당신'을 주어로 사용합니다. "
                        "가능한 한 짧은 문장으로 고통을 인정하고, 마음을 놓게 하며, 스스로를 탓하지 않도록 합니다. "
                        "예시 표현:\n"
                        "- '지금 이 괴로움도 지나갈 것입니다.'\n"
                        "- '스스로를 탓하지 마십시오.'\n"
                        "- '그대는 이미 충분히 애썼습니다.'\n"
                        "- '숨을 고르고, 마음을 들여다보십시오.'"
                    )
                },
                {"role": "user", "content": f"사용자의 고해성사: {user_input}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"에러 발생: {str(e)}"

# 4. 앱 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)