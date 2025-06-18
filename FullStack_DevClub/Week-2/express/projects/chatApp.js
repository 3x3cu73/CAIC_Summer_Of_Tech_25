const express = require("express");
const router = express.Router();
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");
const nodemailer = require("nodemailer");
const crypto = require("crypto");
const mongoose = require("mongoose");
require('dotenv').config();
const JWT_SECRET = process.env.JWT_SECRET || "17s_MY_53CR37_K3Y";






console.log(process.env);
//MONGOSE Connection string

mongoose.connect(process.env.MONGO_URL, {
}).then(r => {
    console.log("Connected to DB");
}).catch(err => {
    console.error("DB connection error:", err);
});



// ===== SCHEMAS =====
const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true, trim: true },
    email: {
        type: String, required: true, unique: true, trim: true, lowercase: true,
        match: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    },
    password: { type: String, required: true }
}, { timestamps: true });

const passwordResetTokenSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, required: true, ref: "User" },
    token: { type: String, required: true, unique: true },
    createdAt: { type: Date, default: Date.now, expires: 3600 } // 1hr expiry
}, { timestamps: false });

const User = mongoose.model("User", userSchema);
const PasswordResetToken = mongoose.model("PasswordResetToken", passwordResetTokenSchema);

// ===== MAIL SETUP =====
const createGmailTransporter = nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 587,
    secure: false,
    auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_APP_PASSWORD
    }
});

const sendEmail = async (to, subject, htmlContent, textContent = "") => {
    try {
        const info = await createGmailTransporter.sendMail({
            from: `"Sumit Kumar Saw" <${process.env.GMAIL_APP_PASSWORD}>`,
            to, subject, html: htmlContent, text: textContent
        });
        return { success: true, messageId: info.messageId };
    } catch (err) {
        console.error("Error sending mail:", err.message);
        return { success: false, error: err.message };
    }
};

const sendWelcomeEmail = (email, username) => {
    return sendEmail(
        email,
        "Welcome to ChatAPP",
        `<h1>Welcome ${username}!</h1><p>You’ve successfully registered.</p>`,
        `Welcome ${username}!`
    );
};

const sendResetEmail = (email, token) => {
    const link = `${process.env.FRONTEND_URL}/reset-password?token=${token}&email=${encodeURIComponent(email)}`;
    return sendEmail(
        email,
        "Reset Password",
        `<p>Click below to reset password:</p><a href="${link}">${link}</a>`,
        `Reset password: ${link}`
    );
};

// ===== ROUTES =====

// Register
router.post('/register', async (req, res) => {
    const { username, email, password } = req.body;
    if (!(username && email && password)) return res.status(400).json({ status: "Missing Data" });

    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        const user = await User.create({ username, email, password: hashedPassword });

        const mailResult = await sendWelcomeEmail(email, username);
        res.status(201).json({
            timeStamp: new Date(),
            status: "Registered successfully",
            user: { id: user._id, username, email },
            emailStatus: mailResult.success
        });
    } catch (err) {
        console.error("Register error:", err.message);
        res.status(500).json({ error: err.message });
    }
});

// Login
router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    if (!(username && password)) return res.status(400).json({ error: "Missing credentials" });

    const user = await User.findOne({ username });
    if (!user || !(await bcrypt.compare(password, user.password))) {
        return res.status(401).json({ error: "Invalid credentials" });
    }

    const token = jwt.sign({ id: user._id, email: user.email }, JWT_SECRET, { expiresIn: '1h' });
    res.cookie('token', token, { httpOnly: true, secure: true, sameSite: 'None', maxAge: 3600000 });
    res.status(200).json({ status: "Login successful" });
});

// Forgot Password
router.post('/sendResetMail', async (req, res) => {
    const { email } = req.body;
    if (!email) return res.status(400).json({ status: "Missing Data" });

    const user = await User.findOne({ email: email.toLowerCase() });
    if (!user) return res.status(401).json({ error: "Invalid email" });

    await PasswordResetToken.deleteMany({ userId: user._id });
    const token = crypto.randomBytes(32).toString("hex");
    await PasswordResetToken.create({ userId: user._id, token });

    const emailResult = await sendResetEmail(email, token);
    if (!emailResult.success) {
         console.log({ error: emailResult.error });
    }
    res.status(200).json({
        timeStamp: new Date(),
        success: emailResult.success,
        status: emailResult.success ? "Reset link sent." : "Failed to send reset link."
    });
});

// Reset Password
router.post('/resetPassword', async (req, res) => {
    const { token, email, newPassword } = req.body;
    if (!(token && email && newPassword)) return res.status(400).json({ status: "Missing Data" });

    const tokenDoc = await PasswordResetToken.findOne({ token });
    const user = await User.findOne({ email: email.toLowerCase() });

    if (!tokenDoc || !user) return res.status(401).json({ error: "Invalid token/email" });

    user.password = await bcrypt.hash(newPassword, 10);
    await user.save();
    await PasswordResetToken.deleteMany({ userId: user._id });

    res.status(200).json({ timeStamp: new Date(), status: "Password reset successful" , success:true });
});

// Token Validate
router.post('/validate', async (req, res) => {
    const token = req.cookies.token;
    if (!token) return res.status(401).json({ status: "Invalid token" });

    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        const user = await User.findById(decoded.id);
        if (!user) return res.status(401).json({ status: "Invalid token" , success:false});

        res.status(200).json({ timeStamp: new Date(), status: "Token is valid" , success:true});
    } catch (err) {
        console.error("Validation error:", err.message);
        res.status(401).json({ status: "Invalid token" ,success:false, error: err.message });
    }
});

module.exports = router;
