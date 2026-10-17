import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const html = readFileSync(process.argv[2], 'utf8');
const markup = process.argv[3] === 'markup';
const script = html.match(/<script>\s*([\s\S]*?)\s*<\/script>/)?.[1];
assert.ok(script, 'rendered report must contain its client-side report script');

class Element {
  constructor(id) {
    this.id = id;
    this.hidden = false;
    this.value = id === 'sort' ? 'deal' : '';
    this.checked = id === 'showDoubt';
    this.innerHTML = '';
    this.textContent = '';
    this.handlers = {};
    this.parentElement = { hidden: false };
  }

  addEventListener(type, callback) {
    this.handlers[type] = callback;
  }

  querySelectorAll() {
    return [];
  }

  setAttribute() {}
}

const elements = new Map();
const document = {
  getElementById(id) {
    if (!elements.has(id)) elements.set(id, new Element(id));
    return elements.get(id);
  },
};
vm.runInNewContext(script, { document });

const table = document.getElementById('tb');
assert.match(document.getElementById('count').textContent, /^4 of 4$/);
assert.match(table.innerHTML, /&lt;img src=x onerror=alert\(1\)&gt;/);
assert.doesNotMatch(table.innerHTML, /<img|<script/i);
assert.match(table.innerHTML, /No market data returned/);
assert.match(table.innerHTML, /–/);
assert.equal(document.getElementById('notFoundSection').hidden, false);
assert.match(document.getElementById('notFound').innerHTML, /Unknown &lt;wine&gt;/);
assert.doesNotMatch(document.getElementById('notFound').innerHTML, /<wine>/);

assert.match(table.innerHTML, /6 × 750 ml · \$5,700 lot/);
assert.match(table.innerHTML, /\+25% premium/);
assert.match(table.innerHTML, /sold Oct 3/);
assert.match(table.innerHTML, /Hammer incl\. premium/);
assert.match(table.innerHTML, /Mixed lot/);
assert.match(table.innerHTML, /2010 Latour &lt;b&gt; ×3; 2009 Mouton ×3/);
assert.doesNotMatch(table.innerHTML, /undefined|null/);
if (markup) {
  assert.match(table.innerHTML, /<span class="b am">\+33%<\/span>/);
  assert.match(table.innerHTML, /<span class="b g3">-21%<\/span>/);
  assert.equal(document.getElementById('thRetail').textContent, 'Markup vs retail');
  assert.equal(document.getElementById('minLabel').textContent, 'Max markup');
} else {
  assert.match(table.innerHTML, /21% below/);
  assert.equal(document.getElementById('thRetail').textContent, 'vs Retail');
}

const showDoubt = document.getElementById('showDoubt');
showDoubt.checked = false;
showDoubt.handlers.input();
assert.equal(document.getElementById('count').textContent, '3 of 4');
assert.doesNotMatch(document.getElementById('tb').innerHTML, /No market data returned/);

const query = document.getElementById('q');
query.value = 'no matching wine';
query.handlers.input();
assert.equal(document.getElementById('count').textContent, '0 of 4');
assert.equal(document.getElementById('empty').hidden, false);

console.log('Renderer behavior: PASS');
