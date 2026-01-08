"""
JARVIS - FIXED SCREENSHOT ERROR VERSION
"""

import subprocess
import time
import webbrowser
import os
import datetime
import speech_recognition as sr
import random
import psutil
import ctypes
from ctypes import wintypes


class JarvisFixed:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.awake = False
        self.last_command = ""
        self.last_command_time = 0
        self._setup_listening()

    def _setup_listening(self):
        """SETUP FOR GOOD LISTENING"""
        print("🔧 Configuring listening system...")

        # Good sensitivity settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0

        print("✅ Listening system configured")

    def speak(self, text):
        """SPEAK TEXT"""
        print(f"\n🔊 JARVIS: {text}")
        try:
            cmd = f'PowerShell -Command "$speak = New-Object -ComObject SAPI.SpVoice; $speak.Speak(\'{text}\')"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            print(f"💬 (Speaking): {text}")
        time.sleep(0.1)

    def listen_continuously(self):
        """LISTEN CONTINUOUSLY - waits for natural speech"""
        try:
            with sr.Microphone() as source:
                print("\n" + "=" * 40)
                print("🎤 LISTENING... Speak now")
                print("=" * 40)

                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                print("\n✅ Ready - I'm listening...")

                audio = self.recognizer.listen(source)
                print("🎯 Processing speech...")

                text = self.recognizer.recognize_google(audio, language="en-US").lower()
                print(f"\n✅ HEARD: '{text}'")
                return text

        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception:
            return ""

    def _take_screenshot_windows(self):
        """Take screenshot using Windows API (no pyautogui needed)"""
        try:
            # Use Windows built-in screenshot tool
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

            # Method 1: Try using snipping tool command
            print(f"📸 Taking screenshot using Windows method...")

            # Save to Pictures folder
            pictures_path = os.path.join(os.path.expanduser("~"), "Pictures")
            if not os.path.exists(pictures_path):
                pictures_path = os.getcwd()

            full_path = os.path.join(pictures_path, filename)

            # Try multiple methods for screenshot

            # Method A: Use PowerShell to capture screen
            try:
                ps_script = f'''
                Add-Type -AssemblyName System.Windows.Forms
                Add-Type -AssemblyName System.Drawing
                $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
                $bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
                $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
                $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
                $bitmap.Save("{full_path}")
                $graphics.Dispose()
                $bitmap.Dispose()
                '''

                # Save script to temp file
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
                    f.write(ps_script)
                    ps_file = f.name

                # Run PowerShell script
                subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file],
                               capture_output=True)

                # Clean up
                time.sleep(0.5)
                if os.path.exists(ps_file):
                    os.remove(ps_file)

                if os.path.exists(full_path):
                    print(f"✅ Screenshot saved: {full_path}")
                    return full_path

            except:
                pass

            # Method B: Use PrintScreen key and save from clipboard
            try:
                import tkinter as tk
                from PIL import ImageGrab

                # Simulate PrintScreen key
                ctypes.windll.user32.keybd_event(0x2C, 0, 0, 0)  # PrintScreen down
                ctypes.windll.user32.keybd_event(0x2C, 0, 2, 0)  # PrintScreen up
                time.sleep(0.5)

                # Get image from clipboard
                image = ImageGrab.grabclipboard()
                if image:
                    image.save(full_path)
                    print(f"✅ Screenshot saved: {full_path}")
                    return full_path

            except:
                pass

            # Method C: Simple message if all methods fail
            print("⚠️ Could not take screenshot automatically")
            print("Please press PrintScreen key manually and paste into Paint")
            return None

        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None

    def _volume_control_windows(self, action):
        """Control volume using Windows API"""
        try:
            if action == "up":
                for _ in range(5):
                    ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)  # Volume Up
                    ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
                    time.sleep(0.05)
                return True

            elif action == "down":
                for _ in range(5):
                    ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)  # Volume Down
                    ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
                    time.sleep(0.05)
                return True

            elif action == "mute":
                ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)  # Volume Mute
                ctypes.windll.user32.keybd_event(0xAD, 0, 2, 0)
                return True

        except:
            return False

    def _media_control_windows(self, action):
        """Control media using Windows API"""
        try:
            if action == "play_pause":
                ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)  # Play/Pause
                ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
                return True

            elif action == "next":
                ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)  # Next Track
                ctypes.windll.user32.keybd_event(0xB0, 0, 2, 0)
                return True

            elif action == "previous":
                ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)  # Previous Track
                ctypes.windll.user32.keybd_event(0xB1, 0, 2, 0)
                return True

        except:
            return False

    def _shutdown_computer(self, action):
        """Shutdown, restart, or sleep the computer"""
        try:
            if action == "shutdown":
                print("⚠️ Shutting down computer in 5 seconds...")
                self.speak("Shutting down computer in 5 seconds")
                time.sleep(5)
                os.system("shutdown /s /t 0")
                return True

            elif action == "restart":
                print("🔄 Restarting computer in 5 seconds...")
                self.speak("Restarting computer in 5 seconds")
                time.sleep(5)
                os.system("shutdown /r /t 0")
                return True

            elif action == "sleep":
                print("💤 Putting computer to sleep...")
                self.speak("Putting computer to sleep")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return True

            elif action == "hibernate":
                print("❄️ Hibernating computer...")
                self.speak("Hibernating computer")
                os.system("shutdown /h")
                return True

            elif action == "lock":
                print("🔒 Locking computer...")
                self.speak("Locking computer")
                ctypes.windll.user32.LockWorkStation()
                return True

        except Exception as e:
            print(f"❌ System command error: {e}")
            return False

    def execute_command(self, text):
        """EXECUTE COMMAND WITH FIXED FEATURES"""
        if not text:
            return False

        # Prevent duplicate commands
        current_time = time.time()
        if text == self.last_command and current_time - self.last_command_time < 2:
            print(f"🔄 Same command ignored")
            return True

        text_lower = text.lower()

        # ===== CONTROL COMMANDS =====
        if any(word in text_lower for word in ["exit", "quit", "stop"]):
            self.speak("Goodbye sir")
            return "exit"

        if "jarvis" in text_lower:
            if not self.awake:
                self.awake = True
                self.speak("Yes sir! I'm now always listening")
                print("✅ ALWAYS LISTENING ACTIVATED")
                self.last_command = text
                self.last_command_time = time.time()
                return True
            else:
                self.speak("I'm already listening sir")
                return True

        if any(phrase in text_lower for phrase in ["go to sleep", "sleep now"]):
            self.speak("Going to sleep")
            self.awake = False
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if not self.awake:
            print("💤 Sleeping - say 'jarvis'")
            return False

        # ===== SHUTDOWN & SLEEP COMMANDS =====
        if any(word in text_lower for word in ["shutdown computer", "shutdown pc", "turn off computer"]):
            print(f"🖥️ Shutting down computer")
            self.speak("Shutting down computer")
            self._shutdown_computer("shutdown")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["restart computer", "reboot computer", "restart pc"]):
            print(f"🔄 Restarting computer")
            self.speak("Restarting computer")
            self._shutdown_computer("restart")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["sleep computer", "put computer to sleep", "sleep mode"]):
            print(f"💤 Putting computer to sleep")
            self.speak("Putting computer to sleep")
            self._shutdown_computer("sleep")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["hibernate computer", "hibernate pc"]):
            print(f"❄️ Hibernating computer")
            self.speak("Hibernating computer")
            self._shutdown_computer("hibernate")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["lock computer", "lock pc", "lock screen"]):
            print(f"🔒 Locking computer")
            self.speak("Locking computer")
            self._shutdown_computer("lock")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # ===== WEBSITE COMMANDS =====
        websites = {
            "youtube": "https://youtube.com",
            "google": "https://google.com",
            "gmail": "https://gmail.com",
            "facebook": "https://facebook.com",
            "twitter": "https://twitter.com",
            "instagram": "https://instagram.com",
            "whatsapp": "https://web.whatsapp.com",
            "github": "https://github.com",
            "netflix": "https://netflix.com",
            "amazon": "https://amazon.com",
            "wikipedia": "https://wikipedia.org",
            "chatgpt": "https://chat.openai.com",
            "spotify": "https://spotify.com",
            "reddit": "https://reddit.com",
            "linkedin": "https://linkedin.com",
            "stackoverflow": "https://stackoverflow.com",
            "leetcode": "https://leetcode.com",
            "hackerrank": "https://hackerrank.com",
            "codecademy": "https://codecademy.com",
            "notion": "https://notion.so",
            "trello": "https://trello.com",
            "drive": "https://drive.google.com",
            "docs": "https://docs.google.com",
            "sheets": "https://sheets.google.com",
            "maps": "https://maps.google.com",
            "translate": "https://translate.google.com",
            "calendar": "https://calendar.google.com",
            "meet": "https://meet.google.com",
            "zoom": "https://zoom.us",
            "discord": "https://discord.com",
            "telegram": "https://web.telegram.org",
            "twitch": "https://twitch.tv",
            "hotstar": "https://hotstar.com",
            "prime": "https://primevideo.com",
            "bbc": "https://bbc.com",
            "cnn": "https://cnn.com",
            "weather": "https://weather.com",
            "dropbox": "https://dropbox.com",
            "onedrive": "https://onedrive.live.com",
        }

        for site, url in websites.items():
            if site in text_lower:
                print(f"🌐 Opening: {site}")
                self.speak(f"Opening {site}")
                webbrowser.open(url)
                self.last_command = text
                self.last_command_time = time.time()
                return True

        # ===== TIME COMMANDS =====
        if any(word in text_lower for word in ["time", "clock"]):
            current = datetime.datetime.now().strftime("%I:%M %p")
            print(f"🕒 Time: {current}")
            self.speak(f"The time is {current}")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if "date" in text_lower:
            current = datetime.datetime.now().strftime("%B %d, %Y")
            print(f"📅 Date: {current}")
            self.speak(f"Today's date is {current}")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if "day" in text_lower and ("today" in text_lower or "what" in text_lower):
            current = datetime.datetime.now().strftime("%A")
            print(f"📆 Day: {current}")
            self.speak(f"Today is {current}")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # ===== APPLICATION COMMANDS =====
        app_commands = {
            "notepad": "notepad",
            "calculator": "calc",
            "cmd": "cmd",
            "paint": "mspaint",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "chrome": "chrome",
            "firefox": "firefox",
            "edge": "msedge",
            "vscode": "code",
            "vs code": "code",
            "visual studio": "devenv",
            "task manager": "taskmgr",
            "control panel": "control",
            "settings": "start ms-settings:",
            "file explorer": "explorer",
            "snipping tool": "snippingtool",
            "media player": "wmplayer",
            "outlook": "outlook",
            "calendar app": "outlookcal:",
            "mail app": "outlookmail:",
        }

        for app, command in app_commands.items():
            if app in text_lower:
                print(f"💻 Opening: {app}")
                self.speak(f"Opening {app}")
                os.system(command)
                self.last_command = text
                self.last_command_time = time.time()
                return True

        # ===== COMPUTER CONTROL COMMANDS (FIXED) =====

        # Volume control using Windows API
        if any(word in text_lower for word in ["volume up", "increase volume", "louder"]):
            print(f"🔊 Increasing volume")
            self.speak("Increasing volume")
            self._volume_control_windows("up")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["volume down", "decrease volume", "quieter"]):
            print(f"🔉 Decreasing volume")
            self.speak("Decreasing volume")
            self._volume_control_windows("down")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if "mute" in text_lower or "unmute" in text_lower:
            print(f"🔇 Toggling mute")
            self.speak("Toggling mute")
            self._volume_control_windows("mute")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # Media control using Windows API
        if any(word in text_lower for word in ["play", "pause", "media"]):
            print(f"⏯️ Media play/pause")
            self.speak("Playing/pausing media")
            self._media_control_windows("play_pause")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if "next track" in text_lower or "next song" in text_lower:
            print(f"⏭️ Next track")
            self.speak("Next track")
            self._media_control_windows("next")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if "previous track" in text_lower or "previous song" in text_lower:
            print(f"⏮️ Previous track")
            self.speak("Previous track")
            self._media_control_windows("previous")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # Screenshot (FIXED)
        if any(word in text_lower for word in ["screenshot", "capture screen", "take screenshot"]):
            print(f"📸 Taking screenshot")
            self.speak("Taking screenshot")
            result = self._take_screenshot_windows()
            if result:
                self.speak("Screenshot saved successfully")
                print(f"✅ Saved to: {result}")
            else:
                self.speak("Please take screenshot manually using PrintScreen key")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # ===== SYSTEM INFORMATION COMMANDS =====

        if any(word in text_lower for word in ["system info", "computer info", "specs"]):
            print(f"💻 Getting system information")
            self._show_system_info()
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["battery", "power", "charge"]):
            print(f"🔋 Checking battery")
            self._check_battery()
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["cpu", "processor", "usage"]):
            print(f"⚡ Checking CPU usage")
            self._check_cpu_usage()
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["memory", "ram", "memory usage"]):
            print(f"🧠 Checking memory usage")
            self._check_memory_usage()
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["disk", "storage", "hard disk"]):
            print(f"💾 Checking disk usage")
            self._check_disk_usage()
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # ===== FUN COMMANDS =====

        if "joke" in text_lower:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call fake spaghetti? An impasta!",
                "Why did the computer go to the doctor? It had a virus!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a bear with no teeth? A gummy bear!"
            ]
            print(f"😂 Telling joke")
            self.speak("Here's a joke")
            joke = random.choice(jokes)
            print(f"   {joke}")
            self.speak(joke)
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if "quote" in text_lower:
            quotes = [
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Innovation distinguishes between a leader and a follower. - Steve Jobs",
                "Stay hungry, stay foolish. - Steve Jobs",
                "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
                "It does not matter how slowly you go as long as you do not stop. - Confucius"
            ]
            print(f"💬 Giving quote")
            self.speak("Here's a quote")
            quote = random.choice(quotes)
            print(f"   {quote}")
            self.speak(quote)
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["flip coin", "toss coin"]):
            result = random.choice(["Heads", "Tails"])
            print(f"🪙 Coin flip: {result}")
            self.speak(f"It's {result}")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["roll dice", "dice roll"]):
            result = random.randint(1, 6)
            print(f"🎲 Dice roll: {result}")
            self.speak(f"You rolled a {result}")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # ===== SEARCH COMMANDS =====

        if text_lower.startswith("search for "):
            query = text_lower[11:]
            print(f"🔍 Searching for: {query}")
            self.speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if text_lower.startswith("who is "):
            query = text_lower[7:]
            print(f"👤 Searching: {query}")
            self.speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # ===== UTILITY COMMANDS =====

        if any(word in text_lower for word in ["clear screen", "clear", "clean screen"]):
            os.system('cls')
            print(f"🧹 Screen cleared")
            self.speak("Screen cleared")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # ===== HELP COMMANDS =====

        if "help" in text_lower:
            print(f"📚 Showing help")
            self._show_help()
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # ===== GREETINGS =====

        if any(word in text_lower for word in ["hello", "hi", "hey"]):
            greetings = ["Hello sir!", "Hi there!", "Hey! How can I help?"]
            response = random.choice(greetings)
            print(f"👋 {response}")
            self.speak(response)
            self.last_command = text
            self.last_command_time = time.time()
            return True

        if any(word in text_lower for word in ["thank you", "thanks"]):
            responses = ["You're welcome!", "My pleasure!", "Happy to help!"]
            response = random.choice(responses)
            print(f"🙏 {response}")
            self.speak(response)
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # ===== TEST COMMAND =====

        if "test" in text_lower:
            print(f"🧪 System test")
            self.speak("System test successful!")
            self.last_command = text
            self.last_command_time = time.time()
            return True

        # ===== UNKNOWN COMMAND =====

        if text:
            print(f"❓ Unknown: '{text}'")
            self.speak(f"I heard '{text}'")

        return False

    def _show_system_info(self):
        """Show system information"""
        self.speak("Showing system information")

        print("\n" + "=" * 60)
        print("💻 SYSTEM INFORMATION")
        print("=" * 60)

        try:
            # CPU info
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            print(f"CPU Usage: {cpu_percent}%")
            print(f"CPU Cores: {cpu_count}")

            # Memory info
            memory = psutil.virtual_memory()
            memory_total = memory.total / (1024 ** 3)
            memory_used = memory.used / (1024 ** 3)
            memory_percent = memory.percent
            print(f"Memory: {memory_used:.1f}GB / {memory_total:.1f}GB ({memory_percent}%)")

            # Disk info
            disk = psutil.disk_usage('C:\\')
            disk_total = disk.total / (1024 ** 3)
            disk_used = disk.used / (1024 ** 3)
            disk_percent = disk.percent
            print(f"Disk C: {disk_used:.1f}GB / {disk_total:.1f}GB ({disk_percent}%)")

            # Battery
            try:
                battery = psutil.sensors_battery()
                if battery:
                    print(f"Battery: {battery.percent}%")
                    if battery.power_plugged:
                        print("Status: Plugged in")
            except:
                pass

        except Exception as e:
            print(f"Error getting system info: {e}")

        print("=" * 60)

    def _check_battery(self):
        """Check battery status"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = battery.power_plugged

                self.speak(f"Battery is at {percent} percent")

                if plugged:
                    self.speak("And it's plugged in")
                    print(f"🔋 Battery: {percent}% (Plugged in)")
                else:
                    hours = battery.secsleft // 3600 if battery.secsleft else 0
                    minutes = (battery.secsleft % 3600) // 60 if battery.secsleft else 0
                    self.speak(f"Estimated time remaining is {hours} hours and {minutes} minutes")
                    print(f"🔋 Battery: {percent}% ({hours}h {minutes}m remaining)")
            else:
                self.speak("No battery detected")
                print("❌ No battery detected")
        except:
            self.speak("Could not check battery")
            print("❌ Could not check battery")

    def _check_cpu_usage(self):
        """Check CPU usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            self.speak(f"CPU usage is at {cpu_percent} percent")
            print(f"⚡ CPU Usage: {cpu_percent}%")
        except:
            self.speak("Could not check CPU usage")

    def _check_memory_usage(self):
        """Check memory usage"""
        try:
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used / (1024 ** 3)
            memory_total = memory.total / (1024 ** 3)

            self.speak(f"Memory usage is at {memory_percent} percent")
            self.speak(f"Using {memory_used:.1f} gigabytes out of {memory_total:.1f}")
            print(f"🧠 Memory: {memory_used:.1f}GB / {memory_total:.1f}GB ({memory_percent}%)")
        except:
            self.speak("Could not check memory usage")

    def _check_disk_usage(self):
        """Check disk usage"""
        try:
            disk = psutil.disk_usage('C:\\')
            disk_percent = disk.percent
            disk_used = disk.used / (1024 ** 3)
            disk_total = disk.total / (1024 ** 3)

            self.speak(f"Disk usage is at {disk_percent} percent")
            self.speak(f"Using {disk_used:.1f} gigabytes out of {disk_total:.1f}")
            print(f"💾 Disk: {disk_used:.1f}GB / {disk_total:.1f}GB ({disk_percent}%)")
        except:
            self.speak("Could not check disk usage")

    def _show_help(self):
        """Show help"""
        self.speak("Here are the commands I understand")

        print("\n" + "=" * 60)
        print("🤖 JARVIS - COMMAND LIST")
        print("=" * 60)
        print("WEBSITES: youtube, google, gmail, facebook, chatgpt, etc.")
        print("TIME: time, date, what day is today")
        print("APPS: notepad, calculator, cmd, chrome, vscode")
        print("COMPUTER: volume up/down, mute, play/pause, screenshot")
        print("SHUTDOWN: shutdown computer, restart, sleep, hibernate, lock")
        print("SYSTEM: system info, battery, cpu, memory, disk")
        print("FUN: joke, quote, flip coin, roll dice")
        print("SEARCH: search for [anything], who is [person]")
        print("UTILITIES: clear screen, help")
        print("CONTROL: jarvis, go to sleep, exit")
        print("=" * 60)

    def run_always_listening_mode(self):
        """ALWAYS LISTENING MODE"""
        print("\n" + "=" * 60)
        print("🤖 JARVIS FIXED - ALWAYS LISTENING")
        print("=" * 60)
        print("Say 'jarvis' once to activate always listening")
        print("Then speak commands anytime")
        print("=" * 60)

        self.speak("what's in your mind")

        while True:
            try:
                if not self.awake:
                    print(f"\n[STATUS: SLEEPING]")
                    print("Say 'jarvis' to activate...")

                    text = self.listen_continuously()

                    if text and "jarvis" in text.lower():
                        self.awake = True
                        self.speak("Yes sir! Always listening mode activated")
                        print("[STATUS: ALWAYS LISTENING]")
                    continue

                print(f"\n" + "=" * 40)
                print("👂 STATUS: ALWAYS LISTENING")
                print("Speak your command...")
                print("=" * 40)

                command = self.listen_continuously()

                if command:
                    print(f"\n" + "=" * 40)
                    print(f"🔄 PROCESSING: '{command}'")
                    print("=" * 40)

                    result = self.execute_command(command)

                    print(f"\n" + "=" * 40)
                    print("✅ PROCESSING COMPLETE")
                    print("Returning to listening mode...")
                    print("=" * 40)

                    if result == "exit":
                        break

                    time.sleep(0.3)

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break


# ========== MAIN ==========
if __name__ == "__main__":
    print("🤖 JARVIS FIXED - NO DEPENDENCY ERRORS")

    # Only require psutil
    try:
        import psutil
    except ImportError:
        print("\n⚠️ Missing psutil package")
        print("Install with: pip install psutil")
        choice = input("Continue without system info features? (y/n): ")
        if choice.lower() != 'y':
            exit()

    jarvis = JarvisFixed()

    print("\n🔊 Testing...")
    jarvis.speak("welcome back sir")

    print("\n" + "=" * 60)
    print("CHOOSE MODE:")
    print("1. Always Listening (Fixed features)")
    print("2. Quick Test")
    print("3. Exit")
    print("=" * 60)

    choice = input("\nSelect (1/2/3): ").strip()

    if choice == '1':
        jarvis.run_always_listening_mode()
    elif choice == '2':
        jarvis.awake = True
        test_commands = ["time", "volume up", "play", "screenshot", "system info"]
        for cmd in test_commands:
            print(f"\nTesting: '{cmd}'")
            jarvis.execute_command(cmd)
            time.sleep(2)
        print("\n✅ Test complete!")
        input("Press Enter to start always listening mode...")
        jarvis.run_always_listening_mode()
    else:
        print("👋 Goodbye!")