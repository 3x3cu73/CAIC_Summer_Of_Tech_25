const mongoose = require('mongoose');
const {Schema} = require("mongoose");


const chatMessage = new mongoose.Schema({
    sender : {
        type: Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    content : {
        type: String,
        required: true
    },
    chat : {
        type: Schema.Types.ObjectId,
        ref: 'Chat',
        required: true
    },
    media : {
        type: String,
    },
    seenBy : [{
        type: Schema.Types.ObjectId,
        ref: 'User',
    }]
},{timestamps : true})

module.exports = mongoose.model('Message', chatMessage);
