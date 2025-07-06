// src/components/modal/modal.tsx

import React, { useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';
import { X } from 'lucide-react';
import LoadingButton from "../ui/button.tsx"; // Assuming this path is correct

// Define the props for the Modal component
interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSubmit: () => void;
    title: string;
    children: React.ReactNode;
    // New props for LoadingButton integration
    isLoading?: boolean;
    submitText?: string;
    loadingText?: string;
    isSubmitDisabled?: boolean;
}

const Modal: React.FC<ModalProps> = ({
                                         isOpen,
                                         onClose,
                                         onSubmit,
                                         title,
                                         children,
                                         isLoading = false,
                                         submitText = "Submit",
                                         loadingText = "Processing...",
                                         isSubmitDisabled = false,
                                     }) => {
    const modalRef = useRef<HTMLDivElement>(null);

    // Effect to handle closing the modal on 'Escape' key press
    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                onClose();
            }
        };

        if (isOpen) {
            // Add overflow hidden to body when modal is open to prevent background scrolling
            document.body.style.overflow = 'hidden';
            document.addEventListener('keydown', handleKeyDown);
        }

        // Cleanup function
        return () => {
            document.body.style.overflow = 'unset';
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [isOpen, onClose]);

    // If the modal is not open, render nothing
    if (!isOpen) {
        return null;
    }

    // Use a portal to render the modal
    return ReactDOM.createPortal(
        // Backdrop
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm transition-opacity duration-300 p-4"
            onClick={onClose}
            aria-modal="true"
            role="dialog"
        >
            {/* Modal Panel */}
            <div
                ref={modalRef}
                // Added transform transition for a subtle pop-in effect
                className="relative w-full max-w-lg rounded-xl bg-white p-6 shadow-2xl transition-all duration-300 transform scale-95 hover:scale-100"
                onClick={(e) => e.stopPropagation()} // Prevent clicks inside the modal from closing it
            >
                {/* Modal Header */}
                <div className="flex items-center justify-between mb-5">
                    <h3 className="text-2xl font-bold text-slate-800">
                        {title}
                    </h3>
                    <button
                        onClick={onClose}
                        className="rounded-full p-1 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600"
                        aria-label="Close modal"
                    >
                        <X className="w-6 h-6" />
                    </button>
                </div>

                {/* Modal Body */}
                <div className="text-base text-slate-600">
                    {children}
                </div>

                {/* Modal Footer */}
                <div className="mt-6 flex items-center justify-end space-x-3 pt-4">
                    <button
                        onClick={onClose}
                        type="button"
                        // Secondary style for the cancel button
                        className="rounded-lg border border-slate-300 px-5 py-2.5 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-100 focus:outline-none focus:ring-4 focus:ring-slate-200"
                        disabled={isLoading} // Disable cancel while loading
                    >
                        Cancel
                    </button>

                    {/* Integrated LoadingButton */}
                    <LoadingButton
                        onClick={onSubmit}
                        loading={isLoading}
                        loadText={loadingText}
                        disabled={isSubmitDisabled || isLoading}
                        // Primary style using Indigo to match the app theme
                        className="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-300 disabled:opacity-50"
                    >
                        {submitText}
                    </LoadingButton>
                </div>
            </div>
        </div>,
        document.getElementById('modal-root') as HTMLElement // The portal target
    );
};

export default Modal;
