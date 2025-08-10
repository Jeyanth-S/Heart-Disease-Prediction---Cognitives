import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import Dashboard from "./Dashboard";
import Prediction from "./Prediction";
import Researcher from "./Researcher";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/prediction" element={<Prediction />} />
        <Route path="/researcher" element={<Researcher />} />
      </Routes>
    </Router>
  );
}

export default App;
