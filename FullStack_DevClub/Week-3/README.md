# CAIC Summer of Tech 2025: Full-Stack Chat App Development
## Week 3: Backend-Frontend Integration & Real-time Messaging

Welcome to Week 3! This is where your chat application truly comes alive. You'll connect your Express backend to your React frontend, then add real-time messaging capabilities.

## What You'll Build This Week
By the end of Week 3, you'll have:
- Complete Backend-Frontend Integration: Your React app talking to your Express server
- Real-time Messaging System: Live chat functionality using Firebase
- Working Chat Interface: Fully functional chat UI with real users

## Quick Review: What We Built in Week 2
✅ Express server with MongoDB  
✅ User authentication (register/login) with JWT  
✅ Basic React login/register forms  

## Part 1: Connecting Backend to Frontend 

### Essential Learning Path
Core Concepts to Master:
- HTTP Client Libraries (Axios)
- CORS (Cross-Origin Resource Sharing)
- Token-based Authentication
- React Context for State Management

### 📚 Learning Resources - Study These First!
Primary Video Tutorials (Watch in Order):
1. **[Full Stack Authentication Tutorial (45 mins)](https://www.youtube.com/watch?v=mbsmsi7l3r4)**
   - Complete JWT authentication with React + Express
   - Shows exact connection process
   - Study this carefully - it covers 90% of what you need

2. **[CORS Explained Simply (8 mins)](https://www.youtube.com/watch?v=PNtFSVU-YTI)**
   - Why your frontend can't talk to backend initially
   - How to fix CORS errors

3. **[React Context API in 15 Minutes](https://www.youtube.com/watch?v=35lXWvCuM8o)**
   - Managing user authentication state globally
   - Alternative to prop drilling

Essential Reading:
- [Axios Quick Start Guide](https://axios-http.com/docs/intro) - Making API calls from React
- [React Context Pattern](https://react.dev/learn/passing-data-deeply-with-context) - State management

### 🛠️ Implementation Starter Code

1. Fix CORS in Express (Add to server.js):
```javascript
const cors = require('cors');
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));
```

2. Install Axios in React:
```bash
npm install axios
```

3. Basic API Setup (src/services/api.js):
```javascript
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000/api',
});

// Auto-add token to requests
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (userData) => API.post('/auth/register', userData),
  login: (credentials) => API.post('/auth/login', credentials),
};
```

### 🎯 Your Implementation Task
Study the tutorials above, then build:
- Complete the API service with all endpoints
- Update your login/register forms to use the API
- Implement authentication context
- Add proper error handling

Success Criteria:
- [ ] Login form calls backend and stores JWT token
- [ ] User stays logged in after page refresh
- [ ] Proper error messages for failed requests
- [ ] No CORS errors in console

## Part 2: Real-time Messaging with Firebase

### Why Firebase for Real-time Features?
Firebase Realtime Database is perfect for chat apps because:
- Instant updates - No need to refresh to see new messages
- Easy setup - Less complex than Socket.io
- Scalable - Handles multiple users automatically
- 

### 📚 Learning Resources - Master Firebase First!
Essential Video Tutorials (Watch These!):
1. **[Firebase Realtime Database Complete Tutorial (30 mins)](https://www.youtube.com/watch?v=noB98K6A0TY)**
   - Complete Firebase setup process
   - Understanding NoSQL data structure
   - This is your foundation - watch carefully

2. **[Build a Chat App with Firebase](https://www.youtube.com/watch?v=zQyrwxMPm88)**
   - End-to-end chat app implementation
   - Shows exact data structure for messages
   - Follow along and adapt to your React app

3. **[Firebase + React Integration]([https://firebase.google.com/docs/database/web/start](https://www.youtube.com/watch?v=PKwu15ldZ7k))**
   - How to use Firebase in React components
   - Real-time listeners and updates

Essential Documentation:
- [Firebase Setup Guide](https://firebase.google.com/docs/web/setup) - Official setup steps
- [Realtime Database Structure](https://firebase.google.com/docs/database/web/structure-data) - How to organize chat data
- [React Firebase Hooks](https://github.com/CSFrequency/react-firebase-hooks) - Simplified Firebase integration

### Implementation task
  Database Design for Chat Applications

> In case you’re wondering, it’s JSON written below

Okay, so let's discuss the most interesting and intuitive part of the project (which is kinda very critical). Let’s assume two people, A and B. Messaging happens when A sends a message to B, meaning the database has the sender ID of A and receiver ID of B and the critical info (message, time, etc., you’ll see).  
Here’s the schema for this.

```json
"Chats": {
  "messageId": {
    "message": "text content",
    "sender": "senderId", 
    "receiver": "receiverId",
    "date": "DD/MM/YYYY",
    "time": "HH:MM AM/PM",
    "status": "SEEN/NOT_SEEN",
    "img_message": "image-url-if-any"
  }
}
```

And of course, we are gonna have a track of the users we are chatting with. So for that:

```json
"Users": {
  "userId": {
    "email": "user@example.com",
    "username": "displayName", 
    "photo": "profile-image-url",
    "status": "online/offline",
    "flag": "chat",
    "userId": "same-as-key"
  }
}
```

Okay, so one last thing. Now A texted B, but how’s gonna B see that A texted him? An easy way to do this is to maintain a ChatList like this:

```json
"Chatlist": {
  "userId1": {
    "userId2": { "id": "userId2" },
    "userId3": { "id": "userId3" }
  },
  "userId2": {
    "userId1": { "id": "userId1" }
  }
}
```

The final Schema in Firebase Realtime DB would look like this:

```
ChatApp Database
├── ChatUsers/
├── Chatlist/
├── Chats/
```

### Some clarification:
1. `userId` is the Firebase UID. eg `f0QxzIt8YHafQc8owj5bG0IL9KX2`

---

## Essential Database Concepts

- **CRUD Operations**: Create, Read, Update, Delete  
- **Data Relationships**: How users relate to messages  
- **Indexing**: Optimizing query performance  
- **Real-time Updates**: Listening for data changes  

---

## Implementation Task

### Goal: Set up Firebase for real-time messaging functionality

#### Step 1: Create Firebase Project
Firebase Console → Add project → Enter name → Create

#### Step 2: Create Database
Realtime Database → Create Database → Choose location → Test mode → Done

#### Step 3: Get Config
Project Settings (gear icon) → Copy `firebaseConfig` + `Database URL`

#### Step 4: Security Rules

```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

---

## Backend Integration

```bash
npm install firebase-admin
```

**Basic server setup**

```js
const admin = require('firebase-admin');
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://your-project.firebaseio.com'
});
const db = admin.database();
```

---

## Frontend Integration

```bash
npm install firebase
```

**firebase.js**

```js
import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";

const firebaseConfig = {
  // your config
  databaseURL: "https://your-project.firebaseio.com"
};

const app = initializeApp(firebaseConfig);
export const database = getDatabase(app);
```

---

## Task 3: Core Messaging System

### Task 3A: Basic Auth with Firebase

```js
const handleLogin = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;
    // Update user status to online
    const userRef = ref(database, `ChatUsers/Users/${user.uid}/status`);
    await set(userRef, "online");
  } catch (error) {
    console.error("Login error:", error);
  }
};
```

### Task 3B: View ChatList

```js
useEffect(() => {
  if (currentUser) {
    const chatListRef = ref(database, `Chatlist/${currentUser.uid}`);
    onValue(chatListRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        const contacts = Object.keys(data);
        setChatContacts(contacts);
      }
    });
  }
}, [currentUser]);
```

### Task 3C: Realtime Message Display

```js
const loadMessages = (partnerId) => {
  const messagesRef = ref(database, 'Chats');
  onValue(messagesRef, (snapshot) => {
    const data = snapshot.val();
    if (data) {
      const myMessages = Object.entries(data)
        .filter(([id, msg]) => 
          (msg.sender === currentUser.uid && msg.receiver === partnerId) ||
          (msg.sender === partnerId && msg.receiver === currentUser.uid)
        )
        .sort((a, b) => new Date(a[1].date + ' ' + a[1].time) - new Date(b[1].date + ' ' + b[1].time));
      
      setMessages(myMessages);
    }
  });
};
```

## Part 4: API Routes & Database Models

### Why Enhanced Backend Structure?
While Firebase handles real-time messaging, you still need proper API routes for user management, message history, and data that needs to persist in your MongoDB.

### 📚 Essential Learning Resources
API Design & MongoDB:
- [Express Router Organization (12 mins)](https://www.youtube.com/watch?v=Oe421EPjeBE) - Structuring routes
### 🛠️ Essential Backend Structure

1. Message Model (models/Message.js):
```javascript
const mongoose = require('mongoose');

const messageSchema = new mongoose.Schema({
  sender: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  Receiver: ………………,
  content: { type: String, required: true },
  status: ………
}, { timestamps: true });

module.exports = mongoose.model('Message', messageSchema);
```

2. Basic Message Routes (routes/messages.js):
```javascript
const express = require('express');
const router = express.Router();
const Message = require('../models/Message');
const auth = require('../middleware/auth');

// Get conversation history
router.get('/:userId', auth, async (req, res) => {
	…………
  });

module.exports = router;
```

3. Register Routes (server.js):
```javascript
app.use('/api/messages', require('./routes/messages'));
```

### 🎯 Your Implementation Task
Study the tutorials above, then build:
- Message routes - GET conversation history, POST new message
- User routes - GET all users, UPDATE user profile
- Conversation routes - GET user's conversations

Success Criteria:
- Can fetch message history from MongoDB
- User profiles have additional chat-related fields
- API routes work with Postman testing
- Frontend can call these new endpoints


## Bonus Tasks

### Bonus 1: Group Chats

**Updated schema for group chats:**

```
ChatApp Database
├── ChatUsers/
├── GroupChats/
├── Chatlist/
├── Chats/
```

```json
"GroupChats": {
  "groupId": {
    "groupName": "Group Display Name",
    "description": "Group description",
    "createdBy": "creator-userId",
    "users": ["userId1", "userId2", "userId3"]
  }
}
```

## Success Checklist

### Backend Connection
- [ ] React app calls Express API successfully
- [ ] User login works end-to-end
- [ ] JWT tokens stored and used correctly
- [ ] No CORS errors

### Firebase Setup
- [ ] Firebase project created and configured
- [ ] Can send messages that appear in Firebase console
- [ ] Real-time listeners working
- [ ] Basic chat interface functional

### Polish & Features
- [ ] Messages appear instantly for both users
- [ ] User status indicators working
- [ ] Error handling for network issues
- [ ] Clean, intuitive user interface

Remember: The tutorials are your primary teachers this week. Watch them carefully, pause to understand concepts, and adapt the code to your specific app structure.

You're building something amazing - a real, working chat application! 🚀

## Emergency Help Resources
- Stuck on CORS? → [CORS troubleshooting guide]([https://github.com/CSFrequency/react-firebase-hooks](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors))
- Firebase Not Working? → [Firebase Troubleshooting](https://firebase.google.com/docs/database/web/start#troubleshooting)
- React Context Issues? → [Context API Common Mistakes](https://firebase.google.com/docs/database/web/start#troubleshooting)
- JWT Token Problems? → [JWT Debugging Guide](https://jwt.io/introduction)
