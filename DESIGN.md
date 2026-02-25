# English Scorer - Design Document

## 1. Overview

**English Scorer** is a web application designed to evaluate English language proficiency for non-native speakers. The system accepts text input ranging from a single sentence to 2000 words and provides:
- An overall numerical score from 1 to 10
- Visual breakdown of scores across 6 subcategories
- Actionable feedback to help improve English writing

### 1.1 Purpose

To provide learners of English with immediate, objective feedback on their writing proficiency, helping them track progress and identify areas for improvement.

### 1.2 Target Audience

- Non-native English speakers learning the language
- ESL (English as a Second Language) students
- Self-directed language learners seeking practice and feedback

---

## 2. Goals and Objectives

### 2.1 Primary Goals

1. **Accurate Assessment**: Provide reliable scoring that reflects true English proficiency level
2. **Clear Visualization**: Present scores in an intuitive, visual format that's easy to understand
3. **Actionable Feedback**: Deliver specific, helpful recommendations for improvement
4. **Immediate Results**: Provide scores and feedback quickly to support iterative learning
5. **Accessibility**: Make the web application easy to use for learners at all proficiency levels
6. **Educational Value**: Help users understand their strengths and weaknesses through detailed breakdown

### 2.2 Success Criteria

**MVP Targets (Phase 1):**
- Scoring consistency: 0.6-0.7 correlation with expert ratings
- Processing time: under 10 seconds for 95% of submissions
- Concurrent users: 50 simultaneous users
- User-friendly web interface requiring no training or instructions
- Visual design that works on desktop and mobile browsers

**Long-term Targets (Post-MVP):**
- Scoring consistency: >0.8 correlation with expert ratings
- Processing time: under 5 seconds for 95% of submissions
- Scalable to handle 100+ concurrent users
- Feedback rated as "helpful" or "very helpful" by 80%+ of users

---

## 3. Functional Requirements

### 3.1 Input Requirements

| Requirement | Specification |
|------------|---------------|
| **Minimum Input** | 1 sentence (approximately 5-10 words minimum) |
| **Maximum Input** | 2000 words |
| **Input Format** | Plain text |
| **Encoding** | UTF-8 |
| **Language** | English only (language detection performed) |
| **Special Characters** | Standard English punctuation supported |
| **Preprocessing** | Smart quotes normalized, URLs/emails preserved, formatting characters removed |

### 3.2 Output Requirements

| Requirement | Specification |
|------------|---------------|
| **Overall Score Range** | 1-10 (decimal with 1 decimal place) |
| **Subcategory Scores** | Individual scores (1-10) for each evaluation criterion |
| **Score Visualization** | Visual indicators (charts, progress bars, color-coded displays) |
| **Feedback** | Actionable recommendations for improvement |
| **Response Time** | < 10 seconds for MVP, < 5 seconds for production (95th percentile) |

#### Output Structure
```json
{
  "overall_score": 7.5,
  "proficiency_level": "Upper-Intermediate",
  "subcategory_scores": {
    "grammar": 8.0,
    "vocabulary": 7.2,
    "spelling_mechanics": 9.0,
    "sentence_structure": 7.0,
    "coherence_organization": 7.3,
    "fluency_naturalness": 6.8
  },
  "feedback": {
    "grammar": "Good subject-verb agreement. Consider reviewing article usage.",
    "vocabulary": "Good range. Try incorporating more advanced vocabulary.",
    "spelling_mechanics": "Excellent spelling and punctuation.",
    "sentence_structure": "Good variety. Add more complex sentences.",
    "coherence_organization": "Clear organization. Use more transition words to connect ideas.",
    "fluency_naturalness": "Work on idiomatic expressions for more natural flow."
  },
  "confidence_level": "high",
  "word_count": 145
}
```

### 3.3 Core Features

1. **Text Input Interface**: Large text area for users to paste or type their text
2. **Word Counter**: Real-time display of current word count
3. **Submit/Analyze Button**: Trigger scoring process
4. **Overall Score Visualization**: Large, prominent display of the final score (1-10) with proficiency level
5. **Subcategory Score Visualization**: Visual representation of individual scores:
   - Grammar
   - Vocabulary
   - Spelling & Mechanics
   - Sentence Structure
   - Coherence & Organization
   - Fluency & Naturalness
   - Display options: Progress bars, charts, color-coded indicators
6. **Confidence Indicator**: Shows reliability of score based on text length
7. **Feedback Panel**: Actionable recommendations for each subcategory
8. **Demo Mode**: "Try an example" with pre-filled sample texts
9. **Input Validation**: Check for minimum/maximum length requirements, language detection

---

## 4. Scoring System Design

### 4.1 Scoring Scale Definition

| Score Range | Proficiency Level | Description |
|-------------|------------------|-------------|
| **1-2** | Beginner | Very limited vocabulary, frequent grammar errors, barely comprehensible |
| **3-4** | Elementary | Basic sentence structure, many grammar errors, limited vocabulary |
| **5-6** | Intermediate | Moderate grammar accuracy, adequate vocabulary, some complex sentences |
| **7-8** | Upper-Intermediate | Good grammar control, varied vocabulary, clear communication |
| **9-10** | Advanced | Near-native proficiency, sophisticated vocabulary, minimal errors |

### 4.1.1 Mapping to International Standards

To provide context for the 1-10 scale, scores are mapped to widely recognized proficiency frameworks:

| Our Score | Proficiency Level | CEFR Level | IELTS Band | TOEFL iBT (Writing) |
|-----------|------------------|------------|------------|---------------------|
| **1.0-2.0** | Beginner | A1 | 1-2 | 0-7 |
| **2.1-3.5** | Elementary | A2 | 3-4 | 8-14 |
| **3.6-5.0** | Pre-Intermediate | A2-B1 | 4-5 | 15-19 |
| **5.1-6.5** | Intermediate | B1 | 5-6 | 20-23 |
| **6.6-7.5** | Upper-Intermediate | B2 | 6-7 | 24-26 |
| **7.6-8.5** | Advanced | C1 | 7-8 | 27-29 |
| **8.6-10.0** | Proficient/Native | C2 | 8.5-9 | 30 |

**Important Notes:**
- These mappings are **approximate** and for general guidance only
- Official CEFR, IELTS, and TOEFL scores require standardized testing
- Our system focuses on written English proficiency only (not speaking/listening)
- Scores may vary based on text type (formal essay vs. casual writing)
- This tool is designed for **learning and improvement**, not certification

**Display in UI:**
- Show the equivalent proficiency level alongside the numerical score
- Example: "7.5 / 10 - Upper-Intermediate (≈ CEFR B2, IELTS 6-7)"
- Optional toggle to show/hide standard equivalents

### 4.2 Evaluation Criteria

The scoring algorithm should consider multiple dimensions of language proficiency:

#### 4.2.1 Grammar (Weight: 25%)
- Subject-verb agreement
- Tense consistency and correctness
- Pronoun usage
- Article usage (a/an/the)
- Preposition usage
- **Metrics**: Error rate per 100 words, error type distribution

#### 4.2.2 Vocabulary (Weight: 20%)
- Vocabulary range and diversity (type-token ratio)
- Appropriate word choice
- Collocation accuracy
- Academic/formal vocabulary usage (Academic Word List coverage)
- Word repetition and variation
- **Metrics**: Lexical diversity, vocabulary sophistication score

#### 4.2.3 Spelling and Mechanics (Weight: 10%)
- Spelling accuracy
- Punctuation correctness
- Capitalization rules
- Formatting consistency
- **Metrics**: Error count, error density

#### 4.2.4 Sentence Structure (Weight: 20%)
- Sentence variety (simple, compound, complex)
- Sentence length variation
- Proper use of conjunctions and connectors
- Subordinate clause usage
- **Metrics**: Average sentence length, sentence complexity index

#### 4.2.5 Coherence and Organization (Weight: 15%)
- Logical flow and progression of ideas
- Paragraph structure and organization
- Use of transition words and phrases
- Topic development and consistency
- Introduction and conclusion (for longer texts)
- **Metrics**: Transition word frequency, cohesion markers, paragraph count

#### 4.2.6 Fluency and Naturalness (Weight: 10%)
- Natural phrasing
- Idiomatic expressions (when appropriate)
- Overall readability
- Native-like expression
- Register appropriateness
- **Metrics**: Readability scores (Flesch-Kincaid), perplexity scores

### 4.3 Scoring Methodology

The system can use one of these approaches:

1. **AI/ML-Based Scoring**
   - Leverage NLP models (e.g., GPT, BERT-based models)
   - Train or fine-tune on labeled datasets of English proficiency texts
   - Use ensemble methods combining multiple assessment dimensions

2. **Hybrid Approach** (Recommended)
   - Rule-based checks for grammar, spelling, and mechanics
   - Statistical analysis for vocabulary diversity and complexity
   - ML model for holistic assessment and naturalness
   - Weighted combination of scores from each component

### 4.4 Score Calculation Formula

Each subcategory is scored independently on a 1-10 scale. The overall score is calculated as a weighted average:

```
Overall Score = (Grammar × 0.25) +
                (Vocabulary × 0.20) +
                (Spelling/Mechanics × 0.10) +
                (Sentence Structure × 0.20) +
                (Coherence/Organization × 0.15) +
                (Fluency/Naturalness × 0.10)
```

**Example Calculation:**
```
Grammar:                  8.0
Vocabulary:               7.2
Spelling & Mechanics:     9.0
Sentence Structure:       7.0
Coherence & Organization: 7.3
Fluency & Naturalness:    6.8

Overall = (8.0 × 0.25) + (7.2 × 0.20) + (9.0 × 0.10) + (7.0 × 0.20) + (7.3 × 0.15) + (6.8 × 0.10)
        = 2.00 + 1.44 + 0.90 + 1.40 + 1.10 + 0.68
        = 7.52
        ≈ 7.5 / 10
```

**Output Format:**
- Overall score rounded to 1 decimal place
- Subcategory scores displayed individually (1 decimal place)
- Proficiency level derived from overall score
- Confidence level indicator (high/medium/low based on text length)
- Feedback messages for each subcategory

### 4.5 Confidence Scoring

Score reliability depends on the amount of text submitted. Shorter texts provide less data for accurate assessment.

#### Confidence Levels

| Text Length | Confidence Level | Display to User | Scoring Implications |
|-------------|-----------------|-----------------|---------------------|
| **< 30 words** | Low | ⚠️ "Low confidence - submit more text for accurate scoring" | Some categories may not be assessable (coherence, organization) |
| **30-100 words** | Medium | ⚡ "Medium confidence - longer text recommended" | Basic assessment possible, limited data for advanced features |
| **100-500 words** | High | ✓ "High confidence" | Full assessment of all categories |
| **500+ words** | Very High | ✓✓ "Very high confidence" | Comprehensive assessment with robust data |

#### Implementation Notes
- **Minimum viable text**: At least 1 sentence (5-10 words) accepted, but flagged as low confidence
- **Category-specific requirements**:
  - Coherence & Organization: Requires 50+ words (multiple sentences)
  - Sentence Structure: Requires 3+ sentences
  - All other categories: Can be assessed from single sentences but with caveats
- **User feedback**: Display confidence level prominently with explanation
- **Warning messages**: For low-confidence scores, suggest submitting longer text

### 4.6 Feedback Generation

Feedback is generated for each subcategory based on the score and specific errors/patterns detected. Feedback should be:
- **Actionable**: Provide specific steps for improvement
- **Positive**: Acknowledge strengths and encourage progress
- **Contextual**: Tailored to the score level and detected issues
- **Specific**: Reference actual patterns from the user's text when possible

#### Feedback Generation Architecture

The system uses a **template-based approach with dynamic content insertion**:

```
┌──────────────────────────────────────────────┐
│       Text Analysis & Scoring                │
│  - Run NLP analysis (spaCy, LanguageTool)   │
│  - Extract errors and patterns              │
│  - Calculate subcategory scores             │
└───────────────┬──────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────┐
│       Error Categorization                   │
│  - Group errors by type (grammar, vocab...)  │
│  - Identify top 3 error types per category   │
│  - Count error frequencies                   │
└───────────────┬──────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────┐
│       Template Selection                     │
│  - Choose template based on score range      │
│  - Select specific sub-template for error    │
│    types detected                            │
└───────────────┬──────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────┐
│       Content Personalization                │
│  - Insert specific error examples            │
│  - Add quantitative data (e.g., "5 errors")  │
│  - Include actionable recommendations        │
│  - Link to learning resources (optional)     │
└───────────────┬──────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────┐
│       Feedback Output                        │
│  - 1-3 sentences per subcategory             │
│  - Tone-adjusted for score level             │
│  - Ready for display                         │
└──────────────────────────────────────────────┘
```

#### Feedback Template Structure

**Template Format:**
```
{greeting_based_on_score} {strength_acknowledgment}. {specific_issue_1}. {recommendation_1}. {optional: specific_issue_2}. {optional: recommendation_2}.
```

**Example Templates:**

**Grammar - High Score (8-10):**
```
Template: "Excellent grammar! {strength_detail}. {minor_improvement_area}."
Variables:
  - strength_detail: "Your verb tenses are consistent and accurate."
  - minor_improvement_area: "Watch for occasional article omissions."
```

**Grammar - Medium Score (5-7):**
```
Template: "Good progress with grammar. {identified_error_pattern} ({error_count} instances). {specific_recommendation}."
Variables:
  - identified_error_pattern: "You have some issues with article usage"
  - error_count: "5"
  - specific_recommendation: "Review when to use 'a', 'an', and 'the' before nouns."
```

**Grammar - Low Score (1-4):**
```
Template: "Grammar needs work. Focus on {priority_issue_1} and {priority_issue_2}. Start by {actionable_step}."
Variables:
  - priority_issue_1: "subject-verb agreement"
  - priority_issue_2: "verb tense consistency"
  - actionable_step: "ensuring your subjects and verbs match in number"
```

#### Error Detection to Feedback Mapping

| Category | Error Detection Method | Feedback Source |
|----------|----------------------|-----------------|
| **Grammar** | LanguageTool API, spaCy parser | Error type (e.g., "ARTICLE_MISSING") → template slot |
| **Vocabulary** | Type-token ratio, word frequency lists | Low diversity → "use more varied vocabulary" template |
| **Spelling** | LanguageTool spell check | Error count → severity-based template |
| **Sentence Structure** | spaCy sentence parsing, length analysis | Short avg sentence length → "try complex sentences" |
| **Coherence** | Transition word detection, paragraph count | Few transitions → "add connectors" template |
| **Fluency** | Perplexity score from language model | High perplexity → "rephrase for clarity" |

#### Prioritization for Feedback

For low-scoring texts with many issues, prioritize feedback:
1. **Top 2-3 error types** per category (not all errors)
2. **High-impact improvements** (grammar > spelling for comprehension)
3. **Learner level appropriate** (beginners: basics; advanced: nuance)

**Example - Overload Avoidance:**
```
Instead of: "You have article errors, subject-verb errors, tense errors, pronoun errors,
and preposition errors."

Use: "Focus on article usage (5 instances) and subject-verb agreement (3 instances).
Master these first, then move to other areas."
```

#### Feedback Structure by Score Range

| Score Range | Feedback Tone | Example Approach |
|-------------|---------------|------------------|
| **8-10** | Positive reinforcement | "Excellent [category]! Keep up the great work." |
| **5-7** | Encouraging with suggestions | "Good [category]. To improve, consider [specific action]." |
| **1-4** | Supportive with clear guidance | "[Category] needs work. Focus on [specific area]. Start by [action]." |

#### Category-Specific Feedback Examples

**Grammar (Score: 6.5)**
```
"Good grammar overall. You have some issues with article usage (a/an/the).
Review the rules for definite and indefinite articles."
```

**Vocabulary (Score: 7.2)**
```
"Good vocabulary range. Try incorporating more advanced or academic vocabulary
to reach the next level. Consider using synonyms to avoid repetition."
```

**Spelling & Mechanics (Score: 9.0)**
```
"Excellent spelling and punctuation! Your attention to mechanics is strong.
Keep maintaining this high standard."
```

**Sentence Structure (Score: 5.8)**
```
"Your sentence structure is developing. Add more variety by using complex
sentences with subordinate clauses. Try combining short sentences."
```

**Coherence & Organization (Score: 7.3)**
```
"Good organization overall. Your ideas flow logically. Use more transition words
like 'however', 'furthermore', and 'in addition' to connect your ideas more smoothly."
```

**Fluency & Naturalness (Score: 6.0)**
```
"Your writing is understandable but could flow more naturally. Work on using
more idiomatic expressions and transition words between ideas."
```

---

## 5. Technical Architecture

### 5.1 System Components (Web Application Architecture)

```
┌─────────────────────────────────────────────────┐
│             Frontend (Web Browser)               │
│  - Text input interface                         │
│  - Score visualization (charts, progress bars)  │
│  - Feedback display                             │
│  - User interaction handling                    │
└───────────────────┬─────────────────────────────┘
                    │ HTTP/HTTPS (REST API)
                    ▼
┌─────────────────────────────────────────────────┐
│              Backend API Server                  │
│  - Request handling (POST /score)               │
│  - Input validation                             │
│  - Text preprocessing                           │
│  - Response formatting (JSON)                   │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│              Scoring Engine                      │
│  ┌──────────────┐  ┌──────────────┐            │
│  │   Grammar    │  │  Vocabulary  │            │
│  │   Analyzer   │  │   Analyzer   │            │
│  └──────────────┘  └──────────────┘            │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  Spelling/   │  │   Sentence   │            │
│  │  Mechanics   │  │   Structure  │            │
│  └──────────────┘  └──────────────┘            │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  Coherence/  │  │   Fluency/   │            │
│  │Organization  │  │ Naturalness  │            │
│  └──────────────┘  └──────────────┘            │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│      Score Aggregation & Feedback Generation    │
│  - Calculate individual subcategory scores      │
│  - Apply weights to component scores            │
│  - Calculate overall score (1-10)               │
│  - Generate category-specific feedback          │
│  - Format JSON response with all data           │
└─────────────────────────────────────────────────┘
```

### 5.2 Technology Stack (Web Application)

#### Frontend (Client-Side)
**Core Framework Options:**
- **React**: Component-based, excellent ecosystem for data visualization
- **Vue.js**: Progressive framework, easy to learn
- **Vanilla JavaScript**: Lightweight, no framework overhead

**Visualization Libraries:**
- **Chart.js**: Simple, flexible charts for score visualization
- **D3.js**: Advanced data visualization capabilities
- **Recharts**: React-based charting library
- **CSS/HTML5**: Custom progress bars and indicators

**UI Framework:**
- **Tailwind CSS**: Utility-first styling
- **Bootstrap**: Responsive design components
- **Material-UI**: Modern component library

#### Backend (Server-Side)
**API Framework:**
- **Python + Flask/FastAPI**: Recommended for NLP integration
  - Flask: Lightweight, simple REST API
  - FastAPI: Modern, fast, automatic API documentation
- **Python + Django**: Full-featured if database needed
- **Node.js + Express**: Alternative if using JavaScript throughout

**NLP Libraries & Tools:**
- **spaCy**: Grammar and syntax analysis
- **NLTK**: Text processing and linguistic analysis
- **LanguageTool**: Grammar and spelling checking (Python API)
- **Transformers (Hugging Face)**: Pre-trained language models for fluency assessment
- **TextStat**: Readability and complexity metrics
- **language-tool-python**: Python wrapper for LanguageTool

#### Deployment
- **Frontend Hosting**: Vercel, Netlify, GitHub Pages
- **Backend Hosting**: Heroku, AWS, Google Cloud, DigitalOcean
- **Containerization**: Docker for consistent deployment

#### Database (Optional for MVP)
- **SQLite**: Simple file-based storage for caching
- **PostgreSQL**: If tracking user history/progress
- Store scoring results for analysis
- Cache common text patterns

#### Internationalization (i18n)

**Rationale:** Target users are non-native English speakers who may prefer UI instructions in their native language, even though they're learning English.

**Implementation Strategy:**

**Phase 1 (MVP):**
- **English UI only**: Keep scope manageable for initial launch
- **Clear, simple English**: Use elementary vocabulary in instructions
- **Visual cues**: Icons and progress bars reduce language dependency

**Phase 2 (Post-MVP):**
- **Multi-language UI support** for:
  - Spanish (large ESL population)
  - Mandarin Chinese (major learning demographic)
  - Arabic (widely spoken, RTL consideration)
  - Portuguese, French, Japanese (secondary priorities)

**What to Translate:**
- ✅ UI labels and buttons ("Score My English", "Submit", "Results")
- ✅ Instructions and help text
- ✅ Feedback message templates
- ✅ Error messages
- ❌ Technical terms (e.g., "Grammar", "Vocabulary" - keep in English or provide glossary)
- ❌ User's submitted text (always in English)

**Technical Approach:**
- **Frontend**: React i18n library (react-i18next) or Vue I18n
- **Backend**: Python gettext or Flask-Babel for API responses
- **Translation files**: JSON format for easy management
  ```json
  {
    "en": {
      "submit_button": "Score My English",
      "word_count": "Word count"
    },
    "es": {
      "submit_button": "Calificar mi inglés",
      "word_count": "Contador de palabras"
    }
  }
  ```

**Language Selector:**
- Dropdown in header/footer
- Browser language auto-detection
- Remember user preference (cookie/localStorage)

**Considerations:**
- **RTL Support**: Arabic requires right-to-left layout
- **Character Encoding**: UTF-8 for all languages
- **Text Length Variations**: Button labels may be longer in some languages (German, Portuguese)
- **Cultural Sensitivity**: Feedback tone and examples appropriate for culture

### 5.3 API Specification

#### Endpoint: Score Text

**Request:**
```
POST /api/score
Content-Type: application/json

{
  "text": "The text to be scored goes here. It can be up to 2000 words."
}
```

**Validation:**
- Minimum: 1 sentence (approximately 5-10 words)
- Maximum: 2000 words
- Text must not be empty

**Response (Success):**
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": {
    "overall_score": 7.5,
    "proficiency_level": "Upper-Intermediate",
    "subcategory_scores": {
      "grammar": 8.0,
      "vocabulary": 7.2,
      "spelling_mechanics": 9.0,
      "sentence_structure": 7.0,
      "coherence_organization": 7.3,
      "fluency_naturalness": 6.8
    },
    "feedback": {
      "grammar": "Good subject-verb agreement. Consider reviewing article usage.",
      "vocabulary": "Good range. Try incorporating more advanced vocabulary.",
      "spelling_mechanics": "Excellent spelling and punctuation.",
      "sentence_structure": "Good variety. Add more complex sentences.",
      "coherence_organization": "Clear organization. Use more transition words to connect ideas.",
      "fluency_naturalness": "Work on idiomatic expressions for more natural flow."
    },
    "confidence_level": "high",
    "word_count": 145
  }
}
```

**Response (Error - Invalid Input):**
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Text must be between 1 sentence and 2000 words"
  }
}
```

**Response (Error - Server Error):**
```
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "success": false,
  "error": {
    "code": "PROCESSING_ERROR",
    "message": "An error occurred while scoring the text"
  }
}
```

### 5.4 Operational Cost Analysis

Understanding the costs of running the English Scorer service is critical for sustainability.

#### Cost Components

**1. Hosting & Infrastructure**

| Service | Provider | MVP Cost (Monthly) | Scale Cost (1000 users/day) |
|---------|----------|-------------------|------------------------------|
| **Frontend** | Vercel/Netlify Free Tier | $0 | $0-20 |
| **Backend Server** | Heroku Hobby ($7) or AWS EC2 t3.small | $7-20 | $50-100 |
| **Database** | PostgreSQL (managed) | $0 (not needed for MVP) | $15-25 |
| **CDN** | Cloudflare Free Tier | $0 | $0-20 |
| **Total Infrastructure** | | **$7-20/month** | **$65-165/month** |

**2. Compute Costs (Processing)**

Assuming self-hosted NLP models (spaCy, LanguageTool):
- **CPU usage**: 2-5 seconds per 500-word text
- **Memory**: 2-4 GB RAM for loaded models
- **Scale**: $0.10-0.20 per 1000 requests (on AWS/GCP)

**3. Third-Party APIs** (if used)

| Service | Use Case | Cost | Notes |
|---------|----------|------|-------|
| **OpenAI GPT** | Fluency assessment | $0.002 per request (500 tokens) | ~$2 per 1000 texts |
| **LanguageTool API** | Grammar checking | $20/month for 100K requests | Free tier available |
| **Google Cloud NLP** | Alternative analysis | $1 per 1000 texts | Overkill for this use case |

**Recommendation for MVP:** Use free, open-source tools only (spaCy, NLTK, local LanguageTool) to avoid API costs.

**Premium Feature Costs (Post-MVP):**

When implementing premium tier AI features:

| Feature | Service | Cost per Use | Monthly Cap | Max Cost per Premium User |
|---------|---------|--------------|-------------|---------------------------|
| **AI-improved text comparison** | OpenAI GPT-4 | $0.02 per text | 20 uses/month | $0.40/month |
| **Click-to-fix suggestions** | Rule-based (free) | $0 | Unlimited | $0 |
| **PDF export** | Library-based | $0.001 per export | Unlimited | Negligible |
| **Progress tracking** | Database storage | $0.01/month | Unlimited | $0.01/month |
| **Weekly emails** | SendGrid/Mailgun | $0.001 per email | 4-5/month | $0.005/month |

**Total Premium Feature Cost:** ~$0.42 per premium user per month

**Revenue Analysis:**
- Premium price: $4.99/month
- Feature costs: $0.42/month
- Infrastructure share: $0.15/month (assuming 100 premium users)
- **Net revenue: $4.42/month per premium user**
- **Margin: 89%** ✅ Sustainable

**Why the 20 AI comparisons/month cap?**
- Prevents abuse: Power user making 100 AI requests = $2/month cost vs $4.99 revenue
- 20 uses = 0.66 per day, sufficient for serious learners
- Additional AI comparisons available as add-on: $2.99/month for 50 more

**Alternative Pricing Models:**
- **Option A (Current)**: $4.99/month with 20 AI uses - **Recommended**
- **Option B**: $9.99/month with unlimited AI uses - Higher revenue but may reduce conversions
- **Option C**: $3.99/month base + $0.10 per AI comparison - Pay-per-use complexity

**4. Storage Costs** (if implementing user accounts)

| Data Type | Size per User | Cost (S3/GCS) | Notes |
|-----------|--------------|---------------|-------|
| User submissions | 10KB avg × 10 submissions | Negligible | Delete after 30 days |
| Score history | 500 bytes × 100 scores | Negligible | |
| **Estimated** | ~100KB per active user | **$0.001/user/month** | Minimal impact |

**5. Bandwidth**

- **Request size**: ~10KB (text submission)
- **Response size**: ~2KB (JSON with scores/feedback)
- **Bandwidth cost**: ~$0.01 per 1000 requests
- **Scale**: Negligible until 100K+ requests/month

#### Total Cost Estimates

**MVP (50 users/day = 1,500 requests/month):**
```
Frontend hosting:        $0
Backend hosting:         $7-20
Compute (self-hosted):   Included in hosting
APIs:                    $0 (using open-source)
Total:                   $7-20/month
```

**Medium Scale (1,000 users/day = 30,000 requests/month):**
```
Frontend:                $0-20
Backend:                 $50-100
Compute:                 $3-6
APIs (optional):         $0-60 (if using OpenAI)
Database:                $15-25
Total:                   $68-211/month
```

**Large Scale (10,000 users/day = 300,000 requests/month):**
```
Frontend:                $20-50
Backend (load balanced): $200-400
Compute:                 $30-60
APIs:                    $0-600 (if using external)
Database:                $50-100
Monitoring/Logs:         $20-50
Total:                   $320-1,260/month
```

#### Cost Optimization Strategies

1. **Use Open-Source Models**: Avoid API costs by hosting spaCy, NLTK, LanguageTool
2. **Caching**: Cache results for identical text (unlikely but possible for test cases)
3. **Bot Detection & Rate Limits**: Prevent automated abuse through 50/day soft limits + CAPTCHA
4. **Auto-scaling with Caps**: Scale down during low-traffic periods, scale up during high demand
   - Set maximum instance count to prevent runaway costs
   - Configure auto-scaling to max 5 backend instances (prevents >$500/month spike)
5. **Efficient Processing**: Optimize NLP pipelines to reduce CPU time per request
6. **Cost Circuit Breakers**: Automatic protections against unexpected spending

**Cost Circuit Breakers & Alerts:**

| Threshold | Alert Level | Action | Notification |
|-----------|-------------|--------|--------------|
| **$50/day** | Info | Log and monitor | Email to admin |
| **$100/day** | Warning | Increase CAPTCHA frequency | Email + Slack alert |
| **$150/day** | Critical | Enable stricter rate limits (25/day) | SMS + Email + Slack |
| **$200/day** | Emergency | Activate emergency mode (CAPTCHA for new users only) | Phone call + all channels |
| **$300/day** | Shutdown | Temporary maintenance mode (1 hour cooldown) | All channels + status page |

**Emergency Mode Details:**
- Triggered if daily costs exceed $200 (>13x normal MVP budget)
- **Targets new users only** to preserve UX during viral growth:
  - **New free tier users** (sessions started after emergency mode activated) must complete CAPTCHA before their first submission
  - **Existing active sessions** (started before emergency mode) continue normally for fairness
  - **Premium users** continue normally (they're revenue generating)
- Prevents cost spiral while avoiding punishing legitimate users already using the service
- Auto-disables after costs drop below $100/day for 2 hours
- Manual override available via admin dashboard

**Why target new users only?**
- Viral traffic surge = many new users discover tool simultaneously
- Existing users already verified as legitimate (have been using service)
- New users during cost spike are statistically more likely to be part of abuse pattern
- Better UX: Don't interrupt active learning sessions with CAPTCHA mid-flow

**Cost Monitoring Tools:**
- AWS Cost Explorer with daily budget alerts
- Custom CloudWatch metrics for request volume
- Datadog cost tracking dashboard
- PagerDuty integration for critical alerts

#### Revenue Considerations

To make the service sustainable:
- **Free Tier**: 50 submissions per day with optional non-intrusive ads
  - Covers 95% of legitimate users (most users submit 5-20 times/day)
  - Prevents cost catastrophe from abuse (single user can't generate excessive costs)
  - Ads displayed in sidebar or footer only (never blocking content)
  - No delays or forced ad viewing
  - Scoring happens immediately without ad-related waiting
  - **Soft limit behavior**:
    - **Submissions 1-40**: Normal operation, no warnings
    - **Submissions 41-50**: Show friendly banner: "You've used 41/50 free submissions today. Upgrade to Premium for unlimited scoring!"
    - **Submissions 51+**: Require CAPTCHA verification for each additional submission + upgrade prompt
    - Daily limit resets at **midnight UTC**
    - Counter tracked via session cookie (expires at midnight UTC) + server-side validation
- **Premium Tier**: $4.99/month for unlimited submissions + advanced features
  - Ad-free experience
  - Unlimited text submissions (no daily limit)
  - Detailed error highlighting with click-to-fix suggestions
  - AI-improved text comparison (side-by-side with enhanced version) - **20 uses per month**
  - Weekly progress reports via email
  - Priority processing (skip queue during high traffic)
  - Export to PDF with detailed analysis
  - Progress tracking over time with charts
- **Educational Institutions**: $99/month for 100 students with teacher dashboard
- **API Access**: $0.01 per request for developers (separate rate limits apply)

**Ad Implementation Guidelines:**
- ✅ Static banner ads in sidebar
- ✅ Small text ads in footer
- ✅ Ads load asynchronously (don't block scoring)
- ❌ NO pop-ups or interstitials
- ❌ NO video ads with sound
- ❌ NO ads that delay results or require clicking
- ❌ NO ads in the scoring input or results area

#### Cost per User (Break-even Analysis)

With 1,000 daily active users and $150/month costs:
- **Cost per user**: $0.005 per submission
- **Break-even**: Need 15% conversion to $4.99/month premium (~150 paying users)
- **Alternative**: Ads could generate $1-3 CPM ($30-90/month for 30K page views)

### 5.5 Error Handling & Fallback Strategies

Robust error handling ensures the system remains functional even when components fail.

#### 5.5.1 Input Validation Errors

| Error Type | Detection | User Response | HTTP Code |
|------------|-----------|---------------|-----------|
| **Empty text** | Length = 0 | "Please enter text to score" | 400 |
| **Too short** | < 5 words | "Please enter at least one complete sentence" | 400 |
| **Too long** | > 2000 words | "Text exceeds 2000 word limit. Please shorten." | 400 |
| **Non-English** | Language detection ≠ EN | "Only English text can be scored" | 400 |
| **Invalid characters** | Control characters, excessive symbols | "Text contains invalid characters" | 400 |

**Implementation:**
```python
def validate_input(text):
    if not text or len(text.strip()) == 0:
        raise ValidationError("EMPTY_TEXT", "Please enter text to score")

    word_count = len(text.split())
    if word_count < 5:
        raise ValidationError("TOO_SHORT", "Please enter at least one complete sentence")

    if word_count > 2000:
        raise ValidationError("TOO_LONG", f"Text exceeds 2000 word limit ({word_count} words)")

    detected_language = detect_language(text)
    if detected_language != 'en':
        raise ValidationError("NON_ENGLISH", "Only English text can be scored")

    return True
```

#### 5.5.2 NLP Model Failures

**Scenario:** spaCy, LanguageTool, or ML model fails to process text

**Fallback Strategy:**

1. **Graceful Degradation:**
   - If Grammar analyzer fails → Use only spell checker for grammar score (lower confidence)
   - If Vocabulary analyzer fails → Use basic word count metrics as fallback
   - If Coherence analyzer fails → Assign neutral score (5.0) with disclaimer

2. **Partial Results:**
   ```json
   {
     "overall_score": 6.5,
     "confidence_level": "medium",
     "subcategory_scores": {
       "grammar": 7.0,
       "vocabulary": "N/A",
       "spelling_mechanics": 8.5,
       ...
     },
     "warnings": [
       "Vocabulary analysis temporarily unavailable. Score calculated from other categories."
     ]
   }
   ```

3. **Error Logging:**
   - Log all model failures with stack traces
   - Alert development team for repeated failures
   - Track which models fail most often

#### 5.5.3 Timeout Handling

**Problem:** Processing takes > 10 seconds (max allowed)

**Solution:**
- Set per-analyzer timeout (2 seconds each)
- If timeout occurs:
  1. Cancel analysis for that component
  2. Use fallback scoring (conservative estimate)
  3. Return response with warning

**Implementation:**
```python
import timeout_decorator

@timeout_decorator.timeout(2)
def analyze_grammar(text):
    # Grammar analysis logic
    pass

try:
    grammar_score = analyze_grammar(text)
except timeout_decorator.TimeoutError:
    grammar_score = 5.0  # Conservative fallback
    warnings.append("Grammar analysis timed out. Using estimated score.")
```

#### 5.5.4 Bot Detection & Abuse Prevention

**Scenario:** Automated bot or suspicious activity detected

**Detection Methods (Privacy-Preserving):**
- **Request timing patterns**: Multiple submissions in rapid succession (< 1 second apart)
- **Duplicate content detection**: Identical text submitted repeatedly within short timeframe
- **Honeypot fields**: Hidden form fields that bots fill but humans don't see (standard anti-bot technique)
- **Basic user agent validation**: Detect obviously fake or missing user agents (not for tracking, just bot detection)
- **JavaScript challenge**: Simple client-side checks that headless bots often fail
- **Session-only analysis**: All detection data discarded after verification, no persistent tracking

**Response:**
```json
HTTP 429 Too Many Requests
{
  "success": false,
  "error": {
    "code": "SUSPICIOUS_ACTIVITY_DETECTED",
    "message": "We've detected unusual activity. Please complete the verification.",
    "verification_required": true
  }
}
```

**User-Friendly Display:**
```
🛡️ Security Check Required

To ensure you're not a robot, please complete this quick verification.

[Complete CAPTCHA] [I'm a human]
```

**After Verification:**
- Legitimate users can continue up to daily limit (50/day free tier)
- Premium users have no limits after passing verification

**Session Data Retention Details:**

To enable bot detection while preserving privacy, minimal session data is collected:

| Data Type | Purpose | Storage Method | Retention Period | Cross-Session? |
|-----------|---------|----------------|------------------|----------------|
| **Submission Count** | Track daily limit (50/day) | Session cookie + server memory | Until midnight UTC | No - resets daily |
| **Request Timestamps** | Detect rapid-fire patterns | Server memory only | 60 seconds | No |
| **Text Hash** | Detect duplicate submissions | Salted SHA-256 hash in memory | 60 seconds | No |
| **CAPTCHA Status** | Whether user passed verification | Session cookie | Until session ends | No |
| **Session ID** | Link requests within session | HTTP-only cookie | Until browser close | No |

**Implementation Notes:**
- Text is hashed before storage using **salted SHA-256** - original text never stored
- **Salt generation**: Random 32-byte salt generated every 60 seconds
- **Hash computation**: `SHA256(salt + text)` - stored in memory
- **Salt destruction**: Salt and all hashes destroyed after 60 seconds, new salt generated
- Submission count cookie expires at midnight UTC daily
- No database storage of any detection data
- No user accounts required for free tier, so no cross-session linking possible

**Privacy Guarantee:**
Even if server is compromised, only anonymized session data (counts, timestamps, salted hashes) for the last 60 seconds would be accessible. **The salted hashes cannot be used to confirm suspected text content** because the salt is unknown and destroyed after 60 seconds. No user text, IP addresses, or persistent identifiers are stored.

**Why Salted Hashes?**
- Unsalted SHA-256 hashes allow "confirmation attacks" - attacker with candidate texts can compute hashes and verify if specific text was submitted
- Salted hashes prevent this: attacker cannot compute correct hash without knowing the salt
- Salt rotation every 60 seconds means even if salt is leaked, exposure window is minimal

#### 5.5.5 Server Overload

**Scenario:** Too many concurrent requests, server at capacity

**Strategies:**

1. **Queue System:**
   - Add requests to queue if server busy
   - Display: "Your request is being processed... Position in queue: 5"
   - Process when resources available

2. **Auto-scaling:**
   - Spin up additional backend instances when load exceeds threshold
   - AWS Auto Scaling or similar

3. **Graceful Rejection:**
   ```json
   HTTP 503 Service Unavailable
   {
     "error": {
       "code": "SERVER_OVERLOADED",
       "message": "Our servers are experiencing high traffic. Please try again in a moment.",
       "retry_after": 60
     }
   }
   ```

#### 5.5.6 Language Detection False Positives

**Problem:** Text is English but detected as another language (or vice versa)

**Solution:**
- Use confidence threshold (e.g., must be >70% confident it's NOT English to reject)
- Allow user to override: "This is English" button
- Analyze anyway but show warning:

```
⚠️ Your text may not be in English. Scores may be inaccurate.
[Score Anyway] [Cancel]
```

#### 5.5.7 Third-Party Service Failures

**If using external APIs** (e.g., OpenAI for fluency):

| Service | Failure Mode | Fallback |
|---------|--------------|----------|
| **OpenAI API** | Down/timeout | Use local perplexity model (lower quality but functional) |
| **LanguageTool API** | Rate limit hit | Use local LanguageTool instance |
| **Any external service** | Complete failure | Disable that feature, inform user, continue with other analysis |

**Circuit Breaker Pattern:**
- If external API fails 5 times in a row, stop calling it for 5 minutes
- Prevents cascading failures and wasted time

#### 5.5.8 Data Corruption

**Scenario:** Text preprocessing corrupts input (encoding issues, etc.)

**Detection:**
```python
original_word_count = len(text.split())
processed_word_count = len(processed_text.split())

if abs(original_word_count - processed_word_count) > 5:
    logger.error("Text preprocessing may have corrupted input")
    # Use original text as fallback
```

#### 5.5.9 User Experience for Errors

**Principles:**
1. **Never show technical errors to users** (stack traces, "NoneType has no attribute...")
2. **Always explain what went wrong** in plain language
3. **Suggest next steps** ("Try submitting again" / "Shorten your text" / "Contact support")
4. **Provide fallback value** whenever possible (partial results > no results)

**Error Message Template:**
```
😕 Something Went Wrong

[Clear explanation of what happened]

What you can do:
• [Action 1]
• [Action 2]

[Primary Action Button] [Secondary Action]
```

---

## 6. User Interface Design

### 6.1 Web Page Layout Structure

```
┌──────────────────────────────────────────────────────────────┐
│                      English Scorer                          │
│              Improve Your English Writing                    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  INPUT SECTION                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │  Paste or type your text here...                       │ │
│  │                                                         │ │
│  │                                                         │ │
│  │                                                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Word count: 0 / 2000                [Score My English]     │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  RESULTS SECTION                                             │
│                                                              │
│  ┌─────────────────────────────────────┐                    │
│  │      Overall Score                  │                    │
│  │                                     │                    │
│  │          7.5 / 10                   │                    │
│  │                                     │                    │
│  │   ● Upper-Intermediate              │                    │
│  └─────────────────────────────────────┘                    │
│                                                              │
│  SCORE BREAKDOWN & VISUALIZATION                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Grammar                           8.0 / 10            │ │
│  │  ████████████████████░░░░░░░░                          │ │
│  │                                                         │ │
│  │  Vocabulary                        7.2 / 10            │ │
│  │  ██████████████░░░░░░░░░░                              │ │
│  │                                                         │ │
│  │  Spelling & Mechanics              9.0 / 10            │ │
│  │  ██████████████████████░░                              │ │
│  │                                                         │ │
│  │  Sentence Structure                7.0 / 10            │ │
│  │  ██████████████░░░░░░░░░░                              │ │
│  │                                                         │ │
│  │  Coherence & Organization          7.3 / 10            │ │
│  │  ██████████████░░░░░░░░░░                              │ │
│  │                                                         │ │
│  │  Fluency & Naturalness             6.8 / 10            │ │
│  │  █████████████░░░░░░░░░░░                              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  FEEDBACK & RECOMMENDATIONS                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  ✓ Grammar: Good subject-verb agreement. Consider      │ │
│  │    reviewing article usage (a/an/the).                 │ │
│  │                                                         │ │
│  │  ↑ Vocabulary: Good range. Try incorporating more      │ │
│  │    advanced vocabulary to reach the next level.        │ │
│  │                                                         │ │
│  │  ★ Spelling & Mechanics: Excellent spelling and        │ │
│  │    punctuation. Keep up the great work!                │ │
│  │                                                         │ │
│  │  ↑ Sentence Structure: Good variety. Add more complex  │ │
│  │    sentences to improve flow.                          │ │
│  │                                                         │ │
│  │  ✓ Coherence & Organization: Clear organization. Use   │ │
│  │    more transitions to connect ideas.                  │ │
│  │                                                         │ │
│  │  ↑ Fluency & Naturalness: Work on idiomatic            │ │
│  │    expressions for more natural flow.                  │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### 6.2 User Flow

1. User navigates to the web application
2. User enters or pastes text into the input text area
3. System shows real-time word count (X / 2000 words)
4. User clicks "Score My English" button
5. System validates input (minimum 1 sentence, maximum 2000 words)
6. System displays loading indicator while processing
7. System scrolls to results section and displays:
   - Overall score (1-10) with large, prominent visualization
   - Proficiency level label (Beginner to Advanced)
   - Visual breakdown of 6 subcategory scores with progress bars
   - Color-coded indicators (red/yellow/green based on score ranges)
   - Actionable feedback for each subcategory
8. User reviews feedback and recommendations
9. User can modify text and re-submit for updated scoring

### 6.3 Demo Mode & Example Submissions

**Purpose:** Help new users understand what to submit and what results look like without requiring them to write text first.

#### "Try an Example" Feature

**Location:** Above or beside the text input area

**UI Implementation:**
```
┌──────────────────────────────────────────────────┐
│  Don't know what to write?                       │
│                                                   │
│  [Try Example: Beginner]  [Intermediate]  [Advanced]│
└──────────────────────────────────────────────────┘
```

**Example Texts:**

**Beginner Level (Expected score: 3-4):**
```
I like to learn english. It is very important for me. I study every day.
I want to be good at english because it help me in my job. Sometimes is
difficult but I try hard.
```

**Intermediate Level (Expected score: 5-6):**
```
Learning English has been a challenging but rewarding experience for me.
I started studying three years ago, and I can now communicate with people
from different countries. My vocabulary has improved significantly, although
I still make mistakes with grammar sometimes. I practice by reading articles
and watching movies in English.
```

**Advanced Level (Expected score: 8-9):**
```
Mastering a foreign language requires dedication, consistency, and a genuine
interest in the culture it represents. Throughout my journey learning English,
I've discovered that immersion through authentic materials—such as podcasts,
literature, and academic journals—accelerates progress far more effectively
than rote memorization. While grammatical accuracy remains important, developing
fluency and the ability to express nuanced ideas should be the ultimate goal
for any language learner.
```

#### Implementation Features

1. **Pre-fill Button**: Click example button → text area populates → user clicks "Score"
2. **Sample Results**: Optionally, show cached results immediately without API call
3. **Educational Labels**: "This is what beginner-level writing looks like"
4. **Edit Capability**: Users can modify example text before submitting
5. **Clear Button**: Easy way to clear example and start fresh

#### Instructional Content

**"How to Use" Section (Collapsible):**
```
📝 What should I submit?
✓ Essays, paragraphs, or short stories
✓ Emails or formal letters
✓ Any original English text you've written

✗ Avoid submitting:
✗ Single sentences (submit at least 3-5 sentences)
✗ Poetry or lyrics (scoring isn't designed for creative formats)
✗ Code, lists, or bullet points
✗ AI-generated text (you won't learn from it!)
```

**Tips for Better Results:**
- Submit at least 100 words for accurate scoring
- Write naturally—don't try to "game" the system
- Focus on clear communication, not fancy vocabulary
- Review feedback carefully and apply suggestions

#### First-Time User Experience

**Welcome Modal (optional, dismissible):**
```
┌─────────────────────────────────────────────┐
│  Welcome to English Scorer! 👋              │
│                                             │
│  We help you improve your English writing  │
│  by scoring your text across 6 categories. │
│                                             │
│  [Try an Example]  [Start Writing]         │
│                                             │
│  [x] Don't show this again                 │
└─────────────────────────────────────────────┘
```

### 6.4 UI Elements

#### Input Section
- **Text Input Area**: Large, scrollable textarea (min-height: 200px)
- **Word Counter**: Dynamic counter showing "X / 2000 words" with color change when approaching limit
- **Submit Button**: Prominent "Score My English" call-to-action button
- **Loading Indicator**: Spinner/progress bar while processing

#### Results Section
- **Overall Score Display**: Large, prominent numerical score with circular progress indicator or large text
- **Proficiency Label**: Badge/chip showing level (Beginner, Elementary, Intermediate, Upper-Intermediate, Advanced)

#### Score Visualization Panel
- **Subcategory Progress Bars**: Horizontal bars for each category showing score out of 10
  - Grammar (color-coded)
  - Vocabulary (color-coded)
  - Spelling & Mechanics (color-coded)
  - Sentence Structure (color-coded)
  - Coherence & Organization (color-coded)
  - Fluency & Naturalness (color-coded)
- **Color Coding**:
  - Red (1-4): Needs improvement
  - Yellow/Orange (5-7): Good progress
  - Green (8-10): Excellent
- **Score Numbers**: Display numerical value alongside each bar

#### Feedback Panel
- **Category-Specific Feedback**: Text blocks for each subcategory with:
  - Icon indicating status (✓ checkmark, ↑ arrow for improvement, ★ star for excellence)
  - Specific, actionable recommendations
  - Positive reinforcement for strong areas

#### Additional Elements
- **Error Messages**: Clear validation feedback for invalid input
- **Try Again/Reset Button**: Option to clear input and start over
- **Responsive Design**: Mobile-friendly layout

### 6.4 Visualization Design Principles

#### Visual Hierarchy
1. **Overall Score**: Largest and most prominent element
2. **Subcategory Scores**: Secondary focus with clear visual indicators
3. **Feedback Text**: Supporting detail, easy to scan

#### Color Psychology
- **Green (8-10)**: Success, excellence, positive reinforcement
- **Yellow/Orange (5-7)**: Progress, room for improvement, encouraging
- **Red (1-4)**: Attention needed, areas requiring focus
- Use color consistently across all visual elements

#### Accessibility
- Ensure sufficient color contrast (WCAG AA standards)
- Don't rely solely on color (use icons and text labels)
- Support keyboard navigation
- Provide alt text for visual elements
- Readable font sizes (minimum 14px for body text)

#### User Experience Principles
- **Immediate Understanding**: Users should grasp their score at a glance
- **Progressive Disclosure**: Overall score first, then details
- **Visual Consistency**: Same design patterns throughout
- **Smooth Animations**: Subtle transitions when scores appear
- **Mobile-First**: Design for mobile, enhance for desktop

#### Example Visualization Approaches

**Option 1: Progress Bars**
```
Grammar              [████████████░░░] 8.0/10
Vocabulary           [██████████░░░░░] 7.2/10
```

**Option 2: Circular Indicators**
```
   8.0        7.2        9.0
  ⬤○○○      ⬤○○○      ⬤○○○
Grammar   Vocab    Spelling
```

**Option 3: Bar Chart**
```
10 |              ▆
 9 |              █
 8 | ▆            █
 7 | █  ▆         █  ▆  ▆
 6 | █  █         █  █  █
   +---------------------------
     G  V  S/M    SS F/N
```

---

## 7. Non-Functional Requirements

### 7.1 Performance

**MVP Targets:**
- **Response Time**: < 10 seconds for 95% of requests
- **Concurrent Users**: Support at least 50 simultaneous users
- **Availability**: 95% uptime

**Production Targets:**
- **Response Time**: < 5 seconds for 95% of requests
- **Concurrent Users**: Support 100+ simultaneous users
- **Availability**: 99% uptime for production deployment

### 7.2 Usability

- **Learning Curve**: Users should be able to use the tool without instructions
- **Accessibility**: Support for screen readers and keyboard navigation
- **Multi-platform**: Work on desktop and mobile browsers

### 7.3 Security & Privacy

#### 7.3.1 Data Privacy & Handling

**Data Collection:**
- **Submitted Text**: Temporarily stored in memory during processing only
- **Scores & Feedback**: Generated on-the-fly, not persisted by default
- **No User Accounts (MVP)**: No personal information collected
- **Optional Analytics**: Anonymous usage metrics (page visits, API calls) - no text content

**Data Retention:**
- **Default**: Zero retention - text and scores discarded after response sent
- **Optional Caching**: If implemented for performance, cached for maximum 5 minutes
- **Logs**: Error logs kept for 30 days (sanitized, no user text included)

**User Rights:**
- **No Data to Delete**: Since nothing is stored, no deletion requests needed (MVP)
- **Transparency**: Clear notice on homepage: "Your text is not saved or shared"
- **Future (with accounts)**: Full GDPR compliance - data export, deletion, access rights

#### 7.3.2 Privacy Policy Summary

**What we collect:**
- Text you submit for scoring (temporarily, during processing only)
- Anonymous usage statistics (optional)

**What we DON'T collect:**
- Personal identification (name, email, IP address) - MVP only
- User text content (not stored beyond processing)
- Browsing history or cookies (except essential session cookies)
- User fingerprints or persistent tracking identifiers
- Cross-session behavioral data

**Bot Detection (Privacy-Preserving):**
- Bot detection is performed using session-only data
- No persistent identifiers created
- Detection data discarded immediately after verification
- Used solely for security, never for tracking or analytics

**How text is processed:**
1. User submits text via web form
2. Text sent to backend API over HTTPS
3. NLP analysis performed in-memory
4. Scores and feedback generated
5. Results returned to browser
6. Text and results discarded from server memory

**Third-party services:**
- **None for MVP**: All processing done on our servers
- **Future**: If using cloud NLP APIs (OpenAI, Google Cloud), must comply with their privacy policies

#### 7.3.3 Content Moderation

**Inappropriate Content Handling:**
- **Profanity Filter**: Detect and flag offensive language
- **PII Detection**: Warn users if text contains emails, phone numbers, addresses
- **Policy**: System will score all English text but may display warning for:
  - Hate speech or discriminatory language
  - Personally identifiable information (PII)
  - Extremely violent or graphic content

**Implementation:**
```
if (contains_pii(text)):
    display_warning("Your text may contain personal information. Consider removing it.")

if (contains_profanity(text)):
    display_warning("Profanity detected. Consider more professional language for accurate scoring.")

# Still process and score, but inform user
```

**User Guidelines (displayed on site):**
- Do not submit copyrighted material you don't own
- Do not include personal information (names, addresses, emails)
- Keep content appropriate for educational use
- Text should be original (not AI-generated for evaluation purposes)

#### 7.3.4 Security Measures

- **HTTPS Only**: All traffic encrypted with TLS
- **Input Sanitization**: Prevent XSS, SQL injection, command injection
  - Strip HTML tags from user input
  - Validate text length limits
  - Escape special characters before processing
- **Abuse Prevention** (Privacy-Preserving):
  - **Soft Rate Limits**: 50 submissions/day for free tier (covers 95% of legitimate use)
    - Submissions 1-40: Normal operation
    - Submissions 41-50: Friendly upgrade banner displayed
    - Submissions 51+: CAPTCHA required for each submission
    - Resets daily at midnight UTC, no tracking across days
  - **CAPTCHA**: Triggered for suspicious patterns or after daily limit reached
    - 10+ requests in 10 seconds from same session
    - Rapid identical text submissions
  - **Honeypot fields**: Hidden form fields that bots fill but humans don't see
  - **Server-side behavior analysis**: Detect automated patterns without tracking individual users
    - Identical text submitted multiple times rapidly
    - Missing JavaScript execution (headless browsers)
    - Abnormal request timing patterns
  - **Challenge-response**: Simple math questions or image selection for suspected bots
  - **Session-only tracking**: All detection happens per-session, no cross-session tracking
- **API Authentication** (future): API keys for programmatic access with separate rate limits
- **No Client-Side Storage**: Scores not saved in browser localStorage by default

**Privacy Commitment:**
- Rate limit tracking uses session cookies only (expires end of day)
- Bot detection data is session-only and discarded immediately after verification
- No persistent user identifiers created across sessions
- No cross-session behavioral profiling
- Detection focuses on behavior patterns, not user identity

#### 7.3.5 GDPR & Legal Compliance

**For MVP (No User Accounts):**
- Minimal compliance needed (no personal data collected)
- Privacy notice displayed prominently
- Cookie consent banner (if analytics used)

**For Future Versions (With Accounts):**
- **Right to Access**: Users can download all their data
- **Right to Erasure**: Delete account and all associated data
- **Right to Portability**: Export data in JSON format
- **Consent Management**: Explicit opt-in for data collection
- **Data Processing Agreement**: If using third-party NLP services

**Legal Pages Required:**
- Privacy Policy
- Terms of Service
- Cookie Policy (if applicable)
- Acceptable Use Policy

### 7.4 Maintainability

- **Code Quality**: Well-documented, modular codebase
- **Testing**: Unit tests for all scoring components
- **Logging**: Track errors and performance metrics

### 7.5 Monitoring & Observability

Comprehensive monitoring ensures system health, identifies issues proactively, and informs optimization decisions.

#### 7.5.1 Key Metrics to Track

**Performance Metrics:**
- **Response Time**: p50, p95, p99 latencies for /api/score endpoint
  - Target: p95 < 10 seconds
  - Alert if: p95 > 15 seconds for 5 minutes
- **Throughput**: Requests per minute/hour
- **Error Rate**: 4xx and 5xx responses as % of total
  - Target: < 1% error rate
  - Alert if: > 5% error rate

**Business Metrics:**
- **Daily Active Users (DAU)**
- **Submissions per day**: Total text scoring requests
- **Average text length**: Median word count submitted
- **Completion rate**: % of users who see results after submitting
- **Conversion rate**: Free to premium (if applicable)

**Scoring Quality Metrics:**
- **Score Distribution**: Histogram of overall scores (are all users getting 7-8? Need recalibration)
- **Subcategory Score Variance**: Are some categories scoring consistently higher/lower?
- **Confidence Level Distribution**: % low/medium/high confidence scores
- **Feedback Helpfulness**: User ratings of feedback quality (if implemented)

**System Health Metrics:**
- **CPU Utilization**: Backend server CPU usage
- **Memory Usage**: RAM consumption (important for NLP models)
- **Model Load Time**: How long to load spaCy/other models on startup
- **Cache Hit Rate**: % of requests served from cache (if caching implemented)

#### 7.5.2 Logging Strategy

**Log Levels:**
- **ERROR**: Model failures, crashes, unhandled exceptions
- **WARN**: Timeouts, fallbacks triggered, bot detection triggered, CAPTCHA required
- **INFO**: Request received, processing started/completed, scores calculated
- **DEBUG**: Detailed NLP analysis steps (disable in production)

**Structured Logging (JSON format):**
```json
{
  "timestamp": "2025-02-25T14:32:01Z",
  "level": "INFO",
  "event": "score_calculated",
  "request_id": "abc123",
  "word_count": 245,
  "overall_score": 7.5,
  "processing_time_ms": 3421,
  "confidence": "high",
  "user_ip_hash": "d8e8fca..."
}
```

**What NOT to Log:**
- ❌ Full user text (privacy violation)
- ❌ IP addresses in plaintext (hash them)
- ❌ Personally identifiable information

**Log Retention:**
- Error logs: 90 days
- Info logs: 30 days
- Debug logs: 7 days (if enabled)

#### 7.5.3 Monitoring Tools

**MVP (Free Tier):**
- **Application Monitoring**: Sentry (error tracking)
- **Infrastructure**: Heroku Metrics or AWS CloudWatch
- **Uptime Monitoring**: UptimeRobot (free)
- **Log Management**: CloudWatch Logs or Papertrail free tier

**Production (Paid):**
- **APM**: Datadog, New Relic, or Honeycomb
- **Logs**: Datadog Logs, Splunk, or ELK Stack
- **Metrics**: Prometheus + Grafana (self-hosted) or Datadog
- **Alerting**: PagerDuty for critical issues

#### 7.5.4 Alerts & Notifications

**Critical Alerts (Immediate Response):**
- API error rate > 10% for 5 minutes
- API down / not responding
- Database connection failures
- Out of memory errors

**Warning Alerts (Review within hours):**
- Response time p95 > 15 seconds
- Error rate > 5% for 15 minutes
- Disk space > 80% full
- Model failures > 10 in 1 hour

**Info Notifications (Daily/Weekly digest):**
- Daily usage summary
- Score distribution anomalies
- User feedback trends

**Alert Channels:**
- **Critical**: SMS, phone call (PagerDuty)
- **Warning**: Slack/Discord channel
- **Info**: Email digest

#### 7.5.5 Dashboards

**Real-Time Operations Dashboard:**
```
┌─────────────────────────────────────────────┐
│  English Scorer - Live Metrics             │
├─────────────────────────────────────────────┤
│  Requests (last hour): 1,247               │
│  Error Rate: 0.8%         ✓ Healthy       │
│  Avg Response Time: 4.2s  ✓ Good          │
│  Active Users: 89                           │
│                                             │
│  Score Distribution (today):                │
│  1-3: █░░░░ 12%                            │
│  4-6: ████░ 35%                            │
│  7-9: █████ 48%                            │
│  10:  ░░░░░ 5%                             │
└─────────────────────────────────────────────┘
```

**Business Dashboard:**
- Daily/weekly/monthly active users
- Submissions over time (trend line)
- Top errors encountered
- User retention metrics
- Revenue (if applicable)

#### 7.5.6 Anomaly Detection

Monitor for unusual patterns that might indicate issues:

- **Score Drift**: Sudden change in average scores (model broken?)
- **Traffic Spike**: 10x normal requests (being scraped? viral post?)
- **Error Clustering**: Specific error type suddenly increases
- **Geography Anomalies**: Unexpected traffic from new regions (DDoS?)

**Example Alert:**
```
⚠️ Anomaly Detected
Average overall score dropped from 6.8 to 4.2 in the last hour.
Possible causes:
  - Grammar model regression
  - Bad deployment
  - Input validation issue

[View Logs] [Rollback] [Investigate]
```

#### 7.5.7 User-Facing Status

**Status Page** (e.g., status.englishscorer.com):
- Current system status (🟢 All Systems Operational)
- Incident history
- Scheduled maintenance
- Subscribe to updates

**In-App Status:**
If experiencing issues, show banner:
```
⚠️ We're experiencing higher than normal response times.
    Your request may take longer than usual.
```

---

## 8. Data Requirements

### 8.1 Input Data

- Plain text submitted by users
- Length: 1 sentence (minimum) to 2000 words (maximum)

### 8.2 Training Data (if using ML)

**Purpose:** Train and validate scoring algorithms, calibrate against human expert ratings

**Requirements:**
- **Minimum viable dataset**: 100-200 labeled texts for initial calibration
- **Production-ready dataset**: 1,000+ texts with expert scores
- **Diverse text types**: Essays (60%), emails (20%), creative writing (10%), other (10%)
- **Proficiency distribution**:
  - Beginner (1-3): 20%
  - Intermediate (4-6): 40%
  - Advanced (7-10): 40%
- **Scoring format**: Each text scored 1-10 by 2-3 expert raters (take average)

**Potential Sources:**

| Dataset | Description | Size | Access | License |
|---------|-------------|------|--------|---------|
| **Cambridge Learner Corpus (CLC)** | Written exam scripts from learners | 50M words | Paid license | Research only |
| **EF-Cambridge Open Language Database (EFCAMDAT)** | Learner texts with CEFR levels | 83M words | Free for research | Attribution required |
| **TOEFL11 Corpus** | Essays from TOEFL test takers | 12,100 essays | Free | Research license |
| **ICLE (International Corpus of Learner English)** | Essays from higher proficiency learners | 3.7M words | Paid | Academic use |
| **Lang-8 Corpus** | Language learner journals with corrections | 1M entries | Free | Open |
| **Write & Improve** | Cambridge assessment texts with scores | Limited access | Request from Cambridge | Research agreement |

**Recommended Approach for MVP:**
1. **Use existing corpora** (EFCAMDAT or Lang-8) for initial development
2. **Manually score 100 texts** using 2-3 ESL teachers as experts
3. **Collect user submissions** (with consent) to build proprietary dataset over time

**Ethical Considerations:**
- Obtain proper licenses for all datasets
- Do not use copyrighted student work without permission
- Anonymize all training data (remove names, locations, personal info)

### 8.3 Reference Data

**Grammar Rules & Error Patterns:**
- **LanguageTool rules**: Built-in, open source
- **Common ESL error database**: Compile from literature (article errors, tense errors, etc.)

**Vocabulary Lists:**
- **Academic Word List (AWL)**: 570 word families - https://www.wgtn.ac.nz/lals/resources/academicwordlist
- **COCA (Corpus of Contemporary American English)**: Frequency lists - free
- **Oxford 3000/5000**: Common English words - https://www.oxfordlearnersdictionaries.com/
- **CEFR Vocabulary**: Words categorized by proficiency level

**Readability Formulas:**
- Flesch-Kincaid Grade Level
- Flesch Reading Ease
- SMOG Index
- Coleman-Liau Index
- All available in Python `textstat` library

**Benchmark Texts:**
Create a gold standard set of 20-30 texts (5 per proficiency level) with known scores:
- Use for system testing and calibration
- Validate that system scores match expected scores
- Track score drift over time

---

## 9. Development Phases

### Phase 1: MVP (Minimum Viable Product)
**Goal: Functional web application with basic scoring and feedback**
- Web page with text input interface
- Backend API for score processing
- Simple rule-based scoring for all six categories
- Overall score display (1-10) with proficiency level
- Subcategory score breakdown with progress bars
- Color-coded visual indicators (red/yellow/green)
- Basic feedback generation for each subcategory
- Input validation (1 sentence to 2000 words)

### Phase 2: Enhanced Visualization & Feedback
**Goal: Improve user experience and feedback quality**
- Refined visual design with better charts/graphics
- More sophisticated feedback generation based on detected patterns
- Responsive design for mobile devices
- Loading animations and smooth transitions
- Improved error messages and user guidance

### Phase 3: Enhanced Scoring Accuracy
**Goal: Improve scoring accuracy and reliability**
- Implement comprehensive evaluation criteria
- Refine weighted scoring algorithm
- Add more sophisticated NLP analysis
- Testing with diverse text samples
- Calibration against human expert ratings

### Phase 4: ML Integration
**Goal: Add AI-powered assessment**
- Integrate pre-trained language model for holistic assessment
- Fine-tune model on English proficiency dataset
- A/B testing to compare rule-based vs. ML-based scoring
- Ensemble approach combining multiple scoring methods
- Context-aware feedback generation

### Phase 5: Advanced Features
**Goal: Premium features for power users**
- Error highlighting within the text (by category)
- Detailed explanations and learning resources for each score
- Historical tracking of user progress over time
- Comparison with proficiency standards (CEFR levels)
- Export/save results (PDF, JSON)
- User accounts and progress tracking

---

## 10. Development Environment Setup

This section provides step-by-step instructions for setting up a local development environment.

### 10.1 Prerequisites

**Required Software:**
- **Python 3.9+**: Backend language
- **Node.js 16+** and **npm/yarn**: Frontend tooling
- **Git**: Version control
- **Docker** (optional but recommended): For consistent environments

**System Requirements:**
- **RAM**: Minimum 8GB (16GB recommended for NLP models)
- **Disk Space**: 5GB free (for models and dependencies)
- **OS**: macOS, Linux, or Windows with WSL2

### 10.2 Backend Setup

**1. Clone the Repository:**
```bash
git clone https://github.com/yourusername/english-scorer.git
cd english-scorer/backend
```

**2. Create Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Download NLP Models:**
```bash
# spaCy English model
python -m spacy download en_core_web_lg

# LanguageTool (if using standalone)
# Download from https://languagetool.org/download/LanguageTool-stable.zip
# Extract to ./languagetool/
```

**5. Set Environment Variables:**
Create `.env` file:
```bash
# .env
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=5242880  # 5MB
CORS_ORIGINS=http://localhost:3000

# Optional: External APIs
# OPENAI_API_KEY=sk-...
# LANGUAGETOOL_API_URL=https://api.languagetool.org/v2/
```

**6. Run Development Server:**
```bash
flask run --port 5000
# or
python app.py
```

Backend should be running at http://localhost:5000

### 10.3 Frontend Setup

**1. Navigate to Frontend Directory:**
```bash
cd ../frontend
```

**2. Install Dependencies:**
```bash
npm install
# or
yarn install
```

**3. Configure Environment:**
Create `.env.local`:
```bash
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

**4. Start Development Server:**
```bash
npm start
# or
yarn start
```

Frontend should be running at http://localhost:3000

### 10.4 Docker Setup (Alternative)

**Using Docker Compose** (recommended for consistency):

**1. docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
    environment:
      - FLASK_ENV=development
    command: flask run --host=0.0.0.0

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - REACT_APP_API_URL=http://localhost:5000/api
```

**2. Start all services:**
```bash
docker-compose up
```

### 10.5 Dependencies List

**Backend (requirements.txt):**
```txt
Flask==2.3.0
Flask-CORS==4.0.0
spacy==3.5.0
language-tool-python==2.7.1
textstat==0.7.3
python-dotenv==1.0.0
gunicorn==21.2.0

# Optional for ML features
transformers==4.30.0
torch==2.0.0
```

**Frontend (package.json):**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.4.0",
    "chart.js": "^4.3.0",
    "react-chartjs-2": "^5.2.0",
    "tailwindcss": "^3.3.0"
  }
}
```

### 10.6 Testing the Setup

**1. Backend Health Check:**
```bash
curl http://localhost:5000/api/health
# Expected: {"status": "healthy"}
```

**2. Test Scoring Endpoint:**
```bash
curl -X POST http://localhost:5000/api/score \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test sentence. I am testing the API."}'
```

**3. Frontend Access:**
- Open http://localhost:3000
- Enter test text
- Click "Score My English"
- Verify results display

### 10.7 Common Setup Issues

| Issue | Solution |
|-------|----------|
| **spaCy model not found** | Run `python -m spacy download en_core_web_lg` |
| **Port 5000 already in use** | Change port in .env or kill process: `lsof -ti:5000 | xargs kill` |
| **CORS errors** | Check CORS_ORIGINS in .env matches frontend URL |
| **Out of memory** | Reduce model size (use `en_core_web_sm` instead of `lg`) or increase RAM |
| **Slow processing** | Expected on first run (models loading). Subsequent requests faster. |

### 10.8 Development Workflow

**Recommended workflow:**
1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes to backend and/or frontend
3. Test locally using curl and browser
4. Run unit tests: `pytest` (backend) and `npm test` (frontend)
5. Commit and push: `git commit -m "Add feature"` && `git push`
6. Create pull request for review

**Hot reload:**
- Backend: Flask dev server auto-reloads on file changes
- Frontend: React dev server auto-refreshes browser

### 10.9 Debugging Tips

**Backend:**
```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
- Use React DevTools browser extension
- Check Network tab in browser for API calls
- Add `console.log()` statements

**Common debugging commands:**
```bash
# Check Python packages
pip list | grep spacy

# Test NLP models
python -c "import spacy; nlp = spacy.load('en_core_web_lg'); print('OK')"

# View logs
tail -f logs/app.log  # if logging to file
```

---

## 11. Testing Strategy

### 11.1 Unit Testing
- Test each scoring component independently (all 6 subcategories)
- Validate scoring algorithm calculations (weighted average formula)
- Test subcategory score generation (1-10 range)
- Test input validation logic

### 10.2 Integration Testing
- Test complete scoring pipeline (frontend to backend)
- Verify correct component interaction
- Test API endpoints (POST /score with various inputs)
- Test feedback generation for all score ranges
- Verify visualization renders correctly with different scores

### 10.3 Validation Testing
- Compare overall scores against human expert ratings
- Validate subcategory scores match expert assessments
- Test with known proficiency level texts (CEFR levels, etc.)
- Ensure scoring consistency across similar texts
- Verify weighted formula produces accurate overall scores

### 10.4 User Acceptance Testing
- Test with target users (English learners at various proficiency levels)
- Gather feedback on score accuracy and usefulness
- Evaluate user interface usability and visual design
- Test feedback clarity and actionability
- Assess whether visualizations are intuitive and helpful
- Measure user satisfaction with the web interface

---

## 12. Future Enhancements

### 11.1 Short-term
- Specific error highlighting in the text (underline errors by category with tooltips)
- Click-to-view detailed error explanations
- Suggested corrections for identified errors
- Downloadable PDF report of scores and feedback

### 11.2 Medium-term
- User accounts and authentication
- Historical progress tracking over time with charts
- Comparison with proficiency standards (CEFR, IELTS, TOEFL)
- Side-by-side comparison of multiple submissions
- Detailed learning resources linked to each feedback item

### 11.3 Long-term
- AI-powered personalized learning recommendations
- Custom writing exercises tailored to user's weak areas
- Multiple language pair support (e.g., Spanish/Chinese speakers learning English)
- Community features (anonymous peer comparison)
- Native mobile applications (iOS/Android)
- Real-time collaborative scoring for teachers/tutors
- API access for integration with learning management systems

---

## 13. Success Metrics

**MVP Success Criteria:**
- **Accuracy**: Correlation 0.6-0.7 with human expert scores
- **User Satisfaction**: 3.5+ star rating from early users
- **Adoption**: 100+ active users within 3 months
- **Performance**: 95% of requests processed under 10 seconds
- **Cost Control**: Daily costs stay under $20

**Long-term Success Targets:**
- **Accuracy**: Correlation > 0.8 with human expert scores
- **User Satisfaction**: 4+ star rating from users
- **Adoption**: 1000+ active users within 6 months
- **Engagement**: 40%+ return user rate
- **Performance**: 95% of requests processed under 5 seconds
- **Conversion**: 3-5% free to premium conversion rate

---

## 14. Risks and Mitigation

| Risk | Impact | Mitigation Strategy |
|------|--------|-------------------|
| Inaccurate scoring | High | Extensive testing with validated datasets, expert review |
| Slow processing times | Medium | Optimize algorithms, use caching, scale infrastructure |
| User privacy concerns | High | Clear privacy policy, minimal data retention, no tracking |
| Model bias | High | Use diverse training data, regular bias audits |
| Service abuse | Medium | Privacy-preserving bot detection (honeypots, CAPTCHA), session-only analysis |

---

## 15. Conclusion

English Scorer is a comprehensive web-based application designed to help non-native English speakers improve their writing through instant, detailed feedback. This design document provides a complete blueprint for building a production-ready system that balances technical feasibility with educational value.

### Key Features

The system evaluates English proficiency across **six dimensions**:
1. Grammar (25%)
2. Vocabulary (20%)
3. Spelling & Mechanics (10%)
4. Sentence Structure (20%)
5. Coherence & Organization (15%)
6. Fluency & Naturalness (10%)

Each text receives an **overall score (1-10)** mapped to international standards (CEFR, IELTS, TOEFL), along with **category-specific scores** visualized through progress bars and color-coding. Users receive **actionable, personalized feedback** for each category to guide their improvement.

### Technical Approach

The architecture combines **rule-based NLP** (spaCy, LanguageTool) with optional **ML models** for nuanced assessment. A Python backend (Flask/FastAPI) processes text and generates scores, while a React/Vue frontend provides an intuitive, mobile-friendly interface. The system is designed for **realistic MVP targets** (0.6-0.7 correlation with expert ratings, 10-second processing time) with a clear path to production quality.

### Comprehensive Coverage

This document addresses not only core functionality but also:
- **Privacy & security**: GDPR compliance, data handling, content moderation
- **Error handling**: Graceful degradation, fallback strategies, user-friendly error messages
- **Monitoring**: Metrics, logging, alerting for production stability
- **Costs**: Detailed operational cost analysis ($7-20/month MVP to $320-1,260/month at scale)
- **Internationalization**: Multi-language UI support for global learners
- **Development setup**: Complete environment configuration guide

### Implementation Strategy

The phased development approach prioritizes delivering value quickly:
- **Phase 1 (MVP)**: Core scoring, visualization, and feedback
- **Phase 2**: Enhanced UX and feedback quality
- **Phase 3**: Improved scoring accuracy through testing
- **Phase 4**: ML integration for advanced assessment
- **Phase 5**: Premium features (error highlighting, progress tracking)

### Success Factors

With realistic targets, robust error handling, comprehensive monitoring, and a strong focus on user experience, English Scorer is positioned to become a valuable tool for millions of English learners worldwide. The modular architecture and clear documentation enable iterative development while maintaining code quality and system reliability.

This design document serves as both a technical specification and an implementation guide, providing development teams with everything needed to build, deploy, and maintain a successful English proficiency scoring service.
