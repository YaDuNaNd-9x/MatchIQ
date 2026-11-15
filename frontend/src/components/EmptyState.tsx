import { Database } from "lucide-react";
export default function EmptyState({message="No records returned by the API."}:{message?:string}) {
  return <div className="empty-state"><Database size={24}/><strong>Nothing to show yet</strong><span>{message}</span></div>;
}
