import React from "react";
import { Bell } from "lucide-react";



interface PingButtonProps {
    isEnabled: boolean;
    onSubmit: () => void;
}



const PingButton: React.FC<PingButtonProps> = ({isEnabled, onSubmit}) => {
    const isDisbaled = !isEnabled;
    return (
        <button
            onClick={onSubmit}
            disabled={isDisbaled}
            className={`w-full px-4 h-auto rounded-lg text-base font-bold shadow-md transition duration-200 flex items-center justify-center 
                ${isDisbaled
                    ? 'bg-red-900 ring-red-600 ring-4 text-red-300 cursor-not-allowed'
                    : 'bg-red-600 ring-red-300 ring-4 text-white'
                }`
            }
        >
            <Bell className="w-5 h-5 mr-2" />
            BẤM CHUÔNG
        </button>
    )
}


export default PingButton;