import { useState } from "react";
import { grabArticle } from "./getPageArticle.js";

function App() {
 const [message, setMessage] = useState("hello world");

 return (
  <div className="p-2">
   {message}
   <button
    className="bg-slate-800 rounded-xl px-2 py-1 text-slate-300"
    onClick={async () => setMessage(await grabArticle())}
   >
    Load Article
   </button>
  </div>
 );
}

export default App;
