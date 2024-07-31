import { Metadata } from 'next';
import NanocalcApp from '../components/NanocalcApp'
import nanocalcApps from '../lib/nanocalc_apps';


export const metadata: Metadata = {
  title: "TMM-Sim | Nanocalc",
  description: "Transfer Matrix Method Simulator",
};

const tmmsimConfig = nanocalcApps["TMM-Sim"]

export default function Tmmsim() {
  return (
    <NanocalcApp appLogoPath={tmmsimConfig.appLogoPath} appName={tmmsimConfig.appName} />
  );
}
