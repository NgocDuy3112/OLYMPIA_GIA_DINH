import React from "react";
import { Send } from "lucide-react";



interface SubmitAnswerButtonProps {
    answerInput: string;
    isInputActive: boolean;
    onSubmit: () => void;
}



const SubmitAnswerButton: React.FC<SubmitAnswerButtonProps> = ({answerInput, isInputActive, onSubmit}) => {
    const isDisabled = answerInput.trim() === '' || !isInputActive;
    return (
        <button
            onClick={onSubmit}
            disabled={isDisabled}
            className={`w-full px-4 h-auto rounded-lg text-base font-bold shadow-md transition duration-200 flex items-center justify-center 
                ${isDisabled
                    ? 'bg-red-900 ring-red-600 ring-4 text-red-300 cursor-not-allowed'
                    : 'bg-red-600 ring-red-300 ring-4 text-white'
                }`
            }
        >
            <Send className="w-5 h-5 mr-2" />
            GỬI ĐÁP ÁN
        </button>
    )
}


export default SubmitAnswerButton;