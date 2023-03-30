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

/* 
_nameId
avatarId

*/

app.post('/api/getUser', async(req, res) => {
    try{
        const userData = await enka.fetchUser(req.body.userUID);
        //console.log(charactersList)
        //console.log('UID ===> ' ,userData);
        //console.log('UID ===> ' ,userData.charactersPreview);
        // 내가 계산하고 싶은 것은 성유물 주옵 및 부옵의 비교!!!!
        // 
        /*** 필요한 데이터 리스트
         * 1. 캐릭터 얼굴 이미지
         * 2. 해당 캐릭터의 성유물
         *  2-1. 성유물 주옵 및 부옵
         *  2-2. 성유물 셋옵
         * 3. 해당 캐릭터의 무기
         *  3-1. 해당 캐릭터의 무기 주옵 및 부옵
         *  3-2. 해당 캐릭터의 무기 옵션
         * 4. 캐릭터 맨몸 스펙
         * 5. 캐릭터 돌파도
        */

        let charactersList = [];
        let character;
        let weapon;
        let artifact = await genshin.Artifact();
        //let test = genshin.Characters(userData.characters[0].characterData._nameId);
        character = await enka.getCharacterById(userData._data.avatarInfoList[0].avatarId);
        for (let i = 0; i < userData._data.avatarInfoList.length; i++) {
            //character = await enka.getCharacterById(userData._data.avatarInfoList[i].avatarId);
            weapon = await enka.getWeaponById(userData._data.avatarInfoList[i].equipList.at(-1).itemId);
            //console.log(i, weapon)
            charactersList[i] = {
                name: userData.characters[i].characterData._nameId,
                image: character.icon.url,
                equip: userData._data.avatarInfoList[i].equipList,
                //artifacts: userData.characters[i].artifacts,
                weapon: { 
                    icon: weapon.icon.url,
                    data: userData._data.avatarInfoList[i].equipList[5],
                },
                // passive: userData.characters[i].characterData.passiveTalents
            }
        }
        
        // for (output in character) {
        //     console.log(JSON.stringify(output));
            
        // }
        // userData._data
        console.log('UID ===> ' ,req.body.userUID);
        res.send({result: userData._data, data: charactersList, });
    }catch(error){
        console.log(error);
        res.send({result: "Error", data: error});
    }
    
});

app.listen(8000, () => { 
    console.log(`Express Start on port 8000!`);  
})