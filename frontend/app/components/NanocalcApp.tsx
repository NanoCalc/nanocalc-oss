import Image from 'next/image'
import { BaseAppConfig } from '../lib/model/NanocalcAppConfig';
import CommonLogos from './CommonLogos';
import commonLogos from '../lib/common_logos';

interface NanocalcAppProps {
  config: BaseAppConfig;
}

export default function NanocalcApp({ config }: NanocalcAppProps) {
  return (
    <main className="flex min-h-screen flex-col justify-between items-center">
      <section className="w-full h-screen flex flex-col items-center">
        
      </section>

      <section className="w-full h-screen flex flex-col items-center">
        <Image
          src={config.appLogoPath}
          width={200}
          height={200}
          alt={`${config.appName} logo`}
          priority={true}
          className="mt-4 rounded-lg w-auto h-auto"
        />
        <CommonLogos logos={commonLogos}/>
      </section>
    </main>
  );
}
