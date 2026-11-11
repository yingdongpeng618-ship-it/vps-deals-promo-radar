/* Optional local enhancement. Source prices and static content never depend on this file. */
(() => {
  const form = document.querySelector('[data-controls]');
  const list = document.querySelector('[data-plan-list]');
  if (!form || !list) return;
  const plans = Array.from(list.querySelectorAll('.plan'));
  const query = form.elements.query;
  const budget = form.elements.budget;
  const sort = form.elements.sort;
  const reset = form.querySelector('[type="reset"]');
  const error = document.querySelector('#filter-error');
  const empty = document.querySelector('[data-no-results]');
  const count = document.querySelector('[data-result-count]');
  const memory = plan => {
    const value = plan.dataset.memory.toLowerCase();
    return parseFloat(value) * (value.includes('gib') || value.includes('gb') ? 1024 : 1);
  };
  function update() {
    const invalid = !budget.validity.valid;
    error.hidden = !invalid;
    budget.setAttribute('aria-invalid', String(invalid));
    const limit = budget.value === '' || invalid ? Infinity : Number(budget.value);
    const term = query.value.trim().toLocaleLowerCase('en-US');
    const ordered = [...plans].sort(sort.value === 'memory'
      ? (a, b) => memory(b) - memory(a) || Number(a.dataset.price) - Number(b.dataset.price)
      : (a, b) => Number(a.dataset.price) - Number(b.dataset.price));
    let visible = 0;
    ordered.forEach(plan => {
      const shown = plan.dataset.search.toLocaleLowerCase('en-US').includes(term) && Number(plan.dataset.price) <= limit;
      plan.hidden = !shown;
      if (shown) visible++;
      list.append(plan);
    });
    empty.hidden = visible !== 0;
    count.textContent = `${visible} of ${plans.length} plans shown`;
    reset.disabled = !query.value && !budget.value && sort.value === 'price';
  }
  form.hidden = false;
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  form.addEventListener('reset', () => setTimeout(update, 0));
  document.querySelector('[data-clear]').addEventListener('click', () => { form.reset(); query.focus(); });
  update();
})();
