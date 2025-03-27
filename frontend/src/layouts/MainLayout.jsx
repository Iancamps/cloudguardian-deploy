import { Outlet } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";

const MainLayout = () => {
    // lo q se reutiliza para cada página. Sirve para poner lo que NO cambia entre rutas
    return (
        <div className="min-h-screen flex flex-col bg-gray-950 text-white">
            <Header />
            <main className="flex-grow">
                <Outlet />
            </main>
            <Footer />
        </div>
    );
};

export default MainLayout;
