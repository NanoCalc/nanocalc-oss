import { Metadata } from 'next';
import NanocalcApp from '../components/NanocalcApp'
import nanocalcApps from '../lib/nanocalc_apps';

//TODO: add metadata description
export const metadata: Metadata = {
  title: "RI-Calc | Nanocalc",
  description: "",
};

const ricalcConfig = nanocalcApps["RI-Calc"]

export default function Ricalc() {
  return (
   <NanocalcApp appLogoPath={ricalcConfig.appLogoPath} appName={ricalcConfig.appName}/>
  );
}
