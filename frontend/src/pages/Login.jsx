import { useState } from "react";

const Login = () => {
    const [usuario, setUsuario] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        // Aquí luego se conecta con el backend
        console.log("Intentando login con:", { usuario, password });
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white">
            <form
                onSubmit={handleSubmit}
                className="bg-gray-900 p-8 rounded-lg shadow-lg w-full max-w-md"
            >
                <h2 className="text-2xl font-bold mb-6 text-center"> Iniciar sesión</h2>

                <label className="block mb-2">Usuario</label>
                <input
                    type="text"
                    className="w-full p-2 mb-4 rounded bg-gray-800 border border-gray-700"
                    value={usuario}
                    onChange={(e) => setUsuario(e.target.value)}
                    required
                />

                <label className="block mb-2">Contraseña</label>
                <input
                    type="password"
                    className="w-full p-2 mb-6 rounded bg-gray-800 border border-gray-700"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button
                    type="submit"
                    className="w-full bg-blue-600 hover:bg-blue-700 py-2 px-4 rounded"
                >
                    Entrar
                </button>
            </form>
        </div>
    );
};

export default Login;
