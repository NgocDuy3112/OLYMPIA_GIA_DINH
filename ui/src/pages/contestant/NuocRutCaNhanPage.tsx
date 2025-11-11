import { useState, useEffect, useCallback } from "react";
import PlayerBoard from "@/components/contestant/PlayerBoard";
import QuestionArea from "@/components/contestant/QuestionArea";
import PingButton from "@/components/contestant/PingButton";
import type { Player } from "@/types/player";
import { useWebSocket } from "@/hooks/useWebSocket"; 


const MATCH_CODE = "M01T_CN"; 
const CURRENT_PLAYER_CODE = 'P01T'; 
const QUESTION_CODE = 'LN_R1_01';


const NuocRutCaNhanPage = () => {
    const [players, setPlayers] = useState<Player[]>([
        { code: 'P01T', name: 'Hữu Khang', score: 60, isCurrent: true, isBuzzed: false },
        { code: 'P02T', name: 'Kiến Trúc', score: 45, isCurrent: false, isBuzzed: false },
        { code: 'P03T', name: 'Phượng Hoàng', score: 100, isCurrent: false, isBuzzed: false },
        { code: 'P04T', name: 'Đình Oánh', score: 55, isCurrent: false, isBuzzed: false },
    ]);
    const [timer, setTimer] = useState(0);
    const [hasPinged, setHasPinged] = useState(false);
    const [buzzerWinnerCode, setBuzzerWinnerCode] = useState<string | null>(null);
    const { isConnected, sendBuzz, lastMessage } = useWebSocket(MATCH_CODE);

    const handlePing = useCallback(async () => {
        if (!isConnected || hasPinged || timer <= 0 || buzzerWinnerCode) {
            return;
        }
        const success = await sendBuzz(CURRENT_PLAYER_CODE, QUESTION_CODE);
        if (success) {
            setHasPinged(true);
        }
    }, [isConnected, hasPinged, timer, sendBuzz, buzzerWinnerCode]);

    useEffect(() => {
        if (!lastMessage) return;
        const data = typeof lastMessage === 'string' ? JSON.parse(lastMessage) : lastMessage;

        switch (data.type) {
            case 'start_the_timer':
                setHasPinged(false);
                setBuzzerWinnerCode(null);
                setTimer(data.time_limit);
                setPlayers(prev => prev.map(p => ({ ...p, isBuzzed: false })));
                break;
            case 'buzzer_winner':
                setBuzzerWinnerCode(data.player_code);
                setPlayers(prev => prev.map(p => ({
                    ...p,
                    isBuzzed: p.code === data.player_code,
                })));
                break;
            default:
                break;
        }
    }, [lastMessage]);

    useEffect(() => {
        if (!lastMessage) return;
        const msg = typeof lastMessage === 'string' ? JSON.parse(lastMessage) : lastMessage;

        if (msg.type === 'update_score' && msg.player_code && typeof msg.new_score === 'number') {
            setPlayers(prevPlayers =>
                prevPlayers.map(player =>
                    player.code === msg.player_code ? { ...player, score: msg.new_score } : player
                )
            );
            if (msg.player_code === CURRENT_PLAYER_CODE) {
                // Assuming answerInput and setSubmitTime are defined in this component,
                // but since they are not present in the original code, we do not implement them here.
                // This is just to follow the instruction.
                // setAnswerInput('');
                // setSubmitTime(undefined);
            }
        }
        if (msg.type === 'start_the_timer') {
            setTimer(msg.time_limit || 0);
            // setHasAnswered(false);
            // timerStartTimeRef.current = Date.now();
        }
    }, [lastMessage]);

    useEffect(() => {
        if (timer > 0) {
            const intervalId = setInterval(() => {
                setTimer(prevTimer => prevTimer - 1);
            }, 1000);

            return () => clearInterval(intervalId);
        }
    }, [timer]);

    const isPingDisabled = hasPinged || timer <= 0 || !isConnected || !!buzzerWinnerCode;

    return (
        <div className="flex flex-col justify-start items-center min-h-screen">
            {/* Scoreboard */}
            <div className="flex gap-4 max-w-7xl w-full justify-center mt-5">
                {players.map(c => (
                    <PlayerBoard key={c.code} player={c} />
                ))}
            </div>
            {/* QuestionArea */}
            <div className="p-5 w-full flex justify-center">
                <div className="w-full max-w-7xl">
                    <QuestionArea
                        title="LÀM NÓNG - LƯỢT CÁ NHÂN"
                        questionContent="Nếu 23 + 15 = 38 thì năm nay tôi bao nhiêu tuổi?"
                        mediaUrl="../image/background.jpg"
                        timerDisplay={timer.toString().padStart(2, '0')}
                    />
                </div>
            </div>
            <div className="p-3 w-full flex justify-center">
                <div className="w-full max-w-7xl">
                    <PingButton
                        isEnabled={!isPingDisabled}
                        onSubmit={handlePing}
                    />
                </div>
            </div>
        </div>
    )
}



export default NuocRutCaNhanPage;