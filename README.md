Realtime Chat App 🟣💬

A modern real-time chat application built with Django, Django Channels, WebSockets, and Bootstrap. 
Features include:
💬 Public and Private Chat Rooms
👤 1-on-1 Direct Messaging (DM)
📱 Typing Indicators
🗑️ Message Deletion (self-only)
🌙 Light/Dark Theme Toggle (with localStorage)
🧑‍🤝‍🧑 Room Access Control for Private Groups
🧾 User Authentication (Login / Logout / Registration)
🖼️ Avatars & Chat Bubble Styling
🎨 Modern UI using Bootstrap and custom CSS

Feature	        Description
Public Rooms	  Anyone can join
Private Rooms	  Only allowed users can join
DMs	            Dedicated chat between 2 users (e.g., dm_user1_user2)
Typing	        Real-time typing feedback
Delete	        Delete your own messages
Themes	        Switch between light/dark modes
Dashboard	      Create/join/delete rooms with access control
Auth	          Secure registration & login system

🛠️ Tech Stack
Backend: Django, Django Channels, Redis (for WebSocket layer)
Frontend: HTML5, Bootstrap 5, JavaScript
Database: SQLite (for dev, can switch to PostgreSQL)
WebSocket: Django Channels + ASGI
Deployment-ready: Docker (optional), Daphne

🔧 Local Setup
# 1. Clone the repo
git clone https://github.com/Saratha1999/Realtime-chat-app.git
cd Realtime-chat-app

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Redis Server (required for Django Channels)
brew services start redis  # MacOS
# OR
redis-server  # Linux

# 5. Apply migrations
python manage.py migrate

# 6. Run the server
python manage.py runserver
# OR for real-time WS:
daphne chatapp.asgi:application

# 🧪 Superuser (for admin login)
python manage.py createsuperuser




