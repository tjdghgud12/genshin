import Head from 'next/head'
import Image from 'next/image'
import { Inter } from 'next/font/google'
import styles from '@/styles/Home.module.css'


const inter = Inter({ subsets: ['latin'] })

export default function Test() {
  return (
    <main className={styles.main}>
        <h1>test Page</h1>
    </main>
    
  )
}
