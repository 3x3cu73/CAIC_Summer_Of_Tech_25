import { createContext, type ReactNode, useEffect, useState, useContext } from "react";
import axios from "axios";

interface User {
    _id: string;
    email: string;
    username: string;
}

interface UserContextType {
    user: User | null;
    loading: boolean;
}

const UserContext = createContext<UserContextType>({
    user: null,
    loading: true,
});

export const UserProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.post(
            `${import.meta.env.VITE_API_BASE}/auth/validate`,
            {},
            { withCredentials: true }
        )
            .then((res) => {
                if (res.data?.user) {
                    setUser(res.data.user);
                } else {
                    console.warn("No user found in response", res.data);
                }
            })
            .catch(() => {
                setUser(null);
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);


    return (
        <UserContext.Provider value={{ user, loading }}>
            {children}
        </UserContext.Provider>
    );
};

// Custom hook
export const useUser = () => useContext(UserContext);
