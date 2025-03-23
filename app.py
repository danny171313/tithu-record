import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="티츄 점수 계산기", layout="wide")
st.title("🎴 티츄 점수 계산기 (웹버전)")

RECORD_FILE = "player_stats.csv"

# 기록 불러오기 함수
def load_saved_names():
    if not os.path.exists(RECORD_FILE):
        return []
    df = pd.read_csv(RECORD_FILE)
    return sorted(df["이름"].unique())

# 세션 초기화
def init_state():
    if "page" not in st.session_state:
        st.session_state.page = "setup"
    if "round" not in st.session_state:
        st.session_state.round = 1
        st.session_state.scores = []
        st.session_state.total = {"A": 0, "B": 0}
        st.session_state.history = []
        st.session_state.names = load_saved_names()

init_state()

# 점수 계산
def calculate():
    a_score = st.session_state.get("a_score")
    b_score = st.session_state.get("b_score")
    a_tichu = st.session_state.get("a_tichu")
    b_tichu = st.session_state.get("b_tichu")
    a_success = st.session_state.get("a_success")
    b_success = st.session_state.get("b_success")
    double_winner = st.session_state.get("double")

    scores = {"A": 0, "B": 0}

    for team, tichu, success in [("A", a_tichu, a_success), ("B", b_tichu, b_success)]:
        if tichu == "티츄":
            scores[team] += 100 if success else -100
        elif tichu == "라지 티츄":
            scores[team] += 200 if success else -200

    if double_winner == "A":
        scores["A"] += 200
        scores["B"] += 0
    elif double_winner == "B":
        scores["B"] += 200
        scores["A"] += 0
    else:
        if a_score != "" and b_score == "":
            a = int(a_score)
            b = 100 - a
        elif b_score != "" and a_score == "":
            b = int(b_score)
            a = 100 - b
        else:
            a = int(a_score)
            b = int(b_score)
        scores["A"] += a
        scores["B"] += b

    st.session_state.total["A"] += scores["A"]
    st.session_state.total["B"] += scores["B"]
    st.session_state.history.append(scores)
    st.session_state.round += 1

# 기록 저장
def save_records(winner_team, names):
    record = {}
    if os.path.exists(RECORD_FILE):
        df = pd.read_csv(RECORD_FILE)
        for _, row in df.iterrows():
            record[row["이름"]] = [int(row["승"]), int(row["패"])]

    for name, team in names:
        if name == "":
            continue
        if name not in record:
            record[name] = [0, 0]
        if team == winner_team:
            record[name][0] += 1
        else:
            record[name][1] += 1

    df = pd.DataFrame([[n, w, l] for n, (w, l) in record.items()], columns=["이름", "승", "패"])
    df.to_csv(RECORD_FILE, index=False)
    st.success("기록이 저장되었습니다!")

# 기록 보기
def record_page():
    st.header("📖 플레이어 기록")
    if not os.path.exists(RECORD_FILE):
        st.info("아직 저장된 기록이 없습니다.")
        return
    df = pd.read_csv(RECORD_FILE)
    df["승률"] = df.apply(lambda row: f"{(row['승']/(row['승']+row['패'])*100):.1f}%" if row['승']+row['패'] > 0 else "0.0%", axis=1)
    st.dataframe(df.sort_values(by="승", ascending=False), use_container_width=True)

    # 기록 삭제 기능
    name_to_delete = st.selectbox("삭제할 플레이어 선택", options=df["이름"].tolist(), key="delete_name")
    if st.button("선택한 플레이어 기록 삭제"):
        df = df[df["이름"] != name_to_delete]
        df.to_csv(RECORD_FILE, index=False)
        st.success(f"'{name_to_delete}'의 기록이 삭제되었습니다.")
        st.rerun()
    if st.button("전체 기록 초기화"):
    st.header("📖 플레이어 기록")
    if not os.path.exists(RECORD_FILE):
        st.info("아직 저장된 기록이 없습니다.")
        return
    df = pd.read_csv(RECORD_FILE)
    df["승률"] = df.apply(lambda row: f"{(row['승']/(row['승']+row['패'])*100):.1f}%" if row['승']+row['패'] > 0 else "0.0%", axis=1)
    st.dataframe(df.sort_values(by="승", ascending=False), use_container_width=True)

    # 기록 삭제 기능
    name_to_delete = st.selectbox("삭제할 플레이어 선택", options=df["이름"].tolist(), key="delete_name")
    if st.button("선택한 플레이어 기록 삭제"):
        df = df[df["이름"] != name_to_delete]
        df.to_csv(RECORD_FILE, index=False)
        st.success(f"'{name_to_delete}'의 기록이 삭제되었습니다.")
        st.rerun()
        if os.path.exists(RECORD_FILE):
    st.header("📖 플레이어 기록")
    if not os.path.exists(RECORD_FILE):
        st.info("아직 저장된 기록이 없습니다.")
        return
    df = pd.read_csv(RECORD_FILE)
    df["승률"] = df.apply(lambda row: f"{(row['승']/(row['승']+row['패'])*100):.1f}%" if row['승']+row['패'] > 0 else "0.0%", axis=1)
    st.dataframe(df.sort_values(by="승", ascending=False), use_container_width=True)

    # 기록 삭제 기능
    name_to_delete = st.selectbox("삭제할 플레이어 선택", options=df["이름"].tolist(), key="delete_name")
    if st.button("선택한 플레이어 기록 삭제"):
        df = df[df["이름"] != name_to_delete]
        df.to_csv(RECORD_FILE, index=False)
        st.success(f"'{name_to_delete}'의 기록이 삭제되었습니다.")
        st.rerun()
            os.remove(RECORD_FILE)
    st.header("📖 플레이어 기록")
    if not os.path.exists(RECORD_FILE):
        st.info("아직 저장된 기록이 없습니다.")
        return
    df = pd.read_csv(RECORD_FILE)
    df["승률"] = df.apply(lambda row: f"{(row['승']/(row['승']+row['패'])*100):.1f}%" if row['승']+row['패'] > 0 else "0.0%", axis=1)
    st.dataframe(df.sort_values(by="승", ascending=False), use_container_width=True)

    # 기록 삭제 기능
    name_to_delete = st.selectbox("삭제할 플레이어 선택", options=df["이름"].tolist(), key="delete_name")
    if st.button("선택한 플레이어 기록 삭제"):
        df = df[df["이름"] != name_to_delete]
        df.to_csv(RECORD_FILE, index=False)
        st.success(f"'{name_to_delete}'의 기록이 삭제되었습니다.")
        st.rerun()
            st.success("모든 기록이 초기화되었습니다.")
    st.header("📖 플레이어 기록")
    if not os.path.exists(RECORD_FILE):
        st.info("아직 저장된 기록이 없습니다.")
        return
    df = pd.read_csv(RECORD_FILE)
    df["승률"] = df.apply(lambda row: f"{(row['승']/(row['승']+row['패'])*100):.1f}%" if row['승']+row['패'] > 0 else "0.0%", axis=1)
    st.dataframe(df.sort_values(by="승", ascending=False), use_container_width=True)

    # 기록 삭제 기능
    name_to_delete = st.selectbox("삭제할 플레이어 선택", options=df["이름"].tolist(), key="delete_name")
    if st.button("선택한 플레이어 기록 삭제"):
        df = df[df["이름"] != name_to_delete]
        df.to_csv(RECORD_FILE, index=False)
        st.success(f"'{name_to_delete}'의 기록이 삭제되었습니다.")
        st.rerun()
            st.rerun()
    st.header("📖 플레이어 기록")
    if not os.path.exists(RECORD_FILE):
        st.info("아직 저장된 기록이 없습니다.")
        return
    df = pd.read_csv(RECORD_FILE)
    df["승률"] = df.apply(lambda row: f"{(row['승']/(row['승']+row['패'])*100):.1f}%" if row['승']+row['패'] > 0 else "0.0%", axis=1)
    st.dataframe(df.sort_values(by="승", ascending=False), use_container_width=True)

    # 기록 삭제 기능
    name_to_delete = st.selectbox("삭제할 플레이어 선택", options=df["이름"].tolist(), key="delete_name")
    if st.button("선택한 플레이어 기록 삭제"):
        df = df[df["이름"] != name_to_delete]
        df.to_csv(RECORD_FILE, index=False)
        st.success(f"'{name_to_delete}'의 기록이 삭제되었습니다.")
        st.rerun()
    
    st.header("📖 플레이어 기록")
    if not os.path.exists(RECORD_FILE):
        st.info("아직 저장된 기록이 없습니다.")
        return
    df = pd.read_csv(RECORD_FILE)
    df["승률"] = df.apply(lambda row: f"{(row['승']/(row['승']+row['패'])*100):.1f}%" if row['승']+row['패'] > 0 else "0.0%", axis=1)
    st.dataframe(df.sort_values(by="승", ascending=False), use_container_width=True)

    # 기록 삭제 기능
    name_to_delete = st.selectbox("삭제할 플레이어 선택", options=df["이름"].tolist(), key="delete_name")
    if st.button("선택한 플레이어 기록 삭제"):
        df = df[df["이름"] != name_to_delete]
        df.to_csv(RECORD_FILE, index=False)
        st.success(f"'{name_to_delete}'의 기록이 삭제되었습니다.")
        st.rerun()
    if st.button("← 돌아가기"):
        st.session_state.page = "main"
        st.rerun()

# 이름 입력 페이지
if st.session_state.page == "setup":
    st.header("👥 플레이어 이름 설정")
    name_options = st.session_state.names + ["직접 입력"]

    a1_select = st.selectbox("A팀 플레이어 1", options=name_options, key="a1_select")
    a1 = st.text_input("직접 입력 - A팀 1", key="a1_manual") if a1_select == "직접 입력" else a1_select
    a2_select = st.selectbox("A팀 플레이어 2", options=name_options, key="a2_select")
    a2 = st.text_input("직접 입력 - A팀 2", key="a2_manual") if a2_select == "직접 입력" else a2_select

    b1_select = st.selectbox("B팀 플레이어 1", options=name_options, key="b1_select")
    b1 = st.text_input("직접 입력 - B팀 1", key="b1_manual") if b1_select == "직접 입력" else b1_select
    b2_select = st.selectbox("B팀 플레이어 2", options=name_options, key="b2_select")
    b2 = st.text_input("직접 입력 - B팀 2", key="b2_manual") if b2_select == "직접 입력" else b2_select

    if st.button("게임 시작"):
        st.session_state.a1 = a1
        st.session_state.a2 = a2
        st.session_state.b1 = b1
        st.session_state.b2 = b2
        st.session_state.page = "main"
        st.rerun()

# 메인 점수 계산 페이지
elif st.session_state.page == "main":
    colA, colB = st.columns([0.5, 0.5])
    with colA:
        st.subheader(f"🟥 A팀 {st.session_state.total['A']}점")
        a_tichu = st.radio("티츄 선언", ["없음", "티츄", "라지 티츄"], key="a_tichu")
        st.checkbox("성공 여부", key="a_success", value=False)
        st.text_input("점수", key="a_score")
    with colB:
        st.subheader(f"🟦 B팀 {st.session_state.total['B']}점")
        b_tichu = st.radio("티츄 선언", ["없음", "티츄", "라지 티츄"], key="b_tichu")
        st.checkbox("성공 여부", key="b_success", value=False)
        st.text_input("점수", key="b_score")

    st.radio("더블 승리 팀", ["없음", "A", "B"], index=0, key="double", horizontal=True)

    if st.button("점수 계산"):
    calculate()
    if st.session_state.total["A"] >= 1000 or st.session_state.total["B"] >= 1000:
        winner = "A팀" if st.session_state.total["A"] >= 1000 else "B팀"
        st.success(f"🎉 축하합니다! {winner}이 승리했습니다!")
        save_choice = st.radio("기록을 저장하시겠습니까?", ["예", "아니오"], key="save_option")

        if save_choice == "예":
            save_records(winner, [
                (st.session_state.a1, "A팀"),
                (st.session_state.a2, "A팀"),
                (st.session_state.b1, "B팀"),
                (st.session_state.b2, "B팀"),
            ])
            st.success("처음 화면으로 돌아갑니다.")
            st.session_state.page = "setup"
            st.rerun()

        elif st.button("처음으로 돌아가기"):
            st.session_state.page = "setup"
            st.rerun()
    else:
        st.rerun()
                elif st.button("처음으로 돌아가기"):
                    st.session_state.page = "setup"
                    st.rerun(),
                (st.session_state.a2, "A팀"),
                (st.session_state.b1, "B팀"),
                (st.session_state.b2, "B팀"),
            ])
        st.rerun()

    if st.button("되돌리기"):
        if st.session_state.history:
            last = st.session_state.history.pop()
            st.session_state.total["A"] -= last["A"]
            st.session_state.total["B"] -= last["B"]
            st.session_state.round -= 1
            st.rerun()
        else:
            st.warning("되돌릴 라운드가 없습니다.")

    st.markdown("---")
    st.subheader("📊 라운드 로그")
    for i, r in enumerate(st.session_state.history):
        st.text(f"🔸 {i+1}R → A팀: +{r['A']}점 | B팀: +{r['B']}점")

    st.markdown("---")
    if st.button("초기화"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    if st.button("기록 보기"):
        st.session_state.page = "record"
        st.rerun()

elif st.session_state.page == "record":
    record_page()
