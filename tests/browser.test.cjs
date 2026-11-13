// npm install --prefix /tmp/blog-test jsdom; NODE_PATH=/tmp/blog-test/node_modules node tests/browser.test.cjs
const {JSDOM}=require('jsdom'), fs=require('fs'), path=require('path'), assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
async function page(route='/') {
 const dom=new JSDOM(fs.readFileSync(path.join(root,route,'index.html'),'utf8'),{url:'https://blog.rmbgame.net'+route,runScripts:'outside-only'});
 const w=dom.window;w.matchMedia=()=>({matches:false});w.scrollTo=()=>{};
 w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false};
 w.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.join(root,url),'utf8'))});
 w.eval(fs.readFileSync(path.join(root,'assets/theme.js'),'utf8'));w.eval(fs.readFileSync(path.join(root,'assets/app.js'),'utf8'));
 await new Promise(r=>setImmediate(r)); return w;
}
(async()=>{
 let w=await page(),d=w.document;
 assert.equal(d.documentElement.dataset.theme,'light');d.querySelector('[data-theme-toggle]').click();assert.equal(d.documentElement.dataset.theme,'dark');assert.equal(w.localStorage.getItem('blog-theme'),'dark');
 d.querySelector('.menu-toggle').click();assert.equal(d.querySelector('.menu-toggle').getAttribute('aria-expanded'),'true');
 d.dispatchEvent(new w.KeyboardEvent('keydown',{key:'/',bubbles:true}));await new Promise(r=>setImmediate(r));assert.equal(d.querySelector('dialog').open,true);
 let input=d.querySelector('#search-input');input.value='NVIDIA';input.dispatchEvent(new w.Event('input'));assert.ok(d.querySelectorAll('#search-results li').length>0);
 input.value='<script>no-such-word';input.dispatchEvent(new w.Event('input'));assert.equal(d.querySelectorAll('#search-results li').length,0);assert.match(d.querySelector('#search-status').textContent,/没有找到/);
 input.value='';input.dispatchEvent(new w.Event('input'));assert.match(d.querySelector('#search-status').textContent,/输入关键词/);
 d.querySelector('[data-search-close]').click();assert.equal(d.querySelector('dialog').open,false);w.close();
 w=await page('/about/');d=w.document;assert.ok(d.querySelectorAll('#outline li').length>=2);assert.match(d.querySelector('#github-comments').textContent,/暂未开启/);assert.equal(d.querySelectorAll('script[src="https://giscus.app/client.js"]').length,0);w.close();
 console.log('PASS: theme persistence, menu, keyboard search, search results/empty/XSS text, close, article outline, comments disabled');
})().catch(e=>{console.error(e);process.exit(1)});
