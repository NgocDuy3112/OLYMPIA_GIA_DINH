import { useState, useEffect, useCallback, useRef } from "react";
import PlayerBoard from "@/components/contestant/PlayerBoard";
import QuestionArea from "@/components/contestant/QuestionArea";
import InputAnswerArea from "@/components/contestant/InputAnswerArea";
import SolveKeywordButton from "@/components/contestant/SolveKeywordButton";
import VuotDeoCluesGrid from "@/components/contestant/VuotDeoCluesGrid";
import { useWebSocket } from "@/hooks/useWebSocket";
import type { Player } from "@/types/player";


const MATCH_CODE = "M01T";
const CURRENT_PLAYER_CODE = "P01T";
const QUESTION_CODE = "VD_01";
const MAX_TIME = 15;



export const VuotDeoPage: React.FC = () => {
    const [players, setPlayers] = useState<Player[]>([
        { code: 'P01T', name: 'Hữu Khang', score: 60, isCurrent: true, lastAnswer: '', timestamp: 8.907 },
        { code: 'P02T', name: 'Kiến Trúc', score: 45, isCurrent: false, lastAnswer: '', timestamp: 9.005 },
        { code: 'P03T', name: 'Phượng Hoàng', score: 100, isCurrent: false, lastAnswer: '' },
        { code: 'P04T', name: 'Đình Oánh', score: 55, isCurrent: false, lastAnswer: '' },
    ]);
    const [timer, setTimer] = useState(0);
    const [answerInput, setAnswerInput] = useState('');
    const [hasKeywordBuzzed, setHasKeywordBuzzed] = useState(false);
    const [, setSubmitTime] = useState<number | undefined>(undefined);
    const [, setHasAnswered] = useState(false);
    const { isConnected, lastMessage, sendAnswer, sendBuzzCnv } = useWebSocket(MATCH_CODE);

    const timerStartTimeRef = useRef<number | null>(null);

    const handleSubmitAnswer = useCallback(async () => {
        const trimmedAnswer = answerInput.trim();
        if (!trimmedAnswer || !isConnected || timer <= 0) {
            return;
        }
        const submitTimestampMs = Date.now();
        const success = await sendAnswer(CURRENT_PLAYER_CODE, QUESTION_CODE, trimmedAnswer, submitTimestampMs);

        if (success) {
            let finalTimestamp: number;
            if (timerStartTimeRef.current !== null) {
                const timeElapsedSinceStart = (submitTimestampMs - timerStartTimeRef.current) / 1000;
                finalTimestamp = timeElapsedSinceStart;
            } else {
                finalTimestamp = MAX_TIME - timer;
            }
            finalTimestamp = Math.max(0, Math.min(MAX_TIME, finalTimestamp));
            setSubmitTime(finalTimestamp);
            setHasAnswered(true);
            setPlayers(prevPlayers => prevPlayers.map(p =>
                p.code === CURRENT_PLAYER_CODE
                    ? {
                        ...p,
                        lastAnswer: trimmedAnswer,
                        timestamp: parseFloat(finalTimestamp.toFixed(3))
                    }
                    : p
            ));
        }
    }, [answerInput, isConnected, sendAnswer, timer, setPlayers]);

    const handleKeywordBuzz = useCallback(async () => {
        if (!isConnected || hasKeywordBuzzed) {
            return;
        }
        const success = await sendBuzzCnv(CURRENT_PLAYER_CODE);
        if (success) {
            setHasKeywordBuzzed(true);
        }
    }, [isConnected, hasKeywordBuzzed, sendBuzzCnv]);


    useEffect(() => {
        timerStartTimeRef.current = Date.now() - (MAX_TIME - timer) * 1000;
        if (timer > 0) {
            const intervalId = setInterval(() => {
                setTimer(prevTimer => prevTimer - 1);
            }, 1000);

            return () => clearInterval(intervalId);
        }
        if (timer === 0) {
            setAnswerInput('');
        }
    }, [timer]);


    useEffect(() => {
        if (!lastMessage) return;
        const data = typeof lastMessage === 'string' ? JSON.parse(lastMessage) : lastMessage;
        switch (data.type) {
            case 'start_the_timer':
                setHasAnswered(false);
                setTimer(data.time_limit);
                timerStartTimeRef.current = Date.now();
                break;
            case 'update_score':
                if (data.player_code && data.new_score !== undefined) {
                    setPlayers(prevPlayers => prevPlayers.map(p =>
                        p.code === data.player_code
                            ? { ...p, score: data.new_score }
                            : p
                    ));
                    if (data.player_code === CURRENT_PLAYER_CODE) {
                        setAnswerInput('');
                        setSubmitTime(undefined);
                    }
                }
                break;
            case 'buzzer_winner':
                break;
            default:
                break;
        }
    }, [lastMessage]);

    const timerDisplay = timer.toString().padStart(2, '0');
    const isSubmissionDisabled = !isConnected || timer <= 0;

    return (
        <div className="flex flex-col justify-start items-center min-h-screen">
            {/* Scoreboard */}
            <div className="flex gap-4 max-w-7xl w-full justify-center mt-5">
                {players.map(c => (
                    <PlayerBoard key={c.code} player={c} />
                ))}
            </div>
            <div className="p-5 w-full flex justify-center">
                <VuotDeoCluesGrid />
            </div>
            {/* QuestionArea */}
            <div className="p-5 w-full flex justify-center">
                <div className="w-full max-w-7xl">
                    <QuestionArea title="LÀM NÓNG - LƯỢT CHUNG" questionContent="Đoạn trailer chính thức của giải đấu Liên Quân quốc tế AIC 2024 có xuất hiện hình ảnh của một chiếc xe lửa được sử dụng cho một tuyến đường sắt là một phần của hệ thống tuyến đường sắt xuyên lục địa Á - Âu. Tuyến đường sắt này có tên là gì, và tuyến đường sắt này không đi qua (các) thành phố nào trong các thành phố sau: Hà Nội (1), Hà Nam (2), Nam Định (3), Ninh Bình (4), Thanh Hoá (5), Nghệ An (6), Hà Tĩnh (7), Quảng Bình (8), Quảng Trị (9), Thừa Thiên Huế (10), Đà Nẵng (11), Quảng Nam (12), Quảng Ngãi (13), Bình Định (14), Phú Yên (15), Khánh Hoà (16), Ninh Thuận (17), Bình Thuận (18), Lâm Đồng (19), Đồng Nai (20), Bình Dương (21), Thành phố Hồ Chí Minh (22), Cần Thơ (23), Đồng Tháp (24)?" timerDisplay={timerDisplay} />
                </div>
            </div>
            {/* InputAnswerArea */}
            <div className="w-full flex justify-center">
                <div className="w-full max-w-7xl">
                    <InputAnswerArea
                        answerInput={answerInput}
                        setAnswerInput={setAnswerInput}
                        isDisabled={isSubmissionDisabled}
                        onSubmit={handleSubmitAnswer}
                    />
                </div>
            </div>
            <div className="p-4 w-full flex justify-center">
                <div className="w-full max-w-7xl">
                    <SolveKeywordButton
                        isEnabled={false}
                        onSubmit={handleKeywordBuzz}
                    />
                </div>
            </div>
        </div>
    )
};


export default VuotDeoPage;