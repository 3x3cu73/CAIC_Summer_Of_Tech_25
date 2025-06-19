const router = require('express').Router();
const authRoutes = require('./routes/authRoutes');


router.use('/', authRoutes);

module.exports = router;
