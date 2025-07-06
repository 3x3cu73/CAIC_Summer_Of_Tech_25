import React from "react";

type ChatProps = {
    user: any;
    isSelected: any,
} & React.HTMLAttributes<HTMLDivElement>;

function AddUser({ user,isSelected, ...props }: ChatProps) {

    return (
        <div
            {...props}
            className={`border-2 ${
                isSelected ? "border-blue-300" : "border-transparent"
            } cursor-pointer px-4 py-2 rounded-sm m-1 flex flex-col ${props.className || ""}`}


        >
            <div className="flex flex-row justify-between items-center">
                <div className="font-normal text-sm">{user.username}</div>
            </div>
        </div>
    );
}

export default AddUser;
