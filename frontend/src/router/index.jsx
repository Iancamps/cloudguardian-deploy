import { createBrowserRouter } from "react-router-dom";
import Home from "../pages/Home";
import MainLayout from "../layouts/MainLayout";

const router = createBrowserRouter([
    {
        path: "/",
        element: <MainLayout />,  // Aquí va el diseño general (header, footer…)
        children: [
            {
                path: "/",
                element: <Home />,
            },
            // aquí irán más páginas luego
        ],
    },
]);

export default router;