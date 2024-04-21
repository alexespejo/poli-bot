import { useState, useEffect } from "react";
import TypingAnimation from "./components/TypingAnimation.js";
import { grabArticle } from "./getPageArticle.js";
import meTheDinosaur from "../src/assets/meTheDinosaur.png";
import poliTheDinosaur from "../src/assets/poli-the-dinosaur-headshot.png";

function App() {
 const [article, setArticle] = useState("");
 const [input, setInput] = useState("");

 const [messages, setMessages] = useState([
  {
   content: "test1",
   role: "assistant",
  },
  {
   content: "test2",
   role: "user",
  },
 ]);

 function addResponse(previousMessages: any) {
  const requestData = {
   context: input + " " + article,
  };

  // Options for the fetch request
  const options = {
   method: "POST",
   headers: {
    "Content-Type": "application/json",
   },
   body: JSON.stringify(requestData),
  };

  // Send the fetch request
  fetch("http://127.0.0.1:5000/conversation", options)
   .then((response) => {
    if (response.ok) {
     return response.text(); // Assuming the server returns a text response
    } else {
     throw new Error("Network response was not ok");
    }
   })
   .then((data) => {
    setMessages([
     ...previousMessages,
     {
      content: data,
      role: "assistant",
     },
    ]);
   })
   .then(() => {
    setIsTyping(false);
   })
   .catch((error) => {
    console.error("There was a problem with the fetch operation:", error);
   });
 }
 const [isTyping, setIsTyping] = useState(false);

 const handleSubmit = async (e) => {
  e.preventDefault();

  const newMessage = {
   content: input,
   role: "user",
  };

  const newMessages = [...messages, newMessage];
  setMessages(newMessages);
  setIsTyping(true);
  e.target.reset();

  // const completion = await openai.createChatCompletion({
  //   model: "gpt-3.5-turbo",
  //   messages: [...newMessages],
  // });

  //   setMessages([...newMessages, completion.data.choices[0].message]);
  addResponse(newMessages);
 };

 useEffect(() => {
  const fetchData = async () => {
   const chat = document.querySelector(".chat-island");
   chat.scrollTop = chat.scrollHeight;

   setArticle(await grabArticle());
  };
  fetchData();
 }, [messages]);

 return (
  <div className="h-screen  relative">
   <div className="navbar bg-base-100 shadow-lg navbar-island top-0">
    <div className="navbar-start">
     <h1 className="btn btn-ghost text-3xl">PoliAI</h1>
    </div>
    <div className="avatar navbar-center">
     <div className="w-16 mask mask-squircle bg">
      <img src={poliTheDinosaur} />
     </div>
    </div>
    <div className="navbar-end">
     <button className="btn btn-square btn-ghost">
      <svg
       xmlns="http://www.w3.org/2000/svg"
       fill="none"
       viewBox="0 0 24 24"
       className="inline-block w-5 h-5 stroke-current"
      >
       <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
        d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"
       ></path>
      </svg>
     </button>
    </div>
   </div>
   <div className="chat-island flex flex-col overflow-auto p-4 relative">
    {article.substring(0, 50)}
    <div className="p-1 pb-8 flex-grow ">
     {messages.length &&
      messages.map((msg, i) => {
       return (
        <div
         className={`chat ${
          msg.role === "assistant" ? "chat-start" : "chat-end"
         }`}
         key={i}
        >
         <div className="chat-image avatar">
          <div className="w-10 rounded-full">
           <img
            className="rounded-full mask mask-squircle border-2 "
            src={msg.role === "assistant" ? poliTheDinosaur : meTheDinosaur}
           />
          </div>
         </div>
         <div className="chat-header">
          {msg.role === "assistant" ? "PoliAI" : "You"}
         </div>
         <div
          className={`chat-bubble ${
           msg.role === "assistant" ? "chat-bubble-info" : "bg-slate-700"
          }`}
         >
          <TypingAnimation text={msg.content} delay={1} />
         </div>
        </div>
       );
      })}
     {isTyping && (
      <div className="chat chat-start">
       <div className="chat-image avatar">
        <div className="w-10 rounded-full">
         <img alt="Tailwind CSS chat bubble component" src={poliTheDinosaur} />
        </div>
       </div>
       <div className="chat-header">PoliBot</div>
       <div className="chat-bubble chat-bubble-info">
        <span className="loading loading-dots loading-xs"></span>
       </div>
      </div>
     )}
     <div className="absolute bottom-0 ">hello world</div>
    </div>
   </div>
   <form
    className="form-control items-center  input-island "
    onSubmit={(e) => handleSubmit(e)}
   >
    <div
     className={`input-group max-w-full w-full relative px-5 ${
      isTyping && "tooltip"
     }`}
     data-tip="Wait for PoliBot to respond..."
    >
     <div className="flex items-center">
      <div className="join w-full ">
       <input
        type="text"
        placeholder="Ask PoliBot..."
        className="input input-bordered flex-grow flex-end italic join-item"
        required
        disabled={isTyping}
        onChange={(e) => setInput(e.target.value)}
       />
       <button className="btn btn-square join-item" type="submit">
        <svg
         xmlns="http://www.w3.org/2000/svg"
         className="h-6 w-6"
         fill="currentColor"
         viewBox="0 0 16 16"
        >
         <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576 6.636 10.07Zm6.787-8.201L1.591 6.602l4.339 2.76 7.494-7.493Z" />
        </svg>
       </button>
      </div>
     </div>
    </div>
   </form>
  </div>
 );
}

export default App;
