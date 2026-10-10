import functools, threading, json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'frontend/public')))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
out=ROOT/'tmp/waves-check';out.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,channel='msedge')
    page=browser.new_page(viewport={'width':1280,'height':800})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.add_init_script("window.messages=[];addEventListener('message',e=>{if(e.data?.type==='simulation_state')messages.push(e.data);});")
    url=base+'/media/simulations/physics/progressive/index.html?variant=progressive&scope=single'
    page.goto(url);page.wait_for_selector('#controls input')
    def advance(n=60):page.evaluate('(n)=>{for(let i=0;i<n;i++)executeAICommand("step")}',n)
    def state():return page.evaluate('messages.at(-1).current_state')
    page.click('#answerTab')
    page.fill('#delayAnswer','1,25');page.fill('#speedAnswer','4')
    page.click('#check');assert 'Lance' in page.inner_text('#feedback')
    page.click('#run');advance();page.click('#check')
    assert not page.is_disabled('#record')
    page.click('#record');assert state()['simulation_status']!='finished'
    t=state()['time_s'];page.wait_for_timeout(150);assert state()['time_s']==t
    page.evaluate('executeAICommand("set_parameters",{sensor_2_m:8})');assert page.is_disabled('#record')
    page.click('#run');advance();page.fill('#delayAnswer','1,50');page.fill('#speedAnswer','40');page.click('#check');assert page.is_disabled('#record')
    page.fill('#speedAnswer','4');page.click('#check');page.click('#record');page.wait_for_function('messages.at(-1).current_state.simulation_status === "finished"',timeout=2000);assert state()['objective_progress']==1
    page.screenshot(path=str(out/'desktop-capteurs.png'))
    for variant in ['cord','spring','water','sound','vacuum','superposition','medium']:
        page.select_option('#variant',variant);page.click('#run');advance(55)
        page.click('#pause');page.click('#pause');page.click('#hint')
        page.screenshot(path=str(out/f'desktop-{variant}.png'))
        if variant=='vacuum':page.evaluate('executeAICommand("set_parameters",{air:0})');page.click('#run');advance()
        if variant=='superposition':page.evaluate('executeAICommand("set_parameters",{sign:1})');page.click('#run');advance()
        if variant=='medium':
            for params in [{'tension':9},{'amplitude':.5}]:
                page.evaluate('p=>executeAICommand("set_parameters",p)',params);page.click('#run');advance()
        page.click('#answerTab');page.check('input[name=choice][value="0"]');page.click('#check');page.wait_for_function('messages.at(-1).current_state.simulation_status === "finished"',timeout=2000)
    for size in [{'width':390,'height':844},{'width':360,'height':640},{'width':1024,'height':600}]:
        page.set_viewport_size(size)
        for variant in ['progressive','medium','vacuum','sound']:
            page.select_option('#variant',variant);page.click('#run');advance()
            for panel in ['settingsTab','answerTab']:
                page.click('#'+panel)
                overflow=page.evaluate('({page:document.documentElement.scrollHeight>innerHeight, aside:document.querySelector("aside").scrollHeight>document.querySelector("aside").clientHeight+1})')
                assert not any(overflow.values()),(size,variant,panel,overflow)
            page.screenshot(path=str(out/f'{size["width"]}-{variant}.png'))
            page.click('#zoom');page.screenshot(path=str(out/f'{size["width"]}-{variant}-large.png'));page.click('#zoom')
    page.goto(base+'/media/simulations/physics/advanced/waves/index.html?variant=progressive')
    page.wait_for_url('**/physics/progressive/**')
    assert not errors,errors
    # Review each new scientific asset as rendered by the browser.
    for asset in ['eau_source','dimensions','air_longitudinal','front_dates','cloche']:
        page.set_viewport_size({'width':900,'height':520});page.goto(base+f'/media/images/physics/ondes/{asset}.svg');page.screenshot(path=str(out/f'figure-{asset}.png'))
    print(json.dumps({'result':'PASS','browser_errors':errors,'screenshots':str(out)}))
    browser.close()
server.shutdown()
