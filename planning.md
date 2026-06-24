# TakeMeter — planning.md

> Complete this document before collecting data or fine-tuning.
> Your label taxonomy is the most important design decision in this project.
> Update this file before starting any stretch features.

---

## Community

**Chosen community:** [r/stocks](https://www.reddit.com/r/stocks/)

**Why this community:**

r/stocks is one of the largest serious investing forums on Reddit, with daily posts about individual tickers, sector trends, macro news, and portfolio strategy. Discourse is text-heavy and varied enough that the same ticker can appear in a due-diligence write-up, a beginner question, a headline repost, or a one-line bullish take — without relying on subjective "good vs. bad take" labels.

**Why it fits a classification task:**

Posts fall into observable **discourse types** (argument, question, news relay, bare opinion) that members recognize in practice. These categories are mutually exclusive when labeled by **primary purpose**, making them suitable for a classifier without needing to judge whether a take is correct.

**Community summary (Milestone 1 checkpoint):**

r/stocks mixes long-form theses, beginner questions, earnings/news reposts, and quick sentiment posts about US public-market stocks. The four labels (`analysis`, `question`, `news_share`, `opinion`) reflect how members actually use the sub — sharing research, asking for input, spreading headlines, or stating a view — which matters for any tool that might filter or rank posts by type rather than by "quality."

---

## Mutual exclusivity

Each post gets **exactly one label**, chosen by its **primary purpose**:


| If the post mainly…                                        | Label        |
| ---------------------------------------------------------- | ------------ |
| Presents a reasoned investment case                        | `analysis`   |
| Asks the community for help or input                       | `question`   |
| Relays news, links, or wire summaries                      | `news_share` |
| States a view or prediction without a structured "because" | `opinion`    |


**Overlap check (40-post pilot):** In the first 40 labeled posts, most assignments were straightforward. Borderline cases (listed under each label below) were resolved with the tie-break rules in **Hard edge cases**. No two labels were merged — boundaries were tightened instead of allowing double-labeling.

---

## Labels

Define each label in one complete sentence. Include two example posts per label.
Use the **primary purpose** of the post as the tie-break when a post could fit multiple labels.

### Label 1: `analysis`

**Definition:**

A post that makes a structured investment argument using reasoning, data, fundamentals, technicals, or macro context.

**Example 1:**

- **Title:** Semis vs. Software & MSFT's conundrum
- **Snippet:** "Since semi stocks have soared while software stocks have cratered… This brings me to Microsoft: they have the best of both worlds but are treated as the worst… TLDR; MSFT seems oversold to me."
- **URL:** [reddit.com/r/stocks/comments/1ucp36c](https://www.reddit.com/r/stocks/comments/1ucp36c/semis_vs_software_msfts_conundrum/)

**Example 2:**

- **Title:** Bought 50 shares of AIPO ETF
- **Snippet:** "A trend I've seen in the last 9 months has been a huge shift to behind the meter power generation… So I bought 50 shares of AIPO, thinking power will be the next bottleneck."
- **URL:** [reddit.com/r/stocks/comments/1uczxy4](https://www.reddit.com/r/stocks/comments/1uczxy4/bought_50_shares_of_aipo_etf/)

**Uncertain example (between two labels):**

- **Title:** The top has yet to come for MU and DRAM
- **Between:** `analysis` vs `opinion` (price targets like "MU hitting $1500" sound like opinion, but the post builds a multi-paragraph supply/demand case)
- **Chose:** `analysis` — structured HBM/margin argument dominates over the bare price call

---

### Label 2: `question`

**Definition:**

A post that primarily asks the community for advice, information, or input rather than presenting an argument.

**Example 1:**

- **Title:** MU or SNDK which one looks better going forward?
- **Snippet:** "Right now I'm stuck between whether MU is still the safer bet… or if sentiment really rotates into memory names and SNDK still has real upside to hold"
- **URL:** [reddit.com/r/stocks/comments/1ubw0yf](https://www.reddit.com/r/stocks/comments/1ubw0yf/mu_or_sndk_which_one_looks_better_going_forward/)

**Example 2:**

- **Title:** What's the idea behind buying stock of a company that doesn't pay dividend
- **Snippet:** "But what's the rationale behind buying stock of a company that doesn't pay dividend… why would anyone buy stock in the first place when they don't receive anything from the company?"
- **URL:** [reddit.com/r/stocks/comments/1ucbhkk](https://www.reddit.com/r/stocks/comments/1ucbhkk/whats_the_idea_behind_buying_stock_of_a_company/)

**Uncertain example:**

- **Title:** AI is disruptive. Individual companies have never been more volatile. What's the argument to not just buy indexes?
- **Between:** `question` vs `analysis` (includes observations about MSFT volatility, but the title explicitly asks for the counter-argument to stock-picking)
- **Chose:** `question` — primary purpose is soliciting the community's view

---

### Label 3: `news_share`

**Definition:**

A post that mainly shares, links, or summarizes news, earnings, or external content with minimal original argument.

**Example 1:**

- **Title:** SpaceX Investors Are Losing a Colossal Amount of Money
- **Snippet:** Brief IPO price recap, then "News: [https://finance.yahoo.com/…/spacex-investors-losing-colossal-amount…](https://finance.yahoo.com/…/spacex-investors-losing-colossal-amount…)"
- **URL:** [reddit.com/r/stocks/comments/1ud4b4p](https://www.reddit.com/r/stocks/comments/1ud4b4p/spacex_investors_are_losing_a_colossal_amount_of/)

**Example 2:**

- **Title:** SK Hynix overtakes Samsung to become South Korea's most valuable company
- **Snippet:** Full Reuters wire paste with link to reuters.com article
- **URL:** [reddit.com/r/stocks/comments/1ucj1kk](https://www.reddit.com/r/stocks/comments/1ucj1kk/sk_hynix_overtakes_samsung_to_become_south_koreas/)

**Uncertain example:**

- **Title:** Last quarter Lululemon sold more but made way less money
- **Between:** `news_share` vs `analysis` (reports earnings result, but adds a customs-rule explanation)
- **Chose:** `news_share` — primary content is relaying the quarterly result; the customs note is one sentence, not a full thesis

---

### Label 4: `opinion`

**Definition:**

A post that states a view, prediction, or sentiment without supporting reasoning (no clear "because" or evidence).

**Example 1:**

- **Title:** GOOG down ~6% today due to two top AI researchers departing
- **Snippet:** "Good time to add more GOOG? Bought a few more shares today." (pasted market context, no original investment case)
- **URL:** [reddit.com/r/stocks/comments/1ucqxip](https://www.reddit.com/r/stocks/comments/1ucqxip/goog_down_6_today_due_to_two_top_ai_researchers/)

**Example 2:**

- **Title:** $MSFT is nowhere near a bottom
- **Snippet:** "This stock is headed to $300 soon. Co pilot is a failure… To me, MSFT is now in that value trap territory"
- **URL:** [reddit.com/r/stocks/comments/1u9j65a](https://www.reddit.com/r/stocks/comments/1u9j65a/msft_is_nowhere_near_a_bottom/)

**Uncertain example:**

- **Title:** Intel Stock Price Miracle
- **Between:** `opinion` vs `question` (lists facts about revenue/losses, then asks "what triggered this 250% increase?")
- **Chose:** `opinion` — skeptical confusion about the move, not a genuine request for structured help

---

## Hard edge cases

**Hardest anticipated edge case:**

Short posts that mix a **buy/sell action** with **pasted news** — e.g. "GOOG down 6%, good time to add more?" with a block of market context copied from elsewhere.

**How I will handle it during annotation:**

If the poster's main contribution is a personal stance or trade intent (buy, sell, hold) without building an original case, label `**opinion`**. If they paste news but the body is mostly a multi-paragraph thesis, label `**analysis**`.

**Other ambiguous cases:**


| Situation                              | Tie-break rule                                                                                                |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Question with embedded thesis          | Label by **primary purpose** — if the title asks for input, use `question` even if context is included        |
| News link + strong commentary          | `analysis` if original argument dominates; `news_share` if the link/wire text is most of the body             |
| Earnings recap with numbers            | `news_share` if reporting results; `analysis` if interpreting what the numbers mean for valuation             |
| Price target + long thesis             | `analysis` if supply/demand or fundamentals support the call; `opinion` if target is stated without structure |
| Title is a question but body is a rant | `question` if genuinely seeking answers; `opinion` if rhetorical or venting                                   |


### Annotation pause log (Milestone 3)

Most posts in r/stocks were straightforward once I applied the primary-purpose rule. The cases below genuinely slowed me down — usually because the post mixed two discourse types (e.g. news paste + personal trade, or a question title with a hidden thesis).


| #   | Post (short description)                                                                                                                        | Could be                  | Chose        | Why                                                                    |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | ------------ | ---------------------------------------------------------------------- |
| 1   | [GOOG down ~6%…](https://www.reddit.com/r/stocks/comments/1ucqxip/) — "Good time to add more GOOG?" + pasted market context                     | `opinion` / `news_share`  | `opinion`    | Poster adds buy intent; pasted text is not original reporting          |
| 2   | [Last quarter Lululemon…](https://www.reddit.com/r/stocks/comments/1uc1hwn/) — earnings result + one-sentence customs explanation               | `news_share` / `analysis` | `news_share` | Primary content is the quarterly result; customs note is brief context |
| 3   | [The top has yet to come for MU…](https://www.reddit.com/r/stocks/comments/1ubo4yf/) — price targets + multi-paragraph HBM thesis               | `opinion` / `analysis`    | `analysis`   | Structured supply/demand argument dominates the price calls            |
| 4   | [AI is disruptive… What's the argument to not just buy indexes?](https://www.reddit.com/r/stocks/comments/1ucs046/) — observations + direct ask | `question` / `analysis`   | `question`   | Title explicitly solicits the community's counter-argument             |
| 5   | [Intel Stock Price Miracle](https://www.reddit.com/r/stocks/comments/1u9x42q/) — lists facts, asks what triggered the move                      | `question` / `opinion`    | `opinion`    | Skeptical confusion, not a genuine help request                        |


**Takeaway:** The `opinion` ↔ `analysis` and `news_share` ↔ `opinion` boundaries caused the most pause. Short posts with a ticker and a question mark were especially tricky — I defaulted to the post's *purpose* (seeking input vs. stating a view vs. relaying news), not how confident I felt about the poster's take.

---

## Data collection plan

**Method:** r/stocks RSS + targeted search RSS (via `scripts/collect_dataset.py`); **40 posts manually reviewed** in Milestone 1 pilot; remaining labels assigned via rule-based heuristics aligned with `planning.md`, then reviewed for balance.

**LLM pre-labeling:** No — all labels follow written definitions. Heuristic bulk labels were checked against the pause log and borderline examples above.

**Output file:** `data/raw_posts.csv` — columns `text` (title + body for Colab), `label`, plus `title`, `body`, `source_url`, `notes` for traceability. **Not pre-split**; Colab notebook applies 70/15/15 stratified split.

**Source:** [r/stocks/new](https://www.reddit.com/r/stocks/new/) and [r/stocks/hot](https://www.reddit.com/r/stocks/hot/)

**Target:** At least **200** labeled examples in `data/raw_posts.csv`.

**Target per label (aim for ~25% each):**


| Label        | Target |
| ------------ | ------ |
| `analysis`   | 50     |
| `question`   | 50     |
| `news_share` | 50     |
| `opinion`    | 50     |


**Collection workflow:**

1. Open a post on Reddit; copy **title**, **body** (if any), and **permalink URL**.
2. Paste into the next row of `data/raw_posts.csv`.
3. Assign exactly one label using the definitions above.
4. Update counts in `data/label_counts.csv`.
5. Skip stickied posts, AutoModerator, and posts with no meaningful text (title-only spam).

**If a label is underrepresented after 200 examples:**

1. Check `data/label_counts.csv` after every batch of ~25 new posts.
2. If any label is below **40 examples (20%)** at the 200-post mark, pause general browsing and **target that label**:
  - `**analysis`:** browse DD-style posts, ticker thesis threads, `[DD]` flairs if present
  - `**question`:** search r/stocks for titles starting with "Should I", "What do you think", "How do I"
  - `**news_share`:** browse during market hours; look for Reuters/Yahoo reposts and "BREAKING" headlines
  - `**opinion`:** look for short bullish/bearish one-liners and "I sold / I bought" posts
3. Collect **~15–20 extra posts** for the underrepresented label before finalizing the dataset.
4. Re-review borderline posts in that label to ensure definitions stayed consistent during oversampling.
5. If still short after targeted collection, lower the total dataset floor to **220 rows** rather than accepting a label below 20%.

**Train / validation / test split:**

- Split **after** all 200+ rows are labeled.
- Planned split: **70% train / 15% val / 15% test** (stratified by label).
- Test set stays untouched until final evaluation.

---

## Evaluation metrics

Accuracy alone is not enough when labels are imbalanced.

**Metrics I will report:**


| Metric                          | Why it matters for this task                            |
| ------------------------------- | ------------------------------------------------------- |
| Overall accuracy                | Baseline summary metric                                 |
| Per-class precision, recall, F1 | Shows which discourse types the model confuses          |
| Confusion matrix                | Reveals systematic errors (e.g. `opinion` → `analysis`) |
| Macro F1                        | Treats all four labels equally despite class imbalance  |


**Why these fit r/stocks:**

The main failure modes I expect are `**opinion` ↔ `analysis`** (short bullish takes vs. mini-theses) and `**news_share` ↔ `opinion**` (headline repost vs. "I bought the dip" commentary). Per-class F1 and the confusion matrix will show whether those boundaries held in data — not just whether the model memorized the majority class. Macro F1 matters because a feed-ranking tool should treat all four discourse types as equally worth detecting, even if one label is slightly more common in the raw subreddit stream.

---

## Baseline reflection (Milestone 4)

**Groq zero-shot baseline** (`llama-3.3-70b-versatile`, test set n=30): accuracy **0.533**, macro F1 **0.490**. All 30 responses were parseable.

### Where the baseline struggled


| Label        | Baseline F1 | Baseline recall | Reading                                                                                  |
| ------------ | ----------- | --------------- | ---------------------------------------------------------------------------------------- |
| `news_share` | **0.71**    | 0.75            | Strongest — wire-style posts and headline reposts match generic “sharing news” intuition |
| `analysis`   | 0.57        | **0.75**        | High recall, **low precision (0.46)** — labels too many posts as structured argument     |
| `question`   | 0.46        | 0.43            | Moderate — titles with context or embedded thesis confuse the model                      |
| `opinion`    | **0.22**    | **0.14**        | Weakest — barely detects bare sentiment / trade-intent posts                             |


The baseline’s main failure was `**opinion`**: recall **0.14** means it missed most opinion posts entirely. `**analysis`** looked better on paper (F1 0.57) but with low precision — consistent with `**opinion` → `analysis**` and possibly `**question` → `analysis**` confusion when a post mentions tickers or includes reasoning-like text.

### Likely confusions

1. `**opinion` ↔ `analysis**` — Short bullish takes or “good time to buy?” posts with pasted context read as mini-theses to a generic prompt that doesn’t know our primary-purpose tie-break.
2. `**news_share` ↔ `opinion**` — Buy/sell intent plus headline paste (see pause log #1) — baseline may lump these with news or analysis instead of `opinion`.
3. `**question` ↔ `analysis**` — Posts that ask for input but include observations (pause log #4) — zero-shot may default to the more “substantive” label.

### Hypothesis (to test after fine-tuning)

Fine-tuning DistilBERT on **200 r/stocks-labeled examples** should:

- **Raise `opinion` recall and F1** — the model will see our tie-break rules in data, not just in the prompt.
- **Improve `analysis` precision** — fewer false-positive theses on short takes.
- **Leave `news_share` roughly stable** — already strong at baseline.
- **Improve `question` only modestly** — boundary with `analysis` is ambiguous even in human labels.

### After fine-tuning (hypothesis check)


| Label        | Baseline F1 | Fine-tuned F1 | Hypothesis                                    |
| ------------ | ----------- | ------------- | --------------------------------------------- |
| `opinion`    | 0.22        | **~0.46**     | **Confirmed** — largest gain                  |
| `analysis`   | 0.57        | **~0.62**     | **Partially confirmed** — better balanced P/R |
| `news_share` | 0.71        | **~0.67**     | **Roughly stable**                            |
| `question`   | 0.46        | **~0.43**     | **Confirmed modest** — still the weak pair    |


Overall: macro F1 **0.490 → 0.554** (+0.063). Fine-tuning beat the generic LLM on the labels we defined; `**question`** remains the main remaining confusion for both models.

---

## Limitations & honest assessment (Milestone 5)

### Against course benchmarks

The Milestone 5 guide suggests **per-class F1 ≥ 0.70** means the model is learning all distinctions well. Our fine-tuned results fall short of that bar:


| Label        | Fine-tuned F1 | Course “learning well” (≥ 0.70) |
| ------------ | ------------- | ------------------------------- |
| `news_share` | ~0.67         | Close, but below                |
| `analysis`   | ~0.62         | Below                           |
| `opinion`    | ~0.46         | Well below                      |
| `question`   | ~0.43         | Well below                      |


On **accuracy**, fine-tuning improved **0.533 → 0.567** (+0.033) — a modest gain that fits the guide’s “**fine-tuned barely beats baseline**” pattern when judged on that single number alone. **Macro F1** tells a slightly stronger story (+0.063), driven mainly by recovering `**opinion`** posts the baseline missed — but neither metric suggests a production-ready classifier.

We also **narrowly missed two self-set success criteria**: beat Groq by **+0.08** macro F1 (achieved +0.063), and test accuracy **≥ 0.60** (achieved 0.567).

### Contributing factors

1. **Small data** — 200 labeled posts (~140 train) and **30 test examples** (7–8 per class). Metrics swing with a handful of mislabels.
2. **Fuzzy boundaries** — The pause log cases (`opinion` vs `analysis`, `question` vs `analysis`) are genuinely ambiguous even for a human annotator following written rules.
3. **Heuristic bulk labels** — 160 of 200 rows were rule-labeled; noise at borderline posts likely caps achievable F1.
4. **Four-way task** — Random baseline is 25% accuracy; ~57% is above chance but far from “solved.”

### Why these hard boundaries still matter

Easier taxonomies (e.g. “long post vs short post” or sentiment-only) would score higher but deliver **less useful** feed behavior. r/stocks members care about *kind* of content: a due-diligence thread, a beginner question, breaking news, and a hot take are different experiences — even when the same ticker appears in all four.

A discourse-type filter with imperfect F1 could still add practical value:

- **Ranking / filtering** does not require perfection — surfacing more `analysis` and fewer misfired `opinion` posts (where fine-tuning improved most) improves a “research mode” even at ~0.55 macro F1.
- **Transparent failure modes** — confusion between `question` and `analysis` is a known, documentable pattern moderators can override; a simpler label set would hide that nuance.
- **Iterative improvement** — hard boundaries define *what* to fix next (re-annotate borderline rows, oversample `question`), whereas a coarse taxonomy would not expose those errors.

**Conclusion:** The outcome is **respectable for a course project** — fine-tuning beat a generic LLM on custom labels and confirmed the baseline hypothesis on `**opinion`** — but **not strong by strict F1 benchmarks**. The results support keeping these labels for product relevance, while treating **~0.55 macro F1** as a prototype floor, not a ship threshold. More manually reviewed data at the documented edge cases would be the first lever before further hyperparameter tuning.

---

## Definition of success

**Useful in a real community tool:**

A classifier that reliably separates `**analysis`** posts from `**opinion**` and `**news_share**` would let r/stocks build a "substantive discussion" filter — surfacing due-diligence and macro threads without hiding beginner `**question**` posts or breaking news relays. Success means users see fewer low-signal hot takes when they want research, while news and questions still reach the right audiences.

**Good enough for this project:**

All criteria measured on the **held-out test set** (15% stratified split, untouched until final eval):


| Criterion                    | Threshold                                                                   | Rationale                                                            |
| ---------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Macro F1                     | **≥ 0.55**                                                                  | Balanced performance across all four labels on a fuzzy-boundary task |
| Beat Groq zero-shot baseline | **Macro F1 at least +0.08 higher** than `llama-3.3-70b-versatile` zero-shot | Fine-tuning should beat a generic LLM that never saw my labels       |
| `analysis` recall            | **≥ 0.50**                                                                  | Don't miss substantive posts — main value of the classifier          |
| Worst-class F1               | **≥ 0.40**                                                                  | No label is effectively ignored                                      |
| Test accuracy                | **≥ 0.60**                                                                  | Sanity floor; not the primary metric                                 |


**Not good enough:**

- Macro F1 **< 0.45** or fine-tuned model **does not beat** the Groq zero-shot baseline → labels or data need revision, not more epochs.
- `**question` or `opinion` F1 < 0.30** → likely confusion with `analysis`; revisit tie-break rules and re-annotate borderline rows.
- **Test accuracy > 0.90** on this task → suspect data leakage, overly simple labels, or test examples duplicated in training.
- Model predicts `**question` for > 50%** of all posts → collapsed to the safest generic class; not deployable.

---

## Evaluation report (Milestone 6)

Final evaluation on held-out **test set (n=30)**. Machine-readable metrics: `report/evaluation_results.json` · plot: `confusion_matrix.png` (Colab). Polished summary for readers: `**README.md`** → Evaluation.

### Model & training


|                |                                                                       |
| -------------- | --------------------------------------------------------------------- |
| **Base model** | `distilbert-base-uncased`                                             |
| **Baseline**   | Groq `llama-3.3-70b-versatile` (zero-shot)                            |
| **Training**   | 3 epochs, batch 16, lr `2e-5`, `warmup_steps=3`, weight decay 0.01    |
| **Checkpoint** | Best epoch by validation **macro F1** (`load_best_model_at_end=True`) |


### Results comparison


| Model                     | Accuracy   | Macro F1   |
| ------------------------- | ---------- | ---------- |
| Zero-shot baseline (Groq) | 0.533      | 0.490      |
| Fine-tuned DistilBERT     | **0.567**  | **0.554**  |
| **Improvement**           | **+0.033** | **+0.063** |


### Baseline vs fine-tuned (outcome)

Macro F1 **0.490 → 0.554** (+0.063). Fine-tuning beat Groq on custom labels; main gain was `**opinion`** (F1 **0.22 → 0.46**). Dominant remaining error: `**question` ↔ `opinion`** (5 mislabels in confusion matrix). See **Baseline reflection** and **Limitations** above for pre/post analysis.

### Per-class metrics — Groq baseline


| Label        | Precision | Recall | F1   | Support |
| ------------ | --------- | ------ | ---- | ------- |
| `analysis`   | 0.46      | 0.75   | 0.57 | 8       |
| `question`   | 0.50      | 0.43   | 0.46 | 7       |
| `news_share` | 0.67      | 0.75   | 0.71 | 8       |
| `opinion`    | 0.50      | 0.14   | 0.22 | 7       |


### Per-class metrics — fine-tuned DistilBERT


| Label        | Precision | Recall | F1   | Support |
| ------------ | --------- | ------ | ---- | ------- |
| `analysis`   | 0.62      | 0.62   | 0.62 | 8       |
| `question`   | 0.50      | 0.43   | 0.46 | 7       |
| `news_share` | 0.60      | 0.75   | 0.67 | 8       |
| `opinion`    | 0.50      | 0.43   | 0.46 | 7       |


### Confusion matrix — fine-tuned model

Rows = **true** label, columns = **predicted** label (17/30 correct).


| True Pred        | `analysis` | `question` | `news_share` | `opinion` |
| ---------------- | ---------- | ---------- | ------------ | --------- |
| `**analysis`**   | **5**      | 1          | 2            | 0         |
| `**question`**   | 0          | **3**      | 1            | 3         |
| `**news_share`** | 2          | 0          | **6**        | 0         |
| `**opinion`**    | 1          | 2          | 1            | **3**     |


**Main off-diagonal patterns:**

- `**question` → `opinion` (3)** and `**opinion` → `question` (2)**
- `**analysis` ↔ `news_share` (2 each way)**
- `**opinion` → `analysis` (1)** and `**opinion` → `news_share` (1)**

### Success criteria — measured results


| Criterion          | Target          | Result                | Verdict       |
| ------------------ | --------------- | --------------------- | ------------- |
| Macro F1           | ≥ 0.55          | **0.554**             | Pass (barely) |
| Beat Groq macro F1 | +0.08 (≥ 0.570) | **+0.063**            | Fail (narrow) |
| `analysis` recall  | ≥ 0.50          | **0.62**              | Pass          |
| Worst-class F1     | ≥ 0.40          | **0.46** (`question`) | Pass          |
| Test accuracy      | ≥ 0.60          | **0.567**             | Fail          |


### Failure analysis (3 test-set errors)

#### 1. True `question` → predicted `opinion`

- **Post:** [MU or SNDK which one looks better going forward?](https://www.reddit.com/r/stocks/comments/1ubw0yf/)
- **Predicted:** `opinion` (confidence **0.51**)
- **Confusion:** `question` ↔ `opinion` — body states a view before the ask; model weights ticker sentiment over soliciting input.
- **Root cause:** Label boundary (primary-purpose tie-break), not random noise.
- **Fix:** More manually reviewed `question` rows with embedded context.

#### 2. True `opinion` → predicted `question`

- **Post:** [GOOG down ~6% today…](https://www.reddit.com/r/stocks/comments/1ucqxip/) — “Good time to add more GOOG?” + pasted context
- **Predicted:** `question` (confidence **0.48**)
- **Confusion:** `opinion` → `question` — question mark triggers help-request; pause log #1.
- **Root cause:** Label boundary + possible heuristic inconsistency on similar rows.
- **Fix:** Re-annotate “buy the dip + ?” posts; add pause-log-style training examples.

#### 3. True `news_share` → predicted `analysis`

- **Post:** [Last quarter Lululemon sold more but made way less money](https://www.reddit.com/r/stocks/comments/1uc1hwn/)
- **Predicted:** `analysis` (confidence **0.54**)
- **Confusion:** `news_share` ↔ `analysis` — one-sentence customs explanation reads as mini-thesis.
- **Root cause:** Label boundary (brief context vs structured argument).
- **Fix:** More `news_share` rows with single-sentence context after a headline.

### Sample classifications


| Post (short)                                                                               | True         | Predicted    | Confidence |     |
| ------------------------------------------------------------------------------------------ | ------------ | ------------ | ---------- | --- |
| [SK Hynix overtakes Samsung…](https://www.reddit.com/r/stocks/comments/1ucj1kk/)           | `news_share` | `news_share` | **0.89**   | ✓   |
| [Semis vs. Software & MSFT's conundrum](https://www.reddit.com/r/stocks/comments/1ucp36c/) | `analysis`   | `analysis`   | **0.72**   | ✓   |
| [MU or SNDK which one looks better…](https://www.reddit.com/r/stocks/comments/1ubw0yf/)    | `question`   | `opinion`    | 0.51       | ✗   |
| [$MSFT is nowhere near a bottom](https://www.reddit.com/r/stocks/comments/1u9j65a/)        | `opinion`    | `opinion`    | **0.67**   | ✓   |
| [AI is disruptive… buy indexes?](https://www.reddit.com/r/stocks/comments/1ucs046/)        | `question`   | `question`   | **0.58**   | ✓   |


**Correct example (SK Hynix):** Body is a Reuters wire paste with source link and no original thesis — high confidence matches the clearest `news_share` template in training.

### Model reflection


|                |                                                                                         |
| -------------- | --------------------------------------------------------------------------------------- |
| **Intended**   | Classify by **primary purpose** across four discourse types                             |
| **Captured**   | `news_share` lexical patterns; longer `analysis`-like posts; improved `opinion` vs Groq |
| **Missed**     | Primary-purpose tie-breaks — surface cues (?, length, headlines) override intent        |
| **Overfit to** | Length and finance vocabulary; short posts collapse toward `opinion` / `question`       |
| **Gap**        | Annotator judgment vs learned correlates → **~0.55 macro F1** on n=30                   |


---

### Label stress-testing

Before annotating 200 posts, I will use an LLM to generate **5–10 synthetic posts** that sit on the boundary between two labels (e.g. `opinion` vs `analysis`). If my definitions can't classify those consistently, I will tighten the definitions first.

### Annotation assistance

- Heuristic pre-labeling via `scripts/collect_dataset.py` for bulk rows; **40 pilot posts manually reviewed**; borderline cases documented in pause log above

### Failure analysis

- Documented **3 test-set failures** with confusion diagnosis (see **Evaluation report** above)
- Clustered error patterns: `question` ↔ `opinion`, `analysis` ↔ `news_share` (confusion matrix + failure analysis)