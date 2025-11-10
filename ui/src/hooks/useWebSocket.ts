/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useEffect, useRef, useCallback } from "react";


interface WebSocketPayload {
    type: string;
    player_code: string;
    question_code?: string;
    answer?: string;
    [key: string]: any; 
}



const createWsUrl = (matchCode: string) => `ws://localhost:8000/controller/ws/match/${matchCode}`; 



export const useWebSocket = (matchCode: string) => { 
    const ws = useRef<WebSocket | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const [lastMessage, setLastMessage] = useState<any>(null); 

    useEffect(() => {
        const url = createWsUrl(matchCode);
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.close();
        }
        ws.current = new WebSocket(url);

        ws.current.onopen = () => {
            console.log(`[WS] Connected to match: ${matchCode}`);
            setIsConnected(true);
        };

        ws.current.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                setLastMessage(message); 
            } catch (e) {
                console.error("[WS] Error parsing message:", e);
            }
        };

        ws.current.onclose = () => {
            console.log(`[WS] Disconnected from match: ${matchCode}`);
            setIsConnected(false);
            setTimeout(() => {
                if (!ws.current || ws.current.readyState === WebSocket.CLOSED) {
                    ws.current = new WebSocket(url);
                    console.log(`[WS] Reconnecting...`);
                }
            }, 3000);
        };

        ws.current.onerror = (error) => {
            console.error("[WS] WebSocket Error:", error);
        };

        return () => {
            if (ws.current && ws.current.readyState === WebSocket.OPEN) {
                ws.current.close();
            }
        };
    }, [matchCode]); 


    const sendMessage = useCallback(async (payload: WebSocketPayload): Promise<boolean> => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify(payload));
            console.log("[WS] Sent payload:", payload);
            return true;
        } else {
            console.warn("[WS] Cannot send message: Not connected.");
            return false;
        }
    }, []);


    const sendAnswer = useCallback(async (playerCode: string, questionCode: string, answer: string, timestamp: number): Promise<boolean> => {
        return await sendMessage({
            type: "answer",
            player_code: playerCode,
            question_code: questionCode,
            answer: answer.trim(),
            timestamp: timestamp
        });
    }, [sendMessage]);


    const sendBuzz = useCallback(async (playerCode: string, questionCode: string): Promise<boolean> => {
        return await sendMessage({
            type: "buzz",
            player_code: playerCode,
            question_code: questionCode
        });
    }, [sendMessage]);


    const sendBuzzCnv = useCallback(async (playerCode: string): Promise<boolean> => {
        return await sendMessage({
            type: "buzz_cnv",
            player_code: playerCode,
        });
    }, [sendMessage]);


    return { 
        isConnected, 
        lastMessage, 
        sendMessage,
        sendAnswer,
        sendBuzz,
        sendBuzzCnv,
    };
};