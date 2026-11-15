"use client";
import { ReactNode } from "react";
export default function ChartCard({title,subtitle,children,wide=false}:{title:string;subtitle:string;children:ReactNode;wide?:boolean}) {
  return <section className={`panel chart-panel ${wide ? "wide" : ""}`}><div className="panel-heading"><div><h3>{title}</h3><p>{subtitle}</p></div></div>{children}</section>;
}
