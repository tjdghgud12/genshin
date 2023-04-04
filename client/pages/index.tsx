import Head from 'next/head'
import Image from 'next/image'
import { Inter } from 'next/font/google'
import styles from '@/styles/Home.module.css'
import { useEffect, useState } from 'react'
import axios from 'axios';
import { LoadingSpiner } from './api/components'
import { useRouter } from 'next/router'
import Link from 'next/link'

export default function Home() {
  const router = useRouter();
  const [userUID, setuserUID] = useState<string>('');
  const [loadingFlag, setloadingFlag] = useState<boolean>(false);
  useEffect(() => {
    sessionStorage.clear();
  },[])

  const ChangeUID = (e:object) => { 
    if(e.target.value.length > 9){ e.target.value = e.target.value.substr(0, 9); }
    setuserUID(e.target.value); 
  }
  
  const onSubmitHandler = async(e) => {
    e.preventDefault();
    try{
      setloadingFlag(true);
      const datas = { userUID: userUID }
      const res = await axios.post('/api/getUser', datas);
      if(res.statusText === "OK"){
        setloadingFlag(false);
        let userData = JSON.stringify(res.data);
        //console.log(userData);
        // 여기서 cookie에 보관 필요!.
        // state에 저장하면 새로고침 할 때 무조건 어케되든 데이터 증발해
        // 유저 정보를 저장할 방법은
        // 1. cookie나 localstorage 등 브라우저 저장소를 사용한다.
        // 2. back 서버단에서 저장해 두고, front에서는 페이지 그릴때 마다 읽어온다
        //sessionStorage.setItem("userData", userData);
        router.push({
          pathname: 'calculation',
          // query: userData,
        }, 'calculation')
      }
    }catch(error){ 
      console.log("error ===> ", error);
      setloadingFlag(false);
    }
  }


  return (
    <main className={"w-screen h-screen bg-violet-300 "}>
      <div className={'w-full h-full flex items-center justify-center absolute top-0 left-0 z-50 ' + (loadingFlag===true ? '':'hidden')}>
        <div className='w-full h-full absolute top-0 left-0 bg-black opacity-20 z-10' />
        <div className={'w-full absolute left-0 z-20 my-auto' }>
          <LoadingSpiner 
            ClassName='w-fit h-fit flex m-auto '
            spinWidth='14'
            spinHeigth='14'
            spingWeight='4'
          />  
        </div>
      </div>

      <div className={"body absolute z-10"}>
        <div className='w-full h-3/5 flex items-end justify-center'>
          <div className={'w-full' }>
            <Image
              className='m-auto'
              src={"/../public/logo-genshin.png"}
              alt={"background Image for home"}
              width={900}
              height={200}
            />
          </div>
        </div>
        <form className='w-96 m-auto rounded-md bg-white opacity-80' onSubmit={onSubmitHandler}>
          <input 
              className={'w-80 h-14 text-center text-3xl rounded-md'}
              type={'number'}
              placeholder={"UID"}
              value={userUID}
              onChange={ChangeUID}
              maxLength={9}
            />
          <button className='w-16 h-14 text-3xl'> {'>'} </button>
        </form>
      </div>
    </main>
  )
}
