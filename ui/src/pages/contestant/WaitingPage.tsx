import React from "react";

const WaitingPage: React.FC = () => {
    return (
        <div className="flex flex-col justify-center items-center min-h-screen text-white">
            <div className="bg-red-700 border-4 border-red-500 rounded-xl shadow-xl w-3/4 max-w-3xl p-10 text-center">
                <h1 className="text-[64px] font-bold font-[SVN-Gratelos_Display] mb-4">
                    OLYMPIA GIA ĐỊNH 3
                </h1>
                <p className="text-lg font-semibold opacity-80">
                    Trận đấu sẽ quay lại trong chốc lát!
                </p>
            </div>
        </div>
    );
};

export default WaitingPage;