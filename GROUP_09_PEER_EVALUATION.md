# PEER EVALUATION REPORT — GROUP 09

**FROM:** Group 20 (Evaluator)

---

## SUMMARY

12/12 TCs implemented, compile clean, rubric-compliant. Strength: real oracle precision (TC-04, TC-10) — bug-hunting, not crash-checks. Weakness: coverage stays on the happy path (borrow-rejection & case-insensitivity untested).

## RATING

| Area | Rating |
|---|---|
| All 12 tests done | Good |
| Checks are correct | Okay — strong in some, weak in others |
| Flutter/web handling | Good |
| How much is tested | Okay — only easy cases |
| Clean code | Okay — small issues |

## GOOD POINTS

- TC-04/06/07 — assert every result's content matches query (Oracle C), not just `count>0`.
- TC-05 — asserts zero results; kills stale-result bug.
- TC-10 — best in suite: verifies state flip to "Có sẵn" + flags missing overdue warning (REQ-05).
- TC-02/03 — exact error-string match.
- Smart waits throughout; no `time.sleep`; robust semantics selectors.

## WEAK POINTS

| Pri | Target | Defect |
|---|---|---|
| 1 | TC-08 borrow | Checks toast only; never verifies book → "Đã mượn". |
| 2 | REQ-03 case-insens. | Never exercised — searches use matching casing. |
| 3 | REQ-04 rejections | No suspended/expired/at-limit/already-borrowed tests. |
| 4 | REQ-01 | Missing wrong-email branch ("Không tìm thấy thành viên"). |
| 5 | TC-09 / TC-12 | Loose oracles (presence-only / OR-of-three). |
| 6 | Hygiene | Unused `re`,`time` imports; empty f-strings; "sucess" typo. |
