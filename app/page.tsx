import Image from 'next/image';
import { redirect } from 'next/navigation';

// 루트 페이지의 메인화면 제작부
// 여기서 server Com으로 프레임 제작 -> 프레임은 절대 변하지 않는 부분
// 아마 여기서 만들건 배경 꾸미기정도인데
// 입력창은 클라이언트 컴포넌트로 가야하잔아
// 음 loading은 진짜 해당 화면 로딩하는 도중에 보여주는 화면이기 떄문에 통신 대기 때의 로딩은 별도로 해야해.
//

export default function Home() {
  return <main>test</main>;
}
