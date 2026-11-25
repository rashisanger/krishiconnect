export function FormField({ label, name, error, hint, as = 'input', children, ...props }) {
  return <label className="field" htmlFor={name}><span className="field__label">{label}</span>
    {as === 'select' ? <select id={name} name={name} aria-invalid={Boolean(error)} {...props}>{children}</select>
      : as === 'textarea' ? <textarea id={name} name={name} aria-invalid={Boolean(error)} {...props} />
        : <input id={name} name={name} aria-invalid={Boolean(error)} {...props} />}
    {(error || hint) && <small className={error ? 'field__error' : 'field__hint'}>{error || hint}</small>}
  </label>;
}
