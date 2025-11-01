export type ClueStatus = 'correct' | 'incorrect' | 'timeout' | 'pending';
export type GameMode = 'inactive' | 'clue_active' | 'keyword_active' | 'input_keyword';

export interface Contestant {
    id: string;
    name: string;
    score: number;
    isCurrent: boolean;
}