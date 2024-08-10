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
        console.log('Twelve json retrieved.');
        res.json(twelveCredentials);
        console.log('Twelve data send.');
    });
});


app.get('/symbols', function (req, res) {
    fs.readFile(jsonFilePathSymbols, 'utf8', function (err, data) {
        if (err) throw err;
        console.log('Symbols json retrieved.');
        res.json(JSON.parse(data));
        console.log('Symbols data send.');
    });
});

app.post('/symbols', async function (req, res) {
    const result = req.body;
    const fileData = await readSymbolsFile();
    const updatedArray = fileData[(result.symbolType)];
    if(!updatedArray?.includes(result.symbol) && result.symbolType !== 'benchmark') {
        updatedArray.push(result.symbol);
        fs.writeFileSync(jsonFilePathSymbols, JSON.stringify(fileData));
        console.log('Data written in system!');
        res.status(200).send('Data written in system!');
    }
    else if(result.symbolType === 'benchmark') {
        updatedArray.splice(0, updatedArray.length, result.symbol);
        fs.writeFileSync(jsonFilePathSymbols, JSON.stringify(fileData));
        console.log('Benchmark written in system!');
        res.status(200).send('Benchmark written in system!');
    }
    else {
        console.log('Data already in system!');
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
