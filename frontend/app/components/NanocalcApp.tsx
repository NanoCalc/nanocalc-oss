import Image from 'next/image'
import CommonLogos from './CommonLogos';
import commonLogos from '../lib/common_logos';

export default function NanocalcApp({ appLogoPath, appName }) {
	return (
		<main className="flex min-h-screen flex-col justify-between items-center">
			<section className="w-full h-screen flex flex-col items-center">

			</section>

			<section className="w-full h-screen flex flex-col items-center">
				<Image
					src={appLogoPath}
					width={0}
					height={0}
					alt={`${appName} logo`}
					priority={true}
					className="mt-4 rounded-lg  w-auto h-auto"
				/>

				<CommonLogos logos={commonLogos}/>
			</section>
		</main>
	);
}

