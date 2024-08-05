import Image from 'next/image'
import { ContributorConfig } from '../lib/model/ContributorConfig';
import { Fragment } from 'react';

const networksLogosPath = "/networks_logos/"

interface ContributorProps {
    contributor: ContributorConfig
}

const NetworksLinks = ({ contributor }: ContributorProps) => (
    <div className="flex justify-center mt-2 p-3">
        {contributor.github && (
            <a href={contributor.github} target="_blank" rel="noopener noreferrer">
                <Image src={`${networksLogosPath}github.svg`} alt="GitHub logo" width={24} height={24} className="mx-2" />
            </a>
        )}
        {contributor.linkedin && (
            <a href={contributor.linkedin} target="_blank" rel="noopener noreferrer">
                <Image src={`${networksLogosPath}linkedin.svg`} alt="LinkedIn logo" width={24} height={24} className="mx-2" />
            </a>
        )}
        {contributor.orcid && (
            <a href={contributor.orcid} target="_blank" rel="noopener noreferrer">
                <Image src={`${networksLogosPath}orcid.svg`} alt="ORCID logo" width={24} height={24} className="mx-2" />
            </a>
        )}
        {contributor.lattes && (
            <a href={contributor.lattes} target="_blank" rel="noopener noreferrer">
                <Image src={`${networksLogosPath}lattes.svg`} alt="Lattes logo" width={24} height={24} className="mx-2 dark:bg-white dark:rounded-lg" />
            </a>
        )}
    </div>
);

interface ContributorsProps {
    contributors: ContributorConfig[]
}

export default function Contributor({ contributors }: ContributorsProps) {
    return (
        <section className="w-full h-screen flex flex-col items-center pb-8">
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
                    <NetworksLinks contributor={contributor}/>
                </Fragment>
            ))}
        </section>
    );
}