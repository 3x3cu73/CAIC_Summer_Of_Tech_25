const mongoose = require('mongoose');
const {Schema} = require("mongoose");

const Chat = new mongoose.Schema(
    {
        isGroupChat : {
            type : Boolean,
            default : false

        },
        name : {
            type : String,
            unique : false,
        },
        participants : [{
            type: Schema.Types.ObjectId,
            ref: 'User',
        }],
        groupAdmin : {
            type: Schema.Types.ObjectId,
            ref: 'User',
        },
        latestMessage : {
            type: Schema.Types.ObjectId,
            ref: 'Message',
        }
    },{
        timestamps : true,
    }
)

module.exports = mongoose.model('Chat', Chat);
