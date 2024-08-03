import Image from 'next/image'
import { CommonLogoConfig } from '../lib/model/CommonLogoConfig'

const groupFigureAriaLabel = "Logos of associated universities with the project"

interface CommonLogosProps {
    logos: CommonLogoConfig[]
}

export default function CommonLogos({ logos }: CommonLogosProps) {
    const groupedLogos = logos.filter(logo => logo.shouldGroup);
    const ungroupedLogos = logos.filter(logo => !logo.shouldGroup);

    return (
        <>
            {ungroupedLogos.map((logo, index) => (
                <Image
                    key={index}
                    src={logo.appLogoPath}
                    width={logo.width}
                    height={logo.height}
                    alt={logo.description}
                    priority={true}
                    className="mt-4 dark:bg-white rounded-lg"
                />
            ))}
            {groupedLogos.length > 0 && (
                <figure aria-labelledby={groupFigureAriaLabel} className="flex flex-row">
                    {groupedLogos.map((logo, index) => (
                        <Image
                            key={index}
                            src={logo.appLogoPath}
                            width={logo.width}
                            height={logo.height}
                            alt={logo.description}
                            priority={true}
                            className="mt-4 dark:bg-white rounded-lg ml-2"
                        />
                    ))}
                </figure>
            )}
        </>
    );
}
