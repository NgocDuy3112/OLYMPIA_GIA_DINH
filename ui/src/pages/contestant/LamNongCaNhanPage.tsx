/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useEffect, useCallback } from "react";
import PlayerBoard from "@/components/contestant/PlayerBoard";
import QuestionArea from "@/components/contestant/QuestionArea";
import PingButton from "@/components/contestant/PingButton";
import type { Player } from "@/types/player";
import { useWebSocket } from "@/hooks/useWebSocket"; // IMPORT HOOK WS


const MATCH_CODE = "M01T_CN"; 
const CURRENT_PLAYER_CODE = 'P01T'; 
const QUESTION_CODE = 'LN_R1_01';


const LamNongCaNhanPage = () => {
    const [players, setPlayers] = useState<Player[]>([
        { code: 'P01T', name: 'Hữu Khang', score: 60, isCurrent: true, isBuzzed: false }, 
        { code: 'P02T', name: 'Kiến Trúc', score: 45, isCurrent: false, isBuzzed: false },
        { code: 'P03T', name: 'Phượng Hoàng', score: 100, isCurrent: false, isBuzzed: false },
        { code: 'P04T', name: 'Đình Oánh', score: 55, isCurrent: false, isBuzzed: false },
    ]);
    const [timer, setTimer] = useState(10);
    const [hasPinged, setHasPinged] = useState(false); 
    const [pingSuccessful, setPingSuccessful] = useState(false); // Trạng thái bấm chuông thành công
    
    // SỬ DỤNG HOOK WS
    const { isConnected, sendBuzz } = useWebSocket(MATCH_CODE);

    // --- LOGIC BẤM CHUÔNG ---
    const handlePing = useCallback(() => {
        // Kiểm tra điều kiện gửi
        if (!isConnected || hasPinged || timer <= 0) {
            console.warn("Không thể bấm chuông: Ngắt kết nối, đã bấm, hoặc hết giờ.");
            return;
        }

        const success = sendBuzz(CURRENT_PLAYER_CODE, QUESTION_CODE);

        if (success) {
            console.log(`Người chơi ${CURRENT_PLAYER_CODE} đã gửi buzz.`);
            setHasPinged(true); 
            setPingSuccessful(true); // Đánh dấu đã gửi thành công
            
            // Cập nhật state players để hiển thị chuông ngay lập tức
            setPlayers(prevPlayers => prevPlayers.map(p => 
                p.code === CURRENT_PLAYER_CODE
                    ? { ...p, hasPinged: true }
                    : p
            ));
        }
    }, [isConnected, hasPinged, timer, sendBuzz]);


    // --- LOGIC TIMER ---
    useEffect(() => {
        // Chỉ đếm ngược khi timer > 0 VÀ CHƯA BẤM CHUÔNG THÀNH CÔNG
        if (timer > 0 && !pingSuccessful) { 
            const intervalId = setInterval(() => {
                setTimer(prevTimer => prevTimer - 1);
            }, 1000);

            return () => clearInterval(intervalId);
        }
    }, [timer, pingSuccessful]); // Thêm pingSuccessful vào dependency


    const isPingDisabled = hasPinged || timer <= 0 || !isConnected || pingSuccessful;


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
                        questionContent="Đoạn trailer chính thức..." 
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

export default LamNongCaNhanPage;