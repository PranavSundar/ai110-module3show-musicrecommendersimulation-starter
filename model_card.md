# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMixer 1.0**

---

## 2. Intended Use  

This model suggests songs from a small CSV list.  
It is for class practice.  
It is not for real users.  
It assumes users can describe taste with simple settings.

---

## 3. How the Model Works  

Each song gets points.  
Genre match adds points.  
Mood match adds points.  
Energy, valence, danceability, and acousticness add points if close to user targets.  
Then songs are sorted by score.  
Top 5 songs are returned.  
I also tested one experiment.  
I lowered genre weight.  
I raised energy weight.

---

## 4. Data  

The dataset has 20 songs in `data/songs.csv`.  
Each row has genre, mood, energy, tempo, valence, danceability, and acousticness.  
I added songs to increase genre and mood variety.  
The dataset is still small.  
Many tastes are still missing.

---

## 5. Strengths  

The model works best with clear preferences.  
"Chill Lofi" gave chill songs near the top.  
"Deep Intense Rock" put `Storm Runner` first.  
That felt right.  
The CLI reasons make results easy to follow.

---

## 6. Limitations and Bias 

One weakness is energy bias.  
If energy target is high, high-energy songs keep rising.  
This can happen even when mood does not match.  
The model also cannot recommend songs that are not in the catalog.  
If a mood label is missing, results can feel off.  
Also, mood matching is exact text only.

---

## 7. Evaluation  

I tested five profiles.  
High-Energy Pop.  
Chill Lofi.  
Deep Intense Rock.  
Conflicting Sad + High Energy.  
Numeric-Only.  
I compared top 5 results for each one.  
I checked if reasons matched the vibe I expected.  
I also changed weights once.  
Lower genre. Higher energy.  
That made results more energy-driven.

### Intended Use and Non-Intended Use

Intended use: class project demo, simple recommendation experiments, and scoring logic practice.  
Non-intended use: real music apps, mental health mood advice, or decisions that need fairness guarantees.  
This model is too small and too hand-tuned for real production use.

---

## 8. Future Work  

- Add many more songs and broader mood labels.  
- Add a diversity rule so top 5 is not all one style.  
- Support mixed preferences (for example 70% chill + 30% energetic) instead of a single point target.

---

## 9. Personal Reflection  

My biggest learning moment was weight tuning.  
One small weight change moved many songs.  
AI tools helped me move faster.  
But I still had to verify math and file names by hand.  
I was surprised that a simple point system can still feel like a real recommender.  
Next, I would add more data and better diversity rules.  
I would also add a "why not this song" explanation.
