import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { ProtectedRoute } from "./components/ProtectedRoute";
import LoginPage from "@/pages/contestant/LoginPage";
import LamNongChungPage from "@/pages/contestant/LamNongChungPage";
import LamNongCaNhanPage from "@/pages/contestant/LamNongCaNhanPage";
import VuotDeoPage from "@/pages/contestant/VuotDeoPage";
import ButPhaPage from "./pages/contestant/ButPhaPage";
import NuocRutCaNhanPage from "./pages/contestant/NuocRutCaNhanPage";
import NuocRutChungPage from "./pages/contestant/NuocRutChungPage";
import WaitingPage from "./pages/contestant/WaitingPage";


function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/contestant/waiting" element={<WaitingPage />} />

          <Route
            path="/contestant/lnc/:playerCode"
            element={
              <ProtectedRoute>
                <LamNongChungPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/contestant/lncn/:playerCode"
            element={
              <ProtectedRoute>
                <LamNongCaNhanPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/contestant/vd/:playerCode"
            element={
              <ProtectedRoute>
                <VuotDeoPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/contestant/bp/:playerCode"
            element={
              <ProtectedRoute>
                <ButPhaPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/contestant/nrc/:playerCode"
            element={
              <ProtectedRoute>
                <NuocRutChungPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/contestant/nrcn/:playerCode"
            element={
              <ProtectedRoute>
                <NuocRutCaNhanPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}


export default App;