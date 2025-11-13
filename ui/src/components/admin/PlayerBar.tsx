import React from "react";
import type { Player } from "@/types/player";

interface PlayerBarProps {
    player: Player;
}

const PlayerBar: React.FC<PlayerBarProps> = ({ player }) => {
    return (
        <div className="flex justify-between items-centerbg-[#C0392B] text-white rounded-md shadow-md px-4 py-2 w-[450px] h-20">
            <div className="flex flex-col justify-center">
                <div className="flex justify-between items-center">
                    <p className="font-[SVN-Gratelos_Display] font-extrabold uppercase text-[18px] leading-tight">
                        {player.name}
                    </p>
                    {player.timestamp && (
                        <p className="text-sm font-thin italic text-gray-300">
                            {player.timestamp}
                        </p>
                    )}
                </div>
                <p className="text-[16px] font-medium tracking-wide">
                    {player.lastAnswer?.toUpperCase() ?? ""}
                </p>
            </div>

            <div className="font-[SVN-Gratelos_Display] flex items-center justify-center">
                <p className="text-[36px] font-extrabold">{player.score}</p>
            </div>
        </div>
    );
};

export default PlayerBar;