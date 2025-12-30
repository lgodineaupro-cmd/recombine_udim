document.addEventListener('DOMContentLoaded',()=>{
  const slides = Array.from(document.querySelectorAll('.slide'));
  const nextBtn = document.querySelector('.nav.next');
  const prevBtn = document.querySelector('.nav.prev');
  let idx = slides.findIndex(s=>s.classList.contains('active'));
  if(idx<0) idx=0, slides[0].classList.add('active');
  function show(newIdx){
    if(newIdx===idx) return;
    slides[idx].classList.remove('active');
    slides[idx].classList.add('exit-left');
    slides[newIdx].classList.remove('exit-left');
    slides[newIdx].classList.add('active');
    idx=newIdx;
  }
  nextBtn.addEventListener('click',()=> show((idx+1)%slides.length));
  prevBtn.addEventListener('click',()=> show((idx-1+slides.length)%slides.length));
  document.addEventListener('keydown',e=>{
    if(e.key==='ArrowRight') nextBtn.click();
    if(e.key==='ArrowLeft') prevBtn.click();
  });
  const linksBtn = document.getElementById('open-links');
  if(linksBtn){
    linksBtn.addEventListener('click',()=>{
      window.open('../assets/lien/links.html','_blank');
    });
  }
});