import React from "react";
import { Circle, CircleCheckBig } from 'lucide-react';

// Using 'any' for the user prop to match the other components.
type AddUserProps = {
    user: any;
    isSelected: boolean;
    // Accept the avatar as a prop for better reusability and consistency.
    AvatarComponent: React.ReactNode;
} & React.HTMLAttributes<HTMLDivElement>;

function AddUser({ user, isSelected, AvatarComponent, ...props }: AddUserProps) {
    return (
        <div
            {...props}
            className={`
                flex items-center gap-3 w-full p-2.5 rounded-lg cursor-pointer 
                transition-colors duration-200
                ${isSelected ? 'bg-indigo-100 hover:bg-indigo-200' : 'hover:bg-slate-100'}
            `}
            aria-checked={isSelected}
            role="option"
        >
            {/* Column 1: Avatar */}
            <div className="flex-shrink-0">
                {AvatarComponent}
            </div>

            {/* Column 2: Username (takes up available space) */}
            <p className="flex-grow font-semibold text-slate-700">
                {user.username}
            </p>

            {/* Column 3: Selection Icon */}
            <div className="flex-shrink-0">
                {isSelected ? (
                    <CircleCheckBig className="w-6 h-6 text-indigo-600" />
                ) : (
                    <Circle className="w-6 h-6 text-slate-400" />
                )}
            </div>
        </div>
    );
}

export default AddUser;
