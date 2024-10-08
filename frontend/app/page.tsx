import Link from 'next/link';
import Image from 'next/image';

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
          className="mt-10"
        />
        <h1 className="p-4 animate-slideIn text-justify items-center">
          <b>Welcome to the Nanocalc project website!</b>
        </h1>
        <h2 className="p-4 animate-slideIn text-justify items-center">
          We are a research group offering free online tools for calculating important materials science parameters.
        </h2>

        <h2 className="p-4 animate-slideIn text-justify">
          If you have any critics or suggestions regarding the <b>theory</b> behind the web applications,
          get in touch with our team&apos;s professor, Graziâni, at <b><Link href="mailto:gcandiotto@iq.ufrj.br">gcandiotto@iq.ufrj.br</Link></b>
        </h2>
        <h2 className="p-4 animate-slideIn text-justify">
          Otherwise, regarding <b>technical errors and improvements</b>, send an e-mail to the domain&apos;s administrator, Omar,
          at <b><Link href="mailto:omarmsqt@gmail.com">omarmsqt@gmail.com</Link></b>
        </h2>

        <Image
          src="/networks_logos/open_source.svg"
          alt="Open Source Initiative Trademark logo"
          width={250}
          height={250}
          className="mt-12 mx-2"
        />

        <h1 className="p-4 text-justify items-center">
          <b>This website&apos;s source code is open!</b>
        </h1>

        <h2 className="p-4 text-justify items-center">
          While the intricate calculation methods behind the web apps remain proprietary, you&apos;re encouraged to explore the
          Nanocalc universe of apps in our <a href="https://github.com/NanoCalc/nanocalc-oss"><b>public repository on GitHub</b></a>.
        </h2>
      </section>
    </main>
  );
}
