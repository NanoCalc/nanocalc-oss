'use client'

import Image from 'next/image'
import { BaseAppConfig } from '../lib/model/NanocalcAppConfig';
import CommonLogos from './CommonLogos';
import commonLogos from '../lib/common_logos';
import { RegularButton } from "../lib/model/NanocalcAppConfig";
import { handleRegularButtonClick } from '../lib/utils/fileSelectionHandlers';
import { handleCalculateButtonClick } from '../lib/utils/fileSelectionHandlers';

interface NanocalcAppProps {
	config: BaseAppConfig;
}

export default function NanocalcApp({ config }: NanocalcAppProps) {
	const regularButtons: RegularButton[]= config.buttons.filter(button => button.isCalculate !== true);
	const calculateButtons = config.buttons.filter(button => button.isCalculate === true);

	return (
		<main className="flex min-h-screen flex-col justify-between items-center">
			<section className="w-full h-screen flex items-center justify-center bg-nanocalc-apps">
				<div className="flex-1 flex flex-col items-center justify-center">
					{regularButtons.map((button, index) => (
						<div
							key={index}
							className="m-1 rounded-md bg-nanocalc-apps-button flex justify-between items-center space-x-4"
						>
							<button
								className="text-white font-bold py-2 px-4 rounded"
								onClick={() => handleRegularButtonClick(index)}
							>
								Choose {button.text}
							</button>
							<input type="file" id={`regularButtonInput${index}`} style={{ display: 'none' }}/>
						</div>
					))}

					{calculateButtons.map((button, index) => (
						<div
							key={index}
							className="m-1 rounded-md bg-nanocalc-apps-button flex justify-between items-center space-x-4"
						>
							<button
								className="text-white font-bold py-2 px-4 rounded"
								onClick={() => handleCalculateButtonClick(regularButtons)}
							>
								{button.text}
							</button>
							<input type="submit" id={`calculateButtonSubmit${index}`} style={{ display: 'none' }} />
						</div>
					))}
				</div>
			</section>


			<section className="w-full h-screen flex flex-col items-center">
				<Image
					src={config.appLogoPath}
					width={200}
					height={200}
					alt={`${config.appName} logo`}
					priority={true}
					className="mt-4 rounded-lg w-auto h-auto"
				/>
				<CommonLogos logos={commonLogos} />
			</section>
		</main>
	);
}
