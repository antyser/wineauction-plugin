import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const html = readFileSync(process.argv[2], 'utf8');
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
assert.match(document.getElementById('count').textContent, /^2 of 2$/);
assert.match(table.innerHTML, /&lt;img src=x onerror=alert\(1\)&gt;/);
assert.doesNotMatch(table.innerHTML, /<img|<script/i);
assert.match(table.innerHTML, /No market data returned/);
assert.match(table.innerHTML, /–/);
assert.equal(document.getElementById('notFoundSection').hidden, false);
assert.match(document.getElementById('notFound').innerHTML, /Unknown &lt;wine&gt;/);
assert.doesNotMatch(document.getElementById('notFound').innerHTML, /<wine>/);

const showDoubt = document.getElementById('showDoubt');
showDoubt.checked = false;
showDoubt.handlers.input();
assert.equal(document.getElementById('count').textContent, '1 of 2');
assert.doesNotMatch(document.getElementById('tb').innerHTML, /No market data returned/);

const query = document.getElementById('q');
query.value = 'no matching wine';
query.handlers.input();
assert.equal(document.getElementById('count').textContent, '0 of 2');
assert.equal(document.getElementById('empty').hidden, false);

console.log('Renderer behavior: PASS');
