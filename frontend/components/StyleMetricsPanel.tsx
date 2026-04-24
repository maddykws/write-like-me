"use client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import type { VoiceProfile } from "@/lib/types";

interface Props {
  profile: VoiceProfile;
}

const COLORS = ["#4f72ff", "#38bdf8", "#34d399", "#f59e0b", "#f87171"];

export default function StyleMetricsPanel({ profile }: Props) {
  if (!profile.punct_signature) return null;

  const data = Object.entries(profile.punct_signature)
    .map(([name, value]) => ({ name: name.replace("_", " "), value: Number(value.toFixed(2)) }))
    .filter((d) => d.value > 0);

  const metricsData = [
    { name: "Formality", value: profile.formality_score ? Number((profile.formality_score * 100).toFixed(1)) : 0, max: 100 },
    { name: "Vocabulary (TTR)", value: profile.type_token_ratio ? Number((profile.type_token_ratio * 100).toFixed(1)) : 0, max: 100 },
    { name: "Sentence length", value: profile.avg_sentence_length ? Number(profile.avg_sentence_length.toFixed(1)) : 0, max: 40 },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Writing Metrics</h3>
        <div className="space-y-3">
          {metricsData.map((m) => (
            <div key={m.name}>
              <div className="flex justify-between text-xs text-gray-600 mb-1">
                <span>{m.name}</span>
                <span>{m.value}</span>
              </div>
              <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-brand-500 rounded-full transition-all"
                  style={{ width: `${Math.min((m.value / m.max) * 100, 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {data.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Punctuation Signature</h3>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={data} margin={{ top: 4, right: 8, bottom: 4, left: -16 }}>
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip
                formatter={(v: number) => [`${v} per 1k chars`, ""]}
                contentStyle={{ fontSize: 12 }}
              />
              <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                {data.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
