export interface BaseAppConfig {
    appLogoPath: string,
    appName: string,
    appId: string,
    buttons: AppButton[],
    articleBanner: ArticleBannerConfig
}

export interface ArticleBannerConfig {
    title: string,
    doi: string,
    sampleData: string,
    spectralData?: string,
    binaries: string
}

//TODO: only essential props in base button
interface BaseButton {
    text: string;
    allowMultiple?: boolean;
    isCalculate?: boolean;
}

interface CalculateButton extends BaseButton {
    isCalculate: true;
    expectedExtension?: string;
}

export interface RegularButton extends BaseButton {
    isCalculate?: false;
    expectedExtension: string;
    identifier: string;
}

type AppButton = CalculateButton | RegularButton;

export interface NanocalcAppConfig {
    [appName: string]: BaseAppConfig;
}
