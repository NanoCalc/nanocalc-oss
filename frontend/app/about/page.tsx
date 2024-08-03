import Contributor from '../components/Contributor';
import contributors from '../lib/contributors';
import { Metadata } from 'next';

export const metadata: Metadata = {
    title: "About | Nanocalc",
    description: "The creators of the Nanocalc project",
};

export default function About() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-between">
            <Contributor contributors={contributors}/>
        </main>
    );
}
