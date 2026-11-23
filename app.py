import streamlit as st
import pandas as pd

# ----------------------------------------
# 1. 데이터 구조 (리스트): 선택 가능한 적금 상품
# ----------------------------------------
products = [
    {"이름": "청춘 시작 적금", "최소금액": 100_000, "금리": 0.030, "만기": 1},
    {"이름": "든든 목돈 적금", "최소금액": 1_000_000, "금리": 0.035, "만기": 2},
    {"이름": "하이 플러스 적금", "최소금액": 5_000_000, "금리": 0.040, "만기": 3},
]


# ----------------------------------------
# 2. 함수 (def): 상품과 자산을 받아 순이익, 미래자산 리턴
# ----------------------------------------
def future_fund(product, fund):
    asset = fund
    # 4. 반복문 (for): 만기(년)만큼 반복하며 이자를 붙임 (연복리)
    for year in range(product["만기"]):
        asset = asset * (1 + product["금리"])
    asset = int(asset)
    profit = asset - fund
    return profit, asset


def to_korean(won):
    """큰 금액을 '1억 2,345만 원' 처럼 읽기 쉽게 바꿔주는 함수"""
    eok = won // 100_000_000
    man = (won % 100_000_000) // 10_000
    rest = won % 10_000
    parts = []
    if eok:
        parts.append(f"{eok:,}억")
    if man:
        parts.append(f"{man:,}만")
    if rest:
        parts.append(f"{rest:,}")
    return " ".join(parts) + " 원"


# ----------------------------------------
# 화면 구성
# ----------------------------------------
st.title("금융 상품 구매 가이드 📖")

# (1) 상품 선택
names = [p["이름"] for p in products]
selected_name = st.selectbox("(1) 상품 선택", names)
selected = products[names.index(selected_name)]
st.caption(
    f"최소 가입금액 {selected['최소금액']:,}원 · "
    f"연 {selected['금리'] * 100:.1f}% · 만기 {selected['만기']}년"
)

# (2) 현재 자산 입력 (슬라이더)
fund = st.slider(
    "(2) 현재 자산 (원)",
    min_value=1,
    max_value=100_000_000,
    value=1_000_000,
    step=1,
    format="%d",
)
# 슬라이더 바로 아래에 한글 단위로 크게 보여주기
st.markdown(f"### 💰 {to_korean(fund)}")

# 버튼: 분석하기
if st.button("분석하기"):
    # 3. 조건문 (if-elif-else)
    if fund < selected["최소금액"]:
        st.error(
            f"이 상품은 구매 불가합니다. 자금 부족 "
            f"(최소 가입금액 {selected['최소금액']:,}원)"
        )
    else:
        profit, asset = future_fund(selected, fund)

        # 결과 텍스트 메시지
        st.success(
            f"'{selected['이름']}'을(를) 현재 자산으로 구매하면 "
            f"{selected['만기']}년 후 만기일에 {asset:,}원({to_korean(asset)})을 가지게 됩니다."
        )

        # 종합 분석 (테이블)
        st.subheader("종합 분석")
        df = pd.DataFrame(
            {"순이익": [to_korean(profit)], "미래자산": [to_korean(asset)]},
            index=[selected["이름"]],
        )
        st.table(df)
