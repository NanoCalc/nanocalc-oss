import { Metadata } from 'next';
import NanocalcApp from '../components/NanocalcApp'
import nanocalcApps from '../lib/nanocalc_apps';


export const metadata: Metadata = {
  title: "PLQ-Sim | Nanocalc",
  description: "Photoluminescence Quenching Simulator",
};

const plqsimConfig = nanocalcApps["PLQ-Sim"]

export default function Plqsim() {
  return (
    <NanocalcApp appLogoPath={plqsimConfig.appLogoPath} appName={plqsimConfig.appName} />
  );
}
