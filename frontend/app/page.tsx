import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between">
     <section className="bg-blue-500 w-full h-screen flex items-center justify-center">
          <h2>Welcome</h2>
        </section>
       <section className="bg-green-500 w-full h-screen flex items-center justify-center">
          <h2>Open source notice</h2>
        </section>
    </main>
  );
}
