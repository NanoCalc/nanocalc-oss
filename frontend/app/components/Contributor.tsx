import Image from 'next/image'

export default function Contributor({ imagePath, name, text }) {
    return (
        <section className="w-full h-screen flex flex-col items-center">
            <Image
                src={imagePath}
                width={200}
                height={200}
                alt={`Picture of ${name}`}
                className="mt-8 mb-4"
            />
            <h2 className="ml-4 mr-4 mt-10 md:w-1/2 text-justify">
                <b>{name}</b> {text}
            </h2>
        </section>
    );
}
