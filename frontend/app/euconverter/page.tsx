import { Metadata } from 'next';
import EuConverter from '../components/EuConverter';
import energyUnitsArray from '../lib/energy_units';

export const metadata: Metadata = {
    title: "EUConverter | Nanocalc",
    description: "Energy unit converter",
};

export default function Euconverter() {
    return (
        <section className="w-full h-screen flex flex-col items-center p-5">
            <EuConverter units={energyUnitsArray} />
        </section>
    )
}