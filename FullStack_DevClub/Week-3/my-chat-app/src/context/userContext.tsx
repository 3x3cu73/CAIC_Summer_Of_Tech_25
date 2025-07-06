import {createContext, type ReactNode, useContext, useEffect, useState,} from "react";
import axios from "axios";

interface User {
    _id: string;
    email: string;
    username: string;
}

interface UserContextType {
    user: User | null;
    setUser: (user: User | null) => void;
    loading: boolean;
    refetchUser: () => void; // Add this function
}

const UserContext = createContext<UserContextType>({
    user: null,
    setUser: () => {},
    loading: true,
    refetchUser: () => {}, // Add this function
});

export const UserProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    const fetchUser = () => {
        setLoading(true);
        axios.post(`${import.meta.env.VITE_API_BASE}/auth/validate`, {}, { withCredentials: true })
            .then(res => {
                if (res.data?.user) setUser(res.data.user);
                else setUser(null);
            })
            .catch(() => setUser(null))
            .finally(() => setLoading(false));
    };

    useEffect(() => {
        fetchUser();

        // Optional: refetch when window gains focus
        const handleFocus = () => fetchUser();
        window.addEventListener('focus', handleFocus);

        return () => window.removeEventListener('focus', handleFocus);
    }, []);

    return (
        <UserContext.Provider value={{ user, setUser, loading, refetchUser: fetchUser }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);
