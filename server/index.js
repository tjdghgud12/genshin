const express = require('express');
const { EnkaClient } = require('enka-network-api');
const enka = new EnkaClient();
const app = express();

app.get('/', function(req, res){
    
});

enka.fetchUser(840110542).then( user => {
    let character = user.charactersPreview;
    character.map((d, i) => {
        console.log(`Character: ${d.characterData._nameId}(Lv: ${d.level})`);
    })
})

// const test = enka.getAllCharacters();
// console.log(test.map(d => d.name.get("en")));


app.listen(8000, () => { 
    console.log(`Express Start on port 8000!`);  
})