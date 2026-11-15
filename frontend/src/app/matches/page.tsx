"use client";
import { useEffect, useState } from "react";
import { getMatches, getSeasons, getTeams, labelOf, firstNumber } from "@/lib/api";
import Loading from "@/components/Loading";
import EmptyState from "@/components/EmptyState";
export default function MatchesPage(){
 const [teams,setTeams]=useState<any[]>([]);const [seasons,setSeasons]=useState<any[]>([]);const [team,setTeam]=useState("");const [season,setSeason]=useState("");const [page,setPage]=useState(1);const [items,setItems]=useState<any[]>([]);const [count,setCount]=useState(0);const [loading,setLoading]=useState(true);const [error,setError]=useState("");
 useEffect(()=>{Promise.all([getTeams(),getSeasons()]).then(([t,s])=>{setTeams(t);setSeasons(s);}).catch(()=>setError("Could not load filters."));},[]);
 useEffect(()=>{setLoading(true);getMatches({page,page_size:20,team:team||undefined,season:season||undefined}).then(r=>{setItems(r.items);setCount(r.count||r.items.length);}).catch(()=>setError("Matches endpoint failed.")).finally(()=>setLoading(false));},[page,team,season]);
 const pages=Math.max(1,Math.ceil(count/20));
 return <div className="page-stack"><div className="page-intro"><div className="eyebrow">HISTORICAL DATABASE</div><h2>Match explorer</h2><p>Search and inspect the historical EPL match dataset.</p></div>
 <div className="toolbar filters"><div><label className="field-label">SEASON</label><select value={season} onChange={e=>{setSeason(e.target.value);setPage(1);}}><option value="">All seasons</option>{seasons.map((s:any)=><option key={labelOf(s,["name","season"])} value={labelOf(s,["name","season"])}>{labelOf(s,["name","season"])}</option>)}</select></div><div><label className="field-label">TEAM</label><select value={team} onChange={e=>{setTeam(e.target.value);setPage(1);}}><option value="">All teams</option>{teams.map((t:any)=><option key={t.id??t.team_id} value={t.id??t.team_id}>{labelOf(t,["name","team_name"])}</option>)}</select></div><span className="muted">{count.toLocaleString()} matches</span></div>
 {error&&<div className="error-banner">{error}</div>}
 {loading?<Loading label="Loading match records..."/>:items.length?<div className="panel table-panel"><div className="table-scroll"><table><thead><tr><th>DATE</th><th>HOME</th><th>SCORE</th><th>AWAY</th><th>SEASON</th><th>RESULT</th></tr></thead><tbody>{items.map((m:any,i:number)=><tr key={m.id??m.match_id??i}><td>{labelOf(m,["match_date","date"],"—")}</td><td className="club-cell">{labelOf(m,["home_team_name","home_team"])}</td><td><strong className="score">{firstNumber(m,["home_goals"])} – {firstNumber(m,["away_goals"])}</strong></td><td className="club-cell">{labelOf(m,["away_team_name","away_team"])}</td><td>{labelOf(m,["season_name","season"])}</td><td><span className="result-pill">{labelOf(m,["result"],"—")}</span></td></tr>)}</tbody></table></div><div className="pagination"><span>Page {page} of {pages}</span><div><button disabled={page<=1} onClick={()=>setPage(p=>p-1)}>Previous</button><button disabled={page>=pages} onClick={()=>setPage(p=>p+1)}>Next</button></div></div></div>:<EmptyState message="No matches match these filters."/>}
 </div>;
}
