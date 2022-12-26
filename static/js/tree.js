const canvas = document.getElementById('my_canvas');
const ctx = canvas.getContext('2d');

ctx.translate(400,550); 
ctx.globalCompositeOperation="xor";

var anglefaktor =0.6;
timer1=setInterval(loop1, 500); 

branch(130, 0, anglefaktor);

//opening
function loop1() { 

ctx.clearRect(-400,-550,800,600); 
	forTree(+0.1);
	
	if(anglefaktor>1.6){
	clearInterval(timer1);
	timer2=setInterval(loop2, 500); 
	}
	
	branch(130, 0, anglefaktor);

}

//closing
function loop2() { 

ctx.clearRect(-400,-550,800,600); 
	
	forTree(-0.1);
	
	if(anglefaktor<0.4){
	clearInterval(timer2);
	timer1=setInterval(loop1, 500); 
	}
	
	branch(130, 0, anglefaktor);

}
//Anglefaktor rotate Grad* anglefaktor 1.4 Mitte
function forTree(fak) {
	anglefaktor+=fak;
}
function branch(branchlength, angle,anglefaktor){

	ctx.save(); 
	
	ctx.rotate(angle*anglefaktor * Math.PI/180);
	ctx.lineWidth = branchlength/4;
	ctx.lineCap = "round"; 
	ctx.strokeStyle ='rgb(255,255,255)';

	ctx.beginPath();
	ctx.moveTo(0, 0);
	ctx.lineTo(0,-branchlength);
	ctx.stroke();
	
	ctx.beginPath();
	ctx.moveTo(6, 0);
	ctx.lineTo(6,-branchlength-4);
	ctx.stroke();
	
	ctx.beginPath();
	ctx.moveTo(6,0);
	ctx.lineTo(6,-branchlength-3);
	ctx.stroke();
	
	ctx.translate(0,-branchlength); 
	
	if(branchlength>14){
		// left hier random sonst Winkel 0.8 ok
		branch( branchlength * random(0.72,0.78),20, anglefaktor);
		// right
		branch( branchlength * random(0.72,0.78) ,-20, anglefaktor);
	}
	
	ctx.restore(); 
		
}

function random(min, max){
	return ((Math.random()*(max-min))+min);
	
}