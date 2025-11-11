import React, { useState } from "react";


interface ClueModalProps {
    title: string;
    content?: string;
    imageUrl?: string;
    onClose: () => void;
}


interface NumberClue {
    id: number;
    content: string;
}


interface LetterClue {
    code: string;
    imageUrl: string;
}


const ClueModal: React.FC<ClueModalProps> = ({ title, content, imageUrl, onClose }) => {
    return (
        <div className="fixed inset-0 flex justify-center items-center bg-black/50 z-50">
            <div className="bg-white rounded-lg p-6 max-w-lg text-center relative">
                <h2 className="text-2xl font-bold mb-4">{title}</h2>
                {content && <p className="text-lg mb-4">{content}</p>}
                {imageUrl && <img src={imageUrl} alt={title} className="rounded-lg mb-4 max-h-[400px] mx-auto" />}
                <button
                    onClick={onClose}
                    className="bg-red-600 text-white font-semibold py-2 px-6 rounded-lg hover:bg-red-700 transition"
                >
                    Đóng
                </button>
            </div>
        </div>
    );
};


const VuotDeoCluesGrid: React.FC = () => {
    const [selectedNumberClue, setSelectedNumberClue] = useState<NumberClue | null>(null);
    const [selectedLetterClue, setSelectedLetterClue] = useState<string | null>(null);

    const clues: NumberClue[] = [
        { id: 1, content: "Gợi ý 1: Một loài chim tượng trưng cho hòa bình." },
        { id: 2, content: "Gợi ý 2: Tên của một quốc gia châu Á." },
        { id: 3, content: "Gợi ý 3: Một loại phương tiện giao thông đường sắt." },
        { id: 4, content: "Gợi ý 4: Liên quan đến Olympic." },
    ];

    const letters: LetterClue[] = [
        { code: "A", imageUrl: "/images/a.jpg" },
        { code: "B", imageUrl: "/images/b.jpg" },
        { code: "C", imageUrl: "/images/c.jpg" },
        { code: "D", imageUrl: "/images/d.jpg" },
    ];

    return (
        <div className="w-full flex justify-center">
            <div className="w-full max-w-7xl flex flex-row justify-center min-h-[400px] items-stretch gap-5">
                <div className="flex flex-col justify-between flex-[0.8]">
                    <div className="flex flex-col justify-between h-full w-full gap-3">
                        {clues.map((clue) => (
                            <div
                                key={clue.id}
                                className="flex-1 bg-red-900 font-[SVN-Gratelos_Display] text-white font-bold text-[40px] flex justify-center items-center rounded-xl border border-[#E28D85] w-full"
                            >
                                {clue.id}
                            </div>
                        ))}
                    </div>
                </div>
                <div className="flex-[1.2] flex justify-center items-center">
                    <div className="grid grid-cols-2 grid-rows-2 gap-0.5 border border-[#E28D85] bg-[#E28D85] w-full h-full ">
                        {letters.map((l) => (
                            <div
                                key={l.code}
                                className="bg-red-900 text-white font-[SVN-Gratelos_Display] font-extrabold text-[80px] flex justify-center items-center cursor-pointer"
                            >
                                {l.code}
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {selectedNumberClue && (
                <ClueModal
                    title={`Gợi ý ${selectedNumberClue.id}`}
                    content={selectedNumberClue.content}
                    onClose={() => setSelectedNumberClue(null)}
                />
            )}

            {selectedLetterClue && (
                <ClueModal
                    title="Hình ảnh"
                    imageUrl={selectedLetterClue}
                    onClose={() => setSelectedLetterClue(null)}
                />
            )}
        </div>
    );
};

export default VuotDeoCluesGrid;