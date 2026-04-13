from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by match score."""
        # Convert the dataclass profile into the functional preference shape.
        user_prefs: Dict = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        if user.likes_acoustic:
            user_prefs["acousticness"] = 0.85
        else:
            user_prefs["acousticness"] = 0.20

        scored: List[Tuple[Song, float]] = []
        for song in self.songs:
            score, _reasons = score_song(
                user_prefs,
                {
                    "genre": song.genre,
                    "mood": song.mood,
                    "energy": song.energy,
                    "valence": song.valence,
                    "danceability": song.danceability,
                    "acousticness": song.acousticness,
                },
            )
            scored.append((song, score))

        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation for a song score."""
        user_prefs: Dict = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        user_prefs["acousticness"] = 0.85 if user.likes_acoustic else 0.20

        score, reasons = score_song(
            user_prefs,
            {
                "title": song.title,
                "artist": song.artist,
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            },
        )
        joined = "; ".join(reasons) if reasons else "No matching signals were found."
        return f"{song.title} scored {score:.2f}: {joined}"

def load_songs(csv_path: str) -> List[Dict]:
    """Load a songs CSV into a list of typed dictionaries."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": int(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song and return (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Categorical matches
    # Data experiment: halve genre weight from 2.0 -> 1.0 to reduce over-dominance.
    if user_prefs.get("genre") is not None and song.get("genre") == user_prefs.get("genre"):
        score += 1.0
        reasons.append("genre match (+1.0)")

    if user_prefs.get("mood") is not None and song.get("mood") == user_prefs.get("mood"):
        score += 1.5
        reasons.append("mood match (+1.5)")

    # Numeric closeness: each term is (1 - abs(diff)) in [0, 1] if inputs are in [0, 1]
    def closeness(feature: str, weight: float) -> None:
        nonlocal score
        if feature in user_prefs and feature in song and user_prefs[feature] is not None and song[feature] is not None:
            diff = abs(float(song[feature]) - float(user_prefs[feature]))
            component = max(0.0, 1.0 - diff)
            points = weight * component
            score += points
            reasons.append(f"{feature} close (+{points:.2f})")

    # Data experiment: double energy weight from 1.0 -> 2.0.
    closeness("energy", 2.0)
    closeness("valence", 0.8)
    closeness("danceability", 0.6)
    closeness("acousticness", 0.6)

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return the top-k with explanations."""
    scored: List[Tuple[Dict, float, List[str]]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    ranked = sorted(scored, key=lambda t: t[1], reverse=True)
    results: List[Tuple[Dict, float, str]] = []
    for song, score, reasons in ranked[:k]:
        explanation = "; ".join(reasons) if reasons else "no strong matches"
        results.append((song, score, explanation))
    return results
