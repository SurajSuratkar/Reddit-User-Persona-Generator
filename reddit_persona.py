# reddit_persona_groq.py

import praw
import os
from datetime import datetime
from groq import Groq


REDDIT_CLIENT_ID = "4b8G_SOt6am--amlYgalcQ"
REDDIT_CLIENT_SECRET = "g00sOmpX9fTlaIZGj_n2_d_Rd9ay1g"
REDDIT_USER_AGENT = "reddit-persona-script by u/Adventurous_Pair8194"
GROQ_API_KEY = "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" 

client = Groq(api_key=GROQ_API_KEY)


def fetch_reddit_data(username):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        check_for_async=False
    )
    try:
        user = reddit.redditor(username)
        _ = user.id
    except Exception as e:
        print(f" Reddit error: {e}")
        return []

    data = []
    for s in user.submissions.new(limit=10):
        data.append({
            "type": "post",
            "title": s.title,
            "body": s.selftext,
            "url": f"https://reddit.com{s.permalink}"
        })

    for c in user.comments.new(limit=20):
        data.append({
            "type": "comment",
            "body": c.body,
            "url": f"https://reddit.com{c.permalink}"
        })

    return data


def generate_persona(data):
    if not data:
        return "No data to analyze."

    content = ""
    for item in data[:10]:
        if item["type"] == "post":
            content += f"\n[POST] {item['title']}\n{item['body'][:300]}\nLink: {item['url']}\n"
        else:
            content += f"\n[COMMENT] {item['body'][:300]}\nLink: {item['url']}\n"

    prompt = f"""
You are an AI tasked with creating a user persona from Reddit activity.

Based on the following content, describe:
- Interests
- Behavior
- Tone
- Opinions
- Personality traits

Cite the links provided for evidence.

{content}

Persona:
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",  
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- MAIN ---
def main():
    url = input("Enter Reddit user URL: ").strip()
    if not url.startswith("https://www.reddit.com/user/"):
        print(" Invalid Reddit URL format")
        return

    username = url.strip("/").split("/")[-1]
    data = fetch_reddit_data(username)
    if not data:
        print("No data found.")
        return

    print("Generating persona using Groq + LLaMA3...")
    persona = generate_persona(data)

    filename = f"{username}_persona_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(persona)

    print(f"✅ Persona saved to {filename}")
    try:
        os.startfile(filename)
    except:
        print(" File saved, but couldn't open automatically.")

if __name__ == "__main__":
    main()
