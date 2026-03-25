# Five Improvements for English Learners
*From the perspective of an English language professor*

---

## 1. Map Scores to CEFR Levels (A1–C2)

**The problem:** The current proficiency labels (Beginner, Elementary, Pre-Intermediate…) are informal and inconsistent across textbooks, schools, and employers. A learner cannot use them to enrol in a course, sit an exam, or describe their level to a recruiter.

**The improvement:** Add a CEFR column alongside the existing label:

| Current score range | Current label | CEFR level |
|---|---|---|
| ≤ 2.0 | Beginner | A1 |
| ≤ 3.5 | Elementary | A2 |
| ≤ 5.0 | Pre-Intermediate | B1 |
| ≤ 6.5 | Intermediate | B2 |
| ≤ 7.5 | Upper-Intermediate | C1 |
| ≤ 8.5 | Advanced | C1+ |
| ≤ 10.0 | Proficient | C2 |

Display both ("B2 – Intermediate") so learners can communicate their level in universally understood terms. Every teacher, employer, and certification body worldwide uses CEFR; showing it makes the score immediately actionable.

---

## 2. Show Specific Errors in Context (Inline Error Highlighting)

**The problem:** The feedback currently says things like *"Watch for subject-verb agreement"* but never shows **which sentence** contained the error. A learner reads this, nods, and moves on — they rarely know which exact sentence to fix.

**The improvement:** Return the offending text alongside the correction:

> ❌ "He walk to school every day."
> ✅ Suggestion: "He **walks** to school every day." *(subject-verb agreement)*

The grammar analyzer already detects agreement errors, double words, and resumptive pronouns — the sentence positions are available. Surfacing even one or two quoted examples per category would transform generic feedback into a grammar lesson. Research consistently shows that *noticing* — seeing the error highlighted in one's own output — is far more effective than abstract advice.

---

## 3. Vocabulary Gap Analysis Using Frequency Bands

**The problem:** The vocabulary analyzer measures type-token ratio and polysyllabic word proportion — statistical proxies — but never tells the learner *what kind* of vocabulary they are using or what level they should be targeting next.

**The improvement:** Classify content words by frequency band (e.g. the Oxford 3000, CEFR A1–B2 list, and C1–C2 list). Then report:

> "78 % of your content words are A1–B2 level. Try replacing common words with higher-frequency C1 alternatives:
> *big → substantial, but → however, help → facilitate*"

This is how vocabulary instruction actually works in IELTS, Cambridge, and TOEFL preparation. Learners need a concrete upgrade path, not just a number. Even a free frequency list (BNC/COCA top 5 000) would enable this without adding heavy dependencies.

---

## 4. Detect Article and Tense Errors

**The problem:** The grammar analyzer detects only four patterns: double words, subject-verb agreement, resumptive pronouns, and missing capitalisation. However, the two most common and persistent errors made by ESL learners at every level are:

- **Article errors**: "I went to park" / "She is teacher" / "I saw the interesting film"
- **Tense inconsistency**: mixing past and present within a single narrative

These are invisible to the current analyzer, so a learner riddled with article errors could still receive a high grammar score.

**The improvement:** Add two lightweight detectors:
- *Article checker*: flag noun phrases (determiner + noun patterns via POS tags) where a definite or indefinite article appears to be missing or misused.
- *Tense consistency checker*: identify the dominant tense in the text and flag sentences that switch without a discourse reason.

This does not require spaCy or LanguageTool — it can be built on top of the existing NLTK POS tagger already in the codebase (`averaged_perceptron_tagger_eng`).

---

## 5. Prescribe Targeted Practice Exercises, Not Just Advice

**The problem:** Almost every feedback message ends with general advice: *"practise reading authentic English content"*, *"use a thesaurus"*, *"review basic grammar rules"*. This is the least useful thing you can tell a language learner. It is the equivalent of a doctor saying "eat healthier." Learners already know they should practise — they need to know *exactly what* to practise.

**The improvement:** Map each low-scoring category to a specific, doable micro-exercise:

| Category | Low score exercise |
|---|---|
| Grammar | "Write 5 sentences about your day using he/she/it + present simple" |
| Vocabulary | "Rewrite your text replacing the 3 most repeated content words with synonyms" |
| Sentence structure | "Find any two short sentences and combine them using 'although' or 'because'" |
| Coherence | "Add one transition word at the start of each paragraph" |
| Spelling | "Look up the correct spelling of each flagged word and write it three times" |
| Fluency | "Read one paragraph of a news article aloud, then try to paraphrase it in writing" |

These exercises are grounded in second-language acquisition research on *output practice* and *noticing*. They give learners something concrete to do in the next five minutes, which is exactly when motivation is highest — immediately after receiving feedback.
