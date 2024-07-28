import { Metadata } from 'next';
import NanocalcApp from '../components/NanocalcApp'
import nanocalcApps from '../lib/nanocalc_apps';

export const metadata: Metadata = {
  title: "FRET-Calc | Nanocalc",
  description: "Förster resonance energy transfer calculator",
};

const fretcalcConfig = nanocalcApps["FRET-Calc"]

export default function Fretcalc() {
  return (
   <NanocalcApp appLogoPath={fretcalcConfig.appLogoPath} appName={fretcalcConfig.appName}/>
  );
}
