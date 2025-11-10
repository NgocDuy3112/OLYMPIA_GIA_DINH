import React from "react";



interface InputAnswerAreaProps {
    answerInput: string;
    setAnswerInput: (value: string) => void;
    isDisabled: boolean;
    onSubmit: () => void;
}



const InputAnswerArea: React.FC<InputAnswerAreaProps> = ({
    answerInput, 
    setAnswerInput, 
    isDisabled, 
    onSubmit
}) => {
    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            event.preventDefault(); 
            if (event.nativeEvent.isComposing || !answerInput.trim()) {
                return;
            }
            
            if (!isDisabled) {
                onSubmit();
                setAnswerInput('');
            }
        }
    };
    return (
        <input
            type="text"
            value={answerInput}
            onChange={(e) => setAnswerInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={!isDisabled ? 'Nhập câu trả lời của bạn tại khung này' : 'Bạn không thể nhập đáp án tại thời điểm này'}
            disabled={isDisabled}
            className={`w-full p-3 rounded-lg text-lg text-black text-center shadow-sm transition duration-150 border-red-500 border-4 bg-white disabled:bg-red-900 disabled:cursor-not-allowed disabled:text-red-300`}
        />
    )
}



export default InputAnswerArea;