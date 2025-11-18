import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import api from "@/lib/axios";
import { IUidSearchResult } from "@/types/calculatorType";
import Image from "next/image";
import { redirect } from "next/navigation";
import React from "react";
import CharacterSettingCard from "./CharacterSettingCard";

const CharacterTabs = async ({ params }: { params: Promise<{ uid: string }> }): Promise<React.ReactElement> => {
  const { uid } = await params;
  const elementBgColors: Record<string, string> = {
    Fire: `bg-Fire`,
    Water: `bg-Water`,
    Wind: `bg-Wind`,
    Electric: `bg-Electric`,
    Ice: `bg-Ice`,
    Rock: `bg-Rock`,
    Grass: `bg-Grass`,
  };

  const res = await api.get(`/user/${uid}`);
  if (res.status !== 200) redirect(`/`);
  const characters: IUidSearchResult[] = res.data.characters;

  return (
    <Tabs defaultValue={characters[0].characterInfo.name as string} className="w-[90%] min-w-[1120px] mx-auto gap-0">
      <TabsList className="w-full h-fit justify-around pt-3 px-3 rounded-2xl mx-auto">
        {characters.map((character) => {
          const element = character.characterInfo.element;
          const iconUrl: string = character.characterInfo.icon?.front;
          const name = character.characterInfo.name;

          return (
            <TabsTrigger
              key={`calculator-tab-trigger-${name}`}
              className={`w-[5vw] h-[5vw] min-w-20 min-h-20 relative overflow-hidden flex-none border-[3px] border-stone-300 ${elementBgColors[element]} rounded-full mx-1 data-[state=active]:border-lime-400 hover:border-lime-400 data-[state=active]:${elementBgColors[element]}`}
              value={name}
            >
              <Image src={iconUrl} alt="" priority fill sizes="(max-width: 1200px) 5vw" />
            </TabsTrigger>
          );
        })}
      </TabsList>
      {characters.map((character) => {
        const name = character.characterInfo.name;
        return (
          <TabsContent key={`calculator-tab-content-${name}`} value={name}>
            <CharacterSettingCard character={character} />
          </TabsContent>
        );
      })}
    </Tabs>
  );
};

export default CharacterTabs;
