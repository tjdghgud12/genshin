import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { store } from './store'
import { HYDRATE, createWrapper } from 'next-redux-wrapper'

// 데이터 구조 정의
// 백단에서 넘겨주는 데이터에 따라 구조 정의 필요하네??
// 싹 다 정의 해야함.
interface ChracterDataState {

}

const initialState: Object[] = [];

export const chracterDataSlice = createSlice({
    name: 'characterData',
    initialState,
    reducers: {
        
    }
})