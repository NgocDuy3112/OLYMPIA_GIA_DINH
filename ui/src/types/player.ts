export interface Player {
    code: string;
    name: string;
    score: number;
    isCurrent: boolean;
    lastAnswer?: string;
    timestamp?: number;
}