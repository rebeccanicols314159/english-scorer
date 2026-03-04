"""Shared text fixtures for scoring analyzer tests."""

# Native-level writing: sophisticated vocabulary, varied structure, clear organisation.
ADVANCED_TEXT = (
    "The proliferation of digital technologies has fundamentally transformed the manner "
    "in which contemporary societies engage with information. Consequently, educational "
    "institutions are grappling with unprecedented challenges in preparing students for "
    "a rapidly evolving knowledge economy. Furthermore, researchers have identified "
    "several promising pedagogical approaches that leverage technology to enhance learning "
    "outcomes. Nevertheless, the long-term implications of widespread internet access on "
    "cognitive development remain poorly understood, despite numerous empirical studies "
    "attempting to quantify these effects. The evidence suggests that thoughtful integration "
    "of digital tools, rather than wholesale adoption or rejection, yields the most "
    "beneficial educational results."
)

# Typical ESL beginner errors: subject-verb disagreement, missing articles, tense mix-up,
# repetitive vocabulary, no transition words, simple structure.
BEGINNER_TEXT = (
    "I go to school yesterday and I have many friend there. "
    "The teacher she very kind to us student. "
    "We learn english grammar but it very hard for me. "
    "My friend he don't understand also. "
    "We both make many mistake on test. "
    "I am not very good at english but I try my best every day."
)

# Intermediate: generally correct grammar, adequate vocabulary, some transition words,
# but limited variety and sophistication.
INTERMEDIATE_TEXT = (
    "Learning English has been challenging but also rewarding for me. "
    "I have improved my vocabulary by reading English books every day. "
    "However, I still make some mistakes with grammar, especially with tenses. "
    "My speaking has also become more natural since I started practicing with native speakers. "
    "In addition, I watch English movies to improve my listening skills. "
    "I think that consistency is the key to success in language learning."
)

# Very short — too little to assess coherence meaningfully.
SHORT_TEXT = "I like cats. Dogs are good."

# Well-structured with many transition words and paragraphs.
COHERENT_TEXT = (
    "First and foremost, exercise improves physical health significantly. "
    "Furthermore, it has well-documented mental health benefits as well. "
    "For example, regular aerobic activity has been shown to reduce symptoms of depression. "
    "However, many people struggle to maintain a consistent exercise routine. "
    "Consequently, health professionals recommend starting with short, manageable sessions. "
    "In conclusion, the evidence for regular exercise is overwhelming and should not be ignored."
)

# Sentences of uniform length — low structural variety.
UNIFORM_SENTENCE_TEXT = (
    "I like to eat food. She goes to work. He reads a book. "
    "They play a game. We watch a show. You write a note. "
    "It makes a sound. I walk to school. She buys some milk. He drives a car."
)

# Many repeated words — low vocabulary diversity.
REPETITIVE_TEXT = (
    "The dog is a good dog. The dog likes to run and the dog likes to play. "
    "The dog eats food and the dog drinks water. The dog is happy when the dog runs. "
    "My dog is the best dog and I love my dog very much every day."
)

# Well-written with diverse, uncommon vocabulary.
RICH_VOCABULARY_TEXT = (
    "The eloquent professor elucidated the intricate nuances of contemporary linguistics "
    "with remarkable precision. Her perspicacious observations illuminated the fundamental "
    "discrepancies between theoretical frameworks and empirical findings. Subsequently, "
    "the symposium participants engaged in a sophisticated discourse on pragmatic implications."
)

# Heavily misspelled text.
MISSPELLED_TEXT = (
    "Teh quikc broun fox jumpd ovr teh layz dog. "
    "She wnet to teh stoer to bye som bred. "
    "He is verry hapyy todya becuase he finshed hsi wrk."
)

# Correct spelling throughout.
CORRECTLY_SPELLED_TEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "She went to the store to buy some bread. "
    "He is very happy today because he finished his work."
)
