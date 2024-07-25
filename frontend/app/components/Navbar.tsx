"use client"
import { useState } from 'react';
import Link from 'next/link';

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <nav className="bg-gray-800 text-white p-4">
            <div className="flex justify-between items-center">
	    {/*<div className="text-xl">NanoCalc</div>*/}
                <div className="md:hidden" onClick={() => setIsOpen(!isOpen)}>
                    <button>
                        <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
                    </button>
                </div>
            </div>
            
            <ul className={`md:flex md:space-x-4 ${isOpen ? 'flex' : 'hidden'} flex-col md:flex-row`}>
                <li>
                    <Link href="/">
                        Home
                    </Link>
                </li>
                <li>
                    <Link href="/fret">
                        FRET-Calc
                    </Link>
                </li>
                <li>
                    <Link href="/ricalc">
                        RI-Calc
                    </Link>
                </li>
                <li>
                    <Link href="/plqsim">
                        PLQ-Sim
                    </Link>
                </li>
                <li>
                    <Link href="/tmmsim">
                        TMM-Sim
                    </Link>
                </li>
                <li>
                    <Link href="/euconverter">
                        EU Converter
                    </Link>
                </li>
                <li>
                    <Link href="/about">
                        About
                    </Link>
                </li>
            </ul>
        </nav>
    );
}

