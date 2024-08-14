export interface BaseAppConfig {
    appLogoPath: string,
    appName: string,
    appId: string,
    buttons: AppButton[],
    articleBanner: ArticleBannerConfig,
    multipleModes?: string[]
}

export interface ArticleBannerConfig {
    title: string,
    doi: string,
    sampleData: string,
    spectralData?: string,
    binaries: string
}

interface BaseButton {
    text: string;
    operatingMode?: string
}

export interface CalculateButton extends BaseButton {
    isCalculate: true;
}

export interface RegularButton extends BaseButton {
    isCalculate?: false;
    expectedExtension: string;
    identifier: string;
    allowMultiple?: boolean;
}

type AppButton = CalculateButton | RegularButton;

export interface NanocalcAppConfig {
    [appName: string]: BaseAppConfig;
}
