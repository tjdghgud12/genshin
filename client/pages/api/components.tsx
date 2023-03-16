import React, {useState} from 'react'
import Next from 'next'

interface spinerProp {
    ClassName: string,
    style: string,
    name: string,
    id: string,
    spinWidth: string,
    spinHeigth: string,
    spingWeight: string,
}
const LoadingSpiner = ( prop:spinerProp ):React.ReactElement => {
    // console.log('prop ===> ', prop);
    // console.log('prop.ClassName ===> ', prop.ClassName);
    // console.log('prop.name ===> ', prop.id);
    let spinStyle:string = "animate-spin rounded-full border-r-white border-t-white border-l-slate-200 border-b-slate-200 ";
    spinStyle += "w-"+prop.spinWidth+" "
    spinStyle += "h-"+prop.spinHeigth+" "
    spinStyle += "border-"+prop.spingWeight+" "
    
    
    return(
        <div className={prop.ClassName}>
            <svg className={spinStyle} >
            </svg>
            <p className='font-sans ml-2 font-bold text-4xl my-auto text-slate-50 '>Loading...</p>
        </div>
    )
}
LoadingSpiner.defaultProps = {
    ClassName: '',
    style: '',
    name: '',
    id: '',
    spinWidth: '8',
    spinHeigth: '8',
    spingWeight: '2',
}


export { LoadingSpiner }