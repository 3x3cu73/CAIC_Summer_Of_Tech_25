const {registerUser,loginUser,sendResetMail, resetPassword, validateUser} = require("../controllers/authController");
const router = require('express').Router();


router.post('/register', registerUser);
router.post('/login', loginUser);
router.post('/sendResetMail', sendResetMail);
router.post('/resetPassword', resetPassword);
router.post('/validate', validateUser);


module.exports = router;
