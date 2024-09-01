'use client'

import Image from 'next/image'
import { BaseAppConfig } from '../lib/model/NanocalcAppConfig';
import CommonLogos from './CommonLogos';
import commonLogos from '../lib/common_logos';
import ArticleBanner from './ArticleBanner';
import { useState } from 'react';
import { NanocalcViewModel } from '../lib/viewmodel/NanocalcViewModel'

interface NanocalcAppProps {
	config: BaseAppConfig;
}

function camelCaseToSpaced(input: string): string {
	return input
		.replace(/([A-Z])/g, ' $1')
		.replace(/^./, (str) => str.toUpperCase())
		.trim();
}

export default function NanocalcApp({ config }: NanocalcAppProps) {
	const viewModel = new NanocalcViewModel()
	const regularButtons = config.buttons.filter(button => button.isCalculate !== true);
	const calculateButtons = config.buttons.filter(button => button.isCalculate === true);
	const articleBanner = config.articleBanner;
	const firstMode = config.multipleModes?.[0] ?? '';
	const [currentMode, setCurrentMode] = useState(firstMode);
	const [selectedFiles, setSelectedFiles] = useState<{[key:string]: File[]}>({});
	const [selectedFileNames, setSelectedFileNames] = useState<{[key:string]: string}>({});


	const handleFileChange = (fileIdentifier: string, event: React.ChangeEvent<HTMLInputElement>) => {
		const newFileList = event.target.files;

		if (newFileList && newFileList.length > 0) {
			const fileNames = Array.from(newFileList).map(file => file.name).join(', ');
			setSelectedFileNames(prevState => ({
				...prevState,
				[fileIdentifier]: fileNames,
			}));

			setSelectedFiles(prevState => ({
				...prevState,
				[fileIdentifier]: Array.from(newFileList),
			}));
		}
	};

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
								{/* TODO: reset previous choices */}
								{camelCaseToSpaced(mode)}
							</button>
						))}
						{regularButtons.filter(button => !button.operatingMode || button.operatingMode === currentMode).map((button, index) => (
							<div key={index} className="m-1 rounded-md bg-nanocalc-apps-button flex justify-between items-center space-x-4 w-full max-w-md">
								<label className="flex justify-between items-center w-full cursor-pointer text-white font-bold py-2 px-4 rounded">
									<span className="mr-2">
										Choose {button.text}
									</span>
									<input
										type="file"
										multiple={button.allowMultiple}
										style={{ display: 'none' }}
										onChange={(e) => handleFileChange(button.identifier, e)}
									/>
									<span className="ml-auto text-white">
										{selectedFileNames[button.identifier] || 'No file chosen'}
									</span>
								</label>
							</div>
						))}

						{calculateButtons.filter(button => button.operatingMode === currentMode).map((button, index) => (
							<div
								key={index}
								className="m-1 rounded-md bg-nanocalc-apps-button flex justify-between items-center space-x-4 w-full max-w-md"
							>
								<button
									className="text-white font-bold py-2 px-4 rounded w-full"
									onClick={() => {
										viewModel.setMode(currentMode)
										viewModel.uploadFiles(config.appId, selectedFiles)
									}
									}
								>
									{button.text}
								</button>
								<input type="submit" style={{ display: 'none' }} />
							</div>
						))}

					</>) : (<>
						{regularButtons.map((button, index) => (
							<div key={index} className="m-1 rounded-md bg-nanocalc-apps-button flex justify-between items-center space-x-4 w-full max-w-md">
								<label className="flex justify-between items-center w-full cursor-pointer text-white font-bold py-2 px-4 rounded">
									<span className="mr-2">
										Choose {button.text}
									</span>
									<input
										type="file"
										multiple={button.allowMultiple}
										style={{ display: 'none' }}
										onChange={(e) => handleFileChange(button.identifier, e)}
									/>
									<span className="ml-auto text-white m-0 p-0">
										{selectedFileNames[button.identifier] || 'No file chosen'}
									</span>
								</label>
							</div>
						))}

						{calculateButtons.map((button, index) => (
							<div
								key={index}
								className="m-1 rounded-md bg-nanocalc-apps-button flex justify-between items-center space-x-4 w-full max-w-md"
							>
								<button
									className="text-white font-bold py-2 px-4 rounded w-full"
									onClick={() => {
										viewModel.setMode(currentMode)
										viewModel.uploadFiles(config.appId, selectedFiles)
									}
									}
								>
									{button.text}
								</button>
								<input type="submit" style={{ display: 'none' }} />
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
