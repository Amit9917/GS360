"use client";

import { useState } from "react";
import { generateQuiz } from "@/lib/api";

interface Question {
  question: string;
  options?: Record<string, string>;
  correct_answer?: string;
  explanation?: string;
  type?: string;
}

const STYLES = [
  { id: "upsc_prelims", label: "Prelims MCQ", icon: "🎯" },
  { id: "upsc_mains", label: "Mains Analytical", icon: "📝" },
  { id: "conceptual", label: "Conceptual", icon: "💡" },
  { id: "mixed", label: "Mixed Format", icon: "🔀" },
];

const UPSC_TOPICS = [
  "Indian Polity",
  "Ancient History",
  "Modern History",
  "Indian Geography",
  "World Geography",
  "Indian Economy",
  "Science & Technology",
  "Environment & Ecology",
  "Ethics & Governance",
  "Current Affairs",
  "International Relations",
  "Indian Society",
];

export default function QuizView() {
  const [topic, setTopic] = useState("");
  const [style, setStyle] = useState("upsc_prelims");
  const [size, setSize] = useState(10);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [showResults, setShowResults] = useState(false);

  const generate = async () => {
    setLoading(true);
    setQuestions([]);
    setAnswers({});
    setShowResults(false);
    try {
      const res = await generateQuiz({ topic: topic || undefined, size, style });
      setQuestions(res.quiz as Question[]);
    } catch (e: unknown) {
      setQuestions([{ question: `Error: ${e instanceof Error ? e.message : "Unknown"}`, type: "error" }]);
    } finally {
      setLoading(false);
    }
  };

  const selectAnswer = (qi: number, option: string) => {
    if (showResults) return;
    setAnswers((prev) => ({ ...prev, [qi]: option }));
  };

  const submit = () => setShowResults(true);

  const score = showResults
    ? questions.filter(
        (q, i) => answers[i] && q.correct_answer && answers[i].toLowerCase() === q.correct_answer.toLowerCase()
      ).length
    : 0;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-primary-500 mb-1">🧩 Quiz Arena</h1>
      <p className="text-[var(--muted)] text-sm mb-6">
        Generate UPSC-style questions powered by DeepTutor AI
      </p>

      {/* Config */}
      <div className="bg-[var(--card)] border border-[var(--card-border)] rounded-xl p-5 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          {/* Topic */}
          <div>
            <label className="text-xs text-[var(--muted)] uppercase tracking-wider block mb-1">
              Topic
            </label>
            <select
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-[var(--background)] border border-[var(--card-border)] text-sm focus:outline-none"
            >
              <option value="">All Topics</option>
              {UPSC_TOPICS.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>

          {/* Size */}
          <div>
            <label className="text-xs text-[var(--muted)] uppercase tracking-wider block mb-1">
              Questions
            </label>
            <input
              type="number"
              min={1}
              max={50}
              value={size}
              onChange={(e) => setSize(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-lg bg-[var(--background)] border border-[var(--card-border)] text-sm focus:outline-none"
            />
          </div>

          {/* Generate */}
          <div className="flex items-end">
            <button
              onClick={generate}
              disabled={loading}
              className="w-full py-2 rounded-lg bg-blue-500 hover:bg-blue-600 text-white font-semibold text-sm transition disabled:opacity-50"
            >
              {loading ? "Generating..." : "Generate Quiz"}
            </button>
          </div>
        </div>

        {/* Style Picker */}
        <div className="flex gap-2">
          {STYLES.map((s) => (
            <button
              key={s.id}
              onClick={() => setStyle(s.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                style === s.id
                  ? "bg-blue-500/20 text-blue-400 border border-blue-400/30"
                  : "bg-[var(--background)] text-[var(--muted)] border border-[var(--card-border)] hover:text-[var(--foreground)]"
              }`}
            >
              {s.icon} {s.label}
            </button>
          ))}
        </div>
      </div>

      {/* Questions */}
      {questions.length > 0 && (
        <div className="space-y-4">
          {questions.map((q, i) => (
            <div
              key={i}
              className="bg-[var(--card)] border border-[var(--card-border)] rounded-xl p-5 animate-fadeInUp"
            >
              <div className="flex items-start gap-3">
                <span className="text-xs font-bold text-[var(--muted)] bg-[var(--background)] px-2 py-1 rounded-lg">
                  Q{i + 1}
                </span>
                <div className="flex-1">
                  <p className="text-sm font-medium mb-3">{q.question}</p>

                  {q.options && (
                    <div className="space-y-2">
                      {Object.entries(q.options).map(([key, val]) => {
                        const selected = answers[i] === key;
                        const correct =
                          showResults && q.correct_answer?.toLowerCase() === key.toLowerCase();
                        const wrong = showResults && selected && !correct;
                        return (
                          <button
                            key={key}
                            onClick={() => selectAnswer(i, key)}
                            className={`w-full text-left px-4 py-2 rounded-lg text-sm border transition ${
                              correct
                                ? "bg-green-500/10 border-green-500/30 text-green-400"
                                : wrong
                                ? "bg-red-500/10 border-red-500/30 text-red-400"
                                : selected
                                ? "bg-blue-500/10 border-blue-400/30 text-blue-400"
                                : "border-[var(--card-border)] hover:border-blue-400/30"
                            }`}
                          >
                            <span className="font-semibold mr-2">{key}.</span>
                            {val}
                          </button>
                        );
                      })}
                    </div>
                  )}

                  {showResults && q.explanation && (
                    <div className="mt-3 text-xs text-[var(--muted)] bg-[var(--background)] p-3 rounded-lg">
                      <strong>Explanation:</strong> {q.explanation}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}

          {/* Submit / Score */}
          {!showResults ? (
            <button
              onClick={submit}
              className="w-full py-3 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-semibold transition"
            >
              Submit Answers
            </button>
          ) : (
            <div className="bg-[var(--card)] border border-[var(--card-border)] rounded-xl p-6 text-center">
              <div className="text-4xl font-bold text-blue-400">
                {score}/{questions.length}
              </div>
              <p className="text-sm text-[var(--muted)] mt-1">
                {score === questions.length
                  ? "Perfect score! 🎉"
                  : score >= questions.length * 0.7
                  ? "Great job! Keep it up."
                  : "Keep practicing — review the explanations."}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
