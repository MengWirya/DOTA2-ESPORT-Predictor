import pandas as pd
import ast
from collections import defaultdict
import math

INPUT_PATH = "data/processed/matches.csv"
OUTPUT_PATH = "data/processed/features.csv"


def load_data():
    df = pd.read_csv(INPUT_PATH)

    # Convert string list → actual list
    df["players"] = df["players"].apply(ast.literal_eval)

    return df


# def compute_overlap(players1, players2):
#     return len(set(players1) & set(players2))


# def main():
#     df = load_data()

#     # Sort by match_id (proxy for time)
#     df = df.sort_values("match_id")

#     # History storage
#     team_history = defaultdict(list)
#     roster_history = defaultdict(lambda: {"matches": 0, "wins": 0})

#     feature_rows = []

#     for _, row in df.iterrows():
#         team_id = row["team_id"]
#         players = row["players"]
#         win = row["win"]

#         # -------- SYNERGY CALCULATION --------

#         past_matches = team_history[team_id]

#         if len(past_matches) == 0:
#             stability = 0
#             shared_matches = 0
#             roster_winrate = 0
#         else:
#             overlaps = []
#             relevant_matches = []

#             for past in past_matches:
#                 overlap = compute_overlap(players, past["players"])
#                 overlaps.append(overlap)

#                 # consider same core (>=3 players)
#                 if overlap >= 3:
#                     relevant_matches.append(past)

#             # Stability: average overlap
#             stability = sum(overlaps) / (5 * len(overlaps))

#             # Shared experience
#             shared_matches = len(relevant_matches)

#             # Performance
#             if shared_matches > 0:
#                 wins = sum(m["win"] for m in relevant_matches)
#                 roster_winrate = wins / shared_matches
#             else:
#                 roster_winrate = 0

#         # Final synergy score
#         synergy_score = (
#             0.4 * stability +
#             0.3 * math.log(1 + shared_matches) +
#             0.3 * roster_winrate
#         )

#         # -------- ACTIVITY FEATURE --------
#         activity = len(past_matches)

#         # -------- RECENT WIN RATE --------
#         if len(past_matches) > 0:
#             recent = past_matches[-10:]  # last 10 matches
#             recent_winrate = sum(m["win"] for m in recent) / len(recent)
#         else:
#             recent_winrate = 0

#         # -------- SAVE ROW --------
#         new_row = row.to_dict()
#         new_row["synergy_score"] = synergy_score
#         new_row["activity"] = activity
#         new_row["recent_winrate"] = recent_winrate

#         feature_rows.append(new_row)

#         # -------- UPDATE HISTORY (AFTER COMPUTE) --------
#         team_history[team_id].append({
#             "players": players,
#             "win": win
#         })

#     feature_df = pd.DataFrame(feature_rows)
#     feature_df.to_csv(OUTPUT_PATH, index=False)

#     print("Saved features to:", OUTPUT_PATH)
#     print(feature_df.head())

def main():
    df = pd.read_csv("data/processed/features.csv")
    print(df["activity"].value_counts())


if __name__ == "__main__":
    main()