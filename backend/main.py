from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

NUM_POOL = list(range(1, 46))

def get_lotto_round(drw_no):
    url = "https://www.dhlottery.co.kr/common.do"

    params = {
        "method": "getLottoNumber",
        "drwNo": drw_no
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)

    try:
        data = response.json()
    except Exception:
        print("JSON 변환 실패")
        print("status:", response.status_code)
        print("text:", response.text[:300])
        return None

    if data.get("returnValue") != "success":
        return None

    return tuple(sorted([
        data["drwtNo1"],
        data["drwtNo2"],
        data["drwtNo3"],
        data["drwtNo4"],
        data["drwtNo5"],
        data["drwtNo6"],
    ]))

def fetch_past_wins():
    past_wins = set()
    round_no = 1

    while True:
        nums = get_lotto_round(round_no)
        if nums is None:
            break
        past_wins.add(nums)
        round_no += 1

    return past_wins

def check_conditions(combo):
    # `combo` is expected to be sorted (tuple/list length 6).

    odds = sum(x % 2 for x in combo)
    if odds not in [2, 3, 4]:
        return False

    total = sum(combo)
    if total < 120 or total > 160:
        return False

    consec = 1
    for i in range(1, 6):
        if combo[i] == combo[i - 1] + 1:
            consec += 1
            if consec >= 4:
                return False
        else:
            consec = 1

    sections = []

    for i in range(5):
        if i < 4:
            low = i * 9 + 1
            high = i * 9 + 10
            count = len([x for x in combo if low <= x <= high])
        else:
            count = len([x for x in combo if 37 <= x <= 45])

        sections.append(count)

    if max(sections) >= 4:
        return False

    return True

@app.get("/pick")
def pick_lotto():
    picked_set = set()
    while len(picked_set) < 5:
        combo = tuple(sorted(random.sample(NUM_POOL, 6)))
        if check_conditions(combo):
            picked_set.add(combo)

    return {
        "numbers": sorted(picked_set),
    }