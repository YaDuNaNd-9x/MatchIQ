import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";

export const metadata: Metadata = {
  title: "MatchIQ | Football Analytics",
  description: "Explore five seasons of Premier League data, club performance and machine-learning match predictions.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><div className="app-shell"><Sidebar/><main className="main-area"><Header/><div className="page-content">{children}</div><footer className="footer">MATCHIQ <span>•</span> FOOTBALL ANALYTICS <span className="footer-right">Historical EPL data: 2020/21–2024/25</span></footer></main></div></body></html>;
}
