import NanocalcApp from '../components/NanocalcApp'
import nanocalcApps from '../lib/nanocalc_apps';

const fretcalcConfig = nanocalcApps["FRET-Calc"]

export default function Fretcalc() {
  return (
   <NanocalcApp appLogoPath={fretcalcConfig.appLogoPath} appName={fretcalcConfig.appName}/>
  );
}
