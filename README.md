# Hobbit House — Link Tree (bio-сторінка)

Єдина сторінка-посилання для bio в LinkedIn / email-підписах / соцмережах.
Статична (один `index.html`), брендована за офіційною дизайн-системою Hobbit House.

## Блоки

| Кнопка | Статус | URL |
|---|---|---|
| Сайт | ✅ готово | https://hobbithouse.com.ua |
| Пограти | ✅ готово | https://rost108.github.io/shliakh-do-ukryttia/ |
| Випробування | ✅ готово | https://www.youtube.com/watch?v=sU0yV2l4sJs |
| Відгуки | ✅ готово | `reviews.html` (форма збору відгуків) |
| Радар | ⚠️ треба URL | `data-track="radar"` |
| Соцмережі | ✅ готово | Instagram, Facebook, YouTube (з сайту) |

Незаповнені кнопки позначені бейджем **URL?** і приглушені — поки `href="#"`.
Щоб заповнити — заміни `href="#"` на реальне посилання в `index.html`.

## Моніторинг (навіщо GitHub Pages, а не Artifact)

Сторінка готова під **GA4** — той самий потік, що й основний сайт, щоб усе в одному місці.

1. У `index.html` заміни `G-XXXXXXXXXX` (3 місця) на свій **GA4 Measurement ID**.
2. У GA4 буде видно:
   - **перегляди** bio-сторінки (звідки прийшли — LinkedIn, email тощо через UTM);
   - **кліки по кожній кнопці** — подія `link_click` з параметром `link_id`
     (`site`, `tests`, `game`, `reviews`, `radar`, `social_linkedin` …).
3. Щоб бачити джерело у bio-посиланні — додавай UTM, напр.:
   `https://<user>.github.io/<repo>/?utm_source=linkedin&utm_medium=bio`

## Форма відгуків (`reviews.html`)

Брендована форма: ім'я, загальна оцінка (зірки), стан укриття (зірки), «Що саме сподобалось?», контакт, згода на публікацію.

**Відправка — через `mailto` (нічого налаштовувати не треба).**
Користувач тисне «Надіслати» → відкривається його поштова програма з уже заповненим листом
на **marketing@hobbithouse.com.ua** → лишається натиснути «Відправити».
Отримувач заданий у `reviews.html` → `<form data-to="...">`.

У GA4 — подія `review_submit` (з обома оцінками) фіксується в момент надсилання.

> Якщо згодом захочеш, щоб відгуки падали автоматично в таблицю без дії користувача —
> підключимо Google Форму або Formspree (це вже потребує твого акаунта).

## Деплой на GitHub Pages

```bash
# з кореня проєкту
cd linktree
git add . && git commit -m "Link tree: bio-сторінка Hobbit House"
git push
```

Варіанти хостингу:
- **Окремий репозиторій** `linktree` → Settings → Pages → Deploy from branch `main` /root → URL `https://<user>.github.io/linktree/`.
- Або цей файл покласти в існуючий Pages-репозиторій у підпапку.

Після деплою зареєструй URL у **Google Search Console** (щоб індексувався й моніторився там теж).
