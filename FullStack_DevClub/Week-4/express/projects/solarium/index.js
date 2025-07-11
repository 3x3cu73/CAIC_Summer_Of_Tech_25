// ✅ Correct in ./projects/solarium/index.js
module.exports = (conn) => {
    const express = require('express');
    const router = express.Router();

    // use `conn` here if needed

    router.get('/', (req, res) => {
        res.send("Solarium connected.");
    });

    return router;
};
