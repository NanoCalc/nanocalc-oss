import Image from 'next/image'
import { ContributorConfig } from '../lib/model/ContributorConfig';
import { Fragment } from 'react';

interface ContributorProps {
    contributors: ContributorConfig[]
}

export default function Contributor({ contributors }: ContributorProps) {
    return (
        <section className="w-full h-screen flex flex-col items-center">
            {contributors.map((contributor, index) => (
                <Fragment key={index}>
                    <Image
                        src={contributor.imagePath}
                        width={200}
                        height={200}
                        alt={`Picture of ${contributor.name}`}
                        className="mt-8 mb-4"
                    />
                    <h2 className="ml-4 mr-4 mt-10 md:w-1/2 text-justify">
                        <b>{contributor.name}</b> {contributor.text}
                    </h2>
                </Fragment>
            ))}
        </section>
    );
}
