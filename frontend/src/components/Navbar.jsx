export default function Navbar() {
  return (
    <header className="h-16 bg-[#111827] border-b border-[#1f2937] flex items-center justify-between px-8 text-[#f9fafb] ml-64">
      {/* Search */}
      <div className="flex-1 flex">
        <div className="w-full max-w-lg relative">
          <input
            type="text"
            className="w-full bg-[#0b1220] border border-[#1f2937] rounded-lg py-2 pl-10 pr-4 text-sm text-[#f9fafb] placeholder-[#9ca3af] focus:outline-none focus:border-[#2563eb]"
            placeholder="Search for alerts, users, IP addresses..."
          />
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg className="h-5 w-5 text-[#9ca3af]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-6">
        <div className="flex flex-col text-right">
          <span className="text-sm font-medium">System Status</span>
          <span className="text-xs text-[#22c55e] flex items-center justify-end gap-1">
            <span className="w-2 h-2 rounded-full bg-[#22c55e]"></span> Online
          </span>
        </div>
        
        <button className="relative p-2 text-[#9ca3af] hover:text-white transition-colors">
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-[#ef4444] rounded-full border-2 border-[#111827]"></span>
        </button>
      </div>
    </header>
  );
}
