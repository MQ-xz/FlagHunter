# FlagHunter 🤖🚩

An autonomous AI agent framework for solving CTF challenges automatically. More than just a tool - it's an extensible framework that you can customize for your specific use cases with plug-and-play architecture.

## ✨ What It Does

- 🎯 **Automatically solves CTF challenges** - Just give it a challenge URL
- 🔧 **Handles everything** - Downloads files, analyzes code, runs exploits, submits flags
- 🏗️ **Framework architecture** - Not just a tool, but an extensible platform
- 🔌 **Plug-and-play extensions** - Easy to add new platforms, tools, and capabilities
- 📦 **Ready to use** - Works out of the box with proper configuration

## 🚀 Quick Start

1. **Get the code:**
```bash
git clone https://github.com/MQ-xz/FlagHunter.git
cd FlagHunter
pip install -r requirements.txt
```

2. **Setup configuration:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Run it:**
```bash
python app.py "https://labs.hackthebox.com/challenges/your-challenge"
```

## 🎥 Demo Videos

### Solving Protein Cookies (HTB)
[![Solving Protein Cookies (HTB)](https://img.youtube.com/vi/wYipvYGVxlQ/maxresdefault.jpg)](https://youtu.be/wYipvYGVxlQ)

### Solving RSAisEasy (HTB)
[![Solving RSAisEasy (HTB)](https://img.youtube.com/vi/ccN4FukafU4/maxresdefault.jpg)](https://youtu.be/ccN4FukafU4)

## ⚙️ Configuration

### Getting HTB Token
1. Login to Hack The Box
2. Open browser dev tools (F12)
3. Look at any API request
4. Copy the `Authorization` header
5. Add to `.env` as `HTB_AUTH_TOKEN=Bearer your_token`

## 🤖 How It Works

Built with LangChain, the AI agent automatically:
1. 📥 Downloads challenge files
2. 🔍 Analyzes the challenge
3. 🛠️ Creates and runs exploits
4. 🚩 Finds and submits the flag

## 🔌 Extending the Agent

### Adding New Platforms

Want to support TryHackMe, PicoCTF, or other platforms? It's easy!

1. **Create a new file** in `ctf_platform/your_platform.py`
2. **Copy the structure** from `htb.py` 
3. **Update the API calls** for your platform
4. **Add to** `app.py` imports

The LangChain framework handles the rest automatically.

### Adding New Tools

Need the agent to do something new?

1. **Add function** to `tools/` directory
2. **Import it** in your platform file
3. **Add to TOOLS list**

The AI will automatically learn to use your new tool! Check the [LangChain documentation](https://docs.langchain.com/docs/modules/agents/tools/) for more details on tool creation.



## 🤝 Contributing

We'd love your help! This project welcomes:

- 🌐 **New platform support** (TryHackMe, PicoCTF, etc.)
- 🛠️ **New tools and features** 
- 📚 **Better documentation**
- 🐛 **Bug fixes and improvements**

Just fork the repo, make your changes, and submit a PR!

## � Roadmap

- [ ] More CTF platforms
- [ ] Web interface 
- [ ] Better logging
- [ ] Challenge difficulty assessment

## 🔒 Security & Environment

**⚠️ IMPORTANT**: Always run FlagHunter in a sandboxed environment or virtual machine since the AI agent executes system commands. This protects your host system from potentially harmful commands generated during exploitation attempts.

Recommended environments:
- Docker containers
- Virtual machines (VMware, VirtualBox)
- Sandboxed Linux environments
- Cloud instances

We recommend using specialized distributions like Kali Linux which come with pre-installed security tools, reducing dependency installation issues.

## 📞 Support & Links

- 🐛 **Issues**: [GitHub Issues](https://github.com/MQ-xz/FlagHunter/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/MQ-xz/FlagHunter/discussions)
- 📖 **LangChain Docs**: [docs.langchain.com](https://docs.langchain.com/)

---

**⚖️ Legal**: For educational and authorized testing only. Always ensure you have permission before testing on any system.