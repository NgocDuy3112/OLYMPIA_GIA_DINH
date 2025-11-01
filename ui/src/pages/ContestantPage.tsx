import React, { useState, useCallback } from "react";
import { ClueGrid } from "@/components/contestant/ClueGrid";
import { useSimpleToast } from "@/components/contestant/hooks/useSimpleToast";
import type { ClueStatus } from "@/types/game";



export const ContestantPage: React.FC = () => {
    const [currentClue, setCurrentClue] = useState<string | null>(null);
    const [answeredClues, setAnsweredClues] = useState<Record<string, ClueStatus>>({});

    const { toastState, showToast, hideToast } = useSimpleToast();

    // Khi người chơi chọn gợi ý
    const handleSelectClue = useCallback(
        (id: string) => {
            setCurrentClue(id);

            // ví dụ mô phỏng kết quả random
            const result: ClueStatus = Math.random() > 0.5 ? "correct" : "incorrect";

            setAnsweredClues((prev) => ({ ...prev, [id]: result }));

            showToast({
                title: result === "correct" ? "Chính xác!" : "Sai mất rồi!",
                description:
                    result === "correct" ? "Bạn đã chọn đúng đáp án." : "Thử lại ở lượt tiếp theo nhé.",
                status: result === "correct" ? "success" : "error",
                duration: 2000,
            });
        },
        [showToast]
    );

    const clueProps = {
        currentClue,
        answeredClues,
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center gap-6 p-4">
            <h1 className="text-3xl sm:text-4xl font-bold mb-2">🏆 Cuộc thi Olympia</h1>

            <div
                onClick={() => hideToast()}
                className="cursor-pointer select-none"
            >
                <ClueGrid {...clueProps} />
            </div>

            {toastState && (
                <div
                    className={`
                        fixed bottom-4 left-1/2 -translate-x-1/2 px-6 py-3 rounded-lg shadow-lg
                        text-white font-semibold
                        ${toastState.status === "success" ? "bg-green-600" : ""}
                        ${toastState.status === "error" ? "bg-red-600" : ""}
                        ${toastState.status === "warning" ? "bg-yellow-500 text-gray-900" : ""}
                        ${toastState.status === "info" ? "bg-blue-600" : ""}
                        animate-fade-in
                    `}
                >
                    <div className="text-lg">{toastState.title}</div>
                    <div className="text-sm opacity-90">{toastState.description}</div>
                </div>
            )}
        </div>
    );
};


export default ContestantPage;