const EXAMPLES = {
  Beginner:
    "I go to school yesterday and I have many friend there. " +
    "The teacher she very kind to us student. " +
    "We learn english grammar but it very hard for me. " +
    "My friend he don't understand also. " +
    "We both make many mistake on test. " +
    "I am not very good at english but I try my best every day.",
  Intermediate:
    "Learning English has been challenging but also rewarding for me. " +
    "I have improved my vocabulary by reading English books every day. " +
    "However, I still make some mistakes with grammar, especially with tenses. " +
    "My speaking has also become more natural since I started practicing with native speakers. " +
    "In addition, I watch English movies to improve my listening skills. " +
    "I think that consistency is the key to success in language learning.",
  Advanced:
    "The proliferation of digital technologies has fundamentally transformed the manner " +
    "in which contemporary societies engage with information. Consequently, educational " +
    "institutions are grappling with unprecedented challenges in preparing students for " +
    "a rapidly evolving knowledge economy. Furthermore, researchers have identified " +
    "several promising pedagogical approaches that leverage technology to enhance learning " +
    "outcomes. Nevertheless, the long-term implications of widespread internet access on " +
    "cognitive development remain poorly understood, despite numerous empirical studies " +
    "attempting to quantify these effects. The evidence suggests that thoughtful integration " +
    "of digital tools, rather than wholesale adoption or rejection, yields the most " +
    "beneficial educational results.",
}

export default function ExampleButtons({ onLoadExample }) {
  return (
    <div className="flex items-center gap-2 flex-wrap">
      <span className="text-sm text-gray-500">Try an example:</span>
      {Object.entries(EXAMPLES).map(([level, text]) => (
        <button
          key={level}
          onClick={() => onLoadExample(text)}
          className="text-sm px-3 py-1 rounded-full border border-gray-300 text-gray-600 hover:border-blue-400 hover:text-blue-600 transition-colors cursor-pointer"
        >
          {level}
        </button>
      ))}
    </div>
  )
}
