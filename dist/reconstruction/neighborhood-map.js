// The same mapped geometry drives navigation, the inset map and the full map.
export function createNeighborhoodMap({data,onTravel,getPosition}){
 const inset=document.querySelector('#mini-map'),large=document.querySelector('#neighborhood-map'),dialog=document.querySelector('#map-dialog');
 const ext=data.extent,pad=30,views=new Map();
 function draw(canvas,full=false){
  const w=full?660:216,h=full?590:178,dpr=Math.min(devicePixelRatio,2);if(canvas.width!==w*dpr){canvas.width=w*dpr;canvas.height=h*dpr;}
  const c=canvas.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);c.clearRect(0,0,w,h);c.fillStyle='#242b25';c.fillRect(0,0,w,h);
  const margin=full?pad:10,scale=Math.min((w-margin*2)/(ext[2]-ext[0]),(h-margin*2)/(ext[3]-ext[1])),ox=(w-(ext[2]-ext[0])*scale)/2,oz=(h-(ext[3]-ext[1])*scale)/2;
  const point=(x,z)=>[ox+(x-ext[0])*scale,oz+(z-ext[1])*scale];views.set(canvas,{point,scale,ox,oz});
  const park=point(226,5);c.fillStyle='#485b40';c.fillRect(park[0],park[1],46*scale,218*scale);
  c.strokeStyle='#777a66';c.lineCap='round';for(const r of data.roads){const a=point(...r.a),b=point(...r.b);c.lineWidth=r.halfWidth*2*scale;c.beginPath();c.moveTo(...a);c.lineTo(...b);c.stroke();}
  for(const b of data.buildings){c.fillStyle=b.core?'#c2a575':b.facadeSpec?.observed?'#ac9974':'#596051';c.beginPath();b.p.forEach((p,i)=>{const q=point(...p);i?c.lineTo(...q):c.moveTo(...q);});c.closePath();c.fill();}
  if(full){c.textAlign='center';c.font='12px Arial';c.fillStyle='#eeeadb';for(const [name,x] of data.avenues){const p=point(x,ext[1]);c.fillText(name,p[0],p[1]-8);}c.textAlign='left';for(const [name,z] of data.streets){const p=point(ext[0]+5,z);c.fillStyle='#252e27';c.fillRect(p[0]-3,p[1]-9,99,18);c.fillStyle='#e5dfcc';c.fillText(name.replace('Street','St'),p[0],p[1]+4);}c.save();const p=point(255,108);c.translate(...p);c.rotate(-Math.PI/2);c.fillStyle='#bcc4a5';c.textAlign='center';c.fillText('TOMPKINS SQUARE PARK',0,0);c.restore();}
  const player=getPosition();if(player){const p=point(player.x,player.z);c.save();c.translate(...p);c.rotate(player.yaw||0);c.shadowColor='#000';c.shadowBlur=6;c.fillStyle='#f6deb0';c.beginPath();c.moveTo(0,-7);c.lineTo(5,5);c.lineTo(0,3);c.lineTo(-5,5);c.closePath();c.fill();c.restore();}
 }
 function refresh(){draw(inset);if(dialog.open)draw(large,true);}
 function open(){dialog.showModal();draw(large,true);}
 document.querySelector('#map-button').onclick=open;document.querySelector('#mini-map-button').onclick=open;
 document.querySelector('#close-map').onclick=()=>dialog.close();
 large.addEventListener('click',e=>{const v=views.get(large),rect=large.getBoundingClientRect();const x=(e.clientX-rect.left)*660/rect.width,z=(e.clientY-rect.top)*590/rect.height;onTravel(ext[0]+(x-v.ox)/v.scale,ext[1]+(z-v.oz)/v.scale);dialog.close();refresh();});
 const destinations=[['First & 10th',1,0],['Second & St. Marks',-229,150.1],['Avenue A & 7th',214,228],['Avenue A & 10th',214,0],['First & 12th',0,-157.8]];
 const list=document.querySelector('#destinations');for(const [name,x,z] of destinations){const button=document.createElement('button');button.textContent=name;button.onclick=()=>{onTravel(x,z);dialog.close();refresh();};list.append(button);}
 dialog.addEventListener('close',()=>document.querySelector('#world').focus({preventScroll:true}));
 return {refresh,open};
}
