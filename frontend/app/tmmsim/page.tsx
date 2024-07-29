import { Metadata } from 'next';
import NanocalcApp from '../components/NanocalcApp'
import nanocalcApps from '../lib/nanocalc_apps';

//TODO: add metadata description
export const metadata: Metadata = {
  title: "TMM-Sim | Nanocalc",
  description: "",
};

const tmmsimConfig = nanocalcApps["TMM-Sim"]

export default function Tmmsim() {
  return (
    <NanocalcApp appLogoPath={tmmsimConfig.appLogoPath} appName={tmmsimConfig.appName} />
  );
}
