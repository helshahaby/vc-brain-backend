# 🧠 VC Brain Backend Engine Setup & Workflow

This system acts as an AI-powered Venture Capital Investment Committee. It connects your web application to a smart backend pipeline that automatically analyzes incoming startup data and provides evaluation scores.

---

## 🗺️ 1. How the Entire System Works (The Architecture)

The system works like a smooth three-way handshake between your frontend web interface, the backend engine, and your database:

1. **Request Phase:** You type a prompt into your web application dashboard (for example, asking to evaluate a startup like Vectorloom or Kairo Health). The frontend packages this request and sends it over the internet to your backend engine.
2. **AI Agent Processing Phase:** The backend engine receives the message. It checks a secret password to ensure the request is authorized. If everything looks good, it boots up an AI framework powered by OpenAI. The AI acts as a tough venture capitalist, analyzing the startup's name and details across multiple categories like leadership capability, technical depth, and market fit.
3. **Hybrid Response Phase:** The AI produces a detailed text write-up alongside raw numerical scores. The backend packages both items together and sends them back to your web browser. 
4. **Database Sync Phase:** The web browser reads the detailed text out loud on your screen and instantly drops the raw scores into your Supabase database table. Because the frontend handles the database update, your data changes instantly and securely.

---

## 🛠️ 2. Setting Up the Environment

To get this backend running on your computer, you need to prepare your machine by setting up the necessary files and credentials.

* **Step A: Install Python:** Make sure you have Python version 3.10 or higher installed on your system.
* **Step B: Prepare Packages:** You will use a package management file to download standard web and AI libraries, including FastAPI (to run the server), Uvicorn (to process traffic), and OpenAI (to connect to the AI model).
* **Step C: Configure Variables:** You must create a hidden configuration file named `.env` in the root directory of your project folder. This file holds your private credentials. You will add your Supabase database URL, your Supabase service key, a custom secret token of your choosing, and your personal OpenAI developer API key.

---

## 💻 3. Explaining the Code Modules

The application is split into two straightforward core segments:

### Module 1: The Communicator (`main.py`)
* This script manages the web server traffic. 
* It opens up security access rules so your frontend preview application won't be blocked by your computer's browser protections.
* It listens at a specific web address called `/api/copilot`. When you send a prompt, it checks your secret token header. If the security secret doesn't match, it completely rejects the visitor.
* It checks the prompt text to figure out which startup you are asking about, triggers the AI engine, and formats the output into a clean package containing a markdown summary and a flat metrics bucket.

### Module 2: The Brain (`agent_engine.py`)
* This script talks directly to OpenAI's smart models.
* It defines a strict data structure to ensure the AI only responds with proper parameters (like numbers from 0 to 100) instead of rambling text.
* It includes smart shortcut rules: for example, if it detects specific founder names or exceptional engineering setups, it bypasses random testing and automatically flags the opportunity as a highly recommended investment.
* It has a built-in safety net. If your internet drops or the AI makes a mistake, the script intercepts the crash and sends a safe fallback recommendation so your application never freezes.

---

## 🚀 4. Step-by-Step Instructions to Run the Project

Follow these exact steps to start the application and connect it to your web workspace:

* **Step 1:** Open your terminal or command prompt. Move into your project workspace folder using your machine's change directory commands.
* **Step 2:** Install your requirements by typing the standard package install command pointed at your package text list file (`pip install -r requirements.txt`).
* **Step 3:** Launch the local server. Run the uvicorn start command with hot-reloading enabled (`uvicorn main:app --reload`). Your terminal will show that the server is successfully alive and listening on your local machine port 8000.
* **Step 4:** Make the server public. Because your web application runs in the cloud, it cannot see a local port on your personal computer. Open a second terminal window and use ngrok to create a secure tunnel (`ngrok http 8000`).
* **Step 5:** Connect to the web app. Copy the public web link provided by ngrok, paste it into your web app's settings panel as your new backend base address, and add your secret authentication token.

---

## 🔍 5. Troubleshooting Common Pitfalls

* **If you see an "API Key Error":** Your hidden configuration file is either missing or using an incorrect OpenAI key. Double-check your environment file variables.
* **If you see "Metrics Not Applied":** This means the backend successfully analyzed the data, but your web dashboard doesn't know where to save it. Simply open a specific startup's detail card or investment memo page on your screen first, then run your prompt again.
