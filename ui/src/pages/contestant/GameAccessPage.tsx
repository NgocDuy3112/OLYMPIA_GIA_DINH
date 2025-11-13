import { useState } from "react";
import { useNavigate } from "react-router-dom";


const GameAccessPage: React.FC = () => {
    const [playerCode, setPlayerCode] = useState("");
    const [matchCode, setMatchCode] = useState("");
    const navigate = useNavigate();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!playerCode || !matchCode) return;
        localStorage.setItem("playerCode", playerCode);
        localStorage.setItem("matchCode", matchCode);
        navigate(`/contestant/waiting`);
    };

    return (
        <div className="flex flex-col justify-center items-center min-h-screen bg-cover bg-center text-white">
            <div className="bg-red-900 bg-opacity-50 p-10 rounded-xl shadow-lg w-full max-w-md">
                <h1 className="text-4xl font-[SVN-Gratelos_Display] font-bold mb-6 text-center">OLYMPIA GIA ĐỊNH 3</h1>
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <div>
                        <label className="block mb-1 font-medium">Mã người chơi</label>
                        <input
                            type="text"
                            value={playerCode}
                            onChange={(e) => setPlayerCode(e.target.value)}
                            className="w-full px-3 py-2 rounded bg-white text-black border border-red-900 focus:outline-none focus:border-red-500"
                            placeholder="VD: P01T"
                        />
                    </div>
                    <div>
                        <label className="block mb-1 font-medium">Mã trận đấu</label>
                        <input
                            type="text"
                            value={matchCode}
                            onChange={(e) => setMatchCode(e.target.value)}
                            className="w-full px-3 py-2 rounded bg-white text-black border border-red-900 focus:outline-none focus:border-red-500"
                            placeholder="VD: M01T"
                        />
                    </div>
                    <button
                        type="submit"
                        className="mt-4 bg-red-600 hover:bg-red-500 text-white font-semibold py-2 rounded transition-all duration-200"
                    >
                        VÀO PHÒNG
                    </button>
                </form>
            </div>
        </div>
    );
};

export default GameAccessPage;