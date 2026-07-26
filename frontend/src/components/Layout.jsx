import { Outlet } from "react-router-dom";

import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

function Layout() {
  return (
    <div className="min-h-screen bg-[#0b1220]">
      <Sidebar />
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-1 ml-64 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default Layout;
