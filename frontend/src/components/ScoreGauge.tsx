import type { ReadinessVerdict } from "../types";

interface Props {
  verdict: ReadinessVerdict;
}

export default function ScoreGauge({ verdict }: Props) {
  return (
    <div className={`score-gauge ${verdict.ready ? "score-ready" : "score-not-ready"}`}>
      <div className="score-number">{verdict.score}%</div>
      <div className="score-status">{verdict.ready ? "READY" : "NOT READY"}</div>
      <div className="score-summary">{verdict.summary}</div>
    </div>
  );
}
