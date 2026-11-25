export function pageRange(page, count, pageSize = 5) {
  if (!count) return { first: 0, last: 0 };
  return {
    first: (page - 1) * pageSize + 1,
    last: Math.min(page * pageSize, count),
  };
}

export function hasMultiplePages(count, pageSize = 5) {
  return Number(count) > pageSize;
}
