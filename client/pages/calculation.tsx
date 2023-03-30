import Head from 'next/head'
import Image from 'next/image'
import { Inter } from 'next/font/google'
import styles from '@/styles/Home.module.css'
import { useEffect, useState } from 'react'
import axios from 'axios';
import { LoadingSpiner } from './api/components'
import { useRouter } from 'next/router'
import Link from 'next/link'
import { AppProps } from 'next/app'

export default function Calculation() {
    const router = useRouter();
    const [userData, setuserData] = useState<object>(new Object());
    // const [userData, setuserData] = useState<object>(new Object());
    useEffect(() => {
        setuserData(JSON.parse(sessionStorage.getItem('userData')));
        console.log(JSON.parse(sessionStorage.getItem('userData')))
    },[])
    

    // let { query }:any = router.query.userData;
    // let {userData}:any = JSON.parse(query);

    // console.log('calculation =====> ', userData);


    return (
        <main className={"w-screen h-screen absolute bg-violet-300 "}>
            <div className='w-full h-1/10 bg-indigo-200'>{/* Header 대충 홈버튼 같은거? */}

            </div>
            <div className='w-full h-6/10 bg-red-200'> {/* 메인 화면 */}
                <div>{/* 캐릭터 선택 버튼 */}

                </div>
                <div>{/* 캐릭터 스팩 표시 및 성유물 표기 */}
                    <div>{JSON.stringify(userData)}</div>
                </div>
            </div>
            <div className='w-full h-3/10'>{/* tail 대충 조건문이라던가 알림내용같은거 */}

            </div>
        </main>
    )
}
