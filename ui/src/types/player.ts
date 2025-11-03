export interface Player {
    id: string;
    name: string;
    score: number;
    isCurrent: boolean;
    lastAnswer?: string;
    timestamp?: number;
}