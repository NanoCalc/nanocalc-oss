export interface BaseAppConfig {
    appLogoPath: string,
    appName: string,
    buttons: AppButton[],
}

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
}

type AppButton = CalculateButton | RegularButton;

export interface NanocalcAppConfig {
    [appName: string]: BaseAppConfig;
}
