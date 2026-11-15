import { ReactNode } from "react";
export default function StatCard({label,value,detail,icon,accent="green"}:{label:string;value:string|number;detail:string;icon:ReactNode;accent?:string}) {
  return <article className={`stat-card accent-${accent}`}><div className="stat-top"><span>{label}</span><div className="stat-icon">{icon}</div></div><div className="stat-value">{value}</div><div className="stat-detail">{detail}</div></article>;
}
