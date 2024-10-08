import { Metadata } from 'next';
import NanocalcApp from '../components/NanocalcApp'
import nanocalcApps from '../lib/nanocalc_apps';
import { BaseAppConfig } from '../lib/model/NanocalcAppConfig';

export const metadata: Metadata = {
  title: "RI-Calc | Nanocalc",
  description: "Refractive index calculator utilizing Kramers-Kronig relations",
};

const ricalcConfig: BaseAppConfig = nanocalcApps["RI-Calc"]

export default function Ricalc() {
  return (
    <NanocalcApp config={ricalcConfig} />
  );
}
