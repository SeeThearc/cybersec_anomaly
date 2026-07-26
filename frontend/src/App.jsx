import { BrowserRouter, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import Alerts from "./pages/Alerts";
import Analytics from "./pages/Analytics";
import Copilot from "./pages/Copilot";
import Dashboard from "./pages/Dashboard";
import Settings from "./pages/Settings";
import Users from "./pages/Users";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="alerts" element={<Alerts />} />
          <Route path="users" element={<Users />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="copilot" element={<Copilot />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
