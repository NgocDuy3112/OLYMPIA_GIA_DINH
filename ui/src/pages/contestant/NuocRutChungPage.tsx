import { useState } from "react";
import PlayerBoard from "@/components/contestant/PlayerBoard";
import QuestionArea from "@/components/contestant/QuestionArea";
import InputAnswerArea from "@/components/contestant/InputAnswerArea";
import SubmitAnswerButton from "@/components/contestant/SubmitAnswerButton";
import type { Player } from "@/types/player";



const NuocRutChungPage = () => {
    const [players, setPlayers] = useState<Player[]>([
        { id: 'C1', name: 'Hữu Khang', score: 60, isCurrent: true, lastAnswer: 'ĐÂY LÀ ĐÁP ÁN CỦA TUI', timestamp: 8.907 },
        { id: 'C2', name: 'Kiến Trúc', score: 45, isCurrent: false, lastAnswer: '1 2 3 4', timestamp: 9.005 },
        { id: 'C3', name: 'Phượng Hoàng', score: 100, isCurrent: false, lastAnswer: '' },
        { id: 'C4', name: 'Đình Oánh', score: 55, isCurrent: false, lastAnswer: '' },
    ]);
    const [timer, setTimer] = useState(10);
    const [answerInput, setAnswerInput] = useState('');
    return (
        <div className="flex flex-col justify-start items-center min-h-screen">
            {/* Scoreboard */}
            <div className="flex gap-4 max-w-7xl w-full justify-center mt-5">
                {players.map(c => (
                    <PlayerBoard key={c.id} player={c} />
                ))}
            </div>
            {/* QuestionArea */}
            <div className="p-5 w-full flex justify-center">
                <div className="w-full max-w-7xl">
                    <QuestionArea title="LÀM NÓNG - LƯỢT CHUNG" questionContent="Đoạn trailer chính thức của giải đấu Liên Quân quốc tế AIC 2024 có xuất hiện hình ảnh của một chiếc xe lửa được sử dụng cho một tuyến đường sắt là một phần của hệ thống tuyến đường sắt xuyên lục địa Á - Âu. Tuyến đường sắt này có tên là gì, và tuyến đường sắt này không đi qua (các) thành phố nào trong các thành phố sau: Hà Nội (1), Hà Nam (2), Nam Định (3), Ninh Bình (4), Thanh Hoá (5), Nghệ An (6), Hà Tĩnh (7), Quảng Bình (8), Quảng Trị (9), Thừa Thiên Huế (10), Đà Nẵng (11), Quảng Nam (12), Quảng Ngãi (13), Bình Định (14), Phú Yên (15), Khánh Hoà (16), Ninh Thuận (17), Bình Thuận (18), Lâm Đồng (19), Đồng Nai (20), Bình Dương (21), Thành phố Hồ Chí Minh (22), Cần Thơ (23), Đồng Tháp (24)?" mediaUrl="../image/background.jpg" timerDisplay="00"/>
                </div>
            </div>
            {/* InputAnswerArea */}
            <div className="w-full flex justify-center">
                <div className="w-full max-w-7xl">
                    <InputAnswerArea answerInput={answerInput} setAnswerInput={setAnswerInput} isDisabled={false} onSubmit={() => setAnswerInput('')}/>
                </div>
            </div>
            {/* SubmitAnswerButton */}
            <div className="p-5 w-full flex justify-center">
                <div className="w-full max-w-7xl">
                    <SubmitAnswerButton answerInput={answerInput} isInputActive={answerInput.trim().length > 0} onSubmit={() => setAnswerInput('')} />
                </div>
            </div>
        </div>
    )
}



export default NuocRutChungPage;