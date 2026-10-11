"""Prompt Engineering Gym: write prompts that make GPT satisfy strict, automatically-checked requirements."""
import json
import re
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import llm  # noqa: E402


def words(s):
    return re.findall(r"[A-Za-z0-9'’-]+", s)


def j(s):
    s = re.sub(r"^```(?:json)?|```$", "", s.strip(), flags=re.M).strip()
    return json.loads(s)


def chk_json(out):
    d = j(out)
    ok = sorted(d) == ["city", "date", "person"] and {p.lower() for p in d["person"]} == {"priya", "tom"} \
        and d["city"].lower() == "paris" and "5" in str(d["date"]) and "may" in str(d["date"]).lower()
    return ok, "Need exactly keys person (list: Priya, Tom), city, date (5 May)." if not ok else "Valid and correct."


LEVELS = [
    dict(title="Level 1 · One word", goal="Make the model reply with exactly the single word: banana (lowercase, no punctuation, nothing else).",
         data="", check=lambda o: (o.strip() == "banana", f"Got: {o[:60]!r}")),
    dict(title="Level 2 · Nuanced sentiment", goal="Classify the INPUT review. Reply with ONE lowercase word: positive, negative or mixed.",
         data="I loved the movie but the popcorn was terrible and the seats were broken.",
         check=lambda o: (o.strip() == "mixed", f"Got: {o[:60]!r} (expected the single word 'mixed')")),
    dict(title="Level 3 · Strict JSON", goal="Extract from INPUT: valid JSON only, keys person (list), city, date. No markdown fences, no commentary.",
         data="Priya met Tom in Paris on 5 May to plan the launch.",
         check=lambda o: chk_json(o) if not o.strip().startswith("```") else (False, "Remove the ``` markdown fences.")),
    dict(title="Level 4 · Exact length", goal="Summarise INPUT in EXACTLY 10 words. Output only the summary.",
         data="The city council voted on Tuesday to build a new bicycle path along the river, hoping to cut traffic and pollution while encouraging residents to exercise more.",
         check=lambda o: (len(words(o)) == 10, f"Your output had {len(words(o))} words, need 10.")),
    dict(title="Level 5 · Format discipline", goal="Give exactly 3 markdown bullets ('- ...') about INPUT, each at most 6 words, with NO intro or outro line.",
         data="Why sleep matters for students",
         check=lambda o: (lambda L: (len(L) == 3 and all(l.startswith(("-", "*")) and len(words(l)) <= 6 for l in L), f"Got {len(L)} lines: {L[:4]}"))([l for l in o.strip().splitlines() if l.strip()])),
    dict(title="Level 6 · Persona + constraint", goal="Translate INPUT into Spanish AND make every sentence end with '!'. Output only the translation.",
         data="Good morning. I would like a coffee, please.",
         check=lambda o: (lambda s: (bool(re.search(r"buen", s.lower())) and all(x.strip().endswith("!") for x in re.split(r"(?<=!)\s+|(?<=\.)\s+", s.strip()) if x.strip()) and "." not in s, f"Got: {o[:80]!r}"))(o)),
]

st.set_page_config(page_title="Prompt Gym", page_icon="🏋️")
st.title("🏋️ Prompt Engineering Gym")
st.caption("You write the prompt. GPT answers at temperature 0. Python checks the answer. 1 tiny Azure call per attempt.")

ss = st.session_state
ss.setdefault("passed", {})
ss.setdefault("attempts", {})
ss.setdefault("last", None)
st.sidebar.metric("Levels cleared", f"{len(ss.passed)} / {len(LEVELS)}")
for i, lv in enumerate(LEVELS):
    st.sidebar.write(("✅ " if i in ss.passed else "⬜ ") + lv["title"] + (f"  ({'⭐' * ss.passed[i]})" if i in ss.passed else ""))
if st.sidebar.button("Reset progress"):
    ss.passed, ss.attempts, ss.last = {}, {}, None
    st.rerun()

i = st.selectbox("Level", range(len(LEVELS)), format_func=lambda k: LEVELS[k]["title"], index=min(len(ss.passed), len(LEVELS) - 1))
lv = LEVELS[i]
st.info(f"🎯 **Goal:** {lv['goal']}")
if lv["data"]:
    st.markdown(f"**INPUT** (appended to your prompt automatically):\n> {lv['data']}")
prompt = st.text_area("Your prompt", height=120, placeholder="Write instructions for the model...", key=f"p{i}")
if st.button("Run", type="primary", disabled=not prompt.strip()):
    ss.attempts[i] = ss.attempts.get(i, 0) + 1
    user = prompt + (f"\n\nINPUT:\n{lv['data']}" if lv["data"] else "")
    try:
        out, _ = llm.chat([{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user}],
                          temperature=0, max_tokens=120)
        try:
            ok, note = lv["check"](out)
        except Exception as e:  # e.g. invalid JSON
            ok, note = False, f"Checker error: {e}"
        if ok and i not in ss.passed:
            ss.passed[i] = 3 if ss.attempts[i] == 1 else 2 if ss.attempts[i] <= 3 else 1
        ss.last = (i, out, ok, note)
    except llm.ContentFiltered:
        ss.last = (i, "", False, "Azure's content filter rejected that prompt.")
    except Exception as e:
        ss.last = (i, "", False, f"API error: {e}")
    st.rerun()

if ss.last and (ss.last[0] == i or ss.last[2]):  # a pass moves on to the next level, so keep showing it
    li, out, ok, note = ss.last
    st.markdown("**Model output**" + (f" (Level {li + 1})" if li != i else ""))
    st.code(out or "(none)", language=None)
    (st.success if ok else st.error)(("✅ Passed! " if ok else "❌ Not yet. ") + note)
    st.caption(f"Attempts on level {li + 1}: {ss.attempts.get(li, 0)} · stars: first try = ⭐⭐⭐, ≤3 tries = ⭐⭐, more = ⭐")
