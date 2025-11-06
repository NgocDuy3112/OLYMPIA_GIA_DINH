import React from "react";


interface QuestionAreaProps {
    title: string;
    questionContent: string;
    mediaUrl?: string;
    timerDisplay: string;
}



const renderMedia = (mediaUrl: string) => {
    const url = mediaUrl.toLowerCase();
    const isImage = /\.(jpg|jpeg|png|gif|webp)$/.test(url);
    const isVideo = /\.(mp4|webm|ogg)$/.test(url);

    const mediaClass = "max-h-100 object-contain rounded-lg w-full";
    const mediaContainerClass = "py-4 flex justify-center pb-1 ";

    if (isImage) {
        return (
            <div className={mediaContainerClass}>
                <img
                    src={mediaUrl}
                    alt="Hình ảnh câu hỏi"
                    className={mediaClass}
                />
            </div>
        );
    }

    if (isVideo) {
        return (
            <div className={mediaContainerClass}>
                <video
                    controls
                    src={mediaUrl}
                    className={mediaClass}
                >
                    Trình duyệt của bạn không hỗ trợ video.
                </video>
            </div>
        );
    }

    return null;
}


const QuestionArea: React.FC<QuestionAreaProps> = ({ title, questionContent, mediaUrl, timerDisplay }) => {
    return (
        <div className="p-5 rounded-xl max-h-[800px] flex flex-col bg-red-900 ring-4 ring-red-600 shadow-xl">
            <div className="flex justify-between items-center pb-1">
                <p className="text-4xl font-[SVN-Gratelos_Display] font-extrabold text-red-300 uppercase">
                    {title}
                </p>
                <div className={`text-5xl font-[SVN-Gratelos_Display] font-extrabold px-3 py-1 transition-colors duration-500 text-white`} >
                    {timerDisplay}
                </div>
            </div>
            <p className="text-lg sm:text-[20px] font-bold text-white leading-relaxed text-left pt-5">
                {questionContent}
            </p>
            {mediaUrl && renderMedia(mediaUrl)}
        </div>
    )
}


export default QuestionArea;