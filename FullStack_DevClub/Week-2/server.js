const express = require("express");
const nodemailer =require('nodemailer')
const jwt = require('jsonwebtoken');
const app = express();
const crypto = require('crypto');
const bcrypt = require('bcrypt');
const PORT = process.env.PORT || 5000;
const cors = require('cors');


//CORS SETUP
app.use(cors({
    origin: 'http://localhost:5173', // Your frontend's origin
    methods: ['GET', 'POST', 'PUT', 'DELETE'], // Allowed HTTP methods
    credentials: true, // Allow cookies, authorization headers, etc.
    allowedHeaders: ['Content-Type', 'Authorization'],
}));


//Cookie Parser
const cookieParser = require('cookie-parser');
app.use(cookieParser());



app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

const apiRoot ="/api";
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
const mongoose = require("mongoose");
mongoose.connect("mongodb://localhost:55000/chatApp", {
}).then(r => {
    console.log("Connected to DB");
}).catch(err => {
    console.error("DB connection error:", err);
});
app.get(apiRoot+'/health', (req, res) => {
    res.send({
        timeStamp: new Date(),
        status: "OK"
    });
})


// Define Mongoose Schema for User
const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true,
        unique: true,
        trim: true
    },
    email: {
        type: String,
        required: true,
        unique: true,
        trim: true,
        lowercase: true,
        match: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ // Basic email regex validation
    },
    password: {
        type: String,
        required: true
    }
}, {
    timestamps: true
});

//Password Reset Schema

const passwordResetTokenSchema =new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        required: true,
        ref: "User"
    },
    token: {
        type: String,
        required: true,
        unique: true,
    },
    createdAt: {
        type: Date,
        required: true,
        default: Date.now,
        expiresIn: Date,

    }
},{
    timestamps: false
})


const PasswordResetToken = mongoose.model('PasswordResetToken', passwordResetTokenSchema);
const User = mongoose.model('User', userSchema);

app.post(apiRoot+'/register', async (req, res) => {
    const data = req.body;

    if (data.username && data.email && data.password) {
        try {
            const saltRounds = 10;
            const hashedPassword = await bcrypt.hash(data.password, saltRounds);

            const newUser = await User.create({
                username: data.username,
                email: data.email,
                password: hashedPassword
            })

            //Send Welcome Mail
            const emailResutl=await sendWelcomeEmail(newUser.email, newUser.username);

            if (!emailResutl) {
                console.log("Email wan't sent :",emailResutl.error);
            }

            res.status(201).send({
                timeStamp: new Date(),
                status: "Registered successfully",
                user : {
                    id: newUser._id,
                    username: newUser.username,
                    email: newUser.email
                },
                emailStatus:emailResutl.success,
            });
        } catch (err) {
            console.error("Error during registration:", err);
            res.status(500).send({"error": err.message});
        }
    } else {
        res.status(400).send({
            timeStamp: new Date(),
            status: "Missing Data"
        });
    }
});

const JWT_SECRET = process.env.JWT_SECRET || "17s_MY_53CR37_K3Y";


app.post(apiRoot+'/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        if (!username || !password) {
            return res.status(400).json({
                timeStamp: new Date(),
                error: "Username and password are required"
            });
        }

        const user = await User.findOne({username: username});

        if (!user) {
            return res.status(401).json({
                timeStamp: new Date(),
                error: "Invalid username or password"
            });
        }

        const isMatch = await bcrypt.compare(password, user.password);

        if (!isMatch) {
            return res.status(403).json({
                timeStamp: new Date(),
                error: "Invalid username or password"
            });
        }

        // Generate JWT token
        const token = jwt.sign(
            {id: user._id, email: user.email},
            JWT_SECRET,
            {expiresIn: "1h"}
        );
        //
        // res.status(200).json({
        //     timeStamp: new Date(),
        //     status: "Login successful",
        //     token: token,
        //     user: {
        //         id: user._id,
        //         username: user.username,
        //         email: user.email
        //     }
        // });

        res.cookie('token', token, {
            httpOnly: true,
            secure: false,
            sameSite: 'lax',
            maxAge: 60 * 60 * 1000  // 1 hour
        });

        res.status(200).json({"Status": "Login successful"});

    } catch (err) {
        console.error("Error during login:", err);
        res.status(500).json({
            timeStamp: new Date(),
            error: "Internal server error"
        });
    }
});



app.post(apiRoot+'/forgotPassword', async (req, res) => {
    const {email} = req.body;

    if (!email || !email.length) {
        return res.status(400).json({status: "Missing Data"});
    }

    try {
        const user =await User.findOne({email : email.toLowerCase()});
        if (!user) {
            return res.status(401).json({"error": "Invalid email."});
        }




        await PasswordResetToken.deleteMany({userId: user._id});

        const resetToken = crypto.randomBytes(32).toString("hex");

        const newResetToken = await PasswordResetToken.create({
            userId : user._id,
            token: resetToken
        });

        const resetUrl= 'http://localhost:5000/reset-password?token=' + resetToken +'&email='+encodeURIComponent(newResetToken.email);

        console.log("Reset URL",resetUrl);

        const emailResult = await sendResetEmail(email,resetToken);

        res.status(200).send({
            timeStamp: new Date(),
            status: emailResult.success?"Reset Link has been sent if that mail Exists. " : "Failed to send reset link.",
        })
    } catch (err){
        console.error("Error during forgotPassword:", err);
    }
})

//Reset password api after getting mail

app.post(apiRoot+'/resetPassword', async (req, res) => {
    const {token,email,newPassword} = req.body;

    if (!token || !email || !newPassword) {
        return res.status(400).json({status: "Missing Data"});
    }

    try {
        const resetToken = await PasswordResetToken.findOne({token: token});

        if (!resetToken) {
            return res.status(401).json({"error": "Invalid token."});
        }

        const user = await User.findOne({email: email.toLowerCase()});

        if (!user) {
            return res.status(401).json({"error": "Invalid email."});
        }

        const saltRounds = 10;
        user.password =await bcrypt.hash(newPassword, saltRounds);
        await user.save();

        await PasswordResetToken.deleteMany({userId: user._id});

        res.status(200).send({
            timeStamp: new Date(),
            status: "Password reset successful."
        })
    } catch (err) {
        console.error("Error during resetPassword:", err);
    }
})


app.post(apiRoot + '/validate', async (req, res) => {
    console.log('Cookies received for validate:', req);

    // Correctly access the 'token' property from req.cookies
    const token = req.cookies.token;

    // 1. Check if token exists in cookies
    if (!token) {
        return res.status(401).json({ status: "Invalid token." });
    }

    try {
        // 2. Verify the JWT token
        // If the token is invalid (malformed, expired, wrong signature), jwt.verify will throw an error
        const decodedToken = jwt.verify(token, JWT_SECRET);
        // console.log('Decoded Token:', decodedToken); // Uncomment for debugging

        // 3. Find the user based on the ID from the decoded token
        const user = await User.findById(decodedToken.id);

        // 4. Check if a user was found
        if (!user) {
            // User ID in token does not correspond to an existing user
            return res.status(401).json({ status: "Invalid token." });
        }

        // If we reach this point, the token is valid and the user exists
        res.status(200).json({ // Use .json() for consistency with error responses
            timeStamp: new Date(),
            status: "Token is valid."
            // You might include user details here if needed, e.g., userId: user._id
        });

    } catch (err) {
        // This catch block handles any errors during the token verification process
        // (e.g., token expired, malformed JWT, signature mismatch)
        // or any error during the database lookup (though less common for a simple findById)
        console.error("Error during token validation:", err.message); // Log the specific error for debugging
        // Always send a response in the catch block to prevent the request from hanging
        return res.status(401).json({ status: "Invalid token." });
    }
});

//GMAIL SMTP Setup

const createGmailTransporter = nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 587,
    secure: false,
    auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_APP_PASSWORD
    }
})

//Email Sending Function
const sendEmail =async (to,subject,htmlContent,textContent) => {
    try {
        const transporter =createGmailTransporter;

        const mailOptions = {
            from: `"Sumit Kumar Saw" <${process.env.GMAIL_APP_PASSWORD}>`,
            to: to,
            subject: subject,
            html: htmlContent,
            text: textContent
        };
        const info = await transporter.sendMail(mailOptions);
        console.log(info);
        return {success:true, messageId:info.messageId};
    } catch (err) {
        console.error("Error during sendEmail:", err);
        return {success:false, messageId:err.message};
    }
}



//Welcome Mail

const sendWelcomeEmail =async (userEmail,username) => {
    const subject = "Welcome to ChatAPP";
    const htmlContent = `
    <h1>Welcome to ChatAPP</h1>
    <h2 style="color: #333;">Welcome ${username}!</h2>
    `;

    const textContent = `Welcome you ${username}!`;

    return await sendEmail(userEmail,subject, htmlContent, textContent);
}


//Send Reset

const sendResetEmail =async (userEmail,token) => {
    const subject = "Reset Password";
    const htmlContent = `
    <h1>Reset Password</h1>
    <p>Please click on the link below to reset your password.</p>
    <a href="http://localhost:5000/reset-password?token=${token}&email=${encodeURIComponent(userEmail)}">Reset Password</a>
    
    <p>Or type : http://localhost:5000/reset-password?token=${token}&email=${encodeURIComponent(userEmail)}</p>`;
    const textContent ="";
    return await sendEmail(userEmail,subject, htmlContent, textContent);
}






module.exports = {
    sendEmail,
    sendWelcomeEmail,
};
