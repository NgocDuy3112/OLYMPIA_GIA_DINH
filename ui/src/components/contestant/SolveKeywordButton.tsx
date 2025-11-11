import React from "react";
import { Key } from "lucide-react";



interface SolveKeywordButtonProps {
    isEnabled: boolean;
    onSubmit: () => void;
}



const SolveKeywordButton: React.FC<SolveKeywordButtonProps> = ({isEnabled, onSubmit}) => {
    const isDisaled = !isEnabled;
    return (
        <button
            onClick={onSubmit}
            disabled={isDisaled}
            className={`w-full px-4 h-auto rounded-lg text-base font-bold shadow-md transition duration-200 flex items-center justify-center 
                ${isDisaled
                    ? 'bg-red-900 ring-red-600 ring-4 text-red-300 cursor-not-allowed'
                    : 'bg-red-600 ring-red-300 ring-4 text-white'
                }`
            }
        >
            <Key className="w-5 h-5 mr-2" />
            BẤM CHUÔNG GIẢI MÃ TỪ KHOÁ
        </button>
    )
}


export default SolveKeywordButton;