import { Metadata } from 'next';
import NanocalcApp from '../components/NanocalcApp'
import nanocalcApps from '../lib/nanocalc_apps';
import { NanocalcAppConfig } from '../lib/model/NanocalcAppConfig';

export const metadata: Metadata = {
  title: "PLQ-Sim | Nanocalc",
  description: "Photoluminescence Quenching Simulator",
};

const plqsimConfig: NanocalcAppConfig = nanocalcApps["PLQ-Sim"]

export default function Plqsim() {
  return (
    <NanocalcApp config={plqsimConfig} />
  );
}
