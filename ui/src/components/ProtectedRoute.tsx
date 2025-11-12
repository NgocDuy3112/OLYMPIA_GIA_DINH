import { Navigate, useLocation, useParams } from "react-router-dom";

interface ProtectedRouteProps {
    children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const { playerCode } = useParams<{ playerCode: string }>();
    const storedPlayer = localStorage.getItem("playerCode");
    const location = useLocation();

    if (!storedPlayer) {
        return <Navigate to="/login" replace />;
    }

    if (playerCode && playerCode !== storedPlayer) {
        console.warn("Unauthorized access attempt:", location.pathname);
        return <Navigate to="/login" replace />;
    }

    return <>{children}</>;
};