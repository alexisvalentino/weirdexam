"use client";

import { cn } from "@/lib/utils";

export interface QuoteData {
  insurance_type: string;
  summary: Record<string, string>;
  estimated_premium: string;
  notes: string;
}

interface QuoteCardProps {
  quote: QuoteData;
  onAccept: () => void;
  onAdjust: () => void;
  onRestart: () => void;
}

export function QuoteCard({ quote, onAccept, onAdjust, onRestart }: QuoteCardProps) {
  return (
    <div className="my-8 w-full md:max-w-[90%] self-start animate-in fade-in zoom-in-95 duration-500 delay-300">
      <div className="overflow-hidden rounded-[2rem] border border-gray-100 bg-white shadow-[0_10px_30px_rgba(0,0,0,0.04)] dark:border-white/5 dark:bg-gray-900">
        <div className="bg-gray-50/50 dark:bg-white/5 px-8 py-5 border-b border-gray-100 dark:border-white/5">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-blue-500" />
            <h3 className="text-sm font-bold uppercase tracking-wider text-gray-500 dark:text-gray-400">
              {quote.insurance_type} Quote Summary
            </h3>
          </div>
        </div>

        <div className="p-8">
          <div className="mb-8 flex flex-col items-center justify-center rounded-[1.5rem] bg-blue-600 p-8 text-center text-white shadow-lg shadow-blue-500/20">
            <p className="text-xs font-semibold uppercase tracking-widest opacity-80 mb-2">
              Monthly Investment
            </p>
            <span className="text-5xl font-black tracking-tight">
              {quote.estimated_premium}
            </span>
            <div className="mt-4 max-w-sm rounded-full bg-white/10 px-4 py-1.5 text-xs font-medium backdrop-blur-sm">
              {quote.notes}
            </div>
          </div>

          <div className="mb-8 overflow-hidden rounded-[1.5rem] border border-gray-100 dark:border-white/5">
            <div className="grid grid-cols-1 sm:grid-cols-2">
              {Object.entries(quote.summary).map(([key, value], idx) => (
                <div 
                  key={key} 
                  className={cn(
                    "flex flex-col p-5 transition-colors hover:bg-gray-50 dark:hover:bg-white/5",
                    idx % 2 === 0 ? "sm:border-r border-b" : "border-b",
                    "border-gray-100 dark:border-white/5"
                  )}
                >
                  <dt className="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-1">
                    {key.replace(/_/g, " ")}
                  </dt>
                  <dd className="text-sm font-semibold text-gray-900 dark:text-gray-100">
                    {value}
                  </dd>
                </div>
              ))}
            </div>
          </div>

          <div className="flex flex-col gap-4 sm:flex-row">
            <button
              onClick={onAccept}
              className="flex-[2] rounded-full bg-blue-600 px-6 py-4 text-sm font-bold text-white shadow-lg shadow-blue-500/25 transition-all hover:bg-blue-700 hover:scale-[1.02] active:scale-[0.98] focus:outline-none focus:ring-4 focus:ring-blue-500/20"
            >
              Accept & Secure Policy
            </button>
            
            <div className="flex flex-1 gap-3">
              <button
                onClick={onAdjust}
                className="flex-1 rounded-full border border-gray-200 bg-white px-4 py-4 text-sm font-bold text-gray-600 transition-all hover:bg-gray-50 hover:border-gray-300 dark:border-white/10 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
              >
                Adjust
              </button>
              <button
                onClick={onRestart}
                className="flex-1 rounded-full border border-gray-200 bg-white px-4 py-4 text-sm font-bold text-gray-600 transition-all hover:bg-gray-50 hover:border-gray-300 dark:border-white/10 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
              >
                Reset
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

