// 사용자 계정 정보를 가져와 장비 퍼센티지 계산 화면으로 지정
'use client';

import { useEffect } from 'react';

export default function Calculator() {
  useEffect(() => {
    if (!localStorage.getItem('test')) {
      localStorage.setItem('test', 'testDat');
    } else {
      console.log('aaaaaaaaaaaaaaaaaaaaaaaaaa!!!!!!!!!!!!!!');
    }
  }, []);
  return <main>Calculator Page</main>;
}
