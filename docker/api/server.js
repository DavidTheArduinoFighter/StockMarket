const express = require('express');
const fs = require('fs');

const app = express();

const port = 4000;


const jsonFilePathTwelve = './json/credentials/twelveCredentials.json';
const jsonFilePathSymbols = './json/symbols/symbols.json';

app.listen(port, () => {
    console.log(`Server is running, listening at http://localhost:${port}`);
});


app.get('/twelveData', function (req, res) {
    fs.readFile(jsonFilePathTwelve, 'utf8', function (err, data) {
        if (err) throw err;
        const twelveCredentials = JSON.parse(data);
        console.log(`Twelve json retrieved.`);
        res.json(twelveCredentials)
        console.log(`Twelve data posted.`);
    });
});


app.get('/symbols', function (req, res) {
    fs.readFile(jsonFilePathSymbols, 'utf8', function (err, data) {
        if (err) throw err;
        console.log(`Symbols json retrieved.`);
        res.json(JSON.parse(data));
        console.log(`Symbols data posted.`);
    });
});

app.use(express.urlencoded({
    extended: true
}));
