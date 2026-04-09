import { ChatWidget } from "@/components/chat-widget";

export default function Home() {
  return (
    <main className="relative flex h-screen w-full flex-col items-center overflow-hidden bg-[#ffffff] dark:bg-[#000000] transition-colors duration-300">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] rounded-full bg-blue-50/30 dark:bg-blue-900/10 blur-[120px]" />
        <div className="absolute top-[20%] -right-[10%] w-[35%] h-[35%] rounded-full bg-purple-50/30 dark:bg-purple-900/10 blur-[120px]" />
      </div>

      <div className="relative z-10 flex w-full max-w-4xl flex-1 flex-col px-4 pt-6 pb-6 sm:px-6 lg:px-8 overflow-hidden">
        {/* Compact Header for Screen Fit */}
        <header className="mb-6 flex flex-col items-center text-center animate-in fade-in slide-in-from-top duration-700">
          <h1 className="mb-2 text-2xl font-extrabold tracking-tight text-gray-900 dark:text-gray-50 md:text-3xl">
            ShieldBase Assistant
          </h1>
          <p className="max-w-md text-sm text-gray-400 dark:text-gray-500 font-normal leading-tight">
            Personalized insurance guidance. Simple, fast, and secure.
          </p>
        </header>


        {/* Chat Area - Flexible to occupy remaining space */}
        <div className="flex-1 w-full min-h-0 overflow-hidden animate-in fade-in zoom-in-95 duration-1000 delay-200">
          <ChatWidget />
        </div>
      </div>
    </main>
  );
}


