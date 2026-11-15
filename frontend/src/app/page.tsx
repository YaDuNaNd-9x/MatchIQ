"use client";
import { useEffect, useState } from "react";
import { Activity, CalendarDays, Crosshair, Shield, Target, Trophy } from "lucide-react";
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getOverviewData, firstNumber, labelOf } from "@/lib/api";
import StatCard from "@/components/StatCard";
import ChartCard from "@/components/ChartCard";
import Loading from "@/components/Loading";
import EmptyState from "@/components/EmptyState";

const palette = ["#16845c", "#5d83c5", "#c4933d", "#8a78b8", "#c56d75"];
export default function OverviewPage() {
  const [data,setData] = useState<any>(null);
  const [error,setError] = useState("");
  useEffect(() => { getOverviewData().then(setData).catch(() => setError("Could not reach the Django API. Check that the backend is running and NEXT_PUBLIC_API_URL is correct.")); }, []);
  if (error) return <div className="error-banner">{error}</div>;
  if (!data) return <Loading/>;
  const totalGoals = data.goals.reduce((sum:number,row:any)=>sum+firstNumber(row,["total_goals","goals","goal_count","total"]),0);
  const seasonsCount = data.seasons.length;
  const resultData = data.results.map((r:any)=>({name:labelOf(r,["result","outcome","label","match_result"]),value:firstNumber(r,["count","total","matches","match_count"])})).filter((r:any)=>r.value>0);
  const goalsData = data.goals.map((r:any)=>({season:labelOf(r,["season","season_name","name"]),goals:firstNumber(r,["total_goals","goals","goal_count","total"])})).filter((r:any)=>r.goals>=0);
  const topTeams = data.topTeams.slice(0,5);
  return <div className="page-stack">
    <div className="welcome-row"><div><div className="eyebrow"><span className="live-dot"/> DATA OVERVIEW</div><h2>Numbers behind the beautiful game.</h2><p>Explore five seasons of English Premier League football through data.</p></div><div className="period-pill"><CalendarDays size={15}/> 2020/21 — 2024/25</div></div>
    {data.errors>0 && <div className="notice">Some analytics endpoints did not respond. Available sections are shown; check the Django API routes if a chart is empty.</div>}
    <div className="stats-grid">
      <StatCard label="Matches analysed" value={data.matchesCount.toLocaleString()} detail="Across five EPL seasons" icon={<Activity size={18}/>}/>
      <StatCard label="Teams tracked" value={data.teams.length} detail="Unique team records" icon={<Shield size={18}/>} accent="blue"/>
      <StatCard label="Seasons covered" value={seasonsCount} detail="2020/21 through 2024/25" icon={<CalendarDays size={18}/>} accent="purple"/>
      <StatCard label="Goals recorded" value={totalGoals.toLocaleString()} detail="Aggregate from goals endpoint" icon={<Target size={18}/>} accent="gold"/>
    </div>
    <div className="charts-grid">
      <ChartCard title="Goals by season" subtitle="Total goals scored in each campaign">
        {goalsData.length ? <div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><BarChart data={goalsData} margin={{top:10,right:8,left:-18,bottom:0}}><CartesianGrid stroke="#edf1ee" vertical={false}/><XAxis dataKey="season" tick={{fill:"#7e8b82",fontSize:11}} axisLine={false} tickLine={false}/><YAxis tick={{fill:"#7e8b82",fontSize:11}} axisLine={false} tickLine={false}/><Tooltip contentStyle={{background:"#ffffff",border:"1px solid #e3eae5",borderRadius:10,color:"#26342c",boxShadow:"0 5px 18px rgba(20,40,28,.08)"}}/><Bar dataKey="goals" fill="#16845c" radius={[5,5,0,0]} maxBarSize={44}/></BarChart></ResponsiveContainer></div> : <EmptyState message="The goals endpoint returned no usable season totals."/>}
      </ChartCard>
      <ChartCard title="Match outcomes" subtitle="Home wins, draws and away wins">
        {resultData.length ? <div className="donut-layout"><div className="donut-wrap"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={resultData} dataKey="value" nameKey="name" innerRadius={62} outerRadius={88} paddingAngle={4}>{resultData.map((_:any,i:number)=><Cell key={i} fill={palette[i%palette.length]}/>)}</Pie><Tooltip contentStyle={{background:"#ffffff",border:"1px solid #e3eae5",borderRadius:10,color:"#26342c",boxShadow:"0 5px 18px rgba(20,40,28,.08)"}}/></PieChart></ResponsiveContainer></div><div className="legend">{resultData.map((r:any,i:number)=><div key={r.name}><span style={{background:palette[i%palette.length]}}/>{r.name}<b>{r.value.toLocaleString()}</b></div>)}</div></div> : <EmptyState message="The results endpoint returned no outcome distribution."/>}
      </ChartCard>
      <ChartCard title="Top attacking teams" subtitle="Highest scoring teams in the dataset" wide>
        {topTeams.length ? <div className="ranking-list">{topTeams.map((team:any,i:number)=><div className="ranking-row" key={labelOf(team,["team_id","team","name"],String(i))}><div className="rank-number">{String(i+1).padStart(2,"0")}</div><div className="rank-name">{labelOf(team,["team_name","team","name"])}</div><div className="rank-bar"><span style={{width:`${Math.max(8,firstNumber(team,["goals_scored","goals_for","total_goals","goals"])/Math.max(1,...topTeams.map((t:any)=>firstNumber(t,["goals_scored","goals_for","total_goals","goals"])))*100)}%`}}/></div><strong>{firstNumber(team,["goals_scored","goals_for","total_goals","goals"]).toLocaleString()}</strong></div>)}</div> : <EmptyState message="No top-team statistics returned."/>}
      </ChartCard>
    </div>
    <div className="insight-strip"><div className="insight-icon"><Trophy size={19}/></div><div><strong>From raw results to predictive insight</strong><p>MatchIQ combines relational data, SQL analytics and machine-learning predictions in one football intelligence workspace.</p></div><div className="insight-tag">DATA → INSIGHT</div></div>
  </div>;
}
