"use client";

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
    <div className="my-4 w-full md:max-w-[85%] rounded-md border border-gray-300 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900 overflow-hidden">
      <div className="bg-gray-50 dark:bg-gray-950 px-6 py-4 border-b border-gray-200 dark:border-gray-800">
        <h3 className="text-base font-semibold text-gray-900 dark:text-white">
          {quote.insurance_type.charAt(0).toUpperCase() + quote.insurance_type.slice(1)} Quote Estimate
        </h3>
      </div>

      <div className="p-6">
        <div className="mb-6 flex flex-col items-start rounded-md bg-blue-50 dark:bg-blue-900/20 p-5 border border-blue-100 dark:border-blue-900">
          <p className="text-xs font-semibold text-blue-700 dark:text-blue-400 uppercase tracking-wide mb-1">
            Estimated Monthly Premium
          </p>
          <span className="text-3xl font-bold text-gray-900 dark:text-white">
            {quote.estimated_premium}
          </span>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">{quote.notes}</p>
        </div>

        <div className="mb-6">
          <h4 className="mb-3 text-sm font-semibold text-gray-900 dark:text-gray-100 border-b border-gray-200 dark:border-gray-800 pb-2">
            Coverage Details
          </h4>
          <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(quote.summary).map(([key, value]) => (
              <div key={key} className="flex flex-col">
                <dt className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-widest mb-1">
                  {key.replace(/_/g, " ")}
                </dt>
                <dd className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {value}
                </dd>
              </div>
            ))}
          </dl>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row mt-8 pt-4 border-t border-gray-200 dark:border-gray-800">
          <button
            onClick={onAccept}
            className="flex-1 rounded-md bg-blue-600 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-offset-2"
          >
            Accept Quote
          </button>
          
          <div className="flex flex-1 gap-3">
            <button
              onClick={onAdjust}
              className="flex-1 rounded-md border border-gray-300 bg-white px-4 py-2 font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-offset-2 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700"
            >
              Adjust
            </button>
            <button
              onClick={onRestart}
              className="flex-1 rounded-md border border-gray-300 bg-white px-4 py-2 font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-offset-2 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700"
            >
              Restart
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
