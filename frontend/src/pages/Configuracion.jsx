const Configuracion = () => {
    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold mb-4"> Configuración general</h2>
            <p className="mb-2">Aquí podrás ver y editar la configuración actual del firewall.</p>
            {/* Simulación de campos */}
            <div className="bg-gray-800 p-4 rounded mb-4">
                <label className="block mb-1">Rate Limit General:</label>
                <input
                    type="number"
                    className="w-full p-2 rounded bg-gray-900 border border-gray-700"
                    placeholder="Ej: 100 req/min"
                />
            </div>
            <button className="bg-blue-600 px-4 py-2 rounded hover:bg-blue-700">Guardar cambios</button>
        </div>
    );
};

export default Configuracion;
