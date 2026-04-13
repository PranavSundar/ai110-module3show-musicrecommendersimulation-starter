"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_profile_results(profile_name: str, user_prefs: dict, songs: list[dict], k: int = 5) -> None:
    """Print a readable recommendation table for one user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n=== Profile: {profile_name} ===")
    print(f"prefs: {user_prefs}")
    print("\nTop recommendations:\n")

    if not recommendations:
        print("(no recommendations)")
        return

    title_width = max(len(song["title"]) for song, _score, _exp in recommendations)
    artist_width = max(len(song["artist"]) for song, _score, _exp in recommendations)

    header = f"{'TITLE'.ljust(title_width)}  {'ARTIST'.ljust(artist_width)}  SCORE"
    print(header)
    print("-" * len(header))

    for song, score, explanation in recommendations:
        print(f"{song['title'].ljust(title_width)}  {song['artist'].ljust(artist_width)}  {score:>5.2f}")
        print(f"  reasons: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Core profiles
    profiles: dict[str, dict] = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.90},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "acousticness": 0.85},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "valence": 0.35},
        # Edge/adversarial profiles to stress-test weighting behavior
        "Conflicting: Sad but Max Energy": {"genre": "ambient", "mood": "sad", "energy": 0.95},
        "No Genre Anchor (numeric-only)": {"energy": 0.55, "valence": 0.50, "danceability": 0.55, "acousticness": 0.55},
    }

    for profile_name, user_prefs in profiles.items():
        print_profile_results(profile_name, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
