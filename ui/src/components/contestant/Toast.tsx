import React from 'react';



interface ToastProps {
    toastState: {
        title: string;
        description: string;
        status: 'success' | 'error' | 'warning' | 'info';
    } | null;
    hideToast: () => void;
}



export const Toast: React.FC<ToastProps> = ({ toastState, hideToast }) => {
    if (!toastState) return null;

    let bg = '', icon = '';
    switch (toastState.status) {
        case 'success': bg = 'bg-green-500'; icon = '✅'; break;
        case 'error': bg = 'bg-red-500'; icon = '❌'; break;
        case 'warning': bg = 'bg-orange-500'; icon = '⚠️'; break;
        case 'info': bg = 'bg-blue-500'; icon = 'ℹ️'; break;
    }

    return (
        <div
            className={`fixed inset-x-0 top-0 mx-auto w-full max-w-lg p-4 m-4 rounded-lg text-white font-bold shadow-xl z-50 ${bg}`}
            onClick={hideToast}
        >
            <p className="text-xl flex items-center mb-1">
                {icon} <span className="ml-2">{toastState.title}</span>
            </p>
            <p className="text-sm font-normal">{toastState.description}</p>
        </div>
    );
};