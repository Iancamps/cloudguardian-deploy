const Footer = () => {
    return (
        <footer className="bg-gray-200 dark:bg-gray-800 text-center py-4 mt-10">
            <p className="text-sm text-gray-600 dark:text-gray-400">
                © {new Date().getFullYear()} CloudGuardian · EQUIPO FCT - FUNDACION MEDAC
            </p>
        </footer>
    );
};

export default Footer;

