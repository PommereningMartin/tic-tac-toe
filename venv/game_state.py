from typing import TypedDict, List, NotRequired


class GameState(TypedDict):
    id: int
    player1Name: str
    player2Name: str
    grid: List
    currentPlayerName: str
    player1Symbol: str
    player2Symbol: str
    winner: NotRequired[str]