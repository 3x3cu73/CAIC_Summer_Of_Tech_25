const express = require('express');
const cors = require('cors');
const dotenv = require("dotenv");
const bodyParser = require('body-parser');
const nginxRoute = require('./projects/ports.js');
const chatApp = require('./projects/chatApp/index.js');
const connectDB = require('./projects/chatApp/config/db.js');
const { Server } = require("socket.io");

const app = express();
const PORT = 3000;

//Cookie Parser
const cookieParser = require('cookie-parser');
const {createServer} = require("node:http");
const server = createServer(app)

const io = new Server(server, {
  cors: {
    origin: process.env.FRONTEND_URL,
    methods: ["GET", "POST"],
    credentials: true,
  },
})
app.use((req, res, next) => {
  req.io = io;
  next();
});
app.use(cookieParser());


dotenv.config();

// Connect to MongoDB
connectDB();

app.use(bodyParser.json());


app.use(cors({
  origin: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));

//API Routes
app.use('/nginx', nginxRoute);
app.use('/chatApp',chatApp);
// app.listen(PORT, () => {
//   console.log(`Server running at http://localhost:${PORT}`);
// });

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
})
