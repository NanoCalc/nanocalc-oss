import Image from 'next/image';
import Contributor from '../components/Contributor';
import contributors from '../lib/contributors'; 

export default function About() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-between">
            {contributors.map((contributor, index) => (
                <Contributor 
                    key={index}
                    imagePath={contributor.imagePath}
                    name={contributor.name}
                    text={contributor.text}
                />
            ))}
        </main>
    );
}
