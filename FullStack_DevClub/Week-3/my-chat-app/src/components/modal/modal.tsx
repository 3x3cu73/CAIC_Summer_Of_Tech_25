// src/components/Modal.tsx

import React, { useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';

// Define the props for the Modal component using a TypeScript interface
interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSubmit: () => void;
    title: string;
    children: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, onSubmit, title, children }) => {
    const modalRef = useRef<HTMLDivElement>(null);

    // Effect to handle closing the modal on 'Escape' key press
    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener('keydown', handleKeyDown);
        }

        // Cleanup function to remove the event listener
        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [isOpen, onClose]);

    // If the modal is not open, render nothing
    if (!isOpen) {
        return null;
    }

    // Use a portal to render the modal at the root of the document
    // This helps in avoiding z-index issues and keeps the DOM clean
    return ReactDOM.createPortal(
        // Backdrop: a semi-transparent overlay that covers the entire screen
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm transition-opacity duration-300"
            onClick={onClose} // Close modal when backdrop is clicked
        >
            {/* Modal Panel: the main content of the modal */}
            <div
                ref={modalRef}
                className="relative w-full max-w-lg rounded-xl bg-white p-6 shadow-2xl transition-all duration-300 dark:bg-slate-800"
                onClick={(e) => e.stopPropagation()} // Prevent clicks inside the modal from closing it
            >
                {/* Modal Header */}
                <div className="flex items-start justify-between border-b border-slate-200 pb-4 dark:border-slate-700">
                    <h3 className="text-2xl font-semibold text-slate-900 dark:text-white">
                        {title}
                    </h3>
                    <button
                        onClick={onClose}
                        className="rounded-full p-1 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600 dark:hover:bg-slate-700 dark:hover:text-white"
                        aria-label="Close modal"
                    >
                        {/* A simple X icon for closing */}
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M6 18L18 6M6 6l12 12"
                            />
                        </svg>
                    </button>
                </div>

                {/* Modal Body: where the custom children are rendered */}
                <div className="mt-4 text-base leading-relaxed text-slate-600 dark:text-slate-300">
                    {children}
                </div>

                {/* Modal Footer: contains action buttons */}
                <div className="mt-6 flex items-center justify-end space-x-3 border-t border-slate-200 pt-4 dark:border-slate-700">
                    <button
                        onClick={onClose}
                        type="button"
                        className="rounded-lg bg-slate-100 px-5 py-2.5 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-200 focus:outline-none focus:ring-4 focus:ring-slate-300 dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={onSubmit}
                        type="button"
                        className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800"
                    >
                        Submit Action
                    </button>
                </div>
            </div>
        </div>,
        document.getElementById('modal-root') as HTMLElement // The portal target
    );
};

export default Modal;
