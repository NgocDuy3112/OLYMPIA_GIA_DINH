import React from "react";
import type { Player } from "@/types/player";



interface PlayerBoardProps {
    player: Player
}



const PlayerBoard: React.FC<PlayerBoardProps> = ({player}) => {
    const answerContent = player.lastAnswer?.trim() ?? '';
    const isAnswered = answerContent !== '---' && answerContent !== '';
    let displayAnswer: string | null = null; 
    let displayTime: string | null = null;

    let answerClasses = 'text-white/60';
    if (isAnswered) {
        displayAnswer = answerContent.toUpperCase();
        
        if (typeof player.timestamp === 'number') {
            displayTime = player.timestamp.toFixed(3);
        }
        answerClasses = 'text-white'; 
    }
    const showPingBell = (player.isBuzzed === true);
    return (
        <div
            key={player.code}
            className={`flex flex-col items-center p-2 rounded-lg transition duration-300 w-1/4 ml-1 mr-1 min-h-[125px] shadow-sm
                ${player.isCurrent 
                    ? 'bg-red-600 shadow-xl scale-100 ring-4 text-white ring-red-300' 
                    : 'ring-2 ring-red-600 bg-red-900 text-red-300'
                }`}
        >
            <div className="flex justify-between items-center w-full">
                <p className="text-[28px] font-bold font-[SVN-Gratelos_Display] uppercase truncate text-left max-w-[80%]">
                    {player.name}
                </p>
                <div className="flex items-center">
                    {showPingBell && (
                        <span className="mr-1 text-2xl" role="img" aria-label="bell">
                            🔔
                        </span>
                    )}
                    <p className="text-[32px] font-[SVN-Gratelos_Display] font-extrabold">
                        {player.score}
                    </p>
                </div>
            </div>
            <div className="mt-2 text-center min-h-10 flex flex-col items-center justify-center w-full mx-auto">
                <p className={`px-2 rounded-md text-[18px] font-bold text-wrap ${isAnswered ? answerClasses : 'text-white'}`}>
                    {displayAnswer}
                </p>
                
                {displayTime && (
                    <p className="text-[15px] font-semibold text-white px-2 rounded-md shadow-inner">
                        {displayTime}
                    </p>
                )}
            </div>
        </div>
    )
}



export default PlayerBoard;