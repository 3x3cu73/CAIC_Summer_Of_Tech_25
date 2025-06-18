const express = require('express');
const cors = require('cors');
const dotenv = require("dotenv");
const bodyParser = require('body-parser');
const nginxRoute = require('./projects/ports.js');
const chatApp = require('./projects/chatApp.js');


const app = express();
const PORT = 3000;

//Cookie Parser
const cookieParser = require('cookie-parser');
app.use(cookieParser());


dotenv.config();

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


app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
