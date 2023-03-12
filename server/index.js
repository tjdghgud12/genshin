const express = require('express');
const { EnkaClient } = require('enka-network-api');
const genshin = require('genshin-api');
const enka = new EnkaClient({ defaultLanguage:"en", caching: false });
const app = express();
const bodyParser = require('body-parser');

app.use(express.urlencoded({
    extended: true
}));
app.use(express.json());
app.use(bodyParser.json());


app.post('/api/getUser', async(req, res) => {
    const userData = await enka.fetchUser(req.body.userUID);
    console.log('UID ===> ' ,userData);
    //console.log('UID ===> ' ,userData.charactersPreview);
    console.log('UID ===> ' ,req.body.userUID);
    res.send({result: userData._data, });
});

app.listen(8000, () => { 
    console.log(`Express Start on port 8000!`);  
})