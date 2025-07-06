const jwt = require('jsonwebtoken');
const User = require('../models/User');

const JWT_SECRET = process.env.JWT_SECRET;


const authorizer = async (req, res, next) => {
    const token = req.cookies.token;

    if (!token) {
        return res.status(401).json({ success: false, message: "Not authorized, no token" });
    }

    try {
        // 1. Verify the token
        const decoded = jwt.verify(token, JWT_SECRET);

        // 2. Find the user from the token's ID and attach them to the request object.
        req.user = await User.findById(decoded.id).select('-password');

        if (!req.user) {
            return res.status(401).json({ success: false, message: "Not authorized, user not found" });
        }

        // 3. The user is authenticated. Pass control to the next middleware or route handler.
        next();

    } catch (err) {
        console.error("Authentication error:", err.message);
        return res.status(401).json({ success: false, message: "Not authorized, token failed" });
    }
};

module.exports = { authorizer };
