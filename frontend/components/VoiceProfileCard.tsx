"use client";
import type { VoiceProfile } from "@/lib/types";

interface Props {
  profile: VoiceProfile;
}

function Metric({ label, value }: { label: string; value: string | number | null }) {
  if (value === null || value === undefined) return null;
  return (
    <div className="bg-gray-50 rounded-lg p-3 border border-gray-200">
      <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">{label}</p>
      <p className="text-lg font-semibold text-gray-900">{value}</p>
    </div>
  );
}

export default function VoiceProfileCard({ profile }: Props) {
  const formalityLabel =
    profile.formality_score === null
      ? null
      : profile.formality_score > 0.6
      ? "Formal"
      : profile.formality_score < 0.4
      ? "Casual"
      : "Neutral";

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">Your Voice Profile</h2>
        <span className="text-sm text-gray-500">{profile.sample_count} samples</span>
      </div>

      {profile.summary_prompt && (
        <div className="p-4 bg-brand-50 border border-brand-100 rounded-lg">
          <p className="text-sm text-brand-900 italic">&ldquo;{profile.summary_prompt}&rdquo;</p>
        </div>
      )}

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Metric label="Avg sentence" value={profile.avg_sentence_length !== null ? `${profile.avg_sentence_length?.toFixed(1)} words` : null} />
        <Metric label="Formality" value={formalityLabel} />
        <Metric label="Vocabulary" value={profile.type_token_ratio !== null ? `${(profile.type_token_ratio! * 100).toFixed(0)}% TTR` : null} />
        {profile.updated_at && (
          <Metric label="Last updated" value={new Date(profile.updated_at).toLocaleDateString()} />
        )}
      </div>

      {profile.punct_signature && (
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Punctuation Signature (per 1000 chars)</p>
          <div className="flex gap-4 flex-wrap text-sm">
            {Object.entries(profile.punct_signature).map(([k, v]) =>
              v > 0.1 ? (
                <span key={k} className="px-2 py-1 bg-gray-100 rounded text-gray-700">
                  {k.replace("_", " ")}: {(v as number).toFixed(1)}
                </span>
              ) : null
            )}
          </div>
        </div>
      )}
    </div>
  );
}
