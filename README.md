# Terence Liu — Portfolio

A refined single-page portfolio site. Replaces the slide-based Canva layout with a responsive, scannable structure while keeping the original warm earth-tone palette.

## Preview locally

```bash
python3 -m http.server 8080
```

Open http://localhost:8080

## Deploy

**Live site:** https://terence0911.github.io/portfolio/

Push to `main` to publish. GitHub Pages deploys automatically on each push.

```bash
git add .
git commit -m "Update portfolio"
git push origin main
```

After pushing, hard-refresh the live site (`Cmd + Shift + R`) if changes do not appear immediately.

## CV

Editable source: `cv.html` (print-optimized A4 layout).

Regenerate PDF:

```bash
./export-cv.sh ~/Downloads/TerenceLiuCV.pdf
```


| Section    | Purpose                                      |
|------------|----------------------------------------------|
| Hero       | Name, role, primary CTAs                     |
| About      | Intro + value cards (cultural competence)    |
| Skills     | Grouped capability tags                      |
| Experience | Timeline of work history                     |
| Projects   | Case studies with clear links                |
| Contact    | Scannable contact panel                      |
