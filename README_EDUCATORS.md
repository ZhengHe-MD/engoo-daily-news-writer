# 📚 Engoo Daily News Writer - For Educators

Transform any online article into professional ESL lessons in seconds! 

**Perfect for:** ESL teachers, language instructors, and educators who want to create engaging lessons from current events and interesting articles.

## ✨ What It Does

- **Converts any article** into Engoo-style ESL lessons
- **Creates vocabulary lists** with definitions and examples  
- **Generates discussion questions** for classroom engagement
- **Shares lessons online** instantly via GitHub
- **Professional formatting** that looks great on any device

## 🚀 Quick Start (5 minutes!)

### Step 1: Download
```bash
git clone https://github.com/ZhengHe-MD/engoo-daily-news-writer.git
cd engoo-daily-news-writer
```

### Step 2: Easy Installation
```bash
./easy_install.sh
```

The installer will:
- ✅ Check your system requirements  
- ✅ Install all needed components
- ✅ Help you set up your API keys
- ✅ Test everything works

### Step 3: Get Your API Keys

You'll need two free accounts:

#### OpenAI API Key (for AI processing)
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

#### GitHub Token (for sharing lessons)
1. Go to [GitHub Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Name it "Engoo Writer" 
4. Check the "gist" permission
5. Generate and copy the token

## 📖 How to Use

### Convert an Article
```bash
./engoo-writer convert https://example.com/interesting-article
```

### Convert and Share Online
```bash
./engoo-writer convert https://example.com/article --gist
```

### Manage Your Shared Lessons
```bash
# List all your lessons
./engoo-writer gist list

# View a specific lesson
./engoo-writer gist get [lesson-id]

# Delete a lesson
./engoo-writer gist delete [lesson-id]
```

## 🎯 Example Output

The tool creates professional ESL lessons with:

- **Title** - Clear, engaging lesson title
- **Vocabulary** - 8-10 intermediate words with definitions
- **Article** - Rewritten for ESL learners (300-500 words)  
- **Discussion** - 4-5 conversation starter questions
- **Further Discussion** - 3-4 advanced thinking questions

## 🌟 Perfect For

- **ESL Teachers** - Create fresh lessons from current events
- **Language Schools** - Quickly generate classroom materials  
- **Online Instructors** - Share lessons with students instantly
- **Private Tutors** - Customize lessons for student interests

## 💡 Pro Tips

1. **Choose good articles** - Tech blogs, science news, and opinion pieces work great
2. **Share with students** - The online links work on any device
3. **Build a library** - Use `gist list` to organize your lessons
4. **Customize further** - Edit the generated HTML for specific needs

## 🆘 Need Help?

- Run `./engoo-writer --help` for all commands
- Check our [Issues page](https://github.com/ZhengHe-MD/engoo-daily-news-writer/issues) for common problems
- The tool works best with articles 500-2000 words long

## 🔒 Privacy & Security

- Your API keys stay on your computer
- Generated lessons are stored in your GitHub account
- No data is sent to our servers
- You control all your content

---

**Ready to revolutionize your ESL teaching?** Run `./easy_install.sh` and start creating amazing lessons! 🚀

---

*Made with ❤️ for educators worldwide*
