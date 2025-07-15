# Reddit User Persona Generator (Groq + LLaMA3)

This project fetches Reddit user activity (posts/comments) and uses Groq's LLaMA3 model to generate a user persona.

## 🔧 How it Works

- Enter a Reddit user URL (e.g., https://www.reddit.com/user/spez/)
- The script fetches their public Reddit posts and comments
- Sends content to Groq’s LLaMA3 API
- Saves a detailed persona as a `.txt` file

## 🚀 Setup

1. Clone the repo
2. Create a `.env` file with your Groq API key:
    ```
    GROQ_API_KEY=your_api_key_here
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the script:
    ```bash
    python reddit_persona_groq.py
    ```

## 🛡️ Notes

- This version uses Groq’s LLaMA3 instead of OpenAI or Hugging Face
- Do not commit your API keys — use `.env` + `.gitignore`

## 📂 Example Output

