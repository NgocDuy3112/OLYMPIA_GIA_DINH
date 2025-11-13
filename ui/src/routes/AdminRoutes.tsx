import { Routes, Route, Navigate } from "react-router-dom";
import { ProtectedRoute } from "@/components/ProtectedRoute";

import LamNongCaNhanPage from "@/pages/admin/LamNongCaNhanPage";


const AdminRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/admin" replace />} />
            <Route
                path="/lncn"
                element={
                    <ProtectedRoute>
                        <LamNongCaNhanPage />
                    </ProtectedRoute>
                }
            />
        </Routes>
    );
};

export default AdminRoutes;