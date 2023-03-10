const express = require('express');
const { EnkaClient } = require('enka-network-api');
const genshin = require('genshin-api');
const enka = new EnkaClient();
const app = express();

app.get('/', function(req, res){
    enka.fetchUser(840110542).then( user => {
        let character = user.charactersPreview;
        // 1. 캐릭터 정보를 본다.
        // 2. 캐릭터 정보에 따라서 genshin 이미지를 불러온다.
        character.map((d, i) => {
            console.log(`Character: ${d.characterData._nameId}(Lv: ${d.level})`);
        })
    })
});

// const test = enka.getAllCharacters();
// console.log(test.map(d => d.name.get("en")));


app.listen(8000, () => { 
    console.log(`Express Start on port 8000!`);  
})