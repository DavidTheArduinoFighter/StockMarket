const  express = require('express');
const app = express();

const port = 4000;

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});

app.get('/foo', function (req, res) {
    res.json({"test": "yes"})
});

app.use(express.urlencoded({
    extended: true
}));

app.post('/bar', function (req, res) {
    let body = req.body;
    console.log(req.body.foo);
    res.send(req.body.foo)
})