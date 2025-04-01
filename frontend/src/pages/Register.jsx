import { useState } from 'react';
import axios from 'axios';

export default function Register() {
    const [username, setUsername] = useState('');
    const [password1, setPassword1] = useState('');
    const [password2, setPassword2] = useState('');
    const [message, setMessage] = useState('');

    const handleRegister = () => {
        axios.post('/api/register', {
            username,
            password1,
            password2
        }).then(res => {
            setMessage('Registro exitoso');
        }).catch(err => {
            setMessage('Error en el registro');
        });
    };

    return (
        <div className="p-4 max-w-md mx-auto">
            <h1 className="text-2xl font-bold mb-4">Registro</h1>
            <input type="text" placeholder="Usuario" className="w-full mb-2 p-2 border rounded"
                value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="password" placeholder="Contraseña" className="w-full mb-2 p-2 border rounded"
                value={password1} onChange={(e) => setPassword1(e.target.value)} />
            <input type="password" placeholder="Repetir contraseña" className="w-full mb-2 p-2 border rounded"
                value={password2} onChange={(e) => setPassword2(e.target.value)} />
            <button onClick={handleRegister} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                Registrarse
            </button>
            {message && <p className="mt-2 text-red-600">{message}</p>}
        </div>
    );
}