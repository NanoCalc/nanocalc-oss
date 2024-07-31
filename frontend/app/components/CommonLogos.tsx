import Image from 'next/image'
import { CommonLogoConfig } from '../lib/model/CommonLogoConfig'


export default function CommonLogos(logos: CommonLogoConfig[]) {
    return(
        <>
        {logos.map((logo) => {
            <Image
            src={logo.appLogoPath}
            width={logo.width}
            height={logo.height}
            alt={logo.description}
            priority={true}
            className="mt-4 dark:bg-white rounded-lg"
            />
        }

        )}
        </>
    )
}