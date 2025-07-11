const router = require('express').Router();


router.get("/health", (req, res) => {
    return res.json({status: "Healthy",dateTime: Date.now()});
})
module.exports = router;
