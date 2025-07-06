// Type for the user/sender object
export interface Sender {
    _id: string;
    username: string;
    email: string;
}

// Type for the message object, using the Sender type
export interface Message {
    _id: string;
    sender: Sender;
    content: string;
    chat: string;
    seenBy: string[];
    createdAt: string; // ISO date string
    updatedAt: string; // ISO date string
    __v?: number;
}
