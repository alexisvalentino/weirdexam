"use client";

import { useEffect, useRef, useState } from "react";
import { ChatMessage, Message } from "./chat-message";
import { QuoteCard, QuoteData } from "./quote-card";

function generateId() {
  return Math.random().toString(36).substring(2, 9);
}

export function ChatWidget() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "init",
      role: "assistant",
      content:
        "Hello! I am the **ShieldBase Assistant**. I can answer questions about our auto, home, and life insurance policies, or help you get a personalized quote. How can I assist you today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [activeQuote, setActiveQuote] = useState<QuoteData | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [sessionId, setSessionId] = useState(() => generateId());

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, activeQuote, isTyping]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || isTyping) return;

    const userMsg: Message = {
      id: generateId(),
      role: "user",
      content: text,
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);
    setActiveQuote(null); // Clear quote if user types something new

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          message: userMsg.content,
          session_id: sessionId 
        }),
      });

      if (!res.ok) {
        throw new Error("Backend offline");
      }

      const data = await res.json();
      
      setIsTyping(false);

      if (data.quote_result) {
        setActiveQuote(data.quote_result);
        setMessages((prev) => [
          ...prev,
          {
            id: generateId(),
            role: "assistant",
            content: data.reply || "I've generated a quote based on your details:",
            isQuote: true,
          },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            id: generateId(),
            role: "assistant",
            content: data.reply || "No reply found.",
          },
        ]);
      }
    } catch (err) {
      console.error(err);
      setIsTyping(false);
      setMessages((prev) => [
        ...prev,
        {
          id: generateId(),
          role: "assistant",
          content: "I'm currently experiencing issues right now, please try again later.",
        },
      ]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(input);
    setInput("");
  };

  // Handlers for quote actions
  const handleQuoteAccept = () => {
    sendMessage("I want to accept this quote.");
  };

  const handleQuoteAdjust = () => {
    sendMessage("I need to adjust some details.");
  };

  const handleQuoteRestart = () => {
    sendMessage("Let's restart the quote.");
  };

  const resetChat = () => {
    setMessages([
      {
        id: "init",
        role: "assistant",
        content: "Chat reset. How can I help you from scratch today?",
      },
    ]);
    setInput("");
    setActiveQuote(null);
    setSessionId(generateId());
  };

  return (
    <div className="flex bg-transparent h-full w-full flex-col overflow-hidden rounded-[2.5rem] border border-gray-100 bg-white/70 shadow-[0_20px_50px_rgba(0,0,0,0.05)] backdrop-blur-xl dark:border-white/5 dark:bg-gray-950/80">
      {/* Header - Transparent and Minimal */}
      <div className="flex items-center justify-between border-b border-gray-100/50 px-8 py-5 dark:border-white/5 bg-transparent">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="absolute inset-0 animate-pulse rounded-full bg-blue-400 opacity-20 blur-sm" />
            <img 
              src="/apple-touch-icon.png" 
              alt="ShieldBase Logo" 
              className="relative h-10 w-10 rounded-xl overflow-hidden object-cover ring-2 ring-white/50 dark:ring-gray-800" 
            />
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-900 dark:text-white">
              ShieldBase
            </h2>
            <div className="flex items-center gap-1.5">
              <div className="h-1.5 w-1.5 rounded-full bg-green-500" />
              <p className="text-xs font-medium text-gray-400 dark:text-gray-500">
                Online & Ready to Help
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
            <button 
              onClick={resetChat}
              title="Reset Conversation"
              className="group h-10 w-10 flex items-center justify-center rounded-full bg-gray-100/80 transition-all hover:bg-red-50 hover:scale-105 active:scale-95 dark:bg-gray-800/80 dark:hover:bg-red-900/20 cursor-pointer"
            >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-gray-500 transition-colors group-hover:text-red-500 dark:text-gray-400">
                  <path d="M12 2C6.477 2 2 6.477 2 12C2 17.523 6.477 22 12 22C17.523 22 22 17.523 22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M22 2V8H16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M22 8L18 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
            </button>
        </div>
      </div>

      {/* Messages Area - More Spacing */}
      <div className="flex-1 overflow-y-auto px-8 py-6 scrollbar-hide">
        <div className="flex flex-col justify-end min-h-full pb-8 gap-2">
          {messages.map((m) => (
            <ChatMessage key={m.id} message={m} />
          ))}
          
          {activeQuote && (
            <QuoteCard
              quote={activeQuote}
              onAccept={handleQuoteAccept}
              onAdjust={handleQuoteAdjust}
              onRestart={handleQuoteRestart}
            />
          )}
          
          {isTyping && (
            <ChatMessage
              message={{ id: "typing", role: "assistant", content: "" }}
              isTyping={true}
            />
          )}
          <div ref={messagesEndRef} className="h-2" />
        </div>
      </div>

      {/* Input Area - Pill Shaped */}
      <div className="px-8 pb-8 pt-2">
        <div className="relative">
          <form
            onSubmit={handleSubmit}
            className="group relative flex items-center"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isTyping}
              placeholder={isTyping ? "Agent is thinking..." : "Ask anything about insurance..."}
              className="h-14 w-full flex-1 rounded-[1.75rem] border border-gray-200 bg-white px-8 pr-16 text-[15px] text-gray-900 shadow-[0_4px_20px_rgba(0,0,0,0.02)] transition-all placeholder:text-gray-400 focus:border-blue-500/50 focus:outline-none focus:ring-4 focus:ring-blue-500/5 disabled:bg-gray-50/50 dark:border-white/10 dark:bg-gray-900 dark:text-white dark:shadow-none dark:focus:border-blue-400/50"
            />
            <button
              type="submit"
              disabled={!input.trim() || isTyping}
              className="absolute right-2 h-10 w-10 flex items-center justify-center rounded-full bg-blue-600 text-white shadow-lg transition-all hover:bg-blue-700 hover:scale-105 active:scale-95 disabled:bg-gray-300 disabled:opacity-50 dark:bg-blue-500 dark:hover:bg-blue-400 dark:disabled:bg-gray-700"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15.8333 10L4.16667 10M15.8333 10L10.8333 5M15.8333 10L10.8333 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </form>
          <div className="mt-3 flex items-center justify-center gap-1.5">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-gray-400">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M12 16V12M12 8H12.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <p className="text-[11px] text-gray-400 dark:text-gray-500">
                ShieldBase AI can occasionally provide incorrect info. Please verify details.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

