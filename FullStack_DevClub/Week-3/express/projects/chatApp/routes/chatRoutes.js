const router = require('express').Router();
const { getChats ,sendMessage, newChat, getMessages, getAllUsers} = require("../controllers/chatController");
const {authorizer} = require("../middlewares/authorizer");

router.post('/message',authorizer, sendMessage);
router.post('/newChat',authorizer, newChat);
router.post('/getChats',authorizer,getChats);
router.post('/getMessages',authorizer, getMessages);
router.get('/allUsers',authorizer,getAllUsers);

module.exports = router;
