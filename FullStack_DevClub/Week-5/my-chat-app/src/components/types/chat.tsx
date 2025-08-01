// Type for the user/sender object
export interface Sender {
    _id: string;
    username: string;
    email: string;
}


export type Message = {
    _id: string;
    content: string;
    chat: {_id:string};
    sender: {
        _id: string;
        username: string;
    };
    createdAt: string;
    updatedAt: string;
};
