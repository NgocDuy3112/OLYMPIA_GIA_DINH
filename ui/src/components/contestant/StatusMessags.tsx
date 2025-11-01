import React from 'react';
import type { GameMode } from '../../types/game';
import { MousePointer2 } from 'lucide-react';



interface StatusMessageProps {
    mode: GameMode;
    statusColorMap: Record<GameMode, string>;
    statusTextMap: Record<GameMode, string>;
}




export const StatusMessage: React.FC<StatusMessageProps> = ({ mode, statusColorMap, statusTextMap }) => {
    const colorClass = statusColorMap[mode] || 'bg-gray-500';
    const textContent = statusTextMap[mode] || 'LỖI TRẠNG THÁI';

    return (
        <div
            className={`mt-4 p-3 rounded-lg font-bold text-white text-center text-lg shadow-inner flex items-center justify-center transition-colors duration-500 ${colorClass}`}
        >
            <MousePointer2 className="w-6 h-6 mr-2" />
            {textContent}
        </div>
    );
};