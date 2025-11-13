import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ContestantRoutes from "./routes/ContestantRoutes";


function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen">
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          {/* Contestant Routes */}
          <Route path="/contestant/*" element={<ContestantRoutes />}/>
        </Routes>
      </div>
    </BrowserRouter>
  );
}


export default App;