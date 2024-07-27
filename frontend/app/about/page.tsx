import Image from 'next/image'

export default function About() {
return (
    <main className="flex min-h-screen flex-col items-center justify-between">
         <section className="w-full h-screen flex flex-col items-center">
         <Image
		src="/graziani.jpg"
		width={200}
		height={200}
		alt="Picture of Graziâni Candiotto"
		className="mt-8 mb-4"
	  />
	<h2 className="ml-4 mr-4 mt-10 md:w-1/2 justify-text">
		<b>Graziâni Candiotto</b> has a BSc, MSc and PhD in Physics by UFSC. He is currently a researcher at UFRJ's Physics Department and a member
		of the NAMOR (Nanoscience Modelling in Rio) group. Has experience in Condensed Matter Physics, Statistical 
		and Quantum Mechanics, as well as in Machine Learning and Materials Science. 
		He also develops high performance software that describes OFEDs and pharmacokinetics.
	</h2>
        </section>
       <section className="w-full h-screen flex flex-col items-center">
      	<Image
		src="/leandro.jpg"
		width={200}
		height={200}
		alt="Picture of Leandro Benatto"
		className="mt-8 mb-4"
	  />
	<h2 className="ml-4 mr-4 mt-10 md:w-1/2 justify-text">
		<b>Leandro Benatto</b> holds a Bachelor's, Master's, and PhD degree in Physics from UFPR. Currently, he is a FAPERJ Postdoctoral 
		Fellow who is primarily focused on the study of new organic materials for use in optoelectronic devices. 
		With extensive knowledge in Python programming, he has also developed software for analyzing lab results 
		and simulating experiments. With his expertise in both physics and programming, Leandro is well-equipped 
		to tackle complex research problems in the field of optoelectronics. 
	</h2>
 
       </section>
	<section className="w-full h-screen flex flex-col items-center">
	<Image
		src="/omar.jpg"
		width={200}
		height={200}
		alt="Picture of Omar Mesquita"
		className="mt-8 mb-4"
	  />
	<h2 className="ml-4 mr-4 mt-10 md:w-1/2 justify-text">
		Hi! My name is Omar Mesquita and I am the developer and administrator of this website and its web applications.
		I am currently studying Computer Science at PUC-RIO.
		Feel free to contact me at my email or social networks :) 
	</h2>

	</section>
       <section className="w-full h-screen flex flex-col items-center">
       <Image
		src="/jose.jpeg"
		width={200}
		height={200}
		alt="Picture of José Furtado"
		className="mt-8 mb-4"
	  />
	<h2 className="ml-4 mr-4 mt-10 md:w-1/2 justify-text">
		Hello! My name is José Furtado and I am studying Chemical Engineering at UFRJ.
		I am currently working as a junior researcher at the Physics Department, where I'm studying programming 
		to eventually be able to do more complex tasks in our research.
	</h2>
       </section>
    </main>
  );


}
