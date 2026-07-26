export default function Timeline({ events }) {
  if (!events || events.length === 0) {
    return (
      <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
        <h2 className="text-lg font-bold text-[#f9fafb] mb-4">Event Timeline</h2>
        <div className="text-center text-[#9ca3af] text-sm py-8">No events to display.</div>
      </div>
    );
  }

  return (
    <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
      <h2 className="text-lg font-bold text-[#f9fafb] mb-6">Recent Activity Stream</h2>
      
      <div className="relative pl-4 border-l border-[#1f2937] space-y-6">
        {events.slice(0, 5).map((event, idx) => (
          <div key={idx} className="relative">
            {/* Timeline Dot */}
            <div className="absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full bg-[#2563eb] border-2 border-[#111827]" />
            
            <div className="mb-1 text-xs text-[#9ca3af]">
              {new Date(event.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
            </div>
            
            <div className="bg-[#0b1220] border border-[#1f2937] rounded-lg p-3 inline-block min-w-[200px]">
              <span className="font-semibold text-sm text-[#f9fafb] block">
                {event.action}
              </span>
              <span className="text-xs text-[#9ca3af] block mt-1">
                {event.resource} • {event.ip_address}
              </span>
            </div>
            
            {idx < events.length - 1 && (
              <div className="absolute left-[3px] top-6 w-px h-8 bg-gradient-to-b from-[#2563eb] to-transparent hidden" />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
