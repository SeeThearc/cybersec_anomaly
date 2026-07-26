function PagePlaceholder({ title, description }) {
  return (
    <section className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-8">
      <h2 className="text-2xl font-semibold text-white">{title}</h2>
      <p className="mt-2 text-[var(--color-text-secondary)]">{description}</p>
    </section>
  );
}

export default PagePlaceholder;
