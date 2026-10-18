// 홈 화면 추가(설치)용 서비스 워커. 네트워크 우선, 안 되면 저장본 — 그래서 새 버전이 올라오면 바로 반영된다
const CACHE='akeo-akeo-v1';
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  e.respondWith(fetch(e.request).then(r=>{ const c=r.clone(); caches.open(CACHE).then(ca=>ca.put(e.request,c)).catch(()=>{}); return r; }).catch(()=>caches.match(e.request)));
});
