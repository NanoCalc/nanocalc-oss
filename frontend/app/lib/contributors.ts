import { ContributorConfig } from '../lib/model/ContributorConfig';

const contributorsPath = "/contributors/"

const contributors: ContributorConfig[] = [
    {
        imagePath: `${contributorsPath}graziani.jpg`,
        name: "Graziani Candiotto",
        text: "has a BSc, MSc and PhD in Physics by UFSC. He is currently a researcher at UFRJ's Physics Department and a member of the NAMOR (Nanoscience Modelling in Rio) group. Has experience in Condensed Matter Physics, Statistical and Quantum Mechanics, as well as in Machine Learning and Materials Science. He also develops high performance software that describes OFEDs and pharmacokinetics.",
        lattes: "https://lattes.cnpq.br/4362978184352541",
        github: "https://github.com/gcandiotto",
        orcid: "https://orcid.org/0000-0001-6755-660X",
    },
    {
        imagePath: `${contributorsPath}leandro.jpg`,
        name: "Leandro Benatto",
        text: "holds a Bachelor's, Master's, and PhD degree in Physics from UFPR. Currently, he is a FAPERJ Postdoctoral Fellow who is primarily focused on the study of new organic materials for use in optoelectronic devices. With extensive knowledge in Python programming, he has also developed software for analyzing lab results and simulating experiments. With his expertise in both physics and programming, Leandro is well-equipped to tackle complex research problems in the field of optoelectronics.",
        lattes: "https://lattes.cnpq.br/6623865899586359",
        github: "https://github.com/LeandroBenatto",
        orcid: "https://orcid.org/0000-0001-9976-3574"
    },
    {
        imagePath: `${contributorsPath}omar.jpg`,
        name: "Omar Mesquita",
        text: "is the developer and administrator of the Nanocalc project website. He currently studies Computer Science at PUC-RIO. You can contact him at his email address or social networks :)",
        lattes: "https://lattes.cnpq.br/4555122711141650",
        github: "https://github.com/OmarMesqq",
        orcid: "https://orcid.org/0000-0002-6656-5683",
        linkedin: "https://www.linkedin.com/in/omar-mesquita/"
    },
    {
        imagePath: `${contributorsPath}jose.jpeg`,
        name: "José Furtado",
        text: "studies Chemical Engineering at UFRJ and is currently working as a junior researcher at the Physics Department, where he learns programming to eventually be able to do more complex tasks in the research group.",
        lattes: "http://lattes.cnpq.br/3431643449287068",
        github: "https://github.com/Chimbalada"
    }
];

export default contributors;
