"use client";
import { usePathname } from "next/navigation";

const titles: Record<string, string> = {
  "/": "Overview",
  "/standings": "League standings",
  "/teams": "Team analytics",
  "/matches": "Match explorer",
  "/predictor": "Match predictor",
};
export default function Header() {
  const path = usePathname();
  const title = titles[path] || "Workspace";
  return <header className="topbar">
    <div><div className="breadcrumb">MATCHIQ <span>/</span> {title}</div><h1>{title}</h1></div>
    <div className="topbar-right"><div className="data-status"><span className="live-dot"/> Connected workspace</div><div className="avatar" aria-label="MatchIQ workspace">MI</div></div>
  </header>;
}
