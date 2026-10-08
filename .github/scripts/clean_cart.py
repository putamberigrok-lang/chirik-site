from pathlib import Path

p=Path('index.html')
html=p.read_text(encoding='utf-8')
start=html.index('<section id="buy">')
end=html.index('</section>',start)+len('</section>')
section=html[start:end]
assert 'Собери свою корзину' in section, 'Unexpected cart section format'
a=section.index('<aside class="cart">')
b=section.index('</aside>',a)+len('</aside>')
aside=section[a:b].replace('<h3>Корзина</h3>','<h2>Корзина 🛍️</h2>')
aside=aside.replace('Нажмите «Добавить», чтобы собрать заказ.','В этой корзине будут выбранные наборы и отдельные товары.')
html=html[:start]+'<section id="buy" class="cart-section"><div class="wrap cart-wrap">'+aside+'</div></section>'+html[end:]
old='<a id="floatingCart" class="floating-cart" href="#buy">🛒 Корзина <span id="floatingCartCount">0</span><small id="floatingCartTotal">0 ₸</small></a>'
assert html.count(old)==1, 'Unexpected floating cart structure'
html=html.replace(old,'')
navstart=html.index('<header>')
navend=html.index('</nav>',navstart)+len('</nav>')
link='<a href="#buy" id="floatingCart" class="header-cart" aria-label="Открыть корзину"><span aria-hidden="true">🛒</span><span id="floatingCartCount">0</span><small id="floatingCartTotal">0 ₸</small></a>'
html=html[:navend]+link+html[navend:]
css="""
/* Compact cart without duplicated explanation or screen-covering overlay. */
.cart-section{padding:38px 0 72px}.cart-wrap{max-width:820px}
.cart-section .cart{position:static;width:100%;padding:clamp(20px,4vw,36px);border-radius:28px}
.cart-section .cart h2{margin-bottom:10px}
.header-cart{display:inline-flex;align-items:center;justify-content:center;gap:9px;white-space:nowrap;background:#313951;color:white;border:2px solid #fff;border-radius:17px;padding:10px 13px;font-size:14px;font-weight:900;box-shadow:0 3px 12px #91749333;margin-left:auto}
.header-cart #floatingCartCount{padding:3px 8px;background:#f4c4d9;color:#30334c;border-radius:999px;min-width:25px;text-align:center}
.header-cart #floatingCartTotal{font-size:12px;color:#fff8fa}
#chirikToast{bottom:23px}#buy{scroll-margin-top:85px}
@media(max-width:650px){.header-cart{padding:9px 12px;gap:7px;border-radius:14px}.header-cart #floatingCartTotal{display:none}.nav{gap:8px}.cart-section{padding-bottom:46px}.cart-section .cart{padding:20px 15px}.cart-item-controls{gap:7px}}
"""
html=html.replace('</style>',css+'\n</style>',1)
assert html.count('id="floatingCart"')==1 and html.count('id="floatingCartTotal"')==1
assert 'Собери свою корзину' not in html
p.write_text(html,encoding='utf-8')
print('Chirik cart cleaned; total bytes:',p.stat().st_size)
