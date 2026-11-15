import axios from "axios";

const baseURL = (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api").replace(/\/$/, "");

export const api = axios.create({
  baseURL,
  timeout: 20000,
  headers: { "Content-Type": "application/json" },
});

export type AnyRecord = Record<string, any>;

export function rows<T = AnyRecord>(payload: any): T[] {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.results)) return payload.results;
  if (Array.isArray(payload?.data)) return payload.data;
  if (Array.isArray(payload?.standings)) return payload.standings;
  if (Array.isArray(payload?.teams)) return payload.teams;
  if (Array.isArray(payload?.matches)) return payload.matches;
  return [];
}

export function firstNumber(obj: AnyRecord, keys: string[], fallback = 0): number {
  for (const key of keys) {
    const value = Number(obj?.[key]);
    if (obj?.[key] !== undefined && obj?.[key] !== null && Number.isFinite(value)) return value;
  }
  return fallback;
}

export function labelOf(obj: AnyRecord, keys: string[], fallback = "—"): string {
  for (const key of keys) {
    const value = obj?.[key];
    if (value !== undefined && value !== null && String(value).trim()) return String(value);
  }
  return fallback;
}

export async function getOverviewData() {
  const [matchesRes, teamsRes, seasonsRes, goalsRes, resultsRes, topTeamsRes] = await Promise.allSettled([
    api.get("/matches/?page_size=1"),
    api.get("/teams/"),
    api.get("/seasons/"),
    api.get("/analytics/goals/"),
    api.get("/analytics/results/"),
    api.get("/analytics/top-teams/"),
  ]);
  const value = (r: PromiseSettledResult<any>) => r.status === "fulfilled" ? r.value.data : null;
  const matches = value(matchesRes);
  return {
    matchesPayload: matches,
    matchesCount: Number(matches?.count ?? matches?.total ?? (Array.isArray(matches) ? matches.length : 0)),
    teams: rows(value(teamsRes)),
    seasons: rows(value(seasonsRes)),
    goals: rows(value(goalsRes)),
    results: rows(value(resultsRes)),
    topTeams: rows(value(topTeamsRes)),
    errors: [matchesRes, teamsRes, seasonsRes, goalsRes, resultsRes, topTeamsRes].filter(x => x.status === "rejected").length,
  };
}

export async function getStandings(season?: string) {
  const { data } = await api.get("/analytics/standings/", { params: season ? { season } : {} });
  return rows(data);
}
export async function getTeamStats() {
  const { data } = await api.get("/analytics/team-stats/");
  return rows(data);
}
export async function getTeams() {
  const { data } = await api.get("/teams/");
  return rows(data);
}
export async function getSeasons() {
  const { data } = await api.get("/seasons/");
  return rows(data);
}
export async function getMatches(params: Record<string, string | number | undefined> = {}) {
  const { data } = await api.get("/matches/", { params });
  return { items: rows(data), count: Number(data?.count ?? 0), next: data?.next ?? null, previous: data?.previous ?? null };
}
export async function predictMatch(home_team_id: number, away_team_id: number) {
  const { data } = await api.post("/predictions/predict/", { home_team_id, away_team_id });
  return data;
}
