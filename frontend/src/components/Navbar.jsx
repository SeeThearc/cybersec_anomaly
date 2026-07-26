function Navbar() {
  return (
    <header className="flex h-16 items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-bg-card)] px-6">
      <div>
        <h1 className="text-lg font-semibold text-white">UEBA Security Platform</h1>
        <p className="text-xs text-[var(--color-text-secondary)]">
          User & Entity Behavior Analytics
        </p>
      </div>
      <span className="rounded-full bg-[var(--color-success)]/20 px-3 py-1 text-xs font-medium text-[var(--color-success)]">
        System Online
      </span>
    </header>
  );
}

export default Navbar;
