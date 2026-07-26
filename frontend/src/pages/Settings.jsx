import { useState } from "react";
import { Save, Bell, Shield, Sliders } from "lucide-react";

export default function Settings() {
  const [threshold, setThreshold] = useState(80);
  const [retention, setRetention] = useState(30);

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-10">
      <div>
        <h1 className="text-2xl font-bold text-[#f9fafb]">Platform Settings</h1>
        <p className="text-[#9ca3af] mt-1">Configure UEBA detection thresholds and system preferences</p>
      </div>

      <div className="bg-[#111827] border border-[#1f2937] rounded-xl overflow-hidden shadow-sm">
        
        {/* ML Configuration Section */}
        <div className="p-6 border-b border-[#1f2937]">
          <div className="flex items-center space-x-2 mb-6">
            <Sliders className="w-5 h-5 text-[#2563eb]" />
            <h2 className="text-lg font-bold text-[#f9fafb]">Machine Learning Configuration</h2>
          </div>
          
          <div className="space-y-6 max-w-2xl">
            <div>
              <label className="flex justify-between text-sm font-medium text-[#d1d5db] mb-2">
                <span>Critical Alert Risk Threshold</span>
                <span className="text-[#3b82f6]">{threshold}</span>
              </label>
              <input 
                type="range" 
                min="50" max="95" 
                value={threshold} 
                onChange={(e) => setThreshold(e.target.value)}
                className="w-full h-2 bg-[#374151] rounded-lg appearance-none cursor-pointer accent-[#2563eb]"
              />
              <p className="text-xs text-[#6b7280] mt-2">
                Events scored above {threshold} will be tagged as CRITICAL and trigger automated playbook responses.
              </p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-[#d1d5db] mb-2">Isolation Forest Retraining Interval (Days)</label>
              <select className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-[#374151] bg-[#1f2937] text-[#f9fafb] focus:outline-none focus:ring-[#2563eb] focus:border-[#2563eb] sm:text-sm rounded-md">
                <option>Every 24 hours</option>
                <option selected>Every 7 days</option>
                <option>Every 30 days</option>
                <option>Manual Only</option>
              </select>
            </div>
          </div>
        </div>

        {/* Security Automation Section */}
        <div className="p-6 border-b border-[#1f2937]">
          <div className="flex items-center space-x-2 mb-6">
            <Shield className="w-5 h-5 text-[#ef4444]" />
            <h2 className="text-lg font-bold text-[#f9fafb]">Automated Response Playbooks</h2>
          </div>
          
          <div className="space-y-4">
            <label className="flex items-start space-x-3 cursor-pointer group">
              <div className="flex items-center h-5">
                <input type="checkbox" defaultChecked className="w-4 h-4 rounded border-[#374151] text-[#2563eb] bg-[#1f2937] focus:ring-[#2563eb] focus:ring-offset-[#111827]" />
              </div>
              <div>
                <span className="block text-sm font-medium text-[#d1d5db] group-hover:text-[#f9fafb]">Auto-suspend compromised accounts</span>
                <span className="block text-xs text-[#6b7280]">Temporarily disable SSO for users exceeding the Critical threshold.</span>
              </div>
            </label>

            <label className="flex items-start space-x-3 cursor-pointer group">
              <div className="flex items-center h-5">
                <input type="checkbox" defaultChecked className="w-4 h-4 rounded border-[#374151] text-[#2563eb] bg-[#1f2937] focus:ring-[#2563eb] focus:ring-offset-[#111827]" />
              </div>
              <div>
                <span className="block text-sm font-medium text-[#d1d5db] group-hover:text-[#f9fafb]">Isolate malicious endpoints</span>
                <span className="block text-xs text-[#6b7280]">Dispatch EDR signal to network-isolate devices exhibiting Lateral Movement.</span>
              </div>
            </label>
          </div>
        </div>

        {/* Notifications Section */}
        <div className="p-6">
          <div className="flex items-center space-x-2 mb-6">
            <Bell className="w-5 h-5 text-[#eab308]" />
            <h2 className="text-lg font-bold text-[#f9fafb]">Notifications & Storage</h2>
          </div>
          
          <div className="space-y-6 max-w-2xl">
            <div>
              <label className="block text-sm font-medium text-[#d1d5db] mb-2">SOC Alert Channels</label>
              <div className="flex space-x-4">
                <input type="email" placeholder="soc-team@company.com" className="flex-1 block w-full pl-3 pr-3 py-2 border border-[#374151] bg-[#1f2937] text-[#f9fafb] placeholder-[#6b7280] rounded-md focus:outline-none focus:ring-[#2563eb] focus:border-[#2563eb] sm:text-sm" />
                <input type="text" placeholder="Slack Webhook URL" className="flex-1 block w-full pl-3 pr-3 py-2 border border-[#374151] bg-[#1f2937] text-[#f9fafb] placeholder-[#6b7280] rounded-md focus:outline-none focus:ring-[#2563eb] focus:border-[#2563eb] sm:text-sm" />
              </div>
            </div>

            <div>
              <label className="flex justify-between text-sm font-medium text-[#d1d5db] mb-2">
                <span>Data Retention (Days)</span>
                <span className="text-[#3b82f6]">{retention}</span>
              </label>
              <input 
                type="range" 
                min="7" max="365" 
                value={retention} 
                onChange={(e) => setRetention(e.target.value)}
                className="w-full h-2 bg-[#374151] rounded-lg appearance-none cursor-pointer accent-[#2563eb]"
              />
            </div>
          </div>
        </div>
        
        {/* Footer actions */}
        <div className="bg-[#0b1220] p-4 border-t border-[#1f2937] flex justify-end space-x-3">
          <button className="px-4 py-2 text-sm font-medium text-[#d1d5db] hover:text-white bg-transparent border border-[#374151] hover:bg-[#1f2937] rounded-md transition-colors">
            Cancel
          </button>
          <button className="px-4 py-2 text-sm font-medium text-white bg-[#2563eb] hover:bg-[#1d4ed8] rounded-md flex items-center shadow-sm transition-colors">
            <Save className="w-4 h-4 mr-2" />
            Save Configuration
          </button>
        </div>

      </div>
    </div>
  );
}
