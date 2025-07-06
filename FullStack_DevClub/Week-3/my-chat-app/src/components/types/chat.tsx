// Type for the user/sender object
export interface Sender {
    _id: string;
    username: string;
    email: string;
}

// Type for the message object, using the Sender type
export type Message = {
    _id: string;
    content: string;
    chat: string;
    sender: {
        _id: string;
        username: string;
    };
    createdAt: string;
    updatedAt: string;
};
