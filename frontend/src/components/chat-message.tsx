"use client";

import { cn } from "@/lib/utils";
import ReactMarkdown from "react-markdown";

export type MessageRole = "user" | "assistant" | "system" | "error";

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  isQuote?: boolean;
}

interface ChatMessageProps {
  message: Message;
  isTyping?: boolean;
}

export function ChatMessage({ message, isTyping }: ChatMessageProps) {
  const isUser = message.role === "user";
  const isError = message.role === "error";

  return (
    <div
      className={cn(
        "flex w-full mt-6 group animate-in fade-in slide-in-from-bottom-2 duration-500",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      {(!isUser || isTyping) && (
        <div className="mr-3 mt-1 flex-shrink-0">
          <div className="h-9 w-9 rounded-xl overflow-hidden bg-gray-900 ring-2 ring-white shadow-sm dark:bg-gray-800 dark:ring-gray-950">
            <img 
              src="/apple-touch-icon.png" 
              alt="ShieldBase Assistant" 
              className="h-full w-full object-cover" 
            />
          </div>
        </div>
      )}
      <div
        className={cn(
          "relative max-w-[85%] md:max-w-[80%] px-5 py-3.5 text-[15px] leading-relaxed shadow-sm transition-all",
          isUser
            ? "bg-blue-600 text-white rounded-[20px] rounded-tr-none hover:shadow-md"
            : isError
            ? "bg-red-50 text-red-900 border border-red-100 rounded-[20px] rounded-tl-none dark:bg-red-950/30 dark:text-red-200 dark:border-red-900/50"
            : "bg-gray-100 text-gray-800 rounded-[20px] rounded-tl-none dark:bg-gray-800/60 dark:text-gray-100 hover:bg-gray-200/50 dark:hover:bg-gray-800/80"
        )}
      >
        {isTyping ? (
          <div className="flex h-6 items-center gap-1.5 px-2">
            <div className="h-1.5 w-1.5 rounded-full bg-blue-500 animate-bounce [animation-delay:-0.3s]" />
            <div className="h-1.5 w-1.5 rounded-full bg-blue-500 animate-bounce [animation-delay:-0.15s]" />
            <div className="h-1.5 w-1.5 rounded-full bg-blue-500 animate-bounce" />
          </div>
        ) : (
          <div className="w-full break-words max-w-none text-gray-800 dark:text-gray-100">
            <ReactMarkdown
              components={{
                p: ({ node, ...props }) => <p className="mb-3 last:mb-0 leading-relaxed" {...props} />,
                strong: ({ node, ...props }) => <strong className="font-bold text-gray-950 dark:text-white" {...props} />,
                ul: ({ node, ...props }) => <ul className="list-disc pl-5 mb-3 space-y-1" {...props} />,
                ol: ({ node, ...props }) => <ol className="list-decimal pl-5 mb-3 space-y-1" {...props} />,
                li: ({ node, ...props }) => <li className="mb-1" {...props} />,
                a: ({ node, ...props }) => <a className="text-blue-600 font-medium underline decoration-2 underline-offset-2 transition-colors hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300" {...props} />,
                code: ({ node, ...props }) => <code className="rounded bg-gray-200 px-1.5 py-0.5 text-sm font-mono text-gray-900 dark:bg-gray-700 dark:text-gray-100" {...props} />,
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}

        
        {/* Subtle timestamp or status on hover could go here */}
      </div>
    </div>
  );
}

