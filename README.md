# volibr
Volibr is a self-hosted, privacy-respecting platform that lets users upload and manage their personal book collection and listen to narrated versions using AI-generated voices. Designed for book lovers and tech enthusiasts, Volibr turns your bookshelf into an intelligent, voice-powered experience.

---

## 🚀 Features

- 📚 Upload and organize your personal books (PDF*)
- 🗣️ AI text-to-speech narration using local TTS engines
- 🎧 Streamlined audiobook-style playback with resume support
- 🌐 Clean web-based interface
- 🔐 100% local and self-hosted – no cloud dependency

> \* Scanned PDF files are not supported yet. Even in the future when it does get supported, you should own the material or have permission to consume the material.

---

## ⚙️ Tech Stack

- Python (Flask)
- TTS Engine: Piper
- SQLite
- NGINX

---

## ⚙️ Getting Started

### 🧑‍💻 For Developers

1. **Install Docker & Git**
2. Clone the repository:
   ```bash
   git clone https://github.com/kesh-lk/volibr.git
   cd volibr
   ```
3. Start the development environment:
   ```bash
   docker compose --profile dev up
   ```

> Use this profile if you’re contributing code, debugging, or customizing.

---

### 📦 For Users / Consumers

1. **Install Docker**
2. Clone the repository:
   ```bash
   git clone https://github.com/kesh-lk/volibr.git
   cd volibr
   ```
3. Start the production server:
   ```bash
   docker compose --profile prod up
   ```

> This launches the app with optimal settings for personal use.

---

### 🌐 Login & Usage

Once the app is running:

1. Open your browser and go to:  
   👉 `http://localhost:8080`
2. Login to the admin panel using:  
   - **Email**: `admin`  
   - **Password**: `admin`
3. Inside the admin panel:
   - Add **member accounts** by entering a name and email.
4. For members logging in:
   - On first login, enter the registered **email** and leave the **password blank**.
   - The system will prompt to set a new password.
5. Once logged in as a member:
   - Click the **upload icon** in the navbar to upload books you **own or have permission to use**.

---

## 🤝 Contributing

Pull requests are welcome for personal-use features and bug fixes.  
Commercial enhancements or integrations will not be accepted.

---

## ❗️Disclaimer & Legal Notice

**Volibr is strictly for non-commercial, personal use only.**

This software is provided as a tool to privately manage and interact with books you **legally own**. The author of this software:

- ❌ Does **not condone** or encourage piracy or unauthorized distribution of copyrighted materials.
- ❌ Is **not responsible** for how users obtain, upload, or use content within the platform.
- ✅ Emphasizes that it is the **user’s responsibility** to comply with all applicable copyright laws and licensing terms.

By using this software, you agree that **you are solely liable** for any legal issues arising from the misuse of copyrighted content.

---

## 📄 License

This project is licensed under a **Personal Use License**.  
- ✅ You may use, modify, and self-host this project for **non-commercial, personal purposes only**.  
- ❌ **Commercial use is strictly prohibited** without prior written consent.

See [`LICENSE`](./LICENSE) for full terms.  
For commercial licensing inquiries, contact: `your@email.com`.

---

**Volibr** – Your voice-powered personal reading companion.
