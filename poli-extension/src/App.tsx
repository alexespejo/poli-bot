import { useState } from "react";
import { grabArticle } from "./getPageArticle.js";
import poliTheDinosaur from "../src/assets/poli-the-dinosaur-headshot.png";

function App() {
 const [message, setMessage] = useState("hello world");
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
   context: input,
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
  fetch("http://127.0.0.1:5000/summarize_text", options)
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
  setIsTyping(false);
 };

 return (
  <div className="p-2 h-screen">
   {message}

   <button
    className="bg-slate-800 rounded-xl px-2 py-1 text-slate-300"
    onClick={async () => setMessage(await grabArticle())}
   >
    Load Article
   </button>
   <section className="container mx-auto p-5 fixed inset-0">
    <div className=" h-full flex flex-col">
     <div className="p-5 pb-8 flex-grow overflow-auto">
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
           <div className="w-14 rounded-full">
            <img
             className="rounded-full mask mask-squircle border-2 "
             src={
              msg.role === "assistant"
               ? poliTheDinosaur
               : "https://t3.ftcdn.net/jpg/05/91/98/78/360_F_591987899_VaB4GHecB5lTITiqmvC0dhmrrNUsbPPt.jpg"
             }
            />
           </div>
          </div>
          <div
           className={`chat-bubble ${
            msg.role === "assistant" ? "chat-bubble-info" : "bg-slate-700"
           }`}
          >
           {msg.content}
          </div>
         </div>
        );
       })}
     </div>
     <form
      className="form-control m-5 items-center"
      onSubmit={(e) => handleSubmit(e)}
     >
      <div className="input-group max-w-full w-[800px] relative ">
       <div className="flex items-center">
        {isTyping && (
         <small className="absolute -top-5 left-0.5 animate-pulse">
          BOT is Typing...
         </small>
        )}

        <input
         type="text"
         placeholder="Ask PoliBot..."
         className="input input-bordered flex-grow flex-end italic"
         required
         onChange={(e) => setInput(e.target.value)}
        />
        <button className="btn btn-square" type="submit">
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
     </form>
    </div>
   </section>
  </div>
 );
}

export default App;
