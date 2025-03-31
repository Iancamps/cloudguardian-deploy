const RutasProtegidas = () => {
    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold mb-4"> Rutas Protegidas</h2>
            <ul className="list-disc list-inside mb-4">
                <li>/admin/login</li>
                <li>/api/secure-data</li>
                {/* Simula rutas protegidas */}
            </ul>
            <input
                type="text"
                className="w-full p-2 mb-2 rounded bg-gray-900 border border-gray-700"
                placeholder="Nueva ruta a proteger"
            />
            <button className="bg-green-600 px-4 py-2 rounded hover:bg-green-700">Añadir ruta</button>
        </div>
    );
};

export default RutasProtegidas;
