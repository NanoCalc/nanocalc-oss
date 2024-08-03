import { ContributorConfig } from '../lib/model/ContributorConfig';

const contributorsPath = "/contributors/"

// Array - O(n) lookup
const contributors: ContributorConfig[] = [
    {
        imagePath: `${contributorsPath}graziani.jpg`,
        name: "Graziani Candiotto",
        text: "has a BSc, MSc and PhD in Physics by UFSC. He is currently a researcher at UFRJ's Physics Department and a member of the NAMOR (Nanoscience Modelling in Rio) group. Has experience in Condensed Matter Physics, Statistical and Quantum Mechanics, as well as in Machine Learning and Materials Science. He also develops high performance software that describes OFEDs and pharmacokinetics."
    },
    {
        imagePath: `${contributorsPath}leandro.jpg`,
        name: "Leandro Benatto",
        text: "holds a Bachelor's, Master's, and PhD degree in Physics from UFPR. Currently, he is a FAPERJ Postdoctoral Fellow who is primarily focused on the study of new organic materials for use in optoelectronic devices. With extensive knowledge in Python programming, he has also developed software for analyzing lab results and simulating experiments. With his expertise in both physics and programming, Leandro is well-equipped to tackle complex research problems in the field of optoelectronics."
    },
    {
        imagePath: `${contributorsPath}omar.jpg`,
        name: "Omar Mesquita",
        text: "is the developer and administrator of the Nanocalc project website. He currently studies Computer Science at PUC-RIO. You can contact him at his email address or social networks :)"
    },
    {
        imagePath: `${contributorsPath}jose.jpeg`,
        name: "José Furtado",
        text: "studies Chemical Engineering at UFRJ and is currently working as a junior researcher at the Physics Department, where he learns programming to eventually be able to do more complex tasks in the research group."
    }
];

export default contributors;
