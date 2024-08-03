import { Metadata } from 'next';
import NanocalcApp from '../components/NanocalcApp';
import nanocalcApps from '../lib/nanocalc_apps';
import { BaseAppConfig } from '../lib/model/NanocalcAppConfig';

export const metadata: Metadata = {
  title: "FRET-Calc | Nanocalc",
  description: "Förster resonance energy transfer calculator",
};

const fretcalcConfig: BaseAppConfig = nanocalcApps["FRET-Calc"];

export default function Fretcalc() {
  return (
    <NanocalcApp config={fretcalcConfig} />
  );
}
