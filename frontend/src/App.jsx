import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import CitizenSafety from "./pages/CitizenSafety";

export default function App() {
  return (
    <BrowserRouter>
      <nav className="bg-blue-700 text-white text-sm px-6 py-2 flex gap-4">
        <Link to="/" className="hover:underline">Authority Dashboard</Link>
        <Link to="/citizen" className="hover:underline">Citizen Safety Page</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/citizen" element={<CitizenSafety />} />
      </Routes>
    </BrowserRouter>
  );
}
