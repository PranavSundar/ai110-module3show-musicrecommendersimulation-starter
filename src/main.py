"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    if not recommendations:
        print("(no recommendations)")
        return

    # Simple, readable CLI layout
    title_width = max(len(song["title"]) for song, _score, _exp in recommendations)
    artist_width = max(len(song["artist"]) for song, _score, _exp in recommendations)

    header = f"{'TITLE'.ljust(title_width)}  {'ARTIST'.ljust(artist_width)}  SCORE"
    print(header)
    print("-" * len(header))

    for song, score, explanation in recommendations:
        print(f"{song['title'].ljust(title_width)}  {song['artist'].ljust(artist_width)}  {score:>5.2f}")
        print(f"  reasons: {explanation}")
        print()


if __name__ == "__main__":
    main()
