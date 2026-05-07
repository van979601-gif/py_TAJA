import streamlit as st
import random
import time

st.set_page_config(
    page_title="Python 타자 연습",
    page_icon="🐍",
    layout="wide"
)

# -----------------------------
# 난이도별 Python 연습 코드
# -----------------------------

BEGINNER = [
    "print('Hello World')",

    """name = input("이름 입력: ")
print(name)""",

    """for i in range(5):
    print(i)""",

    """x = 10
y = 20
print(x + y)""",

    """numbers = [1, 2, 3]
for n in numbers:
    print(n)"""
]

INTERMEDIATE = [
    """def add(a, b):
    return a + b

print(add(3, 5))""",

    """students = {
    "kim": 90,
    "lee": 80
}

for name, score in students.items():
    print(name, score)""",

    """nums = [1, 2, 3, 4]

squared = [n**2 for n in nums]

print(squared)""",

    """try:
    x = int(input())
    print(x)
except ValueError:
    print("숫자를 입력하세요")"""
]

ADVANCED = [
    """class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello {self.name}"

p = Person("Tom")
print(p.greet())""",

    """def fibonacci(n):
    if n <= 1:
        return n

    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(6))""",

    """with open("sample.txt", "w") as f:
    f.write("hello")

with open("sample.txt", "r") as f:
    print(f.read())""",

    """data = list(map(lambda x: x * 2, [1, 2, 3, 4]))

print(data)"""
]

LEVELS = {
    "초급": BEGINNER,
    "중급": INTERMEDIATE,
    "고급": ADVANCED
}

# -----------------------------
# 세션 상태
# -----------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

if "finished" not in st.session_state:
    st.session_state.finished = False

if "target_code" not in st.session_state:
    st.session_state.target_code = ""

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "초급"

# -----------------------------
# 제목
# -----------------------------

st.title("🐍 Python 코드 타자 연습")

st.write("Python 코드를 그대로 입력하세요.")
st.write("자동 들여쓰기 지원 코드 입력창 제공")

# -----------------------------
# 난이도 선택
# -----------------------------

difficulty = st.selectbox(
    "난이도 선택",
    ["초급", "중급", "고급"]
)

# -----------------------------
# 새 문제 생성
# -----------------------------

if st.button("새 문제 시작"):

    st.session_state.difficulty = difficulty

    st.session_state.target_code = random.choice(
        LEVELS[difficulty]
    )

    st.session_state.started = False
    st.session_state.finished = False
    st.session_state.start_time = 0

# -----------------------------
# 목표 코드 출력
# -----------------------------

if st.session_state.target_code:

    st.subheader("📝 제시 코드")

    st.code(
        st.session_state.target_code,
        language="python"
    )

    st.subheader("⌨️ 입력")

    # 코드 입력창
    user_input = st.text_area(
        "Python 코드를 입력하세요",
        height=300,
        placeholder="여기에 Python 코드를 입력하세요..."
    )

    # 시작 시간 기록
    if user_input and not st.session_state.started:
        st.session_state.started = True
        st.session_state.start_time = time.time()

    # 정답 체크
    if (
        user_input.strip()
        == st.session_state.target_code.strip()
        and not st.session_state.finished
    ):

        st.session_state.finished = True

        end_time = time.time()

        elapsed = end_time - st.session_state.start_time

        chars = len(st.session_state.target_code)

        cpm = (chars / elapsed) * 60

        accuracy = 100

        st.success("정답입니다! 🎉")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "⏱️ 시간",
                f"{elapsed:.2f}초"
            )

        with col2:
            st.metric(
                "⚡ CPM",
                f"{cpm:.1f}"
            )

        with col3:
            st.metric(
                "🎯 정확도",
                f"{accuracy}%"
            )

# -----------------------------
# 오타 비교 기능
# -----------------------------

if (
    st.session_state.target_code
    and user_input
    and not st.session_state.finished
):

    target = st.session_state.target_code

    correct = 0

    for a, b in zip(user_input, target):
        if a == b:
            correct += 1

    accuracy = (correct / len(target)) * 100

    st.progress(min(int(accuracy), 100))

    st.info(f"현재 정확도: {accuracy:.1f}%")
