import Link from 'next/link';
import Image from 'next/image'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col justify-between items-center">
      <section className="w-full h-screen flex flex-col items-center">
	<Image
	 src="/nanocalc_logo.svg"	
	 width={250}
	 height={250}
	 alt="Nanocalc logo"
	 priority={true}
	 className="mt-4"
	/>
	<h1 className="p-4 animate-slideIn text-justify items-center">
	 <b>Welcome to the Nanocalc project website!</b>
	</h1>
      <h2 className="p-4 animate-slideIn text-justify items-center">
         We are a research group offering free online tools for calculating important materials science parameters.
        </h2>

      	<h2 className="p-4 animate-slideIn text-justify">
          If you have any critics or suggestions regarding the <b>theory</b> behind the web applications,
          get in touch with our team's professor, Graziâni, at <b><Link href="mailto:gcandiotto@iq.ufrj.br">gcandiotto@iq.ufrj.br</Link></b>
        </h2>
        <h2 className="p-4 animate-slideIn text-justify">
          Otherwise, regarding <b>technical errors and improvements</b>, send an e-mail to the domain's administrator, Omar,
          at <b><Link href="mailto:omarmesquita@eq.ufrj.br">omarmesquita@eq.ufrj.br</Link></b>
        </h2>
      </section>
    </main>
  );
}
