export interface Player {
    code: string;
    name: string;
    score: number;
    lastAnswer?: string;
    timestamp?: number;
    isBuzzed?: boolean;
}