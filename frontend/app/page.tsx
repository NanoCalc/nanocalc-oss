import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between">
      <section className="w-full h-screen flex flex-col items-center justify-center">
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
