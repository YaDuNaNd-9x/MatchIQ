export default function Loading({label="Loading analytics..."}:{label?:string}) {
  return <div className="loading" role="status"><span className="spinner"/>{label}</div>;
}
