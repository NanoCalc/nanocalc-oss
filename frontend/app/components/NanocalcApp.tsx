import Image from 'next/image'

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

				<Image
					src="/common_logos/dine.png"
					width={195}
					height={97}
					alt="DINE logo - Grupo de Dispositivos Nanoestruturados"
					priority={true}
					className="mt-4 dark:bg-white rounded-lg"
				/>

				<Image
					src="/common_logos/namor.png"
					width={195}
					height={83}
					alt="NAMOR logo - Nanoscience Modelling in Rio"
					priority={true}
					className="mt-4 dark:bg-white  rounded-lg"
				/>
				<figure aria-labelledby="Logos of associated universities with the project" className="flex flex-row">
					<Image
						src="/common_logos/ufrj.png"
						width={78}
						height={103}
						alt="UFRJ logo - Universidade Federal do Rio de Janeiro"
						priority={true}
						className="mt-4 dark:bg-white  rounded-lg mr-2 "
					/>

					<Image
						src="/common_logos/ufpr.png"
						width={111}
						height={78}
						alt="UFPR logo- Universidade Federal do Paraná"
						priority={true}
						className="mt-4 dark:bg-white  rounded-lg ml-2 "
					/>

				</figure>
			</section>
		</main>
	);
}

