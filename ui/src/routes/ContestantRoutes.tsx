import { Routes, Route, Navigate } from "react-router-dom";
import { ProtectedRoute } from "@/components/ProtectedRoute";

import WaitingPage from "@/pages/contestant/WaitingPage";
import LamNongChungPage from "@/pages/contestant/LamNongChungPage";
import LamNongCaNhanPage from "@/pages/contestant/LamNongCaNhanPage";
import VuotDeoPage from "@/pages/contestant/VuotDeoPage";
import ButPhaPage from "@/pages/contestant/ButPhaPage";
import NuocRutChungPage from "@/pages/contestant/NuocRutChungPage";
import NuocRutCaNhanPage from "@/pages/contestant/NuocRutCaNhanPage";
import GameAccessPage from "@/pages/contestant/GameAccessPage";


const ContestantRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/contestant/waiting" replace />} />
            <Route path="/waiting" element={<WaitingPage />} />
            <Route path="/access" element={<GameAccessPage />} />
            <Route
                path="/lnc/:playerCode"
                element={
                    <ProtectedRoute>
                        <LamNongChungPage />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/lncn/:playerCode"
                element={
                    <ProtectedRoute>
                        <LamNongCaNhanPage />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/vd/:playerCode"
                element={
                    <ProtectedRoute>
                        <VuotDeoPage />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/bp/:playerCode"
                element={
                    <ProtectedRoute>
                        <ButPhaPage />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/nrc/:playerCode"
                element={
                    <ProtectedRoute>
                        <NuocRutChungPage />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/nrcn/:playerCode"
                element={
                    <ProtectedRoute>
                        <NuocRutCaNhanPage />
                    </ProtectedRoute>
                }
            />

            {/* fallback */}
            <Route path="*" element={<Navigate to="/contestant/waiting" replace />} />
        </Routes>
    );
};

export default ContestantRoutes;