const router = require('express').Router();
const authRoutes = require('./routes/authRoutes');
const chatRoutes = require('./routes/chatRoutes');

router.use('/auth', authRoutes);
router.use('/chat', chatRoutes);

module.exports = router;
