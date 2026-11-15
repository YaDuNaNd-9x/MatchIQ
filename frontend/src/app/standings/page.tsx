"use client";
import { useEffect, useState } from "react";
import { getSeasons, getStandings, labelOf, firstNumber } from "@/lib/api";
import Loading from "@/components/Loading";
import EmptyState from "@/components/EmptyState";
export default function StandingsPage() {
  const [seasons,setSeasons]=useState<any[]>([]);
  const [season,setSeason]=useState("2024-25");
  const [rows,setRows]=useState<any[]>([]);
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState("");
  useEffect(()=>{getSeasons().then(s=>{setSeasons(s); if(s.length){const latest=labelOf(s[s.length-1],["name","season","season_name"],"2024-25");setSeason(latest);}}).catch(()=>setError("Could not load seasons."));},[]);
  useEffect(()=>{setLoading(true);getStandings(season).then(setRows).catch(()=>setError("Standings endpoint failed.")).finally(()=>setLoading(false));},[season]);
  return <div className="page-stack"><div className="page-intro"><div className="eyebrow">COMPETITION ANALYTICS</div><h2>League standings</h2><p>Compare club performance across the selected Premier League season.</p></div>
    <div className="toolbar"><div><label className="field-label">SEASON</label><select value={season} onChange={e=>setSeason(e.target.value)}>{(seasons.length?seasons:[{name:"2024-25"},{name:"2023-24"},{name:"2022-23"},{name:"2021-22"},{name:"2020-21"}]).map((s:any)=><option key={labelOf(s,["name","season","season_name"])} value={labelOf(s,["name","season","season_name"])}>{labelOf(s,["name","season","season_name"])}</option>)}</select></div><span className="muted">{rows.length} clubs</span></div>
    {error&&<div className="error-banner">{error}</div>}
    {loading?<Loading label="Calculating table..."/>:rows.length?<div className="panel table-panel"><div className="table-scroll"><table><thead><tr><th>POS</th><th>CLUB</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>PTS</th></tr></thead><tbody>{rows.map((r:any,i:number)=><tr key={labelOf(r,["team_id","team","team_name"],String(i))}><td><span className={`position ${i<4?"top-four":""}`}>{firstNumber(r,["position","rank"],i+1)}</span></td><td className="club-cell">{labelOf(r,["team_name","team","name"])}</td><td>{firstNumber(r,["played","matches_played","p"])}</td><td>{firstNumber(r,["wins","won","w"])}</td><td>{firstNumber(r,["draws","drawn","d"])}</td><td>{firstNumber(r,["losses","lost","l"])}</td><td>{firstNumber(r,["goals_for","goals_scored","gf"])}</td><td>{firstNumber(r,["goals_against","goals_conceded","ga"])}</td><td>{firstNumber(r,["goal_difference","goal_diff","gd"])}</td><td><strong>{firstNumber(r,["points","pts"])}</strong></td></tr>)}</tbody></table></div><div className="table-footnote">GF: Goals for · GA: Goals against · GD: Goal difference · PTS: Points</div></div>:<EmptyState message="No standings found for this season. Check the season query parameter expected by the API."/>}
  </div>;
}
