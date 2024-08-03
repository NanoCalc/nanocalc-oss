import { Metadata } from 'next';
import NanocalcApp from '../components/NanocalcApp'
import nanocalcApps from '../lib/nanocalc_apps';
import { NanocalcAppConfig } from '../lib/model/NanocalcAppConfig';

export const metadata: Metadata = {
  title: "TMM-Sim | Nanocalc",
  description: "Transfer Matrix Method Simulator",
};

const tmmsimConfig: NanocalcAppConfig = nanocalcApps["TMM-Sim"]

export default function Tmmsim() {
  return (
    <NanocalcApp config={tmmsimConfig} />
  );
}
