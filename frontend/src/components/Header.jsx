const Header = () => {
    return (
        <header className="bg-white dark:bg-gray-800 shadow">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                <h1 className="text-xl font-bold text-blue-600 dark:text-blue-400">
                    🛡️ CloudGuardian
                </h1>
                <nav className="space-x-4">
                    <a href="/" className="hover:underline">Inicio</a>
                    <a href="/firewall" className="hover:underline">Firewall</a>
                </nav>
            </div>
        </header>
    );
};

export default Header;

