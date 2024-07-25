import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
     <section className="bg-blue-500 w-full h-screen flex items-center justify-center">
          <h2>Section 1</h2>
        </section>
        <section className="bg-red-500 w-full h-screen flex items-center justify-center">
          <h2>Section 2</h2>
        </section>
        <section className="bg-green-500 w-full h-screen flex items-center justify-center">
          <h2>Section 3</h2>
        </section>
    </main>
  );
}
