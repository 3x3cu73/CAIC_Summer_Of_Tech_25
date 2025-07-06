const Message = require('../models/Message');
const Chat = require('../models/Chat');
const User = require('../models/User');


exports.sendMessage = async (req, res) => {
    const {content, chatId} = req.body;

    if (!content || !chatId) {
        return res.status(400).json({success: false, message: "Missing content or chatId"});
    }


    try {
        let newMessage = await Message.create({
            sender: req.user._id,
            content: content,
            chat: chatId
        });

        newMessage = await newMessage.populate([
            { path: 'sender', select: 'username email' },
            {
                path: 'chat',
                populate: {
                    path: 'participants',
                    select: 'username email'
                }
            }
        ]);

        await Chat.findByIdAndUpdate(chatId, { latestMessage: newMessage._id });

        req.io.to(chatId).emit('receiveMessage', newMessage);


        res.status(200).json(newMessage);


    } catch (err) {
        console.error("Error sending message:", err.message);
        return res.status(500).json({success: false, message: "Error sending message"});
    }
}


exports.newChat = async (req, res) => {
    try {

    const name = req.body.name;
    const participants = req.body.participants;
    const groupAdmin = req.user._id;
    const isGroupChat=participants.length!==2;

    // console.log(groupAdmin._id,participants);
    if (!participants.includes(groupAdmin.toString())){
        return res.status(401).json({success: false, message: "Select yourself"});
    }

    if (!name && isGroupChat) {
        return res.status(400).json({success: false, message: "Missing name chat"});
    }

    if (!participants) {
        return res.status(400).json({success: false, message: "Missing participants"});
    }


    const existingChat = await Chat.findOne({
        participants: {
            $all: participants,
            $size: participants.length
        }
    });

    if (existingChat) {
        return res.status(400).json({ success:false ,message: "Chat already exists with these participants." });
    }

    if (participants.length < 2) {
        return res.status(400).json({success: false, message: "Missing participants"});
    }


        let newChat = await Chat.create({
            participants: participants,
            name: name,
            groupAdmin: groupAdmin,
            isGroupChat:isGroupChat

        });

        // ✅ Create welcome message
        const welcomeContent = isGroupChat
            ? `Welcome to the group "${name}"`
            : `Private chat started`;

        const welcomeMessage = await Message.create({
            sender: groupAdmin,
            content: welcomeContent,
            chat: newChat._id
        });
        newChat.latestMessage = welcomeMessage._id;
        newChat = await newChat.populate([
            {path : 'groupAdmin', select: 'username email'},
            {path : 'participants', select: 'username email'},
            {path : 'latestMessage', select: 'content chat sender media'},]);

        await newChat.save()
        res.status(200).json({success:true,message:"Chat created successfully."});

    } catch (err){
        console.error("Error creating chat :", err.message);
        return res.status(500).json({success: false, message: "Error  creating chat."});
    }
}


exports.getChats = async (req, res) => {
    try {
        const user = req.user.id;

        const chats = await Chat.find({ participants: { $in: user } })
            .populate([
                { path: 'groupAdmin', select: 'username email' },
                { path: 'participants', select: 'username email' },
                { path: 'latestMessage', select: 'content chat sender media' }
            ]);

        return res.status(200).json(chats);
    } catch (err) {
        console.error("Error getting chats from chat:", err.message);
        return res.status(500).json({ success: false, message: "Error getting chats" });
    }
}


exports.getMessages = async (req, res) => {
    try {
        const user = req.user.id;
        const chat = req.body.chat;
        const messages = await Message.find({chat: chat}).populate([
            { path: 'sender', select: 'username email _id' },

        ]);
        return res.status(200).json(messages);
    }
    catch (err) {
        console.error("Error getting chats from chat:", err.message);
        return res.status(500).json({success: false, message: "Error getting chats"});
    }
}


exports.getAllUsers = async (req, res) => {
    try {
        const allUsers = await User.find({}).select('_id email username');
        return res.status(200).json(allUsers);
    } catch (err) {
        console.error("Error getting users from chat:", err.message);
        return res.status(500).json({success: false, message: "Error getting Users."});
    }
}
