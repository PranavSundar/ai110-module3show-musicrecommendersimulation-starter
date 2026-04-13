# Reflection: Profile-to-Profile Comparisons

I compared the recommender outputs across multiple profiles to check whether the ranking logic behaves in a way that makes musical sense.

High-Energy Pop vs Chill Lofi: the pop profile pushed energetic and upbeat songs to the top (`Sunrise City`, `Gym Hero`), while the lofi profile shifted strongly toward calmer tracks (`Library Rain`, `Midnight Coding`). This makes sense because the lofi profile combines low energy with higher acousticness.

High-Energy Pop vs Deep Intense Rock: both profiles still liked high-energy songs, but the top result changed from `Sunrise City` to `Storm Runner` when genre and mood moved to rock/intense. That confirms the categorical features still matter, even after reducing genre weight.

Chill Lofi vs Deep Intense Rock: these produced almost opposite top lists. Chill lofi emphasized lower tempo-feeling and softer vibe songs, while intense rock favored aggressive high-energy tracks with lower valence.

Deep Intense Rock vs Conflicting Sad+High Energy: when mood became "sad" but energy stayed very high, the system mostly returned intense/party songs and ignored the emotional intent. This shows a limitation: when the catalog lacks matching mood labels, the model leans on numeric energy.

Conflicting Sad+High Energy vs Numeric-Only profile: the conflicting profile repeatedly returned very high-energy songs, while the numeric-only profile produced more varied "middle" tracks because it balanced four numeric features at once. That difference suggests multi-feature numeric matching can reduce single-feature dominance.

Plain-language takeaway: if someone says "I want happy pop," the system tends to keep showing songs like `Gym Hero` because they are close on both category and energy. If someone gives mixed signals, the heaviest numeric weight can take over and produce results that feel mathematically consistent but emotionally wrong.
