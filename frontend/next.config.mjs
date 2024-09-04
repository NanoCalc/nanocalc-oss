/** @type {import('next').NextConfig} */
const nextConfig = {
    async redirects() {
        return [
            {
                source: '/fret',
                destination: '/fretcalc',
                permanent: true,
            },
            {
                source: '/ri',
                destination: '/ricalc',
                permanent: true,
            },
            {
                source: '/plq',
                destination: '/plqsim',
                permanent: true,
            },
            {
                source: '/tmm',
                destination: '/tmmsim',
                permanent: true,
            },
        ];
    },
};

export default nextConfig;
