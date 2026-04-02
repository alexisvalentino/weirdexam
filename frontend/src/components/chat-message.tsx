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
        "flex w-full mt-4",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "max-w-[85%] md:max-w-[75%] px-4 py-3 rounded-md text-[15px] leading-relaxed",
          isUser
            ? "bg-blue-600 text-white"
            : isError
            ? "bg-red-50 text-red-900 border border-red-200 dark:bg-red-950/50 dark:text-red-200 dark:border-red-900"
            : "bg-white text-gray-900 border border-gray-200 dark:bg-gray-900 dark:text-gray-100 dark:border-gray-800"
        )}
      >
        {isTyping ? (
          <div className="flex h-5 items-center gap-1">
            <div className="h-1.5 w-1.5 rounded-full bg-gray-400 animate-pulse" />
            <div className="h-1.5 w-1.5 rounded-full bg-gray-400 animate-pulse delay-150" />
            <div className="h-1.5 w-1.5 rounded-full bg-gray-400 animate-pulse delay-300" />
          </div>
        ) : (
          <div className="w-full break-words">
            <ReactMarkdown
              components={{
                p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
                strong: ({ node, ...props }) => <strong className="font-semibold" {...props} />,
                ul: ({ node, ...props }) => <ul className="list-disc pl-4 mb-2" {...props} />,
                ol: ({ node, ...props }) => <ol className="list-decimal pl-4 mb-2" {...props} />,
                li: ({ node, ...props }) => <li className="mb-1" {...props} />,
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}
