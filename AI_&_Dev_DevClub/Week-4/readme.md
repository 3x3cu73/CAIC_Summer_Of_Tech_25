# 🧩 ML+Dev Track: Week 4  
## 🖥️ Frontend + System Integration (Task 3)

### 🔁 Quick Recap  
Last week, you:  
- Built a tweet generation engine  
- Created a `/generate` API using templates (or optional AI)  
- Ran it alongside your Week 2 `/predict` API  
- Saw both endpoints working independently

Now, it’s time to **tie everything together with a frontend**!  

Your goal this week:  
**Build a local app where users enter tweet metadata and get:**
- A generated tweet
- A prediction of how many likes it might get

---  

## 🎯 Week 4 Goals  

By the end of this week, you will:
- Build a frontend (use **Streamlit**, **Flask**, or **React**—your choice)
- Connect the frontend to your existing APIs
- Collect input from the user (like `company`, `message`, `tweet_type`, etc.)
- Display the generated tweet and predicted likes
- Make the app interactive and easy to test

**✅ Deliverable: A working app users can run locally and try out.**

---

## ⚙️ Step 1: Choose a Frontend Stack

You can use one of the following options (whichever you're most comfortable with):

| Option     | Description | Difficulty |
|------------|-------------|------------|
| Streamlit  | Easiest to get started, great for ML demos | ⭐ |
| Flask      | Full control over UI using HTML templates | ⭐⭐ |
| React      | Most flexible, requires frontend skills | ⭐⭐⭐ |

Pick one, and set up a basic form where the user can:
- Enter a company name
- Select tweet type (`announcement`, `question`, etc.)
- Input a message or topic
- Submit the form and get a result

---

## 🔗 Step 2: Connect to Your APIs

You’ve already built:
- `POST /predict` for estimating likes (Week 2)
- `POST /generate` for generating tweet text (Week 3)

Use your frontend to send a `POST` request to each API:

```python
import requests

# Send to /generate
generate_resp = requests.post("http://localhost:5001/generate", json={
    "company": "Nike",
    "tweet_type": "announcement",
    "message": "launching new running shoes",
    "topic": "fitness"
})
generated_tweet = generate_resp.json()["generated_tweet"]

# Use generated tweet to extract features (word count, char count, etc.)
features = {
    "word_count": len(generated_tweet.split()),
    "char_count": len(generated_tweet),
    "has_media": False,   # You can make this a checkbox in the UI
    "hour": 12,           # Or ask user to select a time
    "sentiment": 0.5      # Optional: use a placeholder or basic analysis
}

# Send to /predict
predict_resp = requests.post("http://localhost:5000/predict", json=features)
predicted_likes = predict_resp.json()["predicted_likes"]
```

Once you’ve done this, you can:
- Show the tweet the model generated
- Display how many likes it predicts
- Optionally show the metadata you sent

---

## 💡 UX Tip: Make It Fun

Users should be able to:
- Change the tweet message or topic and see different outputs
- Pick tweet type from a dropdown
- Hit a "Generate & Predict" button and see a result instantly

This is your chance to **turn your model into a product demo** 🎯

---

## 🧪 Step 3: Test the Full Flow

Start both APIs:

```bash
# Terminal 1
python app.py  # Week 2

# Terminal 2
python app_generator.py  # Week 3
```

Then run your frontend:

```bash
# Streamlit
streamlit run app_ui.py

# Flask
python app_frontend.py

# React
npm start
```

Check that the entire flow works from end to end:
- User enters data ➡️
- Tweet is generated ➡️
- Tweet is scored ➡️
- Everything appears in the UI

---

## ✅ Week 4 Core Deliverables

- [ ] Frontend that accepts user input (company, tweet type, etc.)
- [ ] Connects to your `/generate` API
- [ ] Extracts features and calls `/predict` API
- [ ] Displays both the tweet and the like prediction

This is your **first full-stack AI+Dev integration**! 🎉

---

## 🏆 BONUS IDEAS

Want to impress? Try these:

### 🌐 Bonus 1: Host It
- Deploy your app to HuggingFace Spaces (for Streamlit)
- Or try Render, Vercel, or Replit for simple hosting

### 🤖 Bonus 2: Auto Feature Extraction
- Automatically calculate word count, char count, sentiment, etc.
- Use libraries like `textblob` or `vaderSentiment` for quick sentiment scores

### 🔁 Bonus 3: One-Click "Generate + Predict"
- Make a single button that runs both calls and updates the UI

---

## 📚 Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Flask Quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/)
- [requests Library](https://docs.python-requests.org/)
- [HuggingFace Spaces](https://huggingface.co/spaces)

---

## 🔮 What’s Next (Week 5 Preview)

You’ll:
- Polish your code for presentation
- Add visual polish or branding
- Record a demo video or create a walkthrough
- Share it with others!

---

## 🙋 Common Questions

**Q: Do I need to host this online?**  
A: Nope! Just make it work on your machine for now.

**Q: What if I’m not a frontend person?**  
A: Use Streamlit! It’s made for ML developers and super easy.

**Q: Should I still keep the Week 2 & 3 APIs as separate files?**  
A: Yes – no need to merge yet. Just connect to both from your UI.

---
