'use client'

import Image from 'next/image'
import { BaseAppConfig } from '../lib/model/NanocalcAppConfig';
import CommonLogos from './CommonLogos';
import commonLogos from '../lib/common_logos';
import { RegularButton } from "../lib/model/NanocalcAppConfig";
import { handleRegularButtonClick } from '../lib/utils/fileSelectionHandlers';
import { handleCalculateButtonClick } from '../lib/utils/fileSelectionHandlers';
import ArticleBanner from './ArticleBanner';
import { useState } from 'react';

interface NanocalcAppProps {
	config: BaseAppConfig;
}

export default function NanocalcApp({ config }: NanocalcAppProps) {
	const regularButtons: RegularButton[] = config.buttons.filter(button => button.isCalculate !== true);
	const calculateButtons = config.buttons.filter(button => button.isCalculate === true);
	const articleBanner = config.articleBanner;
	const firstMode = config.multipleModes?.[0] ?? '';
	const [currentMode, setCurrentMode] = useState(firstMode);

	return (
		<main className="flex min-h-screen flex-col md:flex-row justify-between items-center">
			<section className="w-full h-screen flex flex-col md:w-1/2 items-center justify-center bg-gradient-theme-nanocalc-apps md:bg-gradient-theme-nanocalc-apps-md">
				<div className="flex flex-col items-center justify-center space-y-4 ml-2 mr-2">
					{config.multipleModes && config.multipleModes.length > 1 ? (<>
						{config.multipleModes.map(mode => (
							<button
								key={mode}
								className={`px-4 py-2 rounded-md font-bold ${currentMode === mode ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'}`}
								onClick={() => setCurrentMode(mode)}
							>
								{mode}
							</button>
						))}
						{regularButtons.filter(button => !button.operatingMode || button.operatingMode === currentMode).map((button, index) => (
							<div
								key={index}
								className="m-1 rounded-md bg-nanocalc-apps-button flex justify-between items-center space-x-4 w-full max-w-md"
							>
								<button
									className="text-white font-bold py-2 px-4 rounded w-full"
									onClick={() => handleRegularButtonClick(button.identifier)}
								>
									Choose {button.text}
								</button>
								<input type="file" id={`regularButtonInput${button.identifier}`} multiple={button.allowMultiple} style={{ display: 'none' }} />
								<span id={`fileNameDisplay${button.identifier}`} className="text-white" onClick={() => handleRegularButtonClick(button.identifier)}>No file chosen</span>
							</div>
						))}

						{calculateButtons.filter(button => button.operatingMode === currentMode).map((button, index) => (
							<div
								key={index}
								className="m-1 rounded-md bg-nanocalc-apps-button flex justify-between items-center space-x-4 w-full max-w-md"
							>
								<button
									className="text-white font-bold py-2 px-4 rounded w-full"
									onClick={() => handleCalculateButtonClick(regularButtons, config.appId)}
								>
									{button.text}
								</button>
								<input type="submit" id={`calculateButtonSubmit${index}`} style={{ display: 'none' }} />
							</div>
						))}

					</>) : (<>
						{regularButtons.map((button, index) => (
							<div
								key={index}
								className="m-1 rounded-md bg-nanocalc-apps-button flex justify-between items-center space-x-4 w-full max-w-md"
							>
								<button
									className="text-white font-bold py-2 px-4 rounded w-full"
									onClick={() => handleRegularButtonClick(button.identifier)}
								>
									Choose {button.text}
								</button>
								<input type="file" id={`regularButtonInput${button.identifier}`} multiple={button.allowMultiple} style={{ display: 'none' }} />
								<span id={`fileNameDisplay${button.identifier}`} className="text-white" onClick={() => handleRegularButtonClick(button.identifier)}>No file chosen</span>
							</div>
						))}

						{calculateButtons.map((button, index) => (
							<div
								key={index}
								className="m-1 rounded-md bg-nanocalc-apps-button flex justify-between items-center space-x-4 w-full max-w-md"
							>
								<button
									className="text-white font-bold py-2 px-4 rounded w-full"
									onClick={() => handleCalculateButtonClick(regularButtons, config.appId)}
								>
									{button.text}
								</button>
								<input type="submit" id={`calculateButtonSubmit${index}`} style={{ display: 'none' }} />
							</div>
						))}
					</>)}

				</div>

				<div className="flex flex-col items-center justify-center mt-8 w-full max-w-md px-4">
					<ArticleBanner config={articleBanner} />
				</div>
			</section>

			<section className="w-full h-screen flex flex-col md:w-1/2 items-center bg-gradient-theme-common-logos md:bg-gradient-theme-common-logos-md">
				<Image
					src={config.appLogoPath}
					width={200}
					height={200}
					alt={`${config.appName} logo`}
					priority={true}
					className="mt-4 md:mt-52 rounded-lg w-auto h-auto"
				/>
				<CommonLogos logos={commonLogos} />
			</section>
		</main>
	);
}
