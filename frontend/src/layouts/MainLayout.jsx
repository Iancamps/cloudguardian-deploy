// RUTA: src/layouts/MainLayout.jsx
import { Outlet } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";

const MainLayout = () => {
    return (
        <div className="flex flex-col min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
            <Header />

            <main className="flex-1 p-4">
                <Outlet />
            </main>

            <Footer />
        </div>
    );
};

export default MainLayout;

