const IpsBloqueadas = () => {
    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold mb-4"> IPs Bloqueadas</h2>
            <ul className="list-disc list-inside mb-4">
                <li>192.168.0.1</li>
                <li>203.0.113.5</li>
                {/* Simula listado de IPs */}
            </ul>
            <input
                type="text"
                className="w-full p-2 mb-2 rounded bg-gray-900 border border-gray-700"
                placeholder="Nueva IP a bloquear"
            />
            <button className="bg-red-600 px-4 py-2 rounded hover:bg-red-700">Añadir IP</button>
        </div>
    );
};

export default IpsBloqueadas;
