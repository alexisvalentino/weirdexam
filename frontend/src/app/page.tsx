import { ChatWidget } from "@/components/chat-widget";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 dark:bg-gray-950 p-4 sm:p-8">
      {/* Hero Content */}
      <div className="z-10 mb-8 flex flex-col items-center text-center">
        <img 
          src="/apple-touch-icon.png" 
          alt="ShieldBase Logo" 
          className="mb-4 h-16 w-16 rounded-md shadow-sm" 
        />
        <h1 className="mb-3 text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-5xl">
          ShieldBase Insurance
        </h1>
        <p className="max-w-[600px] text-lg text-gray-600 dark:text-gray-400 font-medium">
          Get an instant quote for your auto, home, or life insurance policies.
        </p>
      </div>

      <div className="z-10 w-full max-w-4xl">
        <ChatWidget />
      </div>
    </main>
  );
}
