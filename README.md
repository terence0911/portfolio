# Terence Liu — Portfolio

A refined single-page portfolio site. Replaces the slide-based Canva layout with a responsive, scannable structure while keeping the original warm earth-tone palette.

## Preview locally

```bash
python3 -m http.server 8080
```

Open http://localhost:8080

## Deploy

Static files — deploy to any host:

- **GitHub Pages**: push to a repo and enable Pages from the `main` branch
- **Vercel / Netlify**: connect the repo or drag the folder
- **Canva**: use this as reference when updating your Canva site, or point your custom domain here instead

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
