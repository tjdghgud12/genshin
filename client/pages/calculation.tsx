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
    useEffect(() => {
        setuserData(JSON.parse(sessionStorage.getItem('userData')));
    },[])
    

    // let { query }:any = router.query.userData;
    // let {userData}:any = JSON.parse(query);

    // console.log('calculation =====> ', userData);


    return (
        <main className={"w-screen h-screen absolute bg-violet-300 "}>
            <div>{JSON.stringify(userData)}</div>
        </main>
    )
}