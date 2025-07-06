const {registerUser,loginUser,sendResetMail, resetPassword, validateUser, logOut} = require("../controllers/authController");
const router = require('express').Router();


router.post('/register', registerUser);
router.post('/login', loginUser);
router.post('/sendResetMail', sendResetMail);
router.post('/resetPassword', resetPassword);
router.post('/validate', validateUser);
router.post('/logout', logOut);


module.exports = router;
