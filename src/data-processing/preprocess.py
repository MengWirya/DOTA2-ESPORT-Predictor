import os
import json
import pandas as pd

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed/matches.csv"


def load_json_files():
    files = [f for f in os.listdir(RAW_PATH) if f.endswith(".json")]
    data = []

    for file in files:
        path = os.path.join(RAW_PATH, file)
        with open(path, "r") as f:
            try:
                data.append(json.load(f))
            except:
                print(f"Error reading {file}")

    return data


def extract_players(players, is_radiant=True):
    """
    Extract player IDs for a team
    """
    team_players = [
        p.get("account_id")
        for p in players
        if p.get("isRadiant") == is_radiant and p.get("account_id") is not None
    ]

    # Ensure exactly 5 players
    if len(team_players) != 5:
        return None

    return sorted(team_players)


def aggregate_stats(players, is_radiant=True):
    team_players = [p for p in players if p.get("isRadiant") == is_radiant]

    if len(team_players) != 5:
        return None

    kills = sum(p.get("kills", 0) for p in team_players)
    deaths = sum(p.get("deaths", 0) for p in team_players)
    gpm = sum(p.get("gold_per_min", 0) for p in team_players) / 5
    xpm = sum(p.get("xp_per_min", 0) for p in team_players) / 5

    return kills, deaths, gpm, xpm


def process_match(match):
    rows = []

    # Skip matches without team info (non-pro matches)
    if not match.get("radiant_team") or not match.get("dire_team"):
        return rows

    players = match.get("players", [])
    if len(players) < 10:
        return rows

    # Extract team info
    radiant_team = match["radiant_team"]
    dire_team = match["dire_team"]

    radiant_id = radiant_team.get("team_id")
    dire_id = dire_team.get("team_id")

    radiant_name = radiant_team.get("name", "unknown")
    dire_name = dire_team.get("name", "unknown")

    # Extract players
    radiant_players = extract_players(players, True)
    dire_players = extract_players(players, False)

    if not radiant_players or not dire_players:
        return rows

    # Aggregate stats
    radiant_stats = aggregate_stats(players, True)
    dire_stats = aggregate_stats(players, False)

    if not radiant_stats or not dire_stats:
        return rows

    radiant_win = match.get("radiant_win", False)

    # Radiant row
    rows.append({
        "match_id": match["match_id"],
        "team_id": radiant_id,
        "team_name": radiant_name,
        "team": "radiant",
        "win": int(radiant_win),
        "total_kills": radiant_stats[0],
        "total_deaths": radiant_stats[1],
        "avg_gpm": radiant_stats[2],
        "avg_xpm": radiant_stats[3],
        "players": radiant_players
    })

    # Dire row
    rows.append({
        "match_id": match["match_id"],
        "team_id": dire_id,
        "team_name": dire_name,
        "team": "dire",
        "win": int(not radiant_win),
        "total_kills": dire_stats[0],
        "total_deaths": dire_stats[1],
        "avg_gpm": dire_stats[2],
        "avg_xpm": dire_stats[3],
        "players": dire_players
    })

    return rows


def main():
    matches = load_json_files()
    all_rows = []

    print(f"Processing {len(matches)} matches...")

    for match in matches:
        rows = process_match(match)
        all_rows.extend(rows)

    df = pd.DataFrame(all_rows)

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print("Saved to", PROCESSED_PATH)
    print(f"Total rows: {len(df)}")
    print(df.head())


if __name__ == "__main__":
    main()