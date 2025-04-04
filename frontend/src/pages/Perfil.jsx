const Perfil = () => {
    const token = localStorage.getItem("token");

    return (
        <div className="p-6 max-w-3xl mx-auto">
            <h2 className="text-2xl font-bold mb-4"> Mi perfil</h2>
            <p>Token actual:</p>
            <code className="block bg-gray-800 text-green-400 p-2 mt-2 rounded break-words">{token}</code>
        </div>
    );
};

export default Perfil;
