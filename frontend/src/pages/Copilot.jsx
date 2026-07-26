import { useState, useRef, useEffect } from "react";
import { askCopilot } from "../services/api";

export default function Copilot() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello Analyst. I am your AI Security Copilot. I have full context of the UEBA telemetry, recent alerts, and ML classifications. How can I assist you in investigating threats today?"
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      // Calls the backend endpoint we implemented in Milestone 13
      const response = await askCopilot(userMessage);
      
      setMessages(prev => [...prev, { 
        role: "assistant", 
        content: response.answer || "I'm sorry, I could not generate a response." 
      }]);
    } catch (err) {
      console.error("Copilot Error:", err);
      setMessages(prev => [...prev, { 
        role: "assistant", 
        content: "⚠️ **Error:** Unable to reach the AI Copilot service. Please ensure the backend server is running." 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Basic markdown parser for bold text returned by Gemini/Mock
  const renderMessageContent = (text) => {
    // Split by ** for bold text
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, index) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return <strong key={index} className="text-white">{part.slice(2, -2)}</strong>;
      }
      return <span key={index}>{part}</span>;
    });
  };

  return (
    <div className="max-w-[1200px] mx-auto h-[calc(100vh-6rem)] flex flex-col p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-[#f9fafb] flex items-center gap-2">
          <svg className="w-6 h-6 text-[#2563eb]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          AI Security Copilot
        </h1>
        <p className="text-[#9ca3af] text-sm mt-1">
          Powered by Gemini AI Model (Flash-2.5). Context-aware threat investigation.
        </p>
      </div>

      {/* Chat Window */}
      <div className="flex-1 bg-[#111827] border border-[#1f2937] rounded-t-xl overflow-y-auto p-6 space-y-6 shadow-sm">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`flex gap-4 max-w-[80%] ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
              {/* Avatar */}
              <div className={`w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center font-bold text-sm ${
                msg.role === "user" ? "bg-[#2563eb] text-white" : "bg-[#1f2937] text-[#2563eb] border border-[#374151]"
              }`}>
                {msg.role === "user" ? "YOU" : "AI"}
              </div>
              
              {/* Bubble */}
              <div className={`p-4 rounded-2xl whitespace-pre-wrap text-sm leading-relaxed ${
                msg.role === "user" 
                  ? "bg-[#2563eb] text-white rounded-tr-sm" 
                  : "bg-[#1f2937] text-[#f9fafb] rounded-tl-sm border border-[#374151]"
              }`}>
                {renderMessageContent(msg.content)}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex gap-4 max-w-[80%]">
              <div className="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center font-bold text-sm bg-[#1f2937] text-[#2563eb] border border-[#374151]">
                AI
              </div>
              <div className="p-4 rounded-2xl bg-[#1f2937] text-[#9ca3af] rounded-tl-sm border border-[#374151] flex items-center gap-2">
                <span className="w-2 h-2 bg-[#2563eb] rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></span>
                <span className="w-2 h-2 bg-[#2563eb] rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
                <span className="w-2 h-2 bg-[#2563eb] rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-[#111827] border-x border-b border-[#1f2937] p-4 rounded-b-xl shadow-sm">
        <form onSubmit={handleSend} className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            placeholder="Ask about alerts, request summaries, or query user risk profiles..."
            className="w-full bg-[#0b1220] border border-[#374151] rounded-lg py-4 pl-4 pr-16 text-sm text-[#f9fafb] placeholder-[#9ca3af] focus:outline-none focus:border-[#2563eb] disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="absolute right-2 top-2 bottom-2 bg-[#2563eb] hover:bg-[#1d4ed8] text-white rounded-md px-4 flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg className="w-5 h-5 transform rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </form>
        
        <div className="flex gap-2 mt-3 overflow-x-auto pb-1 custom-scrollbar">
          {["Why was User X flagged?", "Summarize recent threats", "Recommend actions for BruteForce"].map(suggestion => (
            <button
              key={suggestion}
              type="button"
              onClick={() => setInput(suggestion)}
              className="whitespace-nowrap px-3 py-1 bg-[#1f2937] hover:bg-[#374151] text-[#9ca3af] hover:text-white rounded-full text-xs transition-colors border border-[#374151]"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
