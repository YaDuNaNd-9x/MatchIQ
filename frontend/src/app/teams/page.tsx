"use client";
import { useEffect, useMemo, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getTeams, getTeamStats, labelOf, firstNumber } from "@/lib/api";
import Loading from "@/components/Loading";
import EmptyState from "@/components/EmptyState";
import StatCard from "@/components/StatCard";
import { Shield, Target, TrendingUp, Award } from "lucide-react";

export default function TeamsPage(){
 const [teams,setTeams]=useState<any[]>([]);
 const [teamId,setTeamId]=useState("");
 const [stats,setStats]=useState<any[]>([]);
 const [loading,setLoading]=useState(true);
 const [error,setError]=useState("");

 useEffect(()=>{
   Promise.all([getTeams(),getTeamStats()])
     .then(([teamRows,statRows])=>{
       setTeams(teamRows);
       setStats(statRows);
       if(teamRows.length) setTeamId(String(teamRows[0].id??teamRows[0].team_id));
     })
     .catch(()=>setError("Could not load team analytics. Check the teams and team-stats API endpoints."))
     .finally(()=>setLoading(false));
 },[]);

 const current=teams.find(t=>String(t.id??t.team_id)===teamId);
 const currentName=labelOf(current||{},["name","team_name"]);
 const selectedStats=useMemo(()=>stats.find((r:any)=>
   labelOf(r,["team","team_name","name"]).trim().toLowerCase()===currentName.trim().toLowerCase()
 ),[stats,currentName]);
 const chart=selectedStats?[{
   metric:"Goals",
   scored:firstNumber(selectedStats,["goals_scored","goals_for","gf"]),
   conceded:firstNumber(selectedStats,["goals_conceded","goals_against","ga"])
 }]:[];

 if(loading) return <Loading label="Loading club performance..."/>;

 return <div className="page-stack">
   <div className="page-intro">
     <div className="eyebrow">CLUB PERFORMANCE</div>
     <h2>Team analytics</h2>
     <p>Compare attacking output, defensive record and points performance across the five-season dataset.</p>
   </div>
   <div className="toolbar">
     <div><label className="field-label" htmlFor="team-select">SELECT TEAM</label>
       <select id="team-select" value={teamId} onChange={e=>setTeamId(e.target.value)}>
         {teams.map((t:any)=><option key={t.id??t.team_id} value={t.id??t.team_id}>{labelOf(t,["name","team_name"])}</option>)}
       </select>
     </div>
     <span className="muted">{currentName||"Choose a club"}</span>
   </div>
   {error&&<div className="error-banner">{error}</div>}
   {!error&&selectedStats?<>
     <div className="stats-grid">
       <StatCard label="Matches played" value={firstNumber(selectedStats,["matches_played","played"])} detail="Across five seasons" icon={<Shield size={18}/>}/>
       <StatCard label="Goals scored" value={firstNumber(selectedStats,["goals_scored","goals_for","gf"])} detail="Attacking output" icon={<Target size={18}/>} accent="blue"/>
       <StatCard label="Goal difference" value={firstNumber(selectedStats,["goal_difference","goal_diff","gd"])} detail="Scored minus conceded" icon={<TrendingUp size={18}/>} accent="purple"/>
       <StatCard label="Points per match" value={firstNumber(selectedStats,["points_per_match","ppm"]).toFixed(2)} detail={`${firstNumber(selectedStats,["total_points","points","pts"])} total points`} icon={<Award size={18}/>} accent="gold"/>
     </div>
     <section className="panel chart-panel">
       <div className="panel-heading"><div><h3>{currentName}: attacking and defensive output</h3><p>Aggregate goals across the available historical matches</p></div></div>
       <div className="chart-wrap tall">
         <ResponsiveContainer width="100%" height="100%">
           <BarChart data={chart} margin={{top:12,right:12,left:0,bottom:0}} barCategoryGap="55%">
             <CartesianGrid stroke="#edf1ee" vertical={false}/>
             <XAxis dataKey="metric" tick={{fill:"#7e8b82",fontSize:11}} axisLine={false} tickLine={false}/>
             <YAxis tick={{fill:"#7e8b82",fontSize:10}} axisLine={false} tickLine={false}/>
             <Tooltip contentStyle={{background:"#fff",border:"1px solid #e3eae5",borderRadius:9,color:"#26342c"}}/>
             <Bar dataKey="scored" name="Goals scored" fill="#16845c" radius={[5,5,0,0]} maxBarSize={70}/>
             <Bar dataKey="conceded" name="Goals conceded" fill="#9db5a7" radius={[5,5,0,0]} maxBarSize={70}/>
           </BarChart>
         </ResponsiveContainer>
       </div>
     </section>
   </>:!error?<EmptyState message="No aggregate statistics matched this club. Check that the team name in the team-stats response matches the teams endpoint."/>:null}
 </div>;
}
