import React, { useCallback } from 'react';
import type { ClueStatus } from '@/types/game';

interface ClueGridProps {
    currentClue: string | null;
    answeredClues: Record<string, ClueStatus>;
}

export const ClueGrid: React.FC<ClueGridProps> = ({ currentClue, answeredClues }) => {
    const getClueStyle = useCallback(
        (id: string, isImage: boolean): string => {
            const status = answeredClues[id];
            // Kích thước chữ dựa trên loại ô
            const textSize = isImage ? 'text-4xl sm:text-6xl' : 'text-2xl sm:text-3xl';
            
            // CSS cơ bản áp dụng cho mọi ô
            const base = `flex items-center justify-center p-3 sm:p-5 shadow-lg font-extrabold transition duration-300 ${textSize} ${isImage ? '' : 'rounded-lg'}`;
            
            let color = '', ring = '';

            if (status === 'correct') {
                // ✅ Đáp án ĐÚNG: Giữ màu XANH LÁ để chỉ trạng thái thành công
                color = 'bg-green-600 text-white shadow-green-900/50';
            } else if (status === 'incorrect' || status === 'timeout') {
                // ❌ Đáp án SAI/HẾT GIỜ: Giữ màu ĐỎ để chỉ lỗi
                color = 'bg-red-600 text-white shadow-red-900/50';
            } else if (currentClue === id) {
                // 🟡 Ô ĐANG CHỌN (Current): Giữ màu VÀNG NỔI BẬT để dễ nhận biết
                color = 'bg-yellow-400 text-gray-900 shadow-yellow-900/50';
                // Tăng ring lên để làm nổi bật hơn
                ring = 'ring-4 ring-yellow-500/80'; 
            } else {
                // 🟤 Ô CHƯA ĐƯỢC CHỌN: Dùng màu ĐỎ SẪM/NÂU ĐỎ (như trong hình)
                // Thay thế gray-500 bằng màu đỏ sẫm: bg-red-800 hoặc custom color
                color = 'bg-red-800 text-white hover:bg-red-700 shadow-xl'; 
            }

            return `${base} ${color} ${ring}`;
        },
        [currentClue, answeredClues]
    );

    const horizontal = ['1', '2', '3', '4'];
    // Đã thay đổi 'A', 'B', 'C', 'D' thành chuỗi trống vì trong hình các ô lớn không có chữ cái
    const images = ['', '', '', '']; 
    // Tuy nhiên, nếu bạn vẫn muốn dùng ID thì giữ nguyên: const images = ['A', 'B', 'C', 'D'];
    
    return (
        <div className="flex flex-col sm:flex-row justify-center gap-4 mb-6"> 
            {/* Cột 1-4 */}
            <div className="w-full sm:w-60 flex flex-col gap-2">
                {horizontal.map(id => (
                    <div key={id} className={getClueStyle(id, false)}>
                        {id}
                    </div>
                ))}
            </div>
            {/* Ô ảnh */}
            <div className="grid sm:w-120 grid-cols-2 gap-2 flex-1 overflow-hidden">
                {images.map((id, index) => (
                    // Để tránh lỗi key, vẫn dùng index làm key, và id là nội dung hiển thị
                    <div key={`image-${index}`} className={getClueStyle(`image-${index}`, true)}> 
                        {/* Nếu bạn muốn hiển thị các chữ cái A, B, C, D thì thay {id} bằng id tương ứng */}
                    </div>
                ))}
            </div>
        </div>
    );
};