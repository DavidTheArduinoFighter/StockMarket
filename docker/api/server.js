const  express = require('express');
const app = express();

const port = 4000;

const fs = require('fs');
let twelveCredentials;
fs.readFile('./credentials/twelveCredentials.json', 'utf8', function (err, data) {
  if (err) throw err;
  twelveCredentials = JSON.parse(data);
});

app.listen(port, () => {
    console.log(`Server is running, listening at http://localhost:${port}`);
});

app.get('/twelveData', function (req, res) {
    res.json(twelveCredentials)
});

app.use(express.urlencoded({
    extended: true
}));
