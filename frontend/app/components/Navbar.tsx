"use client"
import { useState, useRef } from 'react';
import Link from 'next/link';

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);
    const navbarRef = useRef(null);

    const handleToggle = () => {
        setIsOpen(!isOpen);
    };

    const handleLinkClick = () => {
        setIsOpen(false);
    };

    const handleClickOutsideNavbar = (event) => {
	// touch/clicks that are not in the navbar cause it to collapse 
        if (navbarRef.current && !navbarRef.current.contains(event.target)) {
            setIsOpen(false);
        }
    };

    // listener for handling events in elements that aren't the navbar
    if (typeof window !== "undefined") {
        document.addEventListener('click', handleClickOutsideNavbar);
    }

    return (
        <nav ref={navbarRef} className="navbar bg-nanocalc-blue text-white p-4">
            <div className="flex justify-between items-center">
                <div className="text-xl">Nanocalc</div>
                <div className="md:hidden toggle-button" onClick={handleToggle}>
                    <button>
                        <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
                    </button>
                </div>
            </div>
	      <ul className={`collapsible ${isOpen ? 'open' : ''} md:flex md:space-x-4 flex-col md:flex-row`}>            
                <li onClick={handleLinkClick}>
                    <Link href="/">
                        Home
                    </Link>
                </li>
                <li onClick={handleLinkClick}>
                    <Link href="/fret">
                        FRET-Calc
                    </Link>
                </li>
                <li onClick={handleLinkClick}>
                    <Link href="/ricalc">
                        RI-Calc
                    </Link>
                </li>
                <li onClick={handleLinkClick}>
                    <Link href="/plqsim">
                        PLQ-Sim
                    </Link>
                </li>
                <li onClick={handleLinkClick}>
                    <Link href="/tmmsim">
                        TMM-Sim
                    </Link>
                </li>
                <li onClick={handleLinkClick}>
                    <Link href="/euconverter">
                        EU Converter
                    </Link>
                </li>
                <li onClick={handleLinkClick}>
                    <Link href="/about">
                        About
                    </Link>
                </li>
            </ul>
        </nav>
    );
}

