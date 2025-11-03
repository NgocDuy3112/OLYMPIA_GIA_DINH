import { useState } from "react";
import PlayerBoard from "@/components/contestant/PlayerBoard";
import QuestionArea from "@/components/contestant/QuestionArea";
import InputAnswerArea from "@/components/contestant/InputAnswerArea";
import SubmitAnswerButton from "@/components/contestant/SubmitAnswerButton";
import type { Player } from "@/types/player";



export const VuotDeoPage: React.FC = () => {
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
                    <QuestionArea title="VƯỢT ĐÈO" questionContent="Đây là hình ảnh của chương trình nào?" mediaUrl="../image/background.jpg" timerDisplay="00"/>
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
};


export default VuotDeoPage;