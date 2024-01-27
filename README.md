*no logo yet, sorry*

Welcome! :bouquet: **Bouquet** library is collection of awesome widgets
and helpful tools for [Kivy framework](https://kivy.org). With it, you can
build modern and beautiful UI for your applications. Enjoy the experience!

> :hammer_and_pick: Note that the library is under active development and some
> features may be unstable.

## :doughnut: Features

- [x] Linear Gradient
- [x] Radial Gradient
- [ ] List Gradient (like a linear gradient, but with multiple colors and stops)
- [ ] Angular Gradient
- [ ] Mesh Gradient
- [ ] Blurs and noises
- [ ] Animations (including 3D)
- [ ] Cool effects
- [ ] and more!

## :desktop_computer: Installation

> :warning: Project is not published on Pypi.

To install the latest stable version, use this command:

```bash
pip install https://github.com/mak8kammerer/bouquet/archive/stable.zip
```

If you want to use the latest features, install from `main` (development) branch (not recommended for production):

```bash
pip install https://github.com/mak8kammerer/bouquet/archive/main.zip
```

Also you can find the latest version (with changelogs and wheels) on the [releases page](https://github.com/mak8kammerer/bouquet/releases).

## :interrobang: FAQ

### Why I get `ModuleNotFoundError: No module named 'kivy'` during installation?

```bash
pip install wheel setuptools pip kivy --upgrade
```

### Why you do not post project at Kivy Garden?

Each flower in the kivy-garden should be a single widget (or a group of widgets)
that do one task. In turn, Bouquet provides a wide range of widgets and tools
that perform many different tasks.

### Why is the library so named?

Bouquet is a collection of flowers in a creative arrangement :blush:
