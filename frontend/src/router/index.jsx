import { createBrowserRouter } from "react-router-dom";
import Home from "../pages/Home";
import MainLayout from "../layouts/MainLayout";
import Configuracion from "../pages/Configuracion";
import IpsBloqueadas from "../pages/IpsBloqueadas";
import RutasProtegidas from "../pages/RutasProtegidas";
import Login from "../pages/Login";

const router = createBrowserRouter([
    // Añade fuera del layout principal
    {
        path: "/login",
        element: <Login />,
    },
    {
        path: "/",
        element: <MainLayout />,
        children: [
            { path: "/", element: <Home /> },
            { path: "/configuracion", element: <Configuracion /> },
            { path: "/ips-bloqueadas", element: <IpsBloqueadas /> },
            { path: "/rutas-protegidas", element: <RutasProtegidas /> },
        ],
    },
]);

export default router;
