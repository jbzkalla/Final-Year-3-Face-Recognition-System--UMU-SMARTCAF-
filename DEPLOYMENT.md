# UMU SmartCaf Deployment Guide 🚀

This document provides instructions on how to deploy the **UMU SmartCaf** system for real usage at Uganda Martyrs University.

## Option 1: Local University Network (Recommended)
This is the most practical way to run the system in a cafeteria. You run the server on one central PC (Server) and access it from other PCs, Tablets, or Phones in the canteen.

### 1. Preparation
Ensure Python is installed on the Server PC.
Open a terminal in the project folder and install dependencies:
```powershell
pip install -r requirements.txt
```

### 2. Identify Server IP
You need to find the IP address of the Server PC:
1. Open Command Prompt.
2. Type `ipconfig`.
3. Look for "IPv4 Address" (e.g., `192.168.1.15`).

### 3. Launch the System
Instead of using `python main.py`, use the production command:
```powershell
python wsgi.py
```
This will start the system in **Production Mode** on port `8080`.

### 4. Accessing from Other Devices
On any other device connected to the same UMU Wi-Fi:
1. Open a web browser (Chrome/Edge).
2. Enter the Server's IP address followed by `:8080`.
   * Example: `http://192.168.1.15:8080`

## Option 2: Live Online Demo (Using Phone Hotspot)
If you want to show the system to someone *outside* your Wi-Fi immediately, you can use a "Tunneling" tool. This makes your local computer accessible via a temporary public link (e.g., `umu-caf.ngrok-free.app`).

### 1. Using Ngrok (Easiest)
1.  Download **Ngrok** from [ngrok.com](https://ngrok.com).
2.  In your terminal, while the system is running (`python wsgi.py`), run:
    ```powershell
    ngrok http 8080
    ```
3.  Ngrok will give you a "Forwarding" link like `https://xxxx.ngrok-free.app`.
4.  Share that link! Anyone in the world can now view your UMU SmartCaf in real-time.

---

## Option 3: Professional Cloud Hosting
To have the system online 24/7 without needing your laptop to stay on, you should use a Cloud Provider.

### 1. PythonAnywhere (Recommended for Flask)
This is the most popular choice for Python/Flask apps.
1. Create an account at [PythonAnywhere.com](https://www.pythonanywhere.com/).
2. Upload the `try wee3` folder files.
3. Set up a "Web App" pointing to your `main.py` file.
4. Your site will be available at `yourusername.pythonanywhere.com`.

### 2. DigitalOcean or AWS (Advanced)
For a large-scale university system, you would use a VPS (Virtual Private Server). 
*   **Pros**: Higher speed, handles thousands of students.
*   **Cons**: Requires more setup and monthly cost.

---

## The Best Architecture for UMU
For the most reliable cafeteria experience, we recommend a **Hybrid Setup**:

1.  **The Cloud Server**: Host the main portal (Database, Finance, Reports) on **PythonAnywhere** or **Heroku**. This allows students to check their balance from home on their phones.
2.  **The Canteen Terminals**: In the canteen, place a Tablet or a PC with a camera. Open the browser and go to your cloud URL.
3.  **Real-Time Biometrics**: Because the biometric scanning happens in the **Browser**, the Face AI will work perfectly even if the server is in the cloud—as long as the Canteen device has a camera and internet.

---

## Security Checklist for Launch
- [ ] **Change the Default Admin Password**: Don't use `admin123` in a live environment.
- [ ] **Enable 2FA**: Go to System Settings and ensure 2FA is enabled for all Admin/Staff accounts.
- [ ] **HTTPS**: When hosting online, ensure your link starts with `https://`. This is required for the camera to work in modern browsers.
- [ ] **Data Backup**: Regularly download the `data/` folder from your cloud server.

---

**System is ready for the world!** 🕊️
