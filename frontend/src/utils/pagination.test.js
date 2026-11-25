import test from 'node:test';
import assert from 'node:assert/strict';
import { hasMultiplePages, pageRange } from './pagination.js';

test('page range reports the expected first and last rows', () => {
  assert.deepEqual(pageRange(1, 12, 5), { first: 1, last: 5 });
  assert.deepEqual(pageRange(3, 12, 5), { first: 11, last: 12 });
});

test('empty result sets have no row range', () => {
  assert.deepEqual(pageRange(1, 0, 5), { first: 0, last: 0 });
});

test('pagination is needed only when results exceed a page', () => {
  assert.equal(hasMultiplePages(5, 5), false);
  assert.equal(hasMultiplePages(6, 5), true);
});
