import { useState, useEffect } from "react";
import { getUsers } from "../services/api";
import { Search, UserCheck } from "lucide-react";

export default function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const data = await getUsers(0, 100);
        setUsers(data);
      } catch (err) {
        console.error("Failed to fetch users:", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchUsers();
  }, []);

  const filteredUsers = users.filter((user) =>
    user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.department.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.role.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full text-[#9ca3af]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2563eb] mr-3"></div>
        Loading User Directory...
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-[#f9fafb]">Enterprise Directory</h1>
          <p className="text-[#9ca3af] mt-1">Manage users and entity baseline profiles</p>
        </div>
        
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-[#6b7280]" />
          </div>
          <input
            type="text"
            className="block w-72 pl-10 pr-3 py-2 border border-[#374151] rounded-lg leading-5 bg-[#1f2937] text-[#f9fafb] placeholder-[#6b7280] focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] sm:text-sm"
            placeholder="Search by name, dept, or role..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-[#111827] border border-[#1f2937] rounded-xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#0b1220] border-b border-[#1f2937] text-xs uppercase text-[#9ca3af] tracking-wider font-semibold">
                <th className="px-6 py-4">User ID</th>
                <th className="px-6 py-4">Name</th>
                <th className="px-6 py-4">Department</th>
                <th className="px-6 py-4">Role</th>
                <th className="px-6 py-4">Country</th>
                <th className="px-6 py-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1f2937]">
              {filteredUsers.length > 0 ? (
                filteredUsers.map((user) => (
                  <tr key={user.id} className="hover:bg-[#1f2937] hover:bg-opacity-50 transition-colors">
                    <td className="px-6 py-4 font-mono text-xs text-[#9ca3af]">#{user.id}</td>
                    <td className="px-6 py-4 text-sm font-medium text-[#f9fafb]">{user.name}</td>
                    <td className="px-6 py-4 text-sm text-[#d1d5db]">{user.department}</td>
                    <td className="px-6 py-4 text-sm text-[#d1d5db]">{user.role}</td>
                    <td className="px-6 py-4 text-sm text-[#d1d5db]">{user.country}</td>
                    <td className="px-6 py-4">
                      <span className="flex items-center text-xs text-[#22c55e] font-medium">
                        <UserCheck className="w-4 h-4 mr-1" />
                        Monitored
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center text-[#9ca3af] text-sm">
                    No users found matching "{searchTerm}"
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
