import React, { useCallback } from 'react';
import type { ClueStatus } from '@/types/game';



interface ClueGridProps {
    currentClue: string | null;
    answeredClues: Record<string, ClueStatus>;
}



export const ClueGrid: React.FC<ClueGridProps> = ({ currentClue, answeredClues }) => {
    const getClueStyle = useCallback(
        (id: string, isImage: boolean): string => {
            const status = answeredClues[id];
            const textSize = isImage ? 'text-4xl sm:text-6xl' : 'text-2xl sm:text-3xl';
            const base = `flex items-center justify-center p-3 sm:p-5 shadow-inner font-extrabold transition duration-300 ${textSize} ${isImage ? '' : 'rounded-lg'
                }`;
            let color = '', ring = '';

            if (status === 'correct') color = 'bg-green-600 text-white';
            else if (status === 'incorrect' || status === 'timeout') color = 'bg-red-600 text-white';
            else if (currentClue === id) {
                color = 'bg-yellow-400 text-gray-900';
                ring = 'ring-4 ring-yellow-300';
            } else color = 'bg-gray-500 text-white hover:opacity-90';

            return `${base} ${color} ${ring}`;
        },
        [currentClue, answeredClues]
    );

    const horizontal = ['1', '2', '3', '4'];
    const images = ['A', 'B', 'C', 'D'];
    return (
        <div className="flex flex-col sm:flex-row justify-center gap-15 mb-6">
            <div className="w-full sm:w-60 flex flex-col gap-2">
                {horizontal.map(id => (
                    <div key={id} className={getClueStyle(id, false)}>
                        {id}
                    </div>
                ))}
            </div>
            <div className="grid sm:w-120 grid-cols-2 gap-0 flex-1 overflow-hidden">
                {images.map(id => (
                    <div key={id} className={getClueStyle(id, true)}>
                        {id}
                    </div>
                ))}
            </div>
        </div>
    );
};