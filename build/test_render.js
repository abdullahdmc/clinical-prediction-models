// Renders every view of the built page with a stubbed DOM. Run: node build/test_render.js
const fs=require('fs'); const html=fs.readFileSync(__dirname+'/artifact.html','utf8');
let src=html.slice(html.indexOf('<script>')+8, html.lastIndexOf('</script>'));
const el=()=>({innerHTML:'',hidden:true,value:'',addEventListener(){},querySelectorAll(){return[]},classList:{toggle(){}}});
global.document={querySelector:()=>el(),querySelectorAll:()=>[],addEventListener(){}};
global.window={addEventListener(){},scrollTo(){}}; global.location={hash:''}; global.localStorage={getItem:()=>null,setItem(){}};
src=src.replace(/\nroute\(\);\s*$/,'\n');
eval(src+`
let n=0,errs=[];
const t=(f,l)=>{try{const h=f(); if(!h||/undefined|NaN/.test(h)) errs.push(l+' contains undefined/NaN'); n++}catch(e){errs.push(l+': '+e.message)}};
t(home,'home');t(compare,'compare');t(ml,'ml');t(methods,'methods');
D.sections.forEach(s=>{['all','detail','calc','lmic'].forEach(f=>{secFilter=f;t(()=>section(s.id),'section '+s.id+' '+f)})});
D.models.forEach(m=>t(()=>model(m.id),'model '+m.id)); showCombo=true; t(compare,'compare+combo');
console.log('rendered',n,'views; problems:',errs.length); errs.slice(0,20).forEach(e=>console.log(' -',e));`);
