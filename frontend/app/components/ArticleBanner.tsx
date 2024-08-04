import { ArticleBannerConfig } from "../lib/model/NanocalcAppConfig";
import Link from "next/link";

interface ArticleBannerProps {
    config: ArticleBannerConfig;
}

export default function ({ config }: ArticleBannerProps) {
    return (
        <article className="bg-nanocalc-blue rounded-md p-3 text-justify animate-slideIn">
            If you used this tool in your data analysis, please indicate so by citing <b><Link href={config.doi}>{config.title}</Link></b> in your work.
            <br /><br />
            Download some <b><Link href={config.sampleData}>sample data</Link></b>
            {config.spectralData && (
                <>{", "}<b><Link href={config.spectralData}>additional spectral data</Link></b></>
            )}
            {" and "}
            <b><Link href={config.binaries}>executables</Link></b> on our GitHub page.
        </article>
    );
}