"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, ChevronLeft, CircleDot, LayoutDashboard, Shield, Sparkles, Table2 } from "lucide-react";
import { useState } from "react";

const links = [
  { href: "/", label: "Overview", icon: LayoutDashboard },
  { href: "/standings", label: "League standings", icon: Table2 },
  { href: "/teams", label: "Team analytics", icon: Shield },
  { href: "/matches", label: "Match explorer", icon: CircleDot },
  { href: "/predictor", label: "Match predictor", icon: Sparkles },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  return <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
    <div className="brand">
      <div className="brand-mark"><Activity size={21}/></div>
      {!collapsed && <div><strong>Match<span>IQ</span></strong><small>FOOTBALL INTELLIGENCE</small></div>}
    </div>
    {!collapsed && <div className="nav-caption">WORKSPACE</div>}
    <nav aria-label="Main navigation">{links.map(({href,label,icon:Icon}) => {
      const active = pathname === href || (href !== "/" && pathname.startsWith(href));
      return <Link key={href} href={href} className={`nav-link ${active ? "active" : ""}`} title={collapsed ? label : undefined} aria-current={active ? "page" : undefined}>
        <Icon size={18}/>{!collapsed && <span>{label}</span>}{active && !collapsed && <i/>}
      </Link>;
    })}</nav>
    <div className="sidebar-bottom">
      {!collapsed && <div className="season-chip"><span className="live-dot"/> Historical EPL data<br/><small>2020/21 — 2024/25</small></div>}
      <button className="collapse-btn" onClick={() => setCollapsed(!collapsed)} aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}><ChevronLeft size={16}/>{!collapsed && "Collapse sidebar"}</button>
    </div>
  </aside>;
}
