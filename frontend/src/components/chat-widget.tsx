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
        body: JSON.stringify({ message: userMsg.content }),
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

  return (
    <div className="flex h-[80vh] min-h-[500px] w-full flex-col overflow-hidden rounded-md border border-gray-300 bg-gray-50 shadow-sm dark:border-gray-800 dark:bg-[#0a0a0e]">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 bg-white px-6 py-4 dark:border-gray-800 dark:bg-gray-900">
        <div className="flex items-center gap-3">
          <img 
            src="/apple-touch-icon.png" 
            alt="ShieldBase Logo" 
            className="h-8 w-8 rounded-sm overflow-hidden object-cover" 
          />
          <div>
            <h2 className="text-base font-semibold text-gray-900 dark:text-white">
              ShieldBase Sales Agent
            </h2>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Powered by LangGraph
            </p>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-4 scrollbar-hide bg-gray-50 dark:bg-[#0a0a0e]">
        <div className="flex flex-col justify-end min-h-full pb-4">
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

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-gray-900">
        <form
          onSubmit={handleSubmit}
          className="flex items-center gap-3"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isTyping}
            placeholder={isTyping ? "Agent is typing..." : "Type your message..."}
            className="flex-1 rounded-md border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100 disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-blue-500"
          />
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className="rounded-md bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-blue-400 disabled:opacity-50"
          >
            Send
          </button>
        </form>
        <p className="mt-2 text-center text-xs text-gray-500 dark:text-gray-400">
          ShieldBase uses AI technology. Verify important information with an agent before purchasing.
        </p>
      </div>
    </div>
  );
}
