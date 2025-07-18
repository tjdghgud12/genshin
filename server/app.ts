import express from "express";
import { EnkaClient, ArtifactSet, ArtifactSplitSubstat, CharacterStats, ElementalSkill, CharacterData, DetailedGenshinUser, Character } from "enka-network-api";
import _ from "lodash";
import artifactSetStat from "@/public/artifactSetStat";
import characterPassiveStat from "@/public/characterPassiveStat";

/*------------------------------------------------------------------*/
// 추후에 사용
// 레벨 입력 시 기초 스텟값 결과를 리턴받음
// 다른 다양한 함수가 존재하는 것으로 예상됨.
import genshinDb from "genshin-db";
import weaponOptionStat from "@/public/weaponOptionStat";
const a = genshinDb.characters("ganyu");
const testa = a?.stats(90);
// const testaasd = genshinDb.weapons(무기이름);
// const testStat = testaasd?.stats(90);

/*------------------------------------------------------------------*/

//

const enka = new EnkaClient();
const app = express();
const port = 9001;

const characters = _.uniqBy(enka.getAllCharacters(), "id");
const weapons = enka.getAllWeapons().filter((w) => w.stars === 5);
const artifacts = enka.getAllArtifacts();
const artifactSets = enka.getAllArtifactSets();
const artifactetSets5Star = artifactSets.filter((a) => a._data.EKBNEFGNCDP === 5);

// console.log(characters.map((c) => c.name.get('kr')));
// console.log(artifactSets.filter((w) => w.name.get('kr') === '청록색 그림자'));
// let weaponList = weapons.filter((w) => w.name.get('kr') === '안개를 가르는 회광' || w.name.get('kr') === '매의 검' || w.name.get('kr') === '예초의 번개' || w.name.get('kr') === '고요히 샘솟는 빛');
// let weaponList = weapons.filter((w) => w.stars > 2);
// console.log(weaponList);
// console.log(weaponList.map((w) => w.getAscensionData(5)));

enka.fetchUser(840110542).then((resCharacters: DetailedGenshinUser) => {
  const userCharacters = resCharacters.characters;
  const returnData: object[] = [];
  userCharacters.map((characterInfo: Character) => {
    const passiveStat = characterPassiveStat[characterInfo.characterData.name.get("kr")];
    const info = {
      character: {
        // 문제 : enka에 각 특성마다 내용이 discription으로만 정리되어있음 +  대략 90몇개 캐릭터 마다 e, q, 패시브, 운명의 자리 등등이 존재
        // 해결 방법 : 내 캐릭터만 일단 정의해서 사용. 추후 나머지 점점 추가해가기
        // 각종 스킬 및 시너지로 인한 버프는 수동기입하도록 적용
        // 패시브까지만 자동적용하도록 하기
        passive: characterPassiveStat[characterInfo.characterData.name.get("kr")],
      },
      weapon: {
        // 문제 : 수작업하기엔 수량이 너무 많음(3~5성: 200개)
        // 해결 방법 : 내 캐릭터만 일단 정의해서 사용. 추후 나머지 점점 추가해가기
        baseAttack: { type: characterInfo.weapon.weaponStats[0].fightProp, rawValue: characterInfo.weapon.weaponStats[0].rawValue },
        subStat: { type: characterInfo.weapon.weaponStats[1].fightProp, rawValue: characterInfo.weapon.weaponStats[1].rawValue },
        option: weaponOptionStat[characterInfo.weapon.weaponData.name.get("kr")],
      },
      artifacts: {
        artifact: characterInfo.artifacts.map((art) => ({
          name: art.artifactData.name.get("kr"),
          mainStat: { type: art.mainstat.fightProp, rawValue: art.mainstat.rawValue },
          subStat: art.substats.total.map((stat) => ({ type: stat.fightProp, rawValue: stat.rawValue })),
        })),
        setStat: ArtifactSet.getActiveSetBonus(characterInfo.artifacts)
          .filter((set) => set.count > 1)
          .map((set) => {
            const name = set.set.name.get("kr");
            return {
              name: name,
              stat: artifactSetStat[name].filter((stat) => stat.needCount <= set.count),
            };
          }),
      },
      imageUrl: {
        charactor: {
          frontIcon: characterInfo.costume.icon.url,
          splashImage: characterInfo.costume.splashImage.url,
          skill: {
            normalAttack: characterInfo.skillLevels[0].skill.icon.url,
            elementalSkill: characterInfo.skillLevels[1].skill.icon.url,
            elementalBust: characterInfo.skillLevels[2].skill.icon.url,
          },
          passive: characterInfo.characterData.passiveTalents.slice(0, 2).map((d) => ({ url: d.icon.url, name: d.name.get("kr") })),
          constellation: {},
        },
        weapon: characterInfo.weapon.weaponData.splashImage.url,
        artifacts: characterInfo.artifacts.map((artifact) => artifact.artifactData.icon.url),
        // 운명의 자리랑 패시브 이미지도 넣어주는게 좋겠다.
      },
    };

    // 내가아닌 캐릭터 자체의 데이터가 필요할듯.
    // 별자리 on/off를 시키게 하는건 아직 시기상조인가??
    // 일단 패시브먼저
    returnData.push(info);
  });
  // ArtifactSplitSubstat.sumStatProperties
  // userCharacters.characters[0].stats._data => fightProps
  //   let allWeapons = weaponList;
  // artifactSets.map((sets) => sets.)
  // let test = new ArtifactSet(artifactSets, enka);
  // let ganyuArtifact = enkaArtifact.getActiveSetBonus(resCharacters.characters[0].artifacts);
  // 문제가 있단 말이지???
  // ArtifactSet.getActiveSetBonus이걸 써야해.
  // 문제는 저걸 쓰려면 컨스트럭터가 필요해.
  // 띠부레같은 컨스트럭터는 전부 스트링티파이가 안되는거로 보여
  // 음 해당 요소의 키값이 저기에 들어가는거로 보이긴하는데,
  // enka가 들어가자 마자 바로 또 저 ㅈㄹ이긴하거든?
  // 문제는 난 저 오브젝트가 필요하긴해???
  // 캐릭터 데이터는 끄집어 와서 처리하면 댐
  // 성유물은???셋옵이 ㅈㄹ맞거든
});
// .catch((err) => {
//   console.log(err);
// });

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});

/* 
몬스터 내성깍에 대해서는 뭐 없네???

그러고 보니 그렇네??
내성깍에 대한 데미지는 몬스터에 따라서 전부 달라지니까 띠부레잔아?
내성깍에 대한건 직접 계산해서 입력하게 하고, 계산에 필요한 내성또한 입력하게 해버려.
그거에 따른 데미지 최종 데미지를 만들고싶은거니까
스킬 계수는 무조건 100%를 기준으로 진행.

아 알 수가 없구나
스킬에 체퍼가붙을 수도 있고, 공퍼가 붙을 수도 있고, 그렇게 나오니까 띠부레
씨밤바?????

그럼 기초 스텟을 뭐로 지정할지 입력하게 해야하네?
내가 다 데이터를 갖고있을 수는 있는데, 이게 롯같거든?
원신 캐릭터만 몇개여


원신 캐릭터만 81개라고?ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ
이걸 전부 하나하나 지정해줘야한다? 다 파악해서??
헛소리하지마 임마!

주옵션 개꼴받네???
와 이거 다른 스텟으로 치환되는 캐릭터의 경우는 어카냐? ㅈ댓네???
데이터가 한정적일 수 밖에 없네

대표적인게 호두, 노엘은 치환
듀얼 계수는 나히다, 치오리 등등이 있음.

계수를 직접 입력하게 해야하겠는데???
-> 이거 각 스킬렙에 따라서 계수가 변동되기 때문임.
-> 그 뜻은 해당 캐릭터인 경우 스킬렙에 따라서 계수값을 변경해 줘야함.
필요 항목: 계수 입력, 

계수가 반반인 경우는 각 레벨마다 계수 비율을 봐야해.
나히다의 경우를 봤을 때 약간의 오차는 있지만, 아마 안보이는 영역 연산에서 표기상 오류때문에 그럴꺼야.
나히다의 경우 0.5:1로 고정임!!

enka의 데이터는 전부 캐릭터 스텟창에 표시되는 스텟뿐이없음.
또한, 상시효과뿐으로 보임. 조건부 옵션은 없는거로 보임


성유물 spilt데이터라는게 성장할 때 마다 붙은 기록 + 얻었을 때 부여된 옵션이네???



내가 원하는 것 : 각 세팅별 스킬 계수 100%짜리의 데미지
enka에 있는 것 : 무기 주옵, 부옵, 성유물 주옵, 부옵, 성유물 셋옵(상시)
필요한  것 : 무기 옵션에 따른 각종 옵션, 성유물 셋옵(조건부), 각 캐릭터 특성(패시브)에 따른 옵션, 각 캐릭터 돌파에 따른 옵션
            -> 여기서 옵션이란, 스텟 + 피증 + 내성깍 등 데미지에 관여하는 모든 항목을 뜻함.
*/
