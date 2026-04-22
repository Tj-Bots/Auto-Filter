![SearchGram](https://i.ibb.co/v6b10BjN/03f383b6faeb.jpg)

![Typing SVG](https://readme-typing-svg.herokuapp.com/?lines=Welcome+To+My+Search+Movies+Bot!)

# ***Search-Movies***
**A Telegram bot for searching movies quickly and easily.**

---

### ✨ Key Features:
- [x] 🎬 Search for movies and series with ease and speed.
- [x] 💾 Save entire channel content to the database with a single command.
- [x] 🔎 Search from anywhere – use the bot inline in any chat.
- [x] ✅ Mandatory subscription to the updates channel to use the bot.
- [x] 🚫 Ban management – full control over users and groups.
- [x] 📨 Broadcast messages to users and groups (with optional "forwarded from" tag).
- [x] 📊 Log channel – real-time tracking of new users/groups activity.
- [x] 📱 Cool features – TikTok video download without watermark, and many more.
- [x] ℹ️ MediaInfo – display technical details of files.
- [x] 📤 Telegraph – upload images to i.ibb.co.
- [x] 🖼️ Extract thumbnail – extract thumbnails from Telegram videos.

---

### Easy and convenient search interface:
![PhotoSearch](https://i.ibb.co/7JNbBrT1/8fb3d03608dc.jpg)

---

# ⚙️ ***Bot Commands***

```
start       - Start the bot.
stats       - View bot statistics.
id          - Get user/chat ID.
info        - Get user information (profile, name, username, ID, etc.).
tts         - Convert text message to speech.
font        - Transform English text into fancy fonts.
share       - Share text via a quick link.
paste       - Upload text/file to Pastebin and get a link.
stickerid   - Get the ID of a replied sticker.
json        - Get technical (JSON) info of a message.
written     - Convert text into a .txt file.
d           - Download video from TikTok.
mediainfo   - Get MediaInfo of a file.
telegraph   - Upload an image to i.ibb.co servers.
extract_thumbnail - Extract a thumbnail from a media file.
```

---

# ***⌨️ Admin Commands***

```
index          - [link] - [start] – Index a channel. Adds all files to the database. [Admin only]
newindex       - [id] – Auto-index new files sent to a channel. [Admin only]
channels       - Manage watched channels. [Admin only]
clean          - Delete all files or all saved users from the index. [Admin only]
broadcast      - Broadcast a message to all users. [Admin only]
broadcast_groups - Broadcast a message to all groups. [Admin only]
restart        - Restart the bot. [Admin only]
ban            - [id] – Ban a user. [Admin only]
unban          - [id] – Unban a user. [Admin only]
ban_chat       - [id] – Ban a group. [Admin only]
unban_chat     - [id] – Unban a group. [Admin only]
leave          - [id] – Leave a group (without banning). [Admin only]
```

_To add these commands to your bot, send the `/setcommands` command to [@BotFather](https://t.me/botfather)._

---

# 🛠 Variables

<details>
<summary><b>Click to expand</b></summary>

For the bot to work, you must define the following variables in a `.env` file or on your server:

| Variable | Required | Where to get it |
| :--- | :---: | :--- |
| `API_ID` | ✅ | [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | ✅ | [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | ✅ | From [@BotFather](https://t.me/BotFather) |
| `MONGO_URI` | ✅ | From [MongoDB](https://www.mongodb.com) |
| `DB_NAME` | ✅ | Choose a random name (e.g., `MovieBot`) |
| `ADMINS` | ✅ | Send `/me` to [@GetChatID_IL_BOT](https://t.me/GetChatID_IL_BOT) |
| `LOG_CHANNEL` | ✅ | Add bot to channel, send a message, forward it to [@GetChatID_IL_BOT](https://t.me/GetChatID_IL_BOT) |
| `UPDATE_CHANNEL` | ❌ | Channel username (without @) |
| `REQUEST_GROUP` | ❌ | Link to support/request group |
| `PHOTO_URL` | ❌ | Direct image URL (used as bot cover) |
| `AUTH_CHANNEL_FORCE` | ❌ | Force subscription to update channel. `False` or `True` |

</details>

---

# 🚀 Running the Bot

<details>
<summary><b>🐧 Run on Linux Server (VPS / Terminal)</b></summary>

**Update and install git & Python:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git python3-pip -y
```

Clone the repository:

```bash
git clone https://github.com/Tj-Bots/Search-Movies
cd Search-Movies
```

Install required libraries:

```bash
pip3 install -r requirements.txt
```

Create environment file:
Rename sample_env to .env and edit it with your details:

```bash
cp sample.env .env
nano .env
```

Run the bot:

```bash
python3 search_bot.py
```

</details>

<details>
<summary><b>🐳 Run with Docker</b></summary>

1. Build the image:

```bash
docker build . -t movie-bot
```

2. Run the container:
Make sure your .env file is updated and complete.

```bash
docker run --env-file .env movie-bot
```

</details>

---

**Test Bot: [@AutoFilterTestJBot](https://t.me/AutoFilterTestJBot)**
**Updates Channel: [@TJ_Bots](https://t.me/TJ_Bots)**

---

©️ **Bot created by [@TJ_Bots_Admin](https://t.me/TJ_Bots_Admin)**
