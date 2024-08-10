const express = require('express');
const fs = require('fs');
const bodyParser = require('body-parser');

const app = express();

const port = 4000;


const jsonFilePathTwelve = './json/credentials/twelveCredentials.json';
const jsonFilePathSymbols = './json/symbols/symbols.json';

app.listen(port, () => {
    console.log(`Server is running, listening at http://localhost:${port}`);
});

app.use(bodyParser.json()); // Parse JSON bodies
app.use(bodyParser.urlencoded({ extended: true })); // Parse URL-encoded bodies


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

app.post('/symbols', async function (req, res) {
    const result = req.body;
    const fileData = await readSymbolsFile();
    const updatedArray = fileData[(result.symbolTaype)]
    if(!updatedArray.includes(result.symbol)) {
        updatedArray.push(result.symbol)
        fs.writeFileSync(jsonFilePathSymbols, JSON.stringify(fileData));
        res.status(200).send('Data written in system!');
    }
    else {
        res.status(200).send('Data already in system!');
    }
})

app.use(express.urlencoded({
    extended: true
}));

function readSymbolsFile() {
    return new Promise((resolve, reject) => {
        fs.readFile(jsonFilePathSymbols, 'utf8', (err, data) => {
            if (err) {
                reject(err);
            } else {
                resolve(JSON.parse(data));
            }
        });
    });
}
